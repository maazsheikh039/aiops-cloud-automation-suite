import os
import json
import yaml
from config_loader import ConfigLoader, AppConfig


def test_valid_yaml_config():
    """Test loading valid YAML configuration."""
    loader = ConfigLoader("configs/valid_config.yaml")
    config = loader.load()
    assert config.app_name == "MyApp"
    assert config.environment == "production"
    assert config.database.host == "db.example.com"
    assert config.database.port == 5432
    assert config.cache.max_size_mb == 256
    print("✓ Valid YAML config successfully loaded and verified.")


def test_minimal_config_with_defaults():
    """Test configuration with defaults applied."""
    loader = ConfigLoader("configs/minimal_config.json")
    config = loader.load()
    assert config.app_name == "MinimalApp"
    assert config.environment == "development" # Default value
    assert config.database.host == "localhost" # Default value
    assert config.database.port == 5432 # Default value
    assert config.cache.enabled is True # Default value
    assert config.logging.level == "INFO" # Default value
    print("✓ Minimal config correctly applied default values.")


def test_invalid_config_detection():
    """Test invalid configuration detection and exception raising."""
    loader = ConfigLoader("configs/invalid_config.yaml")
    try:
        loader.load()
        raise AssertionError("Should have failed on invalid configuration.")
    except ValueError as e:
        print(f"✓ Successfully caught expected validation error: {e}")


def test_missing_required_fields():
    """Test missing required fields validation."""
    loader = ConfigLoader("configs/minimal_config.json")
    # minimal_config has username, password, database, but let's test a dict missing app_name
    invalid_dict = {
        "database": {
            "username": "u",
            "password": "p",
            "database": "d"
        }
    }
    try:
        loader.validate_config(invalid_dict)
        raise AssertionError("Should have failed due to missing app_name.")
    except ValueError as e:
        print(f"✓ Successfully caught missing field error: {e}")


def test_config_reload():
    """Test configuration reload functionality."""
    # Create temporary config file for testing reload
    temp_path = "configs/temp_reload.json"
    initial_data = {
        "app_name": "ReloadApp",
        "database": {"username": "u", "password": "p", "database": "d"}
    }
    with open(temp_path, "w") as f:
        json.dump(initial_data, f)
        
    loader = ConfigLoader(temp_path)
    cfg1 = loader.load()
    assert cfg1.debug is False
    
    # Modify file contents
    updated_data = {
        "app_name": "ReloadAppUpdated",
        "debug": True,
        "database": {"username": "u", "password": "p", "database": "d"}
    }
    with open(temp_path, "w") as f:
        json.dump(updated_data, f)
        
    cfg2 = loader.reload()
    assert cfg2.app_name == "ReloadAppUpdated"
    assert cfg2.debug is True
    
    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)
    print("✓ Configuration reload verified successfully.")


def run_all_tests():
    """Run all test functions"""
    tests = [
        test_valid_yaml_config,
        test_minimal_config_with_defaults,
        test_invalid_config_detection,
        test_missing_required_fields,
        test_config_reload
    ]
    
    print("Running Configuration Loader Tests\n" + "="*50)
    
    for test in tests:
        try:
            print(f"\nRunning: {test.__name__}")
            test()
            print(f"✓ {test.__name__} PASSED")
        except Exception as e:
            print(f"✗ {test.__name__} FAILED: {str(e)}")


if __name__ == "__main__":
    run_all_tests()
