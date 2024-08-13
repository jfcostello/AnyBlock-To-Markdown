# Anytype to Markdown Exporter

## 1. Project Overview

### Brief Description
The Anytype to Markdown Exporter is a Python-based tool designed to convert Anytype exports (in JSON format) into readable Markdown files. This project aims to provide Anytype users with a way to export their notes and data into a more universally compatible format, preserving the content structure and essential metadata.

### Purpose and Goals
- Convert Anytype's proprietary JSON format (AnyBlock) to standard Markdown
- Preserve the hierarchical structure of notes
- Maintain important metadata such as creation dates and relations
- Provide a user-friendly tool for Anytype users to migrate or back up their data

## 2. Technical Specifications

### Input Format: Anytype JSON (AnyBlock)
The input for this converter is a collection of JSON files exported from Anytype. These files use a proprietary format called AnyBlock. Key characteristics include:

- Multiple JSON files for a single note or object
- Main content file identified by "sbType": "Page"
- Separate files for relations, often referenced by unique identifiers
- Block-based content structure
- Nested JSON objects representing different elements of a note

### Output Format: Markdown
The converter produces standard Markdown files (.md) with the following characteristics:

- GitHub Flavored Markdown (GFM) syntax
- Front matter section for metadata (creation date, tags, etc.)
- Structured headings to represent the original note's hierarchy
- Special sections for relations and other Anytype-specific data

### File Structure and Naming Conventions
Input:
- A folder containing multiple JSON files
- No specific naming convention for input files (randomly generated names)
- Each Anytype object (note) typically consists of multiple JSON files

Output:
- Single Markdown file per Anytype object
- Output filename derived from the original note's title or a unique identifier
- Accompanying folder for any attachments (if applicable)

## 3. System Requirements

### Required Software
- Python 3.7 or higher
- pip (Python package installer)

### Dependencies
- json (built-in)
- os (built-in)
- datetime (built-in)
- argparse (built-in)
- logging (built-in)

### Hardware Recommendations
- Minimum: Any system capable of running Python 3.7+
- Recommended: 
  - 4GB RAM or more for handling large exports
  - SSD for faster file I/O operations when dealing with numerous small JSON files

## 4. Installation

1. Clone the repository:
git clone https://github.com/yourusername/anytype-to-markdown.git
cd anytype-to-markdown
Copy
2. (Optional) Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
Copy
3. Install dependencies:
pip install -r requirements.txt
Copy
## 5. Usage

### Basic Usage
Run the script from the command line, providing the path to the folder containing the Anytype export:
python anytype_to_markdown.py /path/to/anytype/export
Copy
### Command-line Arguments
- `input_folder`: (Required) Path to the folder containing Anytype JSON files
- `--output_folder`: (Optional) Path to save the converted Markdown files. Default is ./output
- `--log_level`: (Optional) Set the logging level (DEBUG, INFO, WARNING, ERROR). Default is INFO

### Input/Output Specifications
Input: A folder containing Anytype JSON export files
Output: 
- A folder containing Markdown files (one per Anytype object)
- A log file detailing the conversion process

## 6. Anytype Export Structure

### JSON File Types
Anytype exports consist of multiple JSON files, each serving a specific purpose:

1. Main Content File:
   - Identified by "sbType": "Page"
   - Contains the primary content and structure of the note
   - Includes references to relations and other linked objects

2. Relation Files:
   - Represent different types of relations (tags, links, etc.)
   - Identified by "sbType": "STRelationOption"
   - Contain metadata about the relation type

3. File Object Files:
   - Represent attachments or embedded files
   - Identified by "sbType": "FileObject"
   - Contain metadata about the file, including its location

### Key Components of Main Content File

