"""
Core downloader module for gdl package.
Contains the main GDL class and download logic.
"""

import os
import re
import time
import requests
from typing import Optional, Dict, Any, List
from pathlib import Path
from tqdm import tqdm

from .config import Config
from .utils import (
    setup_logging, extract_file_id, build_download_url, 
    get_confirmation_url, extract_filename_from_response,
    ensure_directory_exists, format_bytes, format_speed,
    estimate_eta, validate_url, is_google_docs_url
)


class URLError(Exception):
    """Raised when URL is invalid or cannot be processed."""
    pass


class DownloadError(Exception):
    """Raised when download fails."""
    pass


class GDL:
    """
    Google Drive Loader - Main class for downloading files from Google Drive.
    """
    
    def __init__(self, config_file: Optional[str] = None, **kwargs):
        """
        Initialize GDL with configuration.
        
        Args:
            config_file: Optional path to configuration file
            **kwargs: Configuration overrides
        """
        self.config = Config(config_file, **kwargs)
        self.logger = setup_logging(self.config.get('log_level', 'INFO'))
        self.session = requests.Session()
        
        # Set session configuration
        self.session.verify = self.config.get('verify_ssl', True)
        
        # Common headers to mimic browser behavior
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def download_file(self, url: str, output_path: str, 
                     format: Optional[str] = None, 
                     resume: bool = False) -> bool:
        """
        Download a file from Google Drive.
        
        Args:
            url: Google Drive URL
            output_path: Output file path
            format: Export format for Google Docs/Sheets/Slides
            resume: Whether to resume interrupted download
            
        Returns:
            True if download successful, False otherwise
        """
        try:
            # Validate URL
            if not validate_url(url):
                raise URLError(f"Invalid Google Drive URL: {url}")
            
            # Extract file ID
            file_id = extract_file_id(url)
            if not file_id:
                raise URLError(f"Could not extract file ID from URL: {url}")
            
            self.logger.info(f"Extracted file ID: {file_id}")
            
            # Handle Google Docs export format detection
            if is_google_docs_url(url) and not format:
                format = self._detect_export_format(url, output_path)
                if format:
                    self.logger.info(f"Auto-detected export format: {format}")
            
            # Build download URL
            download_url = build_download_url(file_id, format)
            self.logger.info(f"Download URL: {download_url}")
            
            # Ensure output directory exists
            if self.config.get('auto_create_dirs', True):
                ensure_directory_exists(output_path)
            
            # Check for resume
            resume_header = {}
            if resume and os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                resume_header = {'Range': f'bytes={file_size}-'}
                self.logger.info(f"Resuming download from byte {file_size}")
            
            # Start download
            return self._download_with_progress(download_url, output_path, resume_header)
            
        except (URLError, DownloadError) as e:
            self.logger.error(f"Download failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return False
    
    def batch_download(self, urls_file: str, output_dir: str, 
                      format: Optional[str] = None) -> int:
        """
        Download multiple files from a file containing URLs.
        
        Args:
            urls_file: Path to file containing URLs (one per line)
            output_dir: Output directory
            format: Default export format for Google Docs
            
        Returns:
            Number of successfully downloaded files
        """
        if not os.path.exists(urls_file):
            self.logger.error(f"URLs file not found: {urls_file}")
            return 0
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        success_count = 0
        
        with open(urls_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        self.logger.info(f"Starting batch download of {len(urls)} files")
        
        for i, url in enumerate(urls, 1):
            try:
                self.logger.info(f"Downloading file {i}/{len(urls)}: {url}")
                
                # Generate output filename
                file_id = extract_file_id(url)
                if not file_id:
                    self.logger.warning(f"Could not extract file ID from: {url}")
                    continue
                
                # Try to get filename from initial request
                output_path = self._generate_output_path(url, output_dir, format)
                
                if self.download_file(url, output_path, format):
                    success_count += 1
                    self.logger.info(f"Successfully downloaded: {output_path}")
                else:
                    self.logger.error(f"Failed to download: {url}")
                    
            except Exception as e:
                self.logger.error(f"Error downloading {url}: {e}")
        
        self.logger.info(f"Batch download completed: {success_count}/{len(urls)} files")
        return success_count
    
    def _download_with_progress(self, url: str, output_path: str, 
                               resume_header: Dict[str, str]) -> bool:
        """Download file with progress tracking and retry logic."""
        max_retries = self.config.get('max_retries', 3)
        retry_delay = self.config.get('retry_delay', 1.0)
        timeout = self.config.get('timeout', 30)
        chunk_size = self.config.get('chunk_size', 8192)
        
        for attempt in range(max_retries):
            try:
                # Make initial request
                response = self.session.get(
                    url, 
                    headers=resume_header,
                    timeout=timeout,
                    stream=True,
                    allow_redirects=True
                )
                
                # Check if we need to handle Google Drive confirmation
                if 'confirm=' in response.url or 'download_warning' in response.text:
                    response = self._handle_confirmation(response, url)
                
                response.raise_for_status()
                
                # Get file size
                total_size = int(response.headers.get('content-length', 0))
                if resume_header and response.status_code == 206:
                    # Partial content - add existing file size
                    existing_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
                    total_size += existing_size
                
                # Open file for writing
                mode = 'ab' if resume_header and os.path.exists(output_path) else 'wb'
                
                with open(output_path, mode) as f:
                    # Setup progress bar
                    with tqdm(
                        total=total_size,
                        initial=os.path.getsize(output_path) if mode == 'ab' else 0,
                        unit='B',
                        unit_scale=True,
                        desc=os.path.basename(output_path)
                    ) as pbar:
                        
                        start_time = time.time()
                        downloaded = pbar.n
                        
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))
                                downloaded += len(chunk)
                                
                                # Update speed and ETA
                                elapsed = time.time() - start_time
                                if elapsed > 0:
                                    speed = downloaded / elapsed
                                    pbar.set_postfix({
                                        'speed': format_speed(speed),
                                        'eta': estimate_eta(downloaded, total_size, speed)
                                    })
                
                self.logger.info(f"Download completed: {output_path}")
                return True
                
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Download attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    self.logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    raise DownloadError(f"Download failed after {max_retries} attempts: {e}")
            
            except IOError as e:
                raise DownloadError(f"File write error: {e}")
        
        return False
    
    def _handle_confirmation(self, response, original_url: str):
        """Handle Google Drive download confirmation for large files."""
        # Extract confirmation token
        confirm_match = re.search(r'confirm=([^&]+)', response.text)
        if not confirm_match:
            # Try alternative method
            confirm_match = re.search(r'name="confirm" value="([^"]+)"', response.text)
        
        if confirm_match:
            confirm_token = confirm_match.group(1)
            file_id = extract_file_id(original_url)
            
            if file_id:
                confirm_url = get_confirmation_url(file_id, confirm_token)
                self.logger.info("Handling download confirmation for large file")
                return self.session.get(confirm_url, stream=True, allow_redirects=True)
        
        return response
    
    def _detect_export_format(self, url: str, output_path: str) -> Optional[str]:
        """Auto-detect export format based on URL and output extension."""
        # Extract extension from output path
        ext = Path(output_path).suffix.lower()
        
        # Map extensions to export formats
        format_map = {
            '.pdf': 'pdf',
            '.docx': 'docx', 
            '.doc': 'docx',
            '.xlsx': 'xlsx',
            '.xls': 'xlsx',
            '.csv': 'csv',
            '.tsv': 'tsv',
            '.pptx': 'pptx',
            '.ppt': 'pptx',
            '.txt': 'txt',
            '.html': 'html',
            '.odt': 'odt',
            '.ods': 'ods',
            '.odp': 'odp',
            '.rtf': 'rtf',
            '.epub': 'epub'
        }
        
        return format_map.get(ext)
    
    def _generate_output_path(self, url: str, output_dir: str, 
                             format: Optional[str] = None) -> str:
        """Generate output file path for batch downloads."""
        file_id = extract_file_id(url)
        
        # Try to get filename from a HEAD request
        try:
            head_response = self.session.head(url, timeout=10)
            filename = extract_filename_from_response(head_response)
            if filename:
                return os.path.join(output_dir, filename)
        except:
            pass
        
        # Fallback to file ID with appropriate extension
        if format:
            extension_map = {
                'pdf': '.pdf',
                'docx': '.docx',
                'xlsx': '.xlsx',
                'pptx': '.pptx',
                'csv': '.csv',
                'txt': '.txt'
            }
            ext = extension_map.get(format, '.bin')
        else:
            ext = '.bin'
        
        return os.path.join(output_dir, f"{file_id}{ext}")
