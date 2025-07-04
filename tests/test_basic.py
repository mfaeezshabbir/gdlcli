"""
Test package imports and basic functionality.
"""

def test_package_import():
    """Test that the package can be imported successfully."""
    try:
        import gdlcli
        assert hasattr(gdlcli, 'gdlcli')
        assert hasattr(gdlcli, 'download')
        assert hasattr(gdlcli, '__version__')
        print("✓ Package import successful")
    except ImportError as e:
        print(f"✗ Package import failed: {e}")
        raise


def test_version():
    """Test that version is accessible."""
    import gdlcli
    assert gdlcli.__version__ == "1.0.0"
    print(f"✓ Version: {gdlcli.__version__}")


if __name__ == "__main__":
    test_package_import()
    test_version()
    print("All basic tests passed!")
