"""
gdl - Google Drive Loader

A fast, lightweight Python package for downloading any file from Google Drive.
Simple CLI tool and powerful Python library.

Example usage:
    >>> import gdl
    >>> gdl.download("https://drive.google.com/file/d/FILE_ID/view", "output.pdf")

For more advanced usage:
    >>> downloader = gdl.GDL()
    >>> success = downloader.download_file(url, output_path, resume=True)
"""

__version__ = "1.0.0"
__author__ = "mfaeezshabbir"
__email__ = "mfaeezshabbir@gmail.com"
__license__ = "MIT"

from .downloader import GDL, URLError, DownloadError
from .utils import download

# Make the main classes and functions available at package level
__all__ = [
    "GDL",
    "download", 
    "URLError",
    "DownloadError",
    "__version__"
]
