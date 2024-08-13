import logging
from typing import Dict, Any, List
from anyblock_exporter.utils import format_inline_text, convert_table_to_markdown, format_latex_equation

def is_organizational_block(block: Dict[str, Any]) -> bool:
    """Determine if a block is an organizational block that should not contribute to content."""
    return block.get('layout', {}).get('style') == 'Div' or not block.get('text', {}).get('text', '')

def has_unique_children(block: Dict[str, Any], all_blocks: Dict[str, Any], processed_blocks: set) -> bool:
    """Check if the block has any unprocessed children with different IDs."""
    for child_id in block.get('childrenIds', []):
        if child_id not in processed_blocks and child_id != block['id']:
            return True
    return False

def convert_block_to_markdown(block: Dict[str, Any], all_blocks: Dict[str, Any], parent_indent: str, is_top_level: bool, file_handler, processed_blocks: set) -> str:
    if block is None or block.get('id') is None:
        return ""

    block_id = block['id']
    if block_id in processed_blocks:
        return ""
    processed_blocks.add(block_id)

    # If this is an organizational block, process its children as potential top-level blocks
    if is_organizational_block(block):
        markdown = ""
        for child_id in block.get('childrenIds', []):
            child_block = all_blocks.get(child_id)
            if child_block and child_id not in processed_blocks:
                markdown += convert_block_to_markdown(
                    child_block, 
                    all_blocks, 
                    parent_indent, 
                    is_top_level,  # Pass down the is_top_level flag
                    file_handler, 
                    processed_blocks
                )
        return markdown

    # Determine current indent: no indent for top-level blocks, otherwise add one level
    current_indent = "" if is_top_level else parent_indent + '>'

    # Process content block
    block_type = block.get('text', {}).get('style', 'Paragraph')
    content = block.get('text', {}).get('text', '')
    marks = block.get('text', {}).get('marks', {}).get('marks', [])
    
    content = format_inline_text(content, marks) if content else ""

    def apply_indent(text: str) -> str:
        if not current_indent:
            return text
        return '\n'.join(f"{current_indent}{line}" for line in text.split('\n') if line.strip())

    markdown = ""

    if block_type.startswith('Header'):
        level = block_type[-1]
        markdown += f"{current_indent}{'#' * int(level)} {content}\n\n"
    elif block_type in ['Paragraph', 'Toggle']:
        markdown += apply_indent(content) + "\n\n" if content else ""
    elif block_type in ['Marked', 'Numbered']:
        prefix = '- ' if block_type == 'Marked' else f"1. "
        markdown += apply_indent(f"{prefix}{content}") + "\n"
    elif block_type == 'Code':
        lang = block.get('fields', {}).get('lang', '')
        code_block = f"```{lang}\n{content}\n```"
        markdown += apply_indent(code_block) + "\n"
    elif block_type == 'Checkbox':
        checked = '☒' if block.get('text', {}).get('checked', False) else '☐'
        markdown += apply_indent(f"{checked} {content}") + "\n"
    elif block_type == 'Equation':
        equation = format_latex_equation(content)
        markdown += apply_indent(equation) + "\n\n"
    elif block.get('file'):
        attachment = file_handler.handle_file_attachment(block['file'])
        markdown += apply_indent(attachment) + "\n\n"
    elif block_type == 'Table':
        table = convert_table_to_markdown(block)
        markdown += apply_indent(table) + "\n"
    else:
        logging.warning(f"Unknown block type: {block_type}")
        markdown += apply_indent(content) + "\n\n"

    # Process children, treating them as non-top-level
    if has_unique_children(block, all_blocks, processed_blocks):
        for child_id in block.get('childrenIds', []):
            child_block = all_blocks.get(child_id)
            if child_block and child_id not in processed_blocks and child_id != block_id:
                markdown += convert_block_to_markdown(
                    child_block, 
                    all_blocks, 
                    current_indent, 
                    False,  # Children are not top-level
                    file_handler, 
                    processed_blocks
                )

    return markdown

def process_blocks(blocks: List[Dict[str, Any]], file_handler) -> str:
    all_blocks = {block['id']: block for block in blocks if block.get('id')}
    processed_blocks = set()
    markdown_content = ""
    
    root_block = blocks[0] if blocks else None
    if root_block:
        for child_id in root_block.get('childrenIds', []):
            child_block = all_blocks.get(child_id)
            if child_block and child_id not in processed_blocks:
                markdown_content += convert_block_to_markdown(
                    child_block, 
                    all_blocks, 
                    "", 
                    True,  # Treat direct children of root as top-level
                    file_handler, 
                    processed_blocks
                )
    
    return markdown_content