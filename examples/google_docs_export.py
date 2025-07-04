#!/usr/bin/env python3
"""
Google Docs export example for gdl package.
Demonstrates exporting Google Docs, Sheets, and Slides in various formats.
"""

import gdl

def main():
    """Main example function."""
    print("=== gdl Google Docs Export Example ===")
    print()
    
    # Example URLs (replace with actual Google Docs URLs)
    examples = [
        {
            "type": "Google Doc",
            "url": "https://docs.google.com/document/d/DOC_ID/export",
            "formats": ["pdf", "docx", "txt", "html"]
        },
        {
            "type": "Google Sheet",
            "url": "https://docs.google.com/spreadsheets/d/SHEET_ID/export", 
            "formats": ["xlsx", "csv", "pdf", "html"]
        },
        {
            "type": "Google Slides",
            "url": "https://docs.google.com/presentation/d/SLIDES_ID/export",
            "formats": ["pptx", "pdf", "txt"]
        }
    ]
    
    # Create downloader instance
    downloader = gdl.GDL(log_level="INFO")
    
    for example in examples:
        print(f"--- {example['type']} Export ---")
        print(f"URL: {example['url']}")
        print("Available formats:", ", ".join(example['formats']))
        print()
        
        for format_type in example['formats']:
            output_file = f"export_{example['type'].lower().replace(' ', '_')}.{format_type}"
            
            print(f"Exporting as {format_type.upper()}...")
            success = downloader.download_file(
                url=example['url'],
                output_path=output_file,
                format=format_type
            )
            
            if success:
                print(f"✓ Exported: {output_file}")
            else:
                print(f"✗ Failed to export: {output_file}")
        
        print()
    
    print("=== Export with Custom Configuration ===")
    
    # Example with custom configuration
    custom_downloader = gdl.GDL(
        chunk_size=32768,
        max_retries=5,
        output_dir="./exports"
    )
    
    # Export with resume capability
    url = "https://docs.google.com/document/d/DOC_ID/export"
    output_file = "./exports/large_document.pdf"
    
    print(f"Downloading large document with resume capability...")
    success = custom_downloader.download_file(
        url=url,
        output_path=output_file,
        format="pdf",
        resume=True
    )
    
    if success:
        print(f"✓ Large document downloaded: {output_file}")
    else:
        print(f"✗ Failed to download large document")


if __name__ == "__main__":
    main()
