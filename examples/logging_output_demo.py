#!/usr/bin/env python3
"""
Demo script showing different logging output destinations for the Visual Layer SDK.
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the path so we can import the SDK
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from visual_layer_sdk.logger import configure_logging, log_to_console_only, log_to_file_only, log_to_console_and_file, log_to_stderr, get_logger, get_log_file_path, set_verbose


def demo_console_only():
    """Demo: Log to console only (default behavior)"""
    print("\n" + "=" * 60)
    print("DEMO 1: Console Only Logging (Default)")
    print("=" * 60)

    log_to_console_only()
    logger = get_logger()

    logger.info("This message goes to the console only")
    logger.success("Success message in console")
    logger.warning("Warning message in console")
    logger.error("Error message in console")

    print("✅ All messages above appeared in the console")


def demo_file_only():
    """Demo: Log to file only"""
    print("\n" + "=" * 60)
    print("DEMO 2: File Only Logging")
    print("=" * 60)

    log_file = "logs/demo_file_only.log"
    log_to_file_only(log_file)
    logger = get_logger()

    logger.info("This message goes to the log file only")
    logger.success("Success message in file")
    logger.warning("Warning message in file")
    logger.error("Error message in file")

    print(f"✅ All messages were written to: {log_file}")
    print(f"📄 Check the file to see the logged messages")


def demo_console_and_file():
    """Demo: Log to both console and file"""
    print("\n" + "=" * 60)
    print("DEMO 3: Console and File Logging")
    print("=" * 60)

    log_file = "logs/demo_console_and_file.log"
    log_to_console_and_file(log_file)
    logger = get_logger()

    logger.info("This message goes to both console and file")
    logger.success("Success message in both places")
    logger.warning("Warning message in both places")
    logger.error("Error message in both places")

    print(f"✅ Messages appeared in console AND were written to: {log_file}")


def demo_stderr():
    """Demo: Log to stderr"""
    print("\n" + "=" * 60)
    print("DEMO 4: Stderr Logging")
    print("=" * 60)

    log_to_stderr()
    logger = get_logger()

    logger.info("This message goes to stderr")
    logger.success("Success message in stderr")
    logger.warning("Warning message in stderr")
    logger.error("Error message in stderr")

    print("✅ All messages above went to stderr (error stream)")


def demo_verbose_logging():
    """Demo: Verbose logging with different destinations"""
    print("\n" + "=" * 60)
    print("DEMO 5: Verbose Logging with File Output")
    print("=" * 60)

    log_file = "logs/demo_verbose.log"
    configure_logging(output_destinations=["stdout", "file"], log_file=log_file, level=logging.DEBUG)
    logger = get_logger()

    logger.info("Info message (visible in both console and file)")
    logger.debug("Debug message (only visible in verbose mode)")
    logger.success("Success message with detailed logging")

    # Simulate some operations
    logger.dataset_created("test-123", "My Test Dataset")
    logger.dataset_uploading("My Test Dataset")
    logger.dataset_uploaded("My Test Dataset")
    logger.search_started("labels", "cat")
    logger.search_completed(42, "labels", "cat")

    print(f"✅ Verbose messages appeared in console AND were written to: {log_file}")
    print("🔍 Check the log file for detailed timestamps and debug information")


def demo_custom_configuration():
    """Demo: Custom logging configuration"""
    print("\n" + "=" * 60)
    print("DEMO 6: Custom Logging Configuration")
    print("=" * 60)

    # Configure with custom settings
    configure_logging(output_destinations=["stdout", "file"], log_file="logs/custom_demo.log", level=logging.INFO)
    logger = get_logger()

    logger.info("Custom configuration demo")
    logger.success("This uses custom log file and settings")

    # Show current log file path
    current_log_file = get_log_file_path()
    print(f"📄 Current log file: {current_log_file}")


def show_log_file_contents(log_file: str):
    """Show the contents of a log file"""
    if os.path.exists(log_file):
        print(f"\n📄 Contents of {log_file}:")
        print("-" * 40)
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
            if content.strip():
                print(content)
            else:
                print("(File is empty)")
        print("-" * 40)
    else:
        print(f"❌ Log file not found: {log_file}")


def main():
    """Run all logging output demos"""

    print("🚀 Visual Layer SDK - Logging Output Destinations Demo")
    print("This demo shows where logging output can be directed")

    # Create logs directory
    os.makedirs("logs", exist_ok=True)

    # Run all demos
    demo_console_only()
    demo_file_only()
    demo_console_and_file()
    demo_stderr()

    # Import logging for verbose demo
    import logging

    demo_verbose_logging()
    demo_custom_configuration()

    # Show some log file contents
    print("\n" + "=" * 60)
    print("LOG FILE CONTENTS")
    print("=" * 60)

    log_files = ["logs/demo_file_only.log", "logs/demo_console_and_file.log", "logs/demo_verbose.log", "logs/custom_demo.log"]

    for log_file in log_files:
        show_log_file_contents(log_file)

    print("\n" + "=" * 60)
    print("📝 SUMMARY OF LOGGING OUTPUT OPTIONS")
    print("=" * 60)

    print("\n🎯 Available Output Destinations:")
    print("• stdout (console) - Default, user-friendly messages")
    print("• stderr (error stream) - For error messages")
    print("• file - Persistent logging with timestamps")
    print("• Multiple destinations - Combine any of the above")

    print("\n🔧 Configuration Functions:")
    print("• log_to_console_only() - Console output only")
    print("• log_to_file_only(log_file) - File output only")
    print("• log_to_console_and_file(log_file) - Both console and file")
    print("• log_to_stderr() - Error stream output")
    print("• configure_logging() - Custom configuration")

    print("\n📊 Log Levels:")
    print("• INFO - General information (default)")
    print("• DEBUG - Detailed debugging information")
    print("• WARNING - Warning messages")
    print("• ERROR - Error messages")

    print("\n💡 Use Cases:")
    print("• Development: Console + file for debugging")
    print("• Production: File only for persistent logs")
    print("• Testing: Console only for immediate feedback")
    print("• Errors: Stderr for error handling")

    print("\n✅ Demo Complete! Check the 'logs' directory for generated log files.")


if __name__ == "__main__":
    main()
