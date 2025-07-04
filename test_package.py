#!/usr/bin/env python3
"""
Simple test script to verify the gdl package is working correctly.
"""

def test_imports():
    """Test that all imports work correctly."""
    try:
        import gdl
        from gdl import GDL, URLError, DownloadError
        from gdl.utils import extract_file_id, validate_url
        from gdl.config import Config
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_version():
    """Test that version is accessible."""
    import gdl
    print(f"✓ Version: {gdl.__version__}")
    return gdl.__version__ == "1.0.0"

def test_basic_functionality():
    """Test basic functionality."""
    from gdl.utils import extract_file_id, validate_url
    from gdl.config import Config
    
    # Test URL parsing
    test_url = 'https://drive.google.com/file/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/view'
    file_id = extract_file_id(test_url)
    print(f"✓ File ID extraction: {file_id}")
    
    # Test URL validation
    is_valid = validate_url(test_url)
    print(f"✓ URL validation: {is_valid}")
    
    # Test config
    config = Config()
    print(f"✓ Config loaded: chunk_size={config.get('chunk_size')}")
    
    return file_id and is_valid

def main():
    """Run all tests."""
    print("=== Testing gdl Package ===")
    
    tests = [
        ("Imports", test_imports),
        ("Version", test_version),
        ("Basic Functionality", test_basic_functionality)
    ]
    
    passed = 0
    for name, test_func in tests:
        print(f"\n--- {name} ---")
        try:
            if test_func():
                print(f"✓ {name} passed")
                passed += 1
            else:
                print(f"✗ {name} failed")
        except Exception as e:
            print(f"✗ {name} failed with exception: {e}")
    
    print(f"\n=== Results ===")
    print(f"Tests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 All tests passed! Package is ready for use.")
        return True
    else:
        print("❌ Some tests failed. Check the issues above.")
        return False

if __name__ == "__main__":
    main()
