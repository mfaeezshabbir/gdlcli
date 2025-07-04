#!/usr/bin/env python3
"""
Basic usage example for gdlcli package.
Demonstrates simple file download functionality.
"""

import gdlcli

def main():
    """Main example function."""
    # Example Google Drive file URL (replace with actual URL)
    url = "https://drive.google.com/file/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/view"
    output_file = "downloaded_file.pdf"
    
    print("=== gdlcli Basic Usage Example ===")
    print(f"URL: {url}")
    print(f"Output: {output_file}")
    print()
    
    # Method 1: Simple download function
    print("Method 1: Using simple download function")
    success = gdlcli.download(url, output_file)
    
    if success:
        print(f"✓ File downloaded successfully: {output_file}")
    else:
        print("✗ Download failed")
    
    print()
    
    # Method 2: Using gdlcli class with options
    print("Method 2: Using gdlcli class with options")
    downloader = gdlcli.gdlcli(
        chunk_size=16384,  # Larger chunk size
        max_retries=5,     # More retries
        log_level="DEBUG"  # Verbose logging
    )
    
    success = downloader.download_file(
        url=url,
        output_path="advanced_download.pdf",
        resume=True  # Enable resume capability
    )
    
    if success:
        print("✓ Advanced download completed successfully")
    else:
        print("✗ Advanced download failed")


if __name__ == "__main__":
    main()
