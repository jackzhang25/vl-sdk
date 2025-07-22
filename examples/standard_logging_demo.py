#!/usr/bin/env python3
"""
Demo script showing standard logging directory structure and organization.
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the path so we can import the SDK
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from visual_layer_sdk.logger import get_default_log_directory, list_log_files, get_latest_log_file, show_log_directory_info, log_to_console_and_file, log_to_file_only, get_logger, configure_logging
import logging


def demo_standard_log_directory():
    """Demo: Show standard log directory structure"""
    print("🚀 Visual Layer SDK - Standard Logging Directory Demo")
    print("=" * 60)

    # Show default log directory
    default_log_dir = get_default_log_directory()
    print(f"📁 Default log directory: {default_log_dir}")

    # Show current platform
    import platform

    print(f"🖥️  Platform: {platform.system()} {platform.release()}")

    # Show log directory info
    print("\n📊 Log Directory Information:")
    show_log_directory_info()


def demo_daily_log_files():
    """Demo: Show how daily log files work"""
    print("\n" + "=" * 60)
    print("DEMO: Daily Log File Organization")
    print("=" * 60)

    # Configure logging to use default directory
    log_to_console_and_file()
    logger = get_logger()

    print("📝 Creating some log entries...")

    # Simulate some operations that will be logged
    logger.info("Starting daily log file demo")
    logger.success("SDK initialized successfully")

    # Simulate dataset operations
    logger.dataset_created("demo-123", "Daily Demo Dataset")
    logger.dataset_uploading("Daily Demo Dataset")
    logger.dataset_uploaded("Daily Demo Dataset")

    # Simulate search operations
    logger.search_started("labels", "cat")
    logger.search_completed(25, "labels", "cat")

    # Show current log file
    current_log_file = get_logger().logger.handlers[1].baseFilename if len(get_logger().logger.handlers) > 1 else "None"
    print(f"\n✅ Log entries written to: {current_log_file}")

    # Show log file contents
    if os.path.exists(current_log_file):
        print(f"\n📄 Log file contents:")
        print("-" * 50)
        with open(current_log_file, "r", encoding="utf-8") as f:
            content = f.read()
            if content.strip():
                print(content)
            else:
                print("(File is empty)")
        print("-" * 50)


def demo_log_file_management():
    """Demo: Log file management features"""
    print("\n" + "=" * 60)
    print("DEMO: Log File Management")
    print("=" * 60)

    # List all log files
    log_files = list_log_files()
    print(f"📄 Found {len(log_files)} log files:")

    for i, log_file in enumerate(log_files[-5:], 1):  # Show last 5
        file_size = os.path.getsize(log_file)
        file_time = os.path.getmtime(log_file)
        from datetime import datetime

        file_time_str = datetime.fromtimestamp(file_time).strftime("%Y-%m-%d %H:%M:%S")
        print(f"  {i}. {os.path.basename(log_file)}")
        print(f"     Size: {file_size} bytes")
        print(f"     Modified: {file_time_str}")

    # Get latest log file
    latest_log = get_latest_log_file()
    if latest_log:
        print(f"\n🔄 Most recent log file: {os.path.basename(latest_log)}")
    else:
        print("\n🔄 No log files found")


def demo_custom_log_directory():
    """Demo: Using custom log directory"""
    print("\n" + "=" * 60)
    print("DEMO: Custom Log Directory")
    print("=" * 60)

    # Create custom log directory
    custom_log_dir = "custom_logs"
    custom_log_file = os.path.join(custom_log_dir, "custom_app.log")

    print(f"📁 Using custom log directory: {custom_log_dir}")

    # Configure logging with custom directory
    configure_logging(output_destinations=["stdout", "file"], log_file=custom_log_file, level=logging.INFO)

    logger = get_logger()
    logger.info("Testing custom log directory")
    logger.success("Custom logging configured successfully")

    print(f"✅ Custom log file created: {custom_log_file}")

    # Show custom log file contents
    if os.path.exists(custom_log_file):
        print(f"\n📄 Custom log file contents:")
        print("-" * 50)
        with open(custom_log_file, "r", encoding="utf-8") as f:
            content = f.read()
            if content.strip():
                print(content)
            else:
                print("(File is empty)")
        print("-" * 50)


def demo_production_logging():
    """Demo: Production-style logging"""
    print("\n" + "=" * 60)
    print("DEMO: Production Logging Setup")
    print("=" * 60)

    # Configure for production (file only, no console output)
    production_log_dir = "production_logs"
    production_log_file = os.path.join(production_log_dir, "production.log")

    print(f"🏭 Configuring production logging...")
    print(f"📁 Production log directory: {production_log_dir}")
    print(f"📄 Production log file: {production_log_file}")

    log_to_file_only(production_log_file)
    logger = get_logger()

    # Simulate production operations
    logger.info("Production application started")
    logger.info("Loading configuration...")
    logger.success("Configuration loaded successfully")

    # Simulate some API operations
    logger.api_health_check({"status": "healthy", "version": "1.0.0"})
    logger.info("Processing batch of 1000 images...")
    logger.success("Batch processing completed successfully")

    # Simulate error handling
    logger.warning("High memory usage detected")
    logger.error("Failed to connect to external service")

    print(f"✅ Production log entries written to: {production_log_file}")
    print("🔇 Note: No console output in production mode")


def show_platform_specific_info():
    """Show platform-specific log directory information"""
    print("\n" + "=" * 60)
    print("PLATFORM-SPECIFIC LOG DIRECTORY INFORMATION")
    print("=" * 60)

    import platform

    system = platform.system()

    print(f"🖥️  Operating System: {system}")

    if system == "Windows":
        print("\n📁 Windows Log Directory:")
        print("  Default: %APPDATA%/VisualLayer/logs/")
        print("  Example: C:\\Users\\Username\\AppData\\Roaming\\VisualLayer\\logs\\")
        print("  Files: visual_layer_sdk_YYYY-MM-DD.log")

    elif system == "Darwin":  # macOS
        print("\n📁 macOS Log Directory:")
        print("  Default: ~/.local/share/visual-layer/logs/")
        print("  Example: /Users/username/.local/share/visual-layer/logs/")
        print("  Files: visual_layer_sdk_YYYY-MM-DD.log")

    else:  # Linux
        print("\n📁 Linux Log Directory:")
        print("  Default: ~/.local/share/visual-layer/logs/")
        print("  Example: /home/username/.local/share/visual-layer/logs/")
        print("  Files: visual_layer_sdk_YYYY-MM-DD.log")

    print("\n💡 Standard Application Logging Conventions:")
    print("  • Daily log files with date stamps")
    print("  • Platform-appropriate directory locations")
    print("  • Automatic directory creation")
    print("  • Timestamped log entries")
    print("  • Log level indicators")
    print("  • UTF-8 encoding for international support")


def main():
    """Run all standard logging demos"""

    print("🚀 Visual Layer SDK - Standard Logging Directory Demo")
    print("This demo shows how logs are organized following standard conventions")

    # Run all demos
    demo_standard_log_directory()
    demo_daily_log_files()
    demo_log_file_management()
    demo_custom_log_directory()
    demo_production_logging()
    show_platform_specific_info()

    print("\n" + "=" * 60)
    print("📝 SUMMARY OF STANDARD LOGGING FEATURES")
    print("=" * 60)

    print("\n🎯 Standard Log Directory Structure:")
    print("• Platform-appropriate default locations")
    print("• Daily log files with date stamps")
    print("• Automatic directory creation")
    print("• Organized file naming conventions")

    print("\n🔧 Log File Management:")
    print("• List all log files")
    print("• Get latest log file")
    print("• Show log directory information")
    print("• Custom log directory support")

    print("\n💼 Production Features:")
    print("• File-only logging for production")
    print("• Timestamped entries")
    print("• Log level indicators")
    print("• UTF-8 encoding support")

    print("\n🔄 Log File Organization:")
    print("• One file per day")
    print("• Automatic rotation")
    print("• Easy to find and manage")
    print("• Standard naming convention")

    print("\n✅ Demo Complete!")
    print("Check the log directories to see the organized log files.")


if __name__ == "__main__":
    main()
