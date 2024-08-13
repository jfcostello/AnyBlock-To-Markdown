# Anyblock Exporter

Anyblock Exporter is an open-source tool designed to convert Anytype exports into Markdown format. This tool allows users to easily transform their Anytype content into a more universal and portable format, facilitating content migration, backup, or integration with other Markdown-compatible systems.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Converts Anytype JSON exports to Markdown format
- Preserves document structure, including headers, lists, and code blocks
- Handles nested content and maintains hierarchy
- Extracts and links file attachments
- Processes tables and equations
- Maintains metadata and relations as properties

## Requirements

- Python 3.7 or higher

## Installation

Clone the repository:
   ```
   git clone https://github.com/yourusername/anyblock-exporter.git
   cd anyblock-exporter
   ```

## Usage

1. Export your files from Anytype, use their Anyblock format and export in JSON

2. Place your Anytype JSON export files in the `anyblock_files` directory.

4. Run the conversion script:
   ```
   python anyblock_exporter.py
   ```

4. Find the converted Markdown files in the `markdown_files` directory.

### Command-line Options

- `input_folder`: Specify a custom input folder (default: `anyblock_files`)
- `--output_folder`: Specify a custom output folder (default: `markdown_files`)
- `--log_level`: Set the logging level (choices: DEBUG, INFO, WARNING, ERROR, CRITICAL)

Example:
```
python anyblock_exporter.py custom_input --output_folder custom_output --log_level DEBUG
```

## Configuration

The project uses a `Config` class (in `config.py`) to manage configuration settings. You can modify these settings directly in the `config.py` file:

- `INPUT_FOLDER`: Directory containing Anytype JSON files
- `OUTPUT_FOLDER`: Directory for generated Markdown files
- `ATTACHMENTS_FOLDER`: Subdirectory for file attachments
- `LOG_FILE`: Name of the log file
- `LOG_LEVEL`: Logging verbosity

Additionally, as there are many relations and most are unimportant or a repeat, there are a list of ignored relations in 'relation_handler.py'. If you're having trouble seeing a relation you expect to see, you can remove ignored relations from there

## Project Structure

- `anyblock_exporter.py`: Main script to run the conversion
- `anyblock_exporter/`: Package containing the core functionality
  - `__init__.py`: Package initializer
  - `cli.py`: Command-line interface handling
  - `config.py`: Configuration settings
  - `converter.py`: Main conversion logic
  - `block_converter.py`: Individual block type conversion
  - `relation_handler.py`: Processes Anytype relations
  - `file_handler.py`: Manages file attachments
  - `utils.py`: Utility functions
  - `logger.py`: Logging setup

  ## anyblock.md

Found in /anyblock_exporter/docs this is a frankenstein file barely meant for human consumption, it was there mostly to guide the LLMs in the coding process. I put it together by showing them Anytypes documentation, example json, and converters into Anytype people have made. I asked the LLMs to write plain English documentation on how it all works to keep my token count down for future conversations. So as such there's lots of good content in there, but the formatting and structure are all over the place and there's almost certainly lots of repitiion, but I'm keeping it here in case anybody finds it useful at all