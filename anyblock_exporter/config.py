# config.py
import os

class Config:
    # Get the current script's directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Logging configuration
    LOG_FILE = 'anytype_conversion.log'
    LOG_LEVEL = 'INFO'

    # File paths
    INPUT_FOLDER = os.path.join(BASE_DIR, 'anyblock_files')
    OUTPUT_FOLDER = os.path.join(BASE_DIR, 'markdown_files')
    ATTACHMENTS_FOLDER = 'attachments'
    # Conversion settings
    MAX_HEADING_LEVEL = 6
    CODE_BLOCK_LANG_DEFAULT = ''
    EQUATION_DELIMITER = '$$'

    # Relation settings
    RELATION_SECTION_TITLE = '## Relations'

    # File handling
    ALLOWED_FILE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx']
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    # Performance
    BATCH_SIZE = 100  # Number of files to process in a batch