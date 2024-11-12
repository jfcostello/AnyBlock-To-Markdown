import logging
import os
import sys
from anyblock_exporter import (
    parse_arguments,
    setup_logger,
    get_logger,
    AnytypeConverter,
    config
)
from anyblock_exporter.exceptions import AnytypeConverterError, JSONReadError

def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Use config values with fallback to command-line arguments and then default values
    input_folder = args.input_folder or config.get('input_folder', 'anyblock_files')
    output_folder = args.output_folder or config.get('output_folder', 'markdown_files')
    log_level = args.log_level or config.get('log_level', 'INFO')
    log_file = config.get('log_file', 'anytype_conversion.log')

    # Setup logging
    setup_logger(log_level, log_file)
    logger = logging.getLogger("anyblock_exporter")

    logger.info("Starting Anytype to Markdown conversion")

    # Validate input folder
    if not os.path.exists(input_folder):
        logger.error(f"Input folder does not exist: {input_folder}")
        sys.exit(1)

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    try:
        # Initialize and run the converter
        converter = AnytypeConverter(input_folder, output_folder)
        converter.process_all_files()

        logger.info("Conversion completed successfully")
    
    except JSONReadError as e:
        logger.error(f"Error reading JSON files: {str(e)}")
        sys.exit(1)
    except AnytypeConverterError as e:
        logger.error(f"Anytype Converter error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"An unexpected error occurred during conversion: {str(e)}")
        sys.exit(1)

    # Print summary
    print(f"Conversion complete. Output files are in: {output_folder}")

if __name__ == "__main__":
    main()