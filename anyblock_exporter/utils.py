# utils.py

from typing import List, Dict, Any
import re
import unicodedata
import os

def sanitize_filename(filename: str, max_length: int = 150) -> str:
    if not filename.strip():
        return "Untitled"
    
    # Remove invalid characters, but keep spaces
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Truncate if too long
    if len(filename) > max_length:
        filename = filename[:max_length].rstrip()
    
    return filename or "Untitled"

def format_inline_text(text: str, marks: List[Dict[str, Any]]) -> str:
    if not marks:
        return text

    formatted_text = text
    offset = 0

    for mark in sorted(marks, key=lambda x: x['range']['from']):
        start = mark['range']['from'] + offset
        end = mark['range']['to'] + offset
        mark_type = mark['type']

        if mark_type == 'Bold':
            formatted_text = f"{formatted_text[:start]}**{formatted_text[start:end]}**{formatted_text[end:]}"
            offset += 4
        elif mark_type == 'Italic':
            formatted_text = f"{formatted_text[:start]}*{formatted_text[start:end]}*{formatted_text[end:]}"
            offset += 2
        elif mark_type == 'Underscored':
            formatted_text = f"{formatted_text[:start]}_{formatted_text[start:end]}_{formatted_text[end:]}"
            offset += 2
        elif mark_type == 'Strikethrough':
            formatted_text = f"{formatted_text[:start]}~~{formatted_text[start:end]}~~{formatted_text[end:]}"
            offset += 4
        elif mark_type == 'Link':
            url = mark.get('param', '')
            formatted_text = f"{formatted_text[:start]}[{formatted_text[start:end]}]({url}){formatted_text[end:]}"
            offset += len(url) + 4

    return formatted_text

def convert_table_to_markdown(table_block: Dict[str, Any]) -> str:
    markdown_table = ""
    columns = table_block.get('columns', [])
    rows = table_block.get('rows', [])

    # Create header
    header = "|" + "|".join([col.get('name', '') for col in columns]) + "|\n"
    separator = "|" + "|".join(['---' for _ in columns]) + "|\n"
    markdown_table += header + separator

    # Create rows
    for row in rows:
        row_data = "|" + "|".join([cell.get('content', '') for cell in row.get('cells', [])]) + "|\n"
        markdown_table += row_data

    return markdown_table

def format_latex_equation(equation: str) -> str:
    return f"$${equation}$$"

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[^\w\-_\. ]', '_', filename)