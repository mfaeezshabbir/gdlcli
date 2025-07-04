"""
Test configuration for gdl package.
"""

import pytest
import os
import tempfile
from gdl.config import Config


class TestConfig:
    """Test cases for Config class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = Config()
        
        assert config.get('output_dir') == './downloads'
        assert config.get('chunk_size') == 8192
        assert config.get('max_retries') == 3
        assert config.get('verify_ssl') is True
    
    def test_config_override(self):
        """Test configuration override with kwargs."""
        config = Config(chunk_size=16384, max_retries=5)
        
        assert config.get('chunk_size') == 16384
        assert config.get('max_retries') == 5
        assert config.get('output_dir') == './downloads'  # Default preserved
    
    def test_config_file_loading(self):
        """Test loading configuration from file."""
        # Create temporary config file
        config_data = '{"chunk_size": 32768, "max_retries": 10}'
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(config_data)
            config_file = f.name
        
        try:
            config = Config(config_file=config_file)
            assert config.get('chunk_size') == 32768
            assert config.get('max_retries') == 10
        finally:
            os.unlink(config_file)
    
    def test_env_var_loading(self):
        """Test loading configuration from environment variables."""
        # Set environment variables
        os.environ['GDL_CHUNK_SIZE'] = '65536'
        os.environ['GDL_MAX_RETRIES'] = '7'
        os.environ['GDL_VERIFY_SSL'] = 'false'
        
        try:
            config = Config()
            assert config.get('chunk_size') == 65536
            assert config.get('max_retries') == 7
            assert config.get('verify_ssl') is False
        finally:
            # Clean up environment variables
            for key in ['GDL_CHUNK_SIZE', 'GDL_MAX_RETRIES', 'GDL_VERIFY_SSL']:
                if key in os.environ:
                    del os.environ[key]
