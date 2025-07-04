"""
Utility functions for gdlcli package.
Contains helper functions and the simple download interface.
"""

import re
import os
import sys
import time
import logging
from typing import Optional, Tuple
from urllib.parse import urlparse, parse_qs

def setup_logging(level: str = "INFO") -> logging.Logger:
    """Setup logging configuration."""
    logger = logging.getLogger("gdlcli")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def extract_file_id(url: str) -> Optional[str]:
    """
    Extract Google Drive file ID from various URL formats.
    
    Args:
        url: Google Drive URL
        
    Returns:
        File ID if found, None otherwise
    """
    # Common Google Drive URL patterns
    patterns = [
        r'/file/d/([a-zA-Z0-9-_]+)',  # /file/d/FILE_ID/view
        r'/open\?id=([a-zA-Z0-9-_]+)',  # /open?id=FILE_ID
        r'/document/d/([a-zA-Z0-9-_]+)',  # Google Docs
        r'/spreadsheets/d/([a-zA-Z0-9-_]+)',  # Google Sheets
        r'/presentation/d/([a-zA-Z0-9-_]+)',  # Google Slides
        r'id=([a-zA-Z0-9-_]+)',  # Any id= parameter
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def is_google_docs_url(url: str) -> bool:
    """Check if URL is a Google Docs/Sheets/Slides URL."""
    return any(service in url for service in [
        'docs.google.com/document',
        'docs.google.com/spreadsheets', 
        'docs.google.com/presentation'
    ])


def build_download_url(file_id: str, export_format: Optional[str] = None) -> str:
    """
    Build appropriate download URL for Google Drive file.
    
    Args:
        file_id: Google Drive file ID
        export_format: Export format for Google Docs/Sheets/Slides
        
    Returns:
        Download URL
    """
    if export_format:
        # For Google Docs exports
        return f"https://docs.google.com/uc?export=download&format={export_format}&id={file_id}"
    else:
        # For regular file downloads
        return f"https://drive.google.com/uc?export=download&id={file_id}"


def get_confirmation_url(file_id: str, confirm_token: str) -> str:
    """Build confirmation URL for large file downloads."""
    return f"https://drive.google.com/uc?export=download&confirm={confirm_token}&id={file_id}"


def extract_filename_from_response(response) -> Optional[str]:
    """Extract filename from HTTP response headers."""
    content_disposition = response.headers.get('Content-Disposition', '')
    
    if 'filename=' in content_disposition:
        # Extract filename from Content-Disposition header
        filename_match = re.search(r'filename[^;=\n]*=(([\'"]).*?\2|[^;\n]*)', content_disposition)
        if filename_match:
            filename = filename_match.group(1).strip('\'"')
            return filename
    
    return None


def ensure_directory_exists(file_path: str):
    """Ensure the directory for the given file path exists."""
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def format_bytes(bytes_value: int) -> str:
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"


def format_speed(bytes_per_second: float) -> str:
    """Convert bytes per second to human readable format."""
    return f"{format_bytes(int(bytes_per_second))}/s"


def estimate_eta(downloaded: int, total: int, speed: float) -> str:
    """Estimate time remaining for download."""
    if speed <= 0 or total <= 0:
        return "Unknown"
    
    remaining = total - downloaded
    eta_seconds = remaining / speed
    
    if eta_seconds < 60:
        return f"{int(eta_seconds)}s"
    elif eta_seconds < 3600:
        return f"{int(eta_seconds / 60)}m {int(eta_seconds % 60)}s"
    else:
        hours = int(eta_seconds / 3600)
        minutes = int((eta_seconds % 3600) / 60)
        return f"{hours}h {minutes}m"


def validate_url(url: str) -> bool:
    """Validate if the URL is a proper Google Drive URL."""
    if not url:
        return False
    
    try:
        parsed = urlparse(url)
        return parsed.netloc in ['drive.google.com', 'docs.google.com']
    except:
        return False


def download(url: str, output_path: str, **kwargs) -> bool:
    """
    Simple download function for quick usage.
    
    Args:
        url: Google Drive URL
        output_path: Output file path
        **kwargs: Additional options for gdlcli
        
    Returns:
        True if download successful, False otherwise
    """
    from .downloader import gdlcli
    
    downloader = gdlcli(**kwargs)
    return downloader.download_file(url, output_path)