1. Metadata Section:
   ```json
   "details": {
     "createdDate": 1720802378,
     "name": "Note Title",
     "type": "ot-page",
     "id": "unique-identifier"
   }

Block Structure:
jsonCopy"blocks": [
  {
    "id": "block-id",
    "childrenIds": ["child-block-id-1", "child-block-id-2"],
    "fields": {},
    "text": {
      "text": "Block content",
      "marks": {}
    }
  }
]

Relation References:
jsonCopy"relationLinks": [
  {
    "key": "relation-key",
    "format": "relation-format"
  }
]


Block Types and Their Representations

Text Block:
jsonCopy{
  "id": "text-block-id",
  "text": {
    "text": "Plain text content",
    "marks": {}
  }
}

Heading Block:
jsonCopy{
  "id": "heading-block-id",
  "text": {
    "text": "Heading text",
    "style": "Header1"
  }
}

List Item Block:
jsonCopy{
  "id": "list-item-id",
  "text": {
    "text": "List item text",
    "style": "Marked"
  }
}

Code Block:
jsonCopy{
  "id": "code-block-id",
  "text": {
    "text": "Code content",
    "style": "Code"
  },
  "fields": {
    "lang": "python"
  }
}

Image Block:
jsonCopy{
  "id": "image-block-id",
  "file": {
    "hash": "file-hash",
    "name": "image-filename.jpg",
    "mime": "image/jpeg",
    "type": "Image"
  }
}


Relation File Structure
jsonCopy{
  "sbType": "STRelationOption",
  "snapshot": {
    "data": {
      "details": {
        "name": "Relation Name",
        "relationKey": "relation-identifier",
        "relationOptionColor": "color-value"
      }
    }
  }
}
7. Conversion Process

Identify Main Content File:

Scan all JSON files for "sbType": "Page"


Extract Metadata:

Parse the "details" section of the main content file
Convert Unix timestamp to readable date format


Process Blocks:

Iterate through the "blocks" array
Convert each block to its Markdown equivalent based on type
Handle nested blocks using the "childrenIds" property


Handle Relations:

Identify relation references in the main content file
Locate corresponding relation files
Extract relation names and values


Compile Markdown:

Start with a front matter section for metadata
Add converted block content
Append a section for relations


Output:

Write compiled Markdown to a .md file
Name file based on the original note title or ID



8. Relations Handling

Relation Types:

Tags
Links to other notes
Custom relation types defined by the user


Relation Storage:

Main content file contains references (IDs) to relations
Separate JSON files store details of each relation


Relation Extraction Process:

Identify relation IDs in the main content file
Search all JSON files for matching relation details
Extract relation name and value


Markdown Representation:

Add a "Relations" section at the end of the Markdown file
Format: Relation Name: Relation Value



Example:
markdownCopy## Relations
Tags: Project, Important
Linked Notes: Meeting Notes, Project Plan
Custom Relation: Custom Value

## 9. Error Handling and Logging

### Common Error Scenarios

1. Missing Main Content File:
   - Error: No JSON file with "sbType": "Page" found
   - Logging: ERROR level, skip processing for this object

2. Malformed JSON:
   - Error: JSON parsing fails for a file
   - Logging: WARNING level, skip the problematic file, continue processing others

3. Unknown Block Types:
   - Error: Encountered a block type not in the known list
   - Logging: INFO level, convert to plain text, add a comment in the Markdown

4. Missing Relation Files:
   - Error: Referenced relation ID not found in any JSON file
   - Logging: WARNING level, note the missing relation in the output

5. File Attachment Not Found:
   - Error: Referenced file in a block not found in the export
   - Logging: WARNING level, add a placeholder in the Markdown output

### Logging System

- Uses Python's built-in `logging` module
- Log levels: DEBUG, INFO, WARNING, ERROR
- Log file naming: `anytype_conversion_YYYYMMDD_HHMMSS.log`
- Log format: `[TIMESTAMP] [LEVEL] [FUNCTION_NAME] - Message`

Example log entry:
[2023-07-12 14:30:45] [WARNING] [process_block] - Unknown block type encountered: custom_block_type
Copy
## 10. Performance Considerations

### Handling Large Exports

1. File Reading Strategy:
   - Read JSON files one at a time, not all at once
   - Use `json.load()` for smaller files, `ijson` for very large files if needed

2. Memory Management:
   - Process one Anytype object (note) at a time
   - Clear unnecessary data from memory after processing each object

3. Relation Handling:
   - Create an in-memory index of relation IDs to file paths for quicker lookups
   - This index is built once at the start of processing

### Optimization Techniques

1. Parallel Processing:
   - Use `multiprocessing` to convert multiple notes simultaneously
   - Ideal for multi-core systems and large exports

2. Caching:
   - Cache frequently accessed data (e.g., common relation types)
   - Use `lru_cache` decorator for functions that repeatedly process the same data

3. Incremental Processing:
   - Allow for resuming conversion process if interrupted
   - Keep track of processed files to avoid redundant work

## 11. Development Guidelines

### Anytype-Specific Considerations

1. Block Type Handling:
   - Maintain an extensible system for handling block types
   - Use a strategy pattern or factory method for easy addition of new block types

2. Relation Processing:
   - Design a flexible system to handle various relation formats
   - Consider future changes in Anytype's relation structure

3. JSON Parsing:
   - Use defensive programming when parsing JSON
   - Always check for the existence of keys before accessing

4. Markdown Generation:
   - Ensure generated Markdown is compatible with common Markdown parsers
   - Use a Markdown library (e.g., `python-markdown`) for complex formatting

### Testing Procedures

1. Unit Tests:
   - Cover all major functions, especially JSON parsing and Markdown generation
   - Use sample JSON files mimicking various Anytype export scenarios

2. Integration Tests:
   - Test the entire conversion process with real Anytype exports
   - Include exports with various block types, relations, and file attachments

3. Performance Tests:
   - Benchmark conversion speed with different sizes of exports
   - Profile memory usage to identify potential memory leaks

## 12. Known Limitations and Future Improvements

### Current Limitations

1. Complex Layouts:
   - Anytype's advanced layout options may not translate perfectly to Markdown
   - Some visual elements might be simplified or lost in conversion

2. Interactive Elements:
   - Dynamic or interactive components in Anytype notes cannot be replicated in static Markdown

3. Embedded Databases:
   - Anytype's database features are not fully representable in Markdown
   - Only basic table structures can be converted

4. File Attachments:
   - While references to attachments are maintained, the files themselves need to be managed separately

### Planned Improvements

1. Enhanced Relation Handling:
   - Develop a more sophisticated system for representing complex relations in Markdown

2. Custom Block Type Support:
   - Implement a plugin system for users to define custom block type conversions

3. Bidirectional Conversion:
   - Future versions may support converting Markdown back to Anytype format

4. GUI Interface:
   - Develop a graphical user interface for easier use by non-technical users

## 13. Frequently Asked Questions

1. Q: Can this converter handle all Anytype block types?
   A: The converter handles most common block types. Some specialized or newly introduced block types may be converted to plain text.

2. Q: How are file attachments handled?
   A: File attachments are referenced in the Markdown output, but the files themselves need to be managed separately.

3. Q: Does the converter maintain the original creation and modification dates?
   A: Yes, the original creation date is preserved in the Markdown front matter. Modification dates are not currently included but may be added in future versions.

4. Q: Can the converter handle Anytype's database features?
   A: Basic table structures are converted, but complex database features are not fully supported in the current version.

## 14. Changelog

- v1.0.0 (2023-07-12): Initial release
  - Basic conversion of Anytype JSON to Markdown
  - Support for common block types and simple relations

## 15. License Information

This project is licensed under the MIT License. See the LICENSE file for details.

## 16. Contact and Support Information

For support, bug reports, or feature requests, please open an issue on the GitHub 

### Advanced AnyBlock and Anytype Structural Details

#### Block Nesting and Hierarchy
- Anytype uses a flat structure for blocks, with hierarchy represented through `childrenIds`.
- The order of blocks in the `blocks` array doesn't necessarily represent their visual order.
- Hierarchy must be reconstructed using `childrenIds` references.

Example:
```json
{
  "blocks": [
    {
      "id": "parent-block",
      "childrenIds": ["child-block-1", "child-block-2"]
    },
    {
      "id": "child-block-1"
    },
    {
      "id": "child-block-2"
    }
  ]
}
Special Block Types

