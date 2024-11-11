# converter.py

import os
import json
import logging
import traceback
import chardet
from tqdm import tqdm
from typing import List, Dict, Any
from anyblock_exporter.block_converter import process_blocks, convert_block_to_markdown
from anyblock_exporter.utils import sanitize_filename
from anyblock_exporter.relation_handler import RelationHandler
from anyblock_exporter.file_handler import FileHandler
from anyblock_exporter.exceptions import JSONReadError
from datetime import datetime



class AnytypeConverter:
    def __init__(self, input_folder: str, output_folder: str):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.attachments_folder = os.path.join(output_folder, 'attachments')
        self.json_objects = []  # This will store all the JSON objects
        self.relation_handler = None  # Initialize later after reading JSON files
        self.file_handler = FileHandler(self.attachments_folder)

    def read_json_files(self) -> None:
        try:
            # Count total number of files to process
            total_files = sum([len(files) for _, _, files in os.walk(self.input_folder)])
            
            # Initialize progress bar
            pbar = tqdm(total=total_files, desc="Processing files", unit="file")
            
            for root, dirs, files in os.walk(self.input_folder):
                for filename in files:
                    if filename.endswith('.json'):
                        file_path = os.path.join(root, filename)
                        try:
                            # Try reading with default encoding (utf-8)
                            with open(file_path, 'r', encoding='utf-8') as file:
                                json_data = json.load(file)
                                self.json_objects.append(json_data)
                        except (json.JSONDecodeError, UnicodeDecodeError) as e:
                            logging.warning(f"Error decoding JSON in file {file_path} with default encoding: {str(e)}")
                            try:
                                # Detect encoding for files that fail with default encoding
                                with open(file_path, 'rb') as file:
                                    raw_data = file.read()
                                    result = chardet.detect(raw_data)
                                    encoding = result['encoding']
                                
                                # Read file with detected encoding
                                with open(file_path, 'r', encoding=encoding) as file:
                                    json_data = json.load(file)
                                    self.json_objects.append(json_data)
                                    logging.info(f"Successfully read file {file_path} with detected encoding: {encoding}")
                            except (json.JSONDecodeError, IOError) as e:
                                logging.error(f"Error decoding JSON in file {file_path} with detected encoding: {str(e)}")
                            except Exception as e:
                                logging.error(f"An error occurred while reading file {file_path}: {str(e)}")
                        
                        # Update progress bar
                        pbar.update(1)
            
            # Close progress bar
            pbar.close()
            
            if not self.json_objects:
                raise JSONReadError("No valid JSON files were read")
            
            logging.info(f"Read {len(self.json_objects)} JSON files")

            # Initialize RelationHandler after reading JSON files
            self.relation_handler = RelationHandler(self.json_objects)
        except Exception as e:
            logging.error(f"An error occurred while reading JSON files: {str(e)}")
            logging.error(traceback.format_exc()) # more detailed error traceback


    def identify_main_content_files(self) -> List[Dict[str, Any]]:
        main_contents = [obj for obj in self.json_objects if obj.get('sbType') == 'Page']
        if not main_contents:
            logging.error("No main content files found")
        return main_contents

    def extract_creation_date(self, main_content: Dict[str, Any]) -> str:
        try:
            created_date = main_content['snapshot']['data']['details'].get('createdDate')
            if created_date:
                return datetime.fromtimestamp(created_date).strftime('%Y-%m-%d %H:%M:%S')
            else:
                logging.warning("Creation date not found in main content file")
                return "Unknown creation date"
        except KeyError as e:
            logging.error(f"Error extracting creation date: {str(e)}")
            return "Unknown creation date"
        
    def process_nested_blocks(self, all_blocks: List[Dict[str, Any]], block_ids: List[str], depth: int = 0, processed_blocks: set = None) -> str:
        """Processes blocks in the order specified by block_ids, ignoring duplicates."""
        if processed_blocks is None:
            processed_blocks = set()  # Initialize the set to track processed blocks
        markdown = ""
        for block_id in block_ids:
            block = next((b for b in all_blocks if b['id'] == block_id), None)
            if block and block['id'] not in processed_blocks:
                markdown += convert_block_to_markdown(block, depth, self.file_handler, processed_blocks)
                processed_blocks.add(block['id']) # preventing duplicate processing
                # Recursively process children
                if 'childrenIds' in block and block['childrenIds']:
                    markdown += self.process_nested_blocks(all_blocks, block['childrenIds'], depth + 1, processed_blocks)
        return markdown

    def has_descendants(self, block: Dict[str, Any], all_blocks: List[Dict[str, Any]]) -> bool:
        """Recursively checks if a block has any descendants."""
        if 'childrenIds' in block and block['childrenIds']:
            for child_id in block['childrenIds']:
                child_block = next((b for b in all_blocks if b['id'] == child_id), None)
                if child_block and self.has_descendants(child_block, all_blocks):
                    return True
            return True  # Has direct children
        return False  # No children or descendants

    def compile_markdown(self, main_content: Dict[str, Any]) -> str:
        title = main_content['snapshot']['data']['details'].get('name', 'Untitled')
        blocks = main_content['snapshot']['data'].get('blocks', [])
        relations = self.relation_handler.extract_relations(main_content)

        markdown_content = "---\n"
        
        if relations:
            for relation in relations:
                markdown_content += f"{relation}\n"
        
        markdown_content += "---\n\n"

        # Use the new process_blocks function
        markdown_content += process_blocks(blocks, self.file_handler)

        return markdown_content
        
    def write_markdown_file(self, content: str, filename: str) -> None:
        try:
            os.makedirs(self.output_folder, exist_ok=True)
            
            # Handle blank or empty filenames
            if not filename.strip():
                filename = "untitled"
            
            safe_filename = sanitize_filename(filename)
            
            # Truncate filename if it's too long
            max_filename_length = 150
            is_truncated = len(safe_filename) > max_filename_length
            if is_truncated:
                safe_filename = safe_filename[:max_filename_length].rstrip()
            
            # Ensure .md extension
            if not safe_filename.lower().endswith('.md'):
                safe_filename += '.md'
            
            file_path = os.path.join(self.output_folder, safe_filename)
            
            # Handle duplicate filenames
            counter = 1
            while os.path.exists(file_path):
                name, ext = os.path.splitext(safe_filename)
                file_path = os.path.join(self.output_folder, f"{name}-{counter}{ext}")
                counter += 1
                if counter > 1000:  # Prevent infinite loop
                    logging.error("Too many duplicate filenames, aborting.")
                    return
            
            # Handle frontmatter
            content_lines = content.split('\n')
            if content.startswith('---'):
                try:
                    frontmatter_end = content_lines.index('---', 1)
                    frontmatter = content_lines[1:frontmatter_end]
                    
                    # Remove any existing 'title' or 'original_filename' relations
                    frontmatter = [line for line in frontmatter if not line.startswith(('title:', 'original_filename:'))]
                    
                    # Add title as a relation only if filename was truncated
                    if is_truncated:
                        frontmatter.insert(0, f"title: {filename}")
                    
                    # Reconstruct content with updated frontmatter
                    content = "---\n" + "\n".join(frontmatter) + "\n---\n" + "\n".join(content_lines[frontmatter_end+1:])
                except ValueError:
                    logging.error("Frontmatter is malformed or missing.")
                    frontmatter = []
            elif is_truncated:
                # If no frontmatter and filename is truncated, add frontmatter with title
                content = f"---\ntitle: {filename}\n---\n\n{content}"
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            logging.info(f"Markdown file created: {file_path}")
        except Exception as e:
            logging.error(f"Error writing Markdown file '{filename}': {str(e)}")
            fallback_filename = "untitled.md"
            counter = 1
            while os.path.exists(os.path.join(self.output_folder, fallback_filename)):
                fallback_filename = f"untitled-{counter}.md"
                counter += 1
                if counter > 1000:  # Prevent infinite loop
                    logging.error("Too many fallback filenames, aborting.")
                    return
            fallback_path = os.path.join(self.output_folder, fallback_filename)
            try:
                with open(fallback_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                logging.info(f"Fallback Markdown file created: {fallback_path}")
            except Exception as e:
                logging.error(f"Failed to create fallback file: {str(e)}")

    def process_all_files(self) -> None:
        try:
            self.read_json_files()
            main_contents = self.identify_main_content_files()
            os.makedirs(self.attachments_folder, exist_ok=True)
            for main_content in main_contents:
                try:
                    logging.debug(f"Processing content: {main_content.get('id', 'Unknown ID')}")
                    markdown_content = self.compile_markdown(main_content)
                    title = main_content['snapshot']['data']['details'].get('name', 'Untitled')
                    self.write_markdown_file(markdown_content, title)
                except Exception as e:
                    logging.error(f"Error processing file {main_content.get('id', 'Unknown ID')}: {str(e)}")
            self.file_handler.copy_all_files()
        except Exception as e:
            logging.error(f"Error in process_all_files: {str(e)}")