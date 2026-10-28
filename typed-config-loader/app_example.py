from config_loader import ConfigLoader
import sys


def main():
    """Main application demonstrating typed config loading."""
    if len(sys.argv) < 2:
        print("Usage: python3 app_example.py <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    print(f"Loading configuration from: {config_file}")
    
    try:
        loader = ConfigLoader(config_file)
        config = loader.load()
        
        print("\n=== Configuration Summary ===")
        print(f"App Name:    {config.app_name}")
        print(f"Environment: {config.environment}")
        print(f"Debug Mode:  {config.debug}")
        print(f"DB Host:     {config.database.host}:{config.database.port}")
        print(f"DB Name:     {config.database.database}")
        print(f"Cache TTL:   {config.cache.ttl_seconds}s (Enabled: {config.cache.enabled})")
        print(f"Log Level:   {config.logging.level}")
        print("=============================\n")
        
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