Table Blocks:
jsonCopy{
  "id": "table-block",
  "table": {},
  "childrenIds": ["table-columns", "table-rows"]
}

Equation Blocks:
jsonCopy{
  "id": "equation-block",
  "text": {
    "text": "\\frac{a}{b} = c",
    "style": "Equation"
  }
}

Toggle Lists:
jsonCopy{
  "id": "toggle-block",
  "text": {
    "text": "Toggle item"
  },
  "fields": {
    "collapsed": true
  }
}


Relation Formats
Relations can have various formats, indicated in the relationLinks array:
jsonCopy"relationLinks": [
  {
    "key": "status",
    "format": "checkbox"
  },
  {
    "key": "due_date",
    "format": "date"
  }
]
Object Types

Standard types: "ot-page", "ot-note", "ot-task", etc.
Custom types have unique identifiers, e.g., "ot-custom-12345"

Internal Links
Internal links are represented as marks within text blocks:
jsonCopy{
  "text": {
    "text": "Link to another page",
    "marks": {
      "marks": [
        {
          "type": "Link",
          "param": "target-object-id",
          "range": {"from": 0, "to": 20}
        }
      ]
    }
  }
}
Permissions and Sharing
jsonCopy"details": {
  "restrictions": [3, 6, 5],
  "sharedWith": ["user-id-1", "user-id-2"]
}
Version History
While not typically included in exports, each object in Anytype has version history. This might be represented in some exports as additional metadata:
jsonCopy"details": {
  "versionHistory": [
    {
      "versionId": "v1",
      "timestamp": 1625097600,
      "author": "user-id"
    }
  ]
}
Set (Database) Representation
jsonCopy{
  "sbType": "Set",
  "details": {
    "members": ["object-id-1", "object-id-2"],
    "views": [
      {
        "id": "view-id",
        "type": "table",
        "columns": ["col1", "col2"]
      }
    ]
  }
}
Widgets and Embeds
jsonCopy{
  "id": "widget-block",
  "widget": {
    "type": "bookmark",
    "url": "https://example.com",
    "title": "Example Website",
    "description": "An example website"
  }
}
Iconography and Styling
jsonCopy"details": {
  "iconEmoji": "🚀",
  "iconImage": "file-hash-of-icon",
  "backgroundColor": "blue"
}
File Handling Specifics
File reference in a block:
jsonCopy{
  "id": "file-block",
  "file": {
    "hash": "file-hash",
    "name": "document.pdf"
  }
}
Corresponding FileObject:
jsonCopy{
  "sbType": "FileObject",
  "details": {
    "id": "file-id",
    "hash": "file-hash",
    "name": "document.pdf",
    "mime": "application/pdf",
    "size": 1024000
  }
}
Relation Backlinks
Backlinks are typically inferred by Anytype's system and might not be explicitly stated in the JSON. They are created implicitly when certain types of relations are established between objects.
Layout Information
jsonCopy{
  "id": "layout-block",
  "fields": {
    "columns": 2,
    "columnWidths": [0.5, 0.5]
  },
  "childrenIds": ["column-1-content", "column-2-content"]
}
Metadata Timestamps
jsonCopy"details": {
  "createdDate": 1625097600,
  "lastModifiedDate": 1625184000,
  "lastOpenedDate": 1625270400
}
Global Identifiers
Every object and block has a unique identifier used for cross-referencing:
jsonCopy{
  "id": "unique-global-id",
  "details": {
    "id": "same-unique-global-id"
  }
}
Rich Text Formatting
jsonCopy"text": {
  "text": "This is bold and italic text",
  "marks": {
    "marks": [
      {
        "type": "Bold",
        "range": {"from": 8, "to": 12}
      },
      {
        "type": "Italic",
        "range": {"from": 17, "to": 22}
      }
    ]
  }
}

