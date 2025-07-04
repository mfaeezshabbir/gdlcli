"""
Command-line interface for gdlcli package.
Provides the main CLI entry point and argument parsing.
"""

import argparse
import sys
import os
from typing import Optional

from .downloader import gdlcli, URLError, DownloadError
from .utils import validate_url
from . import __version__


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog='gdlcli',
        description='gdlcli - Google Drive Loader: Download any file from Google Drive',
        epilog='''
Examples:
  gdlcli --url "https://drive.google.com/file/d/FILE_ID/view" --output myfile.pdf
  gdlcli --url "https://docs.google.com/spreadsheets/d/ID/export" --format xlsx --output data.xlsx
  gdlcli --batch urls.txt --output-dir ./downloads/
  gdlcli --url "https://drive.google.com/file/d/ID/view" --auto-name --verbose
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Main arguments (mutually exclusive)
    main_group = parser.add_mutually_exclusive_group(required=True)
    main_group.add_argument(
        '--url', 
        type=str,
        help='Google Drive file URL to download'
    )
    main_group.add_argument(
        '--batch',
        type=str,
        metavar='FILE',
        help='File containing list of URLs to download (one per line)'
    )
    
    # Output options
    parser.add_argument(
        '--output', '-o',
        type=str,
        metavar='PATH',
        help='Output file path (required for single URL downloads)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        metavar='PATH',
        default='./downloads',
        help='Output directory for batch downloads (default: ./downloads)'
    )
    
    # Download options
    parser.add_argument(
        '--format',
        type=str,
        metavar='FORMAT',
        help='Export format for Google Docs/Sheets/Slides (pdf, xlsx, docx, csv, etc.)'
    )
    parser.add_argument(
        '--resume',
        action='store_true',
        help='Resume interrupted download'
    )
    parser.add_argument(
        '--auto-name',
        action='store_true', 
        help='Auto-detect filename from response headers'
    )
    
    # Configuration options
    parser.add_argument(
        '--config',
        type=str,
        metavar='FILE',
        help='Custom configuration file path'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    # Information
    parser.add_argument(
        '--version',
        action='version',
        version=f'gdlcli {__version__}'
    )
    
    return parser


def validate_args(args: argparse.Namespace) -> bool:
    """Validate command line arguments."""
    # For single URL downloads, output is required unless auto-name is used
    if args.url and not args.output and not args.auto_name:
        print("Error: --output is required for single URL downloads (or use --auto-name)")
        return False
    
    # Validate URL if provided
    if args.url and not validate_url(args.url):
        print(f"Error: Invalid Google Drive URL: {args.url}")
        return False
    
    # Check if batch file exists
    if args.batch and not os.path.exists(args.batch):
        print(f"Error: Batch file not found: {args.batch}")
        return False
    
    return True


def handle_single_download(args: argparse.Namespace) -> bool:
    """Handle single file download."""
    try:
        # Create downloader instance
        config_options = {}
        if args.verbose:
            config_options['log_level'] = 'DEBUG'
        
        downloader = gdlcli(config_file=args.config, **config_options)
        
        # Determine output path
        output_path = args.output
        if args.auto_name:
            # Try to get filename from response
            import tempfile
            from .utils import extract_filename_from_response, extract_file_id, build_download_url
            
            file_id = extract_file_id(args.url)
            if file_id:
                try:
                    download_url = build_download_url(file_id, args.format)
                    response = downloader.session.head(download_url, timeout=10)
                    filename = extract_filename_from_response(response)
                    
                    if filename:
                        output_path = filename
                        print(f"Auto-detected filename: {filename}")
                    else:
                        # Fallback to file ID
                        ext = '.pdf' if args.format == 'pdf' else '.bin'
                        output_path = f"{file_id}{ext}"
                        print(f"Using fallback filename: {output_path}")
                        
                except Exception as e:
                    print(f"Warning: Could not auto-detect filename: {e}")
                    ext = '.pdf' if args.format == 'pdf' else '.bin'
                    output_path = f"{file_id}{ext}"
        
        if not output_path:
            print("Error: Could not determine output filename")
            return False
        
        # Download the file
        print(f"Downloading: {args.url}")
        print(f"Output: {output_path}")
        
        success = downloader.download_file(
            url=args.url,
            output_path=output_path,
            format=args.format,
            resume=args.resume
        )
        
        if success:
            print(f"✓ Download completed: {output_path}")
            return True
        else:
            print("✗ Download failed")
            return False
            
    except (URLError, DownloadError) as e:
        print(f"Error: {e}")
        return False
    except KeyboardInterrupt:
        print("\nDownload cancelled by user")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def handle_batch_download(args: argparse.Namespace) -> bool:
    """Handle batch file download."""
    try:
        # Create downloader instance
        config_options = {}
        if args.verbose:
            config_options['log_level'] = 'DEBUG'
        
        downloader = gdlcli(config_file=args.config, **config_options)
        
        print(f"Starting batch download from: {args.batch}")
        print(f"Output directory: {args.output_dir}")
        
        success_count = downloader.batch_download(
            urls_file=args.batch,
            output_dir=args.output_dir,
            format=args.format
        )
        
        print(f"✓ Batch download completed: {success_count} files downloaded")
        return success_count > 0
        
    except (URLError, DownloadError) as e:
        print(f"Error: {e}")
        return False
    except KeyboardInterrupt:
        print("\nBatch download cancelled by user")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Validate arguments
    if not validate_args(args):
        sys.exit(1)
    
    # Handle the request
    success = False
    
    if args.url:
        success = handle_single_download(args)
    elif args.batch:
        success = handle_batch_download(args)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
