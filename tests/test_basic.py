"""
Test package imports and basic functionality.
"""

def test_package_import():
    """Test that the package can be imported successfully."""
    try:
        import gdl
        assert hasattr(gdl, 'GDL')
        assert hasattr(gdl, 'download')
        assert hasattr(gdl, '__version__')
        print("✓ Package import successful")
    except ImportError as e:
        print(f"✗ Package import failed: {e}")
        raise


def test_version():
    """Test that version is accessible."""
    import gdl
    assert gdl.__version__ == "1.0.0"
    print(f"✓ Version: {gdl.__version__}")


if __name__ == "__main__":
    test_package_import()
    test_version()
    print("All basic tests passed!")
