# Anyblock Numbered List Handling

Anyblock represents numbered lists using a combination of block properties and relationships between blocks.  Understanding this structure is crucial for correctly converting them to Markdown, where explicit numbering and indentation are required.

## Anyblock Representation

In Anyblock, each item in a numbered list, regardless of its nesting level, is represented as a block with the following key characteristics:

* **`text.style: "Numbered"`**: This property signifies that the block is part of a numbered list.  Crucially, Anyblock *does not* store the actual numerical order of the list items.  It only indicates that they belong to an ordered list.

* **`childrenIds`**:  This property, present in *all* blocks, is used to define the hierarchical relationships between blocks.  For numbered list items, `childrenIds` contains the IDs of any nested list items that are direct children of the current item.  This nesting structure is how Anyblock represents the hierarchy of the list.

Here's an example from the provided JSON data:

json
{
"id": "6732a2d06ac912b3b5145c26",
"text": {
"text": "two",
"style": "Numbered"
},
"childrenIds": [
"6732a2d16ac912b3b5145c27",
"6732a2d66ac912b3b5145c29"
]
}


In this example, the block with ID `6732a2d06ac912b3b5145c26` represents the list item "two".  Its `childrenIds` property indicates that the blocks with IDs `6732a2d16ac912b3b5145c27` and `6732a2d66ac912b3b5145c29` are nested beneath it.

## Conversion to Markdown

Since Anyblock doesn't store the explicit numbering, the converter needs to maintain and manage the numbering itself during the conversion process.  This involves two key aspects:

1. **Numbering**: The converter must keep track of the current list number at each nesting level.  For top-level items, the numbering starts at 1 and increments for each subsequent "Numbered" block.

2. **Nesting and Indentation**:  The converter uses the `childrenIds` property to identify nested list items.  For each level of nesting, the converter adds indentation (two spaces per level) to the Markdown output.  The numbering for nested lists restarts at 1 for each new parent item.

## Implementation Details

The `process_blocks` function in `block_converter.py` now handles the top-level numbering by initializing a `list_number` variable to 1 and incrementing it for each top-level numbered list item encountered.  This variable is passed down to the `convert_block_to_markdown` function.

Within `convert_block_to_markdown`, the `list_level` parameter tracks the nesting depth.  The function constructs the prefix for each numbered list item using the `list_level` for indentation and the `list_number` for the actual number.

For nested lists, the `list_level` is incremented, and the `list_number` is reset to 1 (or the appropriate nested number) to begin the numbering of the sublist.  This recursive approach ensures correct numbering and indentation at all levels of nesting.

The specific logic for nested list numbering is implemented within the `block_type == 'Numbered'` conditional block.  It handles both the case where a `list_number` is provided (for nested items) and the case where it's not (for top-level items).  This ensures seamless integration with the existing code and prevents impact on other block types.