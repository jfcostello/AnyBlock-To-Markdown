# file_handler.py

import os
import shutil
from typing import Dict, Any
import logging

class FileHandler:
    def __init__(self, attachments_folder: str):
        self.attachments_folder = attachments_folder
        self.files_to_copy = {}

    def handle_file_attachment(self, file_info: Dict[str, Any]) -> str:
        file_name = file_info.get('name', 'unnamed_file')
        file_hash = file_info.get('hash', '')
        
        if file_hash:
            self.files_to_copy[file_hash] = file_info
            return f"![{file_name}](attachments/{file_hash}_{file_name})"
        else:
            return f"[{file_name}](file_not_found)"

    def copy_all_files(self):
        for file_hash, file_info in self.files_to_copy.items():
            source_path = os.path.join(self.attachments_folder, '..', file_hash)
            dest_path = os.path.join(self.attachments_folder, f"{file_hash}_{file_info['name']}")
            if os.path.exists(source_path):
                shutil.copy2(source_path, dest_path)
            else:
                logging.warning(f"File not found: {source_path}")