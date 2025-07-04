
# Changelog

All notable changes to the `gdl` (Google Drive Loader) project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Planned: PyPI package publishing
- Planned: GitHub Actions CI/CD pipeline
- Planned: Additional export formats support
- Planned: Configuration validation

## [1.0.0] - 2025-07-04

### Added
- 🎉 **Initial release** of gdl as a professional Python package
- **Universal Google Drive downloader** supporting all file types
- **Multiple URL format support**:
  - `https://drive.google.com/file/d/FILE_ID/view`
  - `https://docs.google.com/document/d/FILE_ID/export`
  - `https://docs.google.com/spreadsheets/d/FILE_ID/export`
  - `https://docs.google.com/presentation/d/FILE_ID/export`
  - `https://drive.google.com/open?id=FILE_ID`
- **Command-line interface** with `gdl` command
- **Python API** for programmatic usage
- **Progress tracking** with tqdm progress bars
- **Resume capability** for interrupted downloads
- **Batch downloads** from URL lists
- **Export format support** for Google Docs/Sheets/Slides:
  - Documents: PDF, DOCX, ODT, RTF, TXT, HTML, EPUB
  - Spreadsheets: XLSX, ODS, CSV, TSV, PDF, HTML
  - Presentations: PPTX, ODP, PDF, TXT, JPEG, PNG
- **Configuration system** with JSON support
- **Error handling** with custom exceptions
- **Retry logic** with exponential backoff
- **Cross-platform support** (Windows, macOS, Linux)
- **Comprehensive logging** with configurable levels
- **Auto-filename detection** from response headers
- **Package structure** with proper modules:
  - `gdl.downloader` - Core download functionality
  - `gdl.cli` - Command-line interface
  - `gdl.utils` - Utility functions
  - `gdl.config` - Configuration management

### Technical Features
- **Streaming downloads** for memory efficiency
- **HTTP session management** with proper headers
- **SSL verification** with configurable options
- **Chunk-based downloading** with configurable size
- **Fallback download method** using urllib
- **Type hints** throughout codebase
- **Professional error handling** with custom exceptions
- **Modular architecture** for maintainability

### Documentation
- **Comprehensive README** with usage examples
- **API documentation** with code samples
- **Installation instructions** for multiple methods
- **Configuration guide** with examples
- **Troubleshooting section** with common issues
- **Contributing guidelines** for developers

### Examples
- Real-world usage scenarios
- Google Sheets export example: `https://docs.google.com/spreadsheets/d/ID/export`
- Batch download workflows
- Python API integration examples

## [0.x.x] - Pre-release Development

### Development History
- Initial concept as standalone script
- Command-line interface development
- Cross-platform wrapper scripts (bash/batch)
- Basic download functionality implementation
- URL parsing and file ID extraction
- Progress tracking implementation

---

## Release Notes

### Version 1.0.0 - Major Release

This is the first stable release of `gdl` as a professional Python package. The package has been completely restructured from a standalone script to a proper Python package with the following improvements:

#### 🚀 **Package Transformation**
- **Before**: Standalone `gdl.py` script
- **After**: Professional Python package with proper structure

#### 📦 **Installation Improvements**
- **Before**: `git clone` and manual script execution
- **After**: `pip install gdl` (ready for PyPI)

#### 🎯 **Usage Simplification**
- **Before**: `python gdl.py --url "URL"`
- **After**: `gdl --url "URL"` (global command)

#### 🐍 **Python API Addition**
- **New**: Import and use as library: `import gdl; gdl.download("URL", "output.pdf")`
- **New**: Advanced API with custom configuration
- **New**: Error handling with custom exceptions

#### ⚙️ **Enhanced Configuration**
- **New**: Multiple configuration file locations
- **New**: Environment variable support
- **New**: Runtime configuration overrides

#### 🧪 **Development Ready**
- **New**: Test framework setup with pytest
- **New**: Development dependencies and tools
- **New**: Code formatting and linting setup
- **New**: Package build and distribution setup

## Migration Guide

### From Script to Package

If you were using the standalone script version:

#### Old Usage
```bash
git clone https://github.com/mfaeezshabbir/gdl.git
cd gdl
python gdl.py --url "https://drive.google.com/file/d/FILE_ID/view" --output file.pdf
```

#### New Usage
```bash
pip install gdl
gdl --url "https://drive.google.com/file/d/FILE_ID/view" --output file.pdf
```

#### Python Integration (New)
```python
import gdl

# Simple usage
gdl.download("https://drive.google.com/file/d/FILE_ID/view", "file.pdf")

# Advanced usage
downloader = gdl.GDL()
success = downloader.download_file("URL", "output.pdf", resume=True)
```

## Compatibility

### Python Versions
- **Minimum**: Python 3.6+
- **Tested**: Python 3.6, 3.7, 3.8, 3.9, 3.10, 3.11

### Dependencies
- **Core**: `requests>=2.25.1`, `tqdm>=4.62.0`
- **Development**: `pytest>=6.0`, `black>=21.0`, `flake8>=3.8`, `mypy>=0.800`

### Operating Systems
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 18.04+, CentOS 7+, etc.)

## Security

### Security Considerations
- HTTPS-only downloads with SSL verification
- No credentials or API keys required
- Safe URL parsing with regex validation
- Secure file writing with proper permissions

### Reporting Security Issues
Please report security vulnerabilities to [mfaeezshabbir](https://github.com/mfaeezshabbir) privately.

## Support

### Getting Help
- 📝 [Issues](https://github.com/mfaeezshabbir/gdl/issues) - Bug reports and feature requests
- 💬 [Discussions](https://github.com/mfaeezshabbir/gdl/discussions) - Questions and community support
- 📧 [Contact](https://github.com/mfaeezshabbir) - Direct contact with maintainer

### Known Issues
- Large files (>1GB) may require confirmation handling (implemented)
- Some corporate firewalls may block Google Drive access
- Rate limiting may apply for bulk downloads

## Contributors

- **[@mfaeezshabbir](https://github.com/mfaeezshabbir)** - Creator and maintainer

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note**: This changelog will be updated with each release. For the most current information, please check the [GitHub repository](https://github.com/mfaeezshabbir/gdl).

*Last updated: July 4, 2025 at 12:43 UTC by [@mfaeezshabbir](https://github.com/mfaeezshabbir)*
