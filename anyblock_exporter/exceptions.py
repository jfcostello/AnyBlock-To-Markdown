# anyblock_exporter/exceptions.py
class AnytypeConverterError(Exception):
    """Base exception class for Anytype Converter errors."""
    pass

class JSONReadError(AnytypeConverterError):
    """Raised when there's an error reading JSON files."""
    pass