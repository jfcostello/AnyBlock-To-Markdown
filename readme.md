# Anyblock Exporter

Anyblock Exporter is an open-source tool designed to convert Anytype exports into Markdown format. This tool allows users to easily transform their Anytype content into a more universal and portable format, facilitating content migration, backup, or integration with other Markdown-compatible systems. Note, this tool was built with a goal of exporting my own data, so had not been tested thoroughly and is liable to break or be missing edge cases I didn't encounter. As such, please either send feedback by opening an issue on Github, emailing jamie@jfcostello.com or, if you want, submit a pull request!

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [How to download and use the tool](#how-to-download-and-use-the-tool)
  - [Step 1: Downloading the files](#step-1-downloading-the-files)
  - [Step 2: Install Pyton](#step-2-install-pyton)
  - [Step 3: Export your Anytype data](#step-3-export-your-anytype-data)
  - [Step 4: Customize the config.yaml file](#step-4-customize-the-configyaml-file)
  - [Step 5: Run the script](#step-5-run-the-script)
- [Configuration](#configuration)
  - [config.yaml](#configyaml)
- [Conversion Process](#conversion-process)
  - [File Naming and Truncation](#file-naming-and-truncation)
  - [Relation Handling](#relation-handling)
  - [Block Conversion](#block-conversion)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Converts Anytype Anyblock JSON exports to Markdown format
- Preserves document structure, including headers, lists, and code blocks
- Handles nested content and maintains hierarchy
- Extracts and links file attachments
- Processes tables and equations
- Maintains metadata and relations as properties

## Requirements

- Python 3.7 or higher
- python modules: tqdm, pyyaml, chardet

## How to download and use the tool

### Step 1: Downloading the files

#### Option 1: Git clone

   Open 'Terminal'
   Navigate to the folder you want to put the tool in, and then type the following:
   ```
   git clone https://github.com/yourusername/anyblock-exporter.git
   ```
   to open the folder in terminal, type:
   ```
   cd anyblock-exporter
   ```

#### Option 2: Download zip 

If you're not familiar with Git commands or using the terminal, you may find it easier to just download the zip file
Goto https://github.com/yourusername/anyblock-exporter, click the green 'Code' button, then click 'Download ZIP'
Extract the zip file to a folder and remember where you put it for later

### Step 2: Install Pyton

Install Python:
   If you don't have Python installed on your computer, follow these steps to install it:

   - **Windows:**
     1. Go to the official Python website: https://www.python.org/
     2. Click on the "Downloads" tab and select "Python 3.x.x" for Windows.
     3. Once the installer is downloaded, open it.
     4. Make sure to check the box that says "Add Python to PATH" before clicking "Install Now".
     5. Follow the prompts to complete the installation.

   - **macOS:**
     1. Go to the official Python website: https://www.python.org/
     2. Click on the "Downloads" tab and select "Python 3.x.x" for macOS.
     3. Once the installer is downloaded, open it.
     4. Follow the prompts to complete the installation.

   - **Linux:**
     1. Open a terminal.
     2. Use the package manager specific to your distribution to install Python. For example, on Ubuntu, you can use the following commands:
        ```
        sudo apt update
        sudo apt install python3
        ```
     3. Follow the prompts to complete the installation.

4. Optional - verify the installation:
   1. Open a terminal or command prompt.
   2. Type `python --version` and press Enter.
   3. You should see the installed Python version displayed. If you see a version number, Python is installed correctly.

### Step 3: Export your Anytype data

1. In Anytype, export your data using the Anyblock option, selecting the JSON format. You can export your entire space, parts of it, or just one page.
2. Place all the exported JSON files in the `anyblock_files` directory of this project (Note, even if you export just one page, you'll end up with hundreds of JSON files and you'll need them all). Ensure all files you want to convert are in the folder rather than in any subfolders.

### Step 4: Optional - Customize the config.yaml file

In the /anyblock_exporter/ directory, you'll see a file called config.yaml. Open this in a text editor, one like notepad will do, and you can customize certain aspects of the conversion process. You don't need to use terminal to access this, you can open it in windows explorer or finder or whatever you use, find config.yaml and open it with any old text editor.

To see what each setting does, look below at the [Configuration](#configuration) section

Note, this is optional, and you can just run the script with the default settings

### Step 5: Run the script

Open a terminal and navigate to the project directory. On windows, to make it easy, you can right click the folder in explorer, select 'open in terminal'. For Mac, you can open the folder in finder, right click and select 'new terminal at folder'.

Once open, just run the script. To do so, type:
```
python anyblock_exporter.py
```

If you get an error saying 'command not found: python' some instances, you may need to instead type
```
python3 anyblock_exporter.py
```

If you get an error about missing modules, you can install them by typing

```
pip install -r requirements.txt
```
OR, if you get an error about pip not being found, you can install the modules by typing
```
pip3 install -r requirements.txt
```

And then try running the script again.

The converted Markdown files will be created in the `markdown_files` directory.

## Configuration

### config.yaml

The `config.yaml` file in the /anyblock_exporter/ directory allows you to customize various aspects of the conversion process:

decode_timestamps: 

Can be set to yes or no, defaults to yes. If set, it'll try convert timestamps into EST, if no, it'll leave them as unix timestamps

ignored_properties:
  - name
  - snippet
  - etc

**This is the most important setting**. Put the list of all properties (relations) you want to ignore here. There's alot of metadata, and it can be verbose without this, so default sets a reasonable amount of ignores. But if something is not showing up for you, come here and see if removing some of these will reveal it. Or, if you see Anytype adding weird things to the metadata, you can add them here to ignore them.

input_folder: anyblock_files
output_folder: markdown_files

Define the input and output folder for the script. Change it if the mood so takes you.

log_level: INFO
log_file: anytype_conversion.log

Sets the log level and name of the file the logs are dumped in, mainly used for troubleshooting. If nothing is going wrong, no need to worry

The exporter supports the following standard Python logging levels, from least to most severe:

- **DEBUG**: Detailed information, typically useful for diagnosing problems. Shows all conversion steps and detailed processing information.
- **INFO** (Default): Confirmation that things are working as expected. Shows general progress and successful operations.
- **WARNING**: Indicates something unexpected happened or may happen in the near future (e.g., 'disk space low'). The program is still working as expected.
- **ERROR**: Due to a more serious problem, the software has not been able to perform some function. Shows failed operations that need attention.
- **CRITICAL**: A serious error indicating the program itself may be unable to continue running.

turn_relations_into_obsidian_links: 

If set to 'none' (or in fact, blank or anything that isn't some or all), all relations are just in plain text - relation: value
If set to some, the script will attempt to identify fields that are time/date stamps or free form text. For those fields, it renders in plain text, relation: value. But for the rest, it'll render relation: "[[value]]" which is useful in Obsidian creating links. If you have selects or multi selects, probably use this especially if you may use Obsidian
If set to all, it does the same as 'some' except it'll also wrap plain text relations in that link style - but still no dates

## Conversion Process

### File Naming and Truncation

- Output filenames are derived from the original Anytype object titles.
- Filenames are sanitized to remove invalid characters, so you may see some weird _s in some titles. Sorry.
- If a filename exceeds 150 characters, it's truncated to preserve the beginning of the name.
- For truncated filenames, the original full title is added as a 'title' relation in the frontmatter.
- Files with no title are named "untitled.md", "untitled-1.md", etc.

### Relation Handling

- Relations from Anytype are converted to YAML frontmatter in the Markdown files.
- Certain relations can be ignored based on the `ignored_properties` list in `config.yaml`.
- Relations can be formatted as Obsidian-style links based on the `turn_relations_into_obsidian_links` setting.
- Timestamps in relations are optionally converted to readable dates.

### Block Conversion

- The converter handles various Anytype block types:
  - Headers (multiple levels)
  - Paragraphs
  - Lists (ordered and unordered)
  - Code blocks (with language specification)
  - Checkboxes
  - Equations
  - Tables
  - File attachments
- Any parent/children blocks (like Toggles, say) are properly indented to maintain hierarchy using the standard markdown >, >> etc. In theory. This proved shockingly annoying to do. Not guaranteed to always work perfectly.

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

## Contributing

Contributions to the Anyblock Exporter are welcome! Please feel free to submit pull requests, create issues or spread the word.



