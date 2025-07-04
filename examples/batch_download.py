#!/usr/bin/env python3
"""
Batch download example for gdl package.
Demonstrates downloading multiple files from a list.
"""

import gdl
import os

def create_sample_urls_file():
    """Create a sample URLs file for demonstration."""
    urls = [
        "# Sample URLs file for gdl batch download",
        "# Lines starting with # are ignored",
        "",
        "# Example URLs (replace with actual Google Drive URLs)",
        "https://drive.google.com/file/d/FILE_ID_1/view",
        "https://docs.google.com/spreadsheets/d/SHEET_ID/export",
        "https://docs.google.com/document/d/DOC_ID/export",
        "https://drive.google.com/file/d/FILE_ID_2/view"
    ]
    
    with open("sample_urls.txt", "w") as f:
        f.write("\n".join(urls))
    
    print("Created sample_urls.txt")
    return "sample_urls.txt"


def main():
    """Main example function."""
    print("=== gdl Batch Download Example ===")
    print()
    
    # Create sample URLs file
    urls_file = create_sample_urls_file()
    output_dir = "./batch_downloads"
    
    print(f"URLs file: {urls_file}")
    print(f"Output directory: {output_dir}")
    print()
    
    # Create downloader instance
    downloader = gdl.GDL(
        output_dir=output_dir,
        log_level="INFO"
    )
    
    # Perform batch download
    print("Starting batch download...")
    success_count = downloader.batch_download(
        urls_file=urls_file,
        output_dir=output_dir,
        format="pdf"  # Default format for Google Docs
    )
    
    print(f"✓ Batch download completed: {success_count} files downloaded")
    
    # List downloaded files
    if os.path.exists(output_dir):
        files = os.listdir(output_dir)
        if files:
            print(f"\nDownloaded files in {output_dir}:")
            for file in files:
                print(f"  - {file}")
        else:
            print(f"\nNo files found in {output_dir}")
    
    # Cleanup
    if os.path.exists(urls_file):
        os.remove(urls_file)
        print(f"\nCleaned up {urls_file}")


if __name__ == "__main__":
    main()
