"""
gdlcli - Google Drive Loader

A fast, lightweight Python package for downloading any file from Google Drive.
Simple CLI tool and powerful Python library.

Example usage:
    >>> import gdlcli
    >>> gdlcli.download("https://drive.google.com/file/d/FILE_ID/view", "output.pdf")

For more advanced usage:
    >>> downloader = gdlcli.gdlcli()
    >>> success = downloader.download_file(url, output_path, resume=True)
"""

__version__ = "1.0.0"
__author__ = "mfaeezshabbir"
__email__ = "mfaeezshabbir@gmail.com"
__license__ = "MIT"

from .downloader import gdlcli, URLError, DownloadError
from .utils import download

# Make the main classes and functions available at package level
__all__ = [
    "gdlcli",
    "download", 
    "URLError",
    "DownloadError",
    "__version__"
]