## Understanding Anytype: Context for New Developers

1. What is Anytype?
   - Anytype is a privacy-focused, open-source personal knowledge management tool.
   - It allows users to create interconnected notes, databases, and other types of content.
   - The app emphasizes local-first storage and end-to-end encryption.

2. Anytype's Unique Features:
   - Object-Oriented Structure: Everything in Anytype is an "object" that can be linked and related to other objects.
   - Flexible Relations: Users can create custom relations between objects, similar to a graph database.
   - Sets: Anytype's version of databases, allowing for structured data collection and views.

3. Data Storage and Synchronization:
   - Anytype uses a peer-to-peer network for syncing between devices.
   - All data is stored locally on the user's device and optionally synced.
   - The AnyBlock format is designed to facilitate this decentralized, encrypted storage and sync system.

4. Encryption Considerations:
   - All data in Anytype is encrypted at rest.
   - The export process typically decrypts data, but be aware of potential encrypted blocks that might require additional handling.

5. Dynamic Nature of Anytype:
   - Anytype is actively developed, and new features are regularly added.
   - The data structure and export format may evolve over time.
   - Stay updated with the latest Anytype releases for potential changes in the export format.

6. Community and Resources:
   - Anytype has an active community forum where developers can ask questions.
   - The official documentation, while primarily user-focused, can provide insights into how features are intended to work.

7. Handling of Unsupported Features:
   - Anytype may have features that don't have direct equivalents in Markdown.
   - Decide on a strategy for handling these (e.g., converting to the closest Markdown representation, adding custom HTML, or including explanatory comments).

8. Import/Export Philosophy:
   - Anytype's export is designed to be as comprehensive as possible, including metadata that might not be immediately visible to users.
   - When converting, consider what level of detail is necessary for the target format (Markdown in this case) and what can be safely omitted.

