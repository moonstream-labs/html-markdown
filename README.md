# HTML ➡️ Markdown

This enhanced Python script converts HTML content from a specified URL to Markdown, including downloading images, videos, audio, and handling code blocks with language specifications. It not only cleans the HTML of unwanted elements and formats notes into a standardized form but also organizes downloaded media into specified directories. The output is a Markdown file saved in a designated directory.

## Usage

1. Execute the script, and provide the necessary inputs as prompted.
2. Input the URL of the HTML content you wish to convert.
3. The script processes the content by downloading media, cleaning the HTML, and converting it to Markdown, including proper formatting for code blocks.
4. The final Markdown file is saved in the chosen directory.

## Code Structure

- `CustomMarkdownConverter`: Extends markdown conversion capabilities to include special handling for code blocks with language specifications.
- `get_input()`: Collects user inputs required for the conversion process.
  - Inputs include:
    - `root_dir`: The root directory for saving the Markdown and media files.
    - `section_dir`: Specific section directory within the root.
    - `module_name`: Name of the module for the Markdown file.
    - `module_number`: Module number, aiding in media file naming.
    - `media_prepend`: Prefix for media file names.
    - `target_div_id`: ID of the target div element in the HTML to convert.
    - `code_block_class`: Class identifier for code block elements.
    - `notes_element`: HTML element used for notes.
    - `notes_class`: Optional class name for notes elements.
- `create_directories()`: Establishes the necessary directory structure for saving output.
- `download_media()`: Downloads media (images, videos, audio) and saves them with standardized naming.
- `clean_html()`: Prepares the HTML for conversion by removing unwanted elements and standardizing notes format.
- `convert_to_markdown()`: Converts the cleaned HTML to Markdown and saves the output.
- `main()`: Orchestrates the conversion process based on provided inputs.

## Dependencies

- BeautifulSoup4
- requests
- markdownify

To install dependencies, run: `pip install -r requirements.in`.

## Example

```python
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import requests
import os
from urllib.parse import urlparse
```

## Media File Naming Convention

Media files are downloaded to the `Assets` folder within the specified directory. File names follow the convention:

`<media_prepend>_<module_number>_<media_order>`, where `<media_order>` indicates the sequence of the media item in the document. Inputs such as `media_prepend` and `module_number` are specified by the user.

## Markdown Formatting for Code Blocks

Code blocks with specified languages are formatted to include the language in the Markdown file for syntax highlighting:

```python
# Example Python code
print("Hello, Markdown!")
```

## Example Input

```
Root directory: MyDocumentation
Section directory: PythonGuides
Module name: GettingStarted
Module number: 01
Media prepend: python-guide
Target div ID: content
Code block class: code
Notes element: div
Notes class (leave blank if none): notes
```