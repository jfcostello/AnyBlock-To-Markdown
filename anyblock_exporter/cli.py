# cli.py

import argparse
from anyblock_exporter.config import Config

def parse_arguments():
    parser = argparse.ArgumentParser(description="Convert Anytype export to Markdown")
    parser.add_argument("input_folder", nargs='?', default=None, 
                        help="Path to the folder containing Anytype export files (default: ./anyblock_files)")
    parser.add_argument("--output_folder", default=None, 
                        help="Path to the output folder for Markdown files (default: ./markdown_files)")
    parser.add_argument("--log_level", default=Config.LOG_LEVEL, 
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="Set the logging level")
    return parser.parse_args()