9. Data Integrity and Validation:
   - Given the complex structure of Anytype data, implement thorough validation checks.
   - Be prepared to handle inconsistencies or unexpected data structures gracefully.

10. Performance and Scalability:
    - Anytype libraries can become quite large, with thousands of interlinked objects.
    - Design your conversion tool with scalability in mind, considering memory usage and processing time for large exports.

11. Privacy and Data Handling:
    - Remember that Anytype users may be particularly privacy-conscious.
    - Ensure your tool handles data securely and doesn't unintentionally expose sensitive information.

12. Cross-Platform Considerations:
    - Anytype is available on multiple platforms (Windows, macOS, Linux, iOS, Android).
    - Be aware that exports from different platforms might have slight variations.

13. Beta Status:
    - As of 2023, Anytype is still in beta.
    - Expect potential changes and improvements in the data structure and export format.

14. Relative vs. Absolute References:
    - Anytype uses a lot of relative references between objects.
    - When converting, you may need to decide how to handle these references in a flat file system like Markdown.

15. Media and File Handling:
    - Anytype can store various media types within notes.
    - Consider how to handle and organize these files when exporting to a simpler format like Markdown.

## Additional Nuances for Anytype Development

1. Bidirectional Relations:
   - Some relations in Anytype are bidirectional, meaning they automatically create a reverse relation on the linked object.
   - These aren't always explicitly represented in the export data but may need to be inferred or handled specially.

2. Unique Identifiers Across Spaces:
   - Anytype uses a concept of "Spaces" for different user environments.
   - Object IDs are unique within a space but may not be globally unique across all of a user's spaces.

3. Text Block Continuity:
   - Consecutive text blocks might represent a single paragraph in the UI.
   - When converting, you may need to determine whether to merge these or keep them separate.

4. Inline Object References:
   - Anytype allows inline mentions of other objects, which appear as links in the text.
   - These are represented differently from standard hyperlinks and may require special handling.

5. Set Views and Layouts:
   - Sets (databases) in Anytype can have multiple views (table, board, gallery, etc.).
   - The export data includes information about these views, which might not directly translate to Markdown.

6. Object Templates:
   - Anytype uses templates for creating new objects.
   - Template information might be included in exports and could be relevant for understanding object structures.

7. Nested Sets:
   - Sets can contain other sets, creating a hierarchical data structure.
   - This nested structure might need special consideration when flattening to Markdown.

8. Relation Types and Constraints:
   - Relations can have types (e.g., text, number, date) and constraints (e.g., single-select, multi-select).
   - These details might be important for accurately representing the data in the converted format.

9. Block-Level Comments:
   - Anytype supports comments on specific blocks.
   - These might be represented in the export data and could require special handling in conversion.

10. Object Merging History:
    - Anytype allows merging of objects, which can create complex history and relation structures.
    - Merged object data might contain remnants or references to the original, separate objects.

11. Lazy Loading of Content:
    - Large Anytype objects might use lazy loading in the app.
    - The export data, however, typically contains all content, which could lead to large JSON files.

12. Custom Widgets and Plugins:
    - Anytype supports custom widgets and plugins.
    - Data related to these custom elements might be present in exports and could require special handling.

13. Versioning of the AnyBlock Format:
    - The AnyBlock format itself might have version information.
    - Be prepared to handle potential variations based on the format version.

14. Localization Data:
    - Object and relation names might include localization data.
    - This could be relevant if maintaining multilingual support in the converted format.

15. Deleted and Archived Content:
    - Exports might include data about deleted or archived objects.
    - Decide how to handle this "hidden" content in the conversion process.

16. Rich Text in Unexpected Places:
    - Rich text formatting can appear in various fields, not just main content blocks.
    - Check relation values, object names, etc., for potential rich text formatting.

17. Default Values and Inheritance:
    - Some properties might have default values inherited from templates or object types.
    - These might not be explicitly stated in every object's data but could be important for full representation.

18. API Limitations vs. Export Data:
    - The data available in exports might be more comprehensive than what's accessible via Anytype's API (if one exists).
    - Be aware of these potential differences if integrating with live Anytype data in the future.

19. Whitespace and Formatting Significance:
    - In some cases, whitespace and line breaks in text blocks might have semantic meaning in Anytype.
    - Consider how to preserve or translate this meaning in the conversion process.

20. Cross-Object Formulas and Dependencies:
    - Anytype supports formulas that can reference data across multiple objects.
    - These inter-object dependencies might be represented in complex ways in the export data.

