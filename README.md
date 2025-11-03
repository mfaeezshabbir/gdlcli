# gdlcli - Google Drive Loader

<div align="center">
  <img src="logos/banner.png" alt="gdlcli Logo" width="400">
</div>

[![PyPI version](https://badge.fury.io/py/gdlcli.svg)](https://badge.fury.io/py/gdlcli)
[![Python versions](https://img.shields.io/pypi/pyversions/gdlcli.svg)](https://pypi.org/project/gdlcli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/gdlcli?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/gdlcli)

<!-- [![Downloads](https://pepy.tech/badge/gdlcli)](https://pepy.tech/project/gdlcli) -->

A fast, lightweight Python package for downloading any file from Google Drive. Simple CLI tool and powerful Python library.

## 🚀 Features

- **⚡ Fast & Reliable**: Optimized downloads with progress tracking and resume capability
- **🎯 Universal**: Download any file type from Google Drive (docs, sheets, videos, images, etc.)
- **🔗 Smart URL Parsing**: Supports all Google Drive URL formats automatically
- **📦 Multiple Interfaces**: Use as CLI tool or import as Python library
- **🛡️ Robust**: Built-in retry logic, error handling, and fallback mechanisms
- **⚙️ Configurable**: Flexible configuration system with sensible defaults
- **🖥️ Cross-Platform**: Works on Windows, macOS, and Linux

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Command Line Usage](#command-line-usage)
- [Python API](#python-api)
- [Supported URLs](#supported-urls)
- [Export Formats](#export-formats)
- [Configuration](#configuration)
- [Advanced Usage](#advanced-usage)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 🔧 Installation

### From PyPI (Recommended)

```bash
pip install gdlcli
```

### From GitHub

```bash
pip install git+https://github.com/mfaeezshabbir/gdlcli.git
```

### Development Installation

```bash
git clone https://github.com/mfaeezshabbir/gdlcli.git
cd gdlcli
pip install -e .
```

### Requirements

- Python 3.6+
- `requests` and `tqdm` (installed automatically)

## ⚡ Quick Start

### Command Line

```bash
# Install the package
pip install gdlcli

# Download any file
gdlcli --url "https://drive.google.com/file/d/FILE_ID/view" --output myfile.pdf

# Your specific Google Sheets file
gdlcli --url "https://docs.google.com/spreadsheets/d/ID/export" --format xlsx --output spreadsheet.xlsx
```

### Python API

```python
import gdlcli

# Simple download
gdlcli.download("https://drive.google.com/file/d/FILE_ID/view", "output.pdf")

# Advanced usage
downloader = gdlcli.gdlcli()
success = downloader.download_file(
    "https://drive.google.com/file/d/FILE_ID/view",
    "output.pdf",
    resume=True
)
```

## 💻 Command Line Usage

### Basic Commands

```bash
# Download with auto-detected filename
gdlcli --url "https://drive.google.com/file/d/FILE_ID/view" --auto-name

# Download to specific location
gdlcli --url "https://drive.google.com/file/d/FILE_ID/view" --output ./downloads/myfile.pdf

# Download with progress and resume capability
gdlcli --url "https://drive.google.com/file/d/FILE_ID/view" --output largefile.zip --resume

# Verbose output for debugging
gdlcli --url "https://drive.google.com/file/d/FILE_ID/view" --verbose
```

### Export Google Docs/Sheets/Slides

```bash
# Export Google Doc as PDF
gdlcli --url "https://docs.google.com/document/d/DOC_ID/export" --format pdf --output document.pdf

# Export Google Sheet as Excel
gdlcli --url "https://docs.google.com/spreadsheets/d/SHEET_ID/export" --format xlsx --output spreadsheet.xlsx

# Export Google Slides as PowerPoint
gdlcli --url "https://docs.google.com/presentation/d/SLIDES_ID/export" --format pptx --output presentation.pptx
```

### Batch Downloads

```bash
# Create a file with URLs (one per line)
echo "https://drive.google.com/file/d/FILE_ID1/view
https://docs.google.com/spreadsheets/d/SHEET_ID/export
https://drive.google.com/file/d/FILE_ID2/view" > urls.txt

# Download all files
gdlcli --batch urls.txt --output-dir ./downloads/
```

### Command Options

```bash
gdlcli [OPTIONS]

Required (one of):
  --url URL                Google Drive file URL
  --batch FILE             File containing list of URLs

Options:
  --output, -o PATH        Output file path
  --output-dir PATH        Output directory (default: ./downloads)
  --format FORMAT          Export format (pdf, xlsx, docx, csv, etc.)
  --resume                 Resume interrupted download
  --auto-name              Auto-detect filename from response
  --config FILE            Custom configuration file
  --verbose, -v            Enable verbose logging
  --version                Show version information
  --help                   Show help message
```

## 🐍 Python API

### Simple Usage

```python
import gdlcli

# Quick download function
success = gdlcli.download(
    url="https://drive.google.com/file/d/FILE_ID/view",
    output="myfile.pdf"
)
```

### Advanced Usage

```python
import gdlcli

# Create downloader instance with custom config
downloader = gdlcli.gdlcli(
    config_file="my_config.json",
    max_retries=5,
    chunk_size=16384
)

# Download with options
success = downloader.download_file(
    url="https://docs.google.com/spreadsheets/d/ID/export",
    output_path="./data/spreadsheet.xlsx",
    format="xlsx",
    resume=True
)

# Batch download
count = downloader.batch_download(
    urls_file="download_list.txt",
    output_dir="./downloads/",
    format="pdf"  # Default format for Google Docs
)

print(f"Downloaded {count} files successfully")
```

### Error Handling

```python
import gdlcli
from gdlcli.downloader import URLError, DownloadError

try:
    downloader = gdlcli.gdlcli()
    downloader.download_file("https://drive.google.com/file/d/INVALID/view", "output.pdf")
except URLError as e:
    print(f"Invalid URL: {e}")
except DownloadError as e:
    print(f"Download failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 🔗 Supported URLs

gdlcli automatically handles all Google Drive URL formats:

- `https://drive.google.com/file/d/FILE_ID/view`
- `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`
- `https://docs.google.com/document/d/FILE_ID/export`
- `https://docs.google.com/spreadsheets/d/FILE_ID/export`
- `https://docs.google.com/presentation/d/FILE_ID/export`
- `https://drive.google.com/open?id=FILE_ID`
- Direct download links with confirmation tokens

## 📄 Export Formats

### Google Docs

- `pdf` - PDF Document
- `docx` - Microsoft Word
- `odt` - OpenDocument Text
- `rtf` - Rich Text Format
- `txt` - Plain Text
- `html` - HTML
- `epub` - EPUB

### Google Sheets

- `xlsx` - Microsoft Excel
- `ods` - OpenDocument Spreadsheet
- `csv` - Comma Separated Values
- `tsv` - Tab Separated Values
- `pdf` - PDF Document
- `html` - HTML

### Google Slides

- `pptx` - Microsoft PowerPoint
- `odp` - OpenDocument Presentation
- `pdf` - PDF Document
- `txt` - Plain Text
- `jpeg` - JPEG Images (zip)
- `png` - PNG Images (zip)

## ⚙️ Configuration

### Configuration File

Create `~/.gdlcli/config.json` or `gdlcli_config.json` in your project:

```json
{
  "output_dir": "./downloads",
  "chunk_size": 8192,
  "max_retries": 3,
  "retry_delay": 1.0,
  "timeout": 30,
  "verify_ssl": true,
  "auto_create_dirs": true,
  "log_level": "INFO"
}
```

### Environment Variables

```bash
export gdlcli_OUTPUT_DIR="./my_downloads"
export gdlcli_MAX_RETRIES="5"
export gdlcli_LOG_LEVEL="DEBUG"
```

### Python Configuration

```python
import gdlcli

# Override configuration
downloader = gdlcli.gdlcli(
    output_dir="./custom_downloads",
    max_retries=5,
    chunk_size=16384,
    log_level="DEBUG"
)
```

## 🔥 Advanced Usage

### Real-World Examples

#### Download Research Papers

```bash
# Create list of paper URLs
echo "https://drive.google.com/file/d/PAPER1_ID/view
https://drive.google.com/file/d/PAPER2_ID/view
https://drive.google.com/file/d/PAPER3_ID/view" > papers.txt

# Download all papers
gdlcli --batch papers.txt --output-dir ./research_papers/ --verbose
```

#### Export Multiple Spreadsheets

```python
import gdlcli

spreadsheet_urls = [
    "https://docs.google.com/spreadsheets/d/SHEET1_ID/export",
    "https://docs.google.com/spreadsheets/d/SHEET2_ID/export",
    "https://docs.google.com/spreadsheets/d/SHEET3_ID/export"
]

downloader = gdlcli.gdlcli()

for i, url in enumerate(spreadsheet_urls, 1):
    success = downloader.download_file(
        url=url,
        output_path=f"./data/spreadsheet_{i}.xlsx",
        format="xlsx"
    )
    if success:
        print(f"Downloaded spreadsheet {i}")
    else:
        print(f"Failed to download spreadsheet {i}")
```

#### Resume Large Downloads

```bash
# Start download (might be interrupted)
gdlcli --url "https://drive.google.com/file/d/LARGE_FILE_ID/view" --output large_dataset.zip

# Resume the download later
gdlcli --url "https://drive.google.com/file/d/LARGE_FILE_ID/view" --output large_dataset.zip --resume
```

#### Custom Processing Pipeline

```python
import gdlcli
import pandas as pd

def download_and_process_sheet(url, output_path):
    """Download Google Sheet and process with pandas."""

    # Download as Excel file
    downloader = gdlcli.gdlcli()
    success = downloader.download_file(
        url=url,
        output_path=output_path,
        format="xlsx"
    )

    if success:
        # Process with pandas
        df = pd.read_excel(output_path)
        print(f"Downloaded sheet with {len(df)} rows")
        return df
    else:
        print("Download failed")
        return None

# Process your specific sheet
df = download_and_process_sheet(
    "https://docs.google.com/spreadsheets/d/ID/export",
    "./data/my_spreadsheet.xlsx"
)
```

## 🧪 Development

### Setup Development Environment

```bash
git clone https://github.com/mfaeezshabbir/gdlcli.git
cd gdlcli
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
pytest --cov=gdlcli  # With coverage
```

### Code Formatting

```bash
black gdlcli/
flake8 gdlcli/
mypy gdlcli/
```

### Package Structure

```
gdlcli/
├── gdlcli/                    # Main package
│   ├── __init__.py        # Package initialization
│   ├── cli.py             # Command-line interface
│   ├── downloader.py      # Core download logic
│   ├── utils.py           # Utility functions
│   └── config.py          # Configuration management
├── tests/                 # Test suite
├── examples/              # Usage examples
└── docs/                  # Documentation
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure tests pass (`pytest`)
6. Format code (`black gdlcli/`)
7. Commit changes (`git commit -m 'Add amazing feature'`)
8. Push to branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## 📊 Performance

gdlcli is optimized for performance:

- **Streaming downloads**: Low memory usage even for large files
- **Resume capability**: No need to restart failed downloads
- **Concurrent processing**: Efficient batch downloads
- **Smart retry logic**: Exponential backoff for reliability
- **Progress tracking**: Real-time speed and ETA information

## 🛠️ Troubleshooting

### Common Issues

**"Could not extract file ID from URL"**

- Ensure the Google Drive URL is public or properly shared
- Check that the URL format is supported

**"Download failed" or "Permission denied"**

- Verify the file is publicly accessible
- Check if the file requires special permissions
- Try with `--verbose` flag for detailed error information

**"Module not found" errors**

- Install required dependencies: `pip install requests tqdm`
- For development: `pip install -e ".[dev]"`

**Slow downloads**

- Increase chunk size in configuration: `"chunk_size": 32768`
- Check your internet connection
- Try resuming the download: `--resume`

### Getting Help

- 📝 [Open an issue](https://github.com/mfaeezshabbir/gdlcli/issues) for bug reports
- 💬 [Start a discussion](https://github.com/mfaeezshabbir/gdlcli/discussions) for questions
- 📧 Contact: [mfaeezshabbir](https://github.com/mfaeezshabbir)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ by [mfaeezshabbir](https://github.com/mfaeezshabbir)
- Inspired by the need for a reliable, cross-platform Google Drive downloader
- Thanks to the Python community for excellent libraries like `requests` and `tqdm`

## 📈 Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed release notes.

---

**gdlcli** - Making Google Drive downloads simple, fast, and reliable. 🚀

_Last updated: July 4, 2025_
