"""
Test utilities for gdl package.
"""

import pytest
from gdl.utils import (
    extract_file_id, validate_url, build_download_url,
    format_bytes, format_speed, is_google_docs_url
)


class TestUtils:
    """Test cases for utility functions."""
    
    def test_extract_file_id(self):
        """Test file ID extraction from various URL formats."""
        test_cases = [
            ("https://drive.google.com/file/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/view", 
             "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"),
            ("https://drive.google.com/open?id=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
             "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"),
            ("https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/export",
             "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"),
            ("invalid_url", None)
        ]
        
        for url, expected in test_cases:
            assert extract_file_id(url) == expected
    
    def test_validate_url(self):
        """Test URL validation."""
        valid_urls = [
            "https://drive.google.com/file/d/FILE_ID/view",
            "https://docs.google.com/spreadsheets/d/ID/export"
        ]
        
        invalid_urls = [
            "",
            "not_a_url",
            "https://example.com/file",
            "https://dropbox.com/file"
        ]
        
        for url in valid_urls:
            assert validate_url(url) is True
        
        for url in invalid_urls:
            assert validate_url(url) is False
    
    def test_build_download_url(self):
        """Test download URL building."""
        file_id = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
        
        # Regular download
        url = build_download_url(file_id)
        assert f"id={file_id}" in url
        assert "drive.google.com" in url
        
        # Export format
        url = build_download_url(file_id, "pdf")
        assert f"id={file_id}" in url
        assert "format=pdf" in url
    
    def test_format_bytes(self):
        """Test byte formatting."""
        test_cases = [
            (1024, "1.0 KB"),
            (1536, "1.5 KB"),
            (1048576, "1.0 MB"),
            (1073741824, "1.0 GB")
        ]
        
        for bytes_val, expected in test_cases:
            assert format_bytes(bytes_val) == expected
    
    def test_is_google_docs_url(self):
        """Test Google Docs URL detection."""
        docs_urls = [
            "https://docs.google.com/document/d/ID/export",
            "https://docs.google.com/spreadsheets/d/ID/export",
            "https://docs.google.com/presentation/d/ID/export"
        ]
        
        non_docs_urls = [
            "https://drive.google.com/file/d/ID/view",
            "https://example.com/document"
        ]
        
        for url in docs_urls:
            assert is_google_docs_url(url) is True
        
        for url in non_docs_urls:
            assert is_google_docs_url(url) is False
