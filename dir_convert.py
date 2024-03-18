from markdownify import markdownify
from bs4 import BeautifulSoup
import os


# Function to convert HTML to Markdown
def convert_html_to_md(html_content):
    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove <figure> elements
    for figure in soup.find_all("figure"):
        figure.extract()

    # Convert <a> elements to plaintext
    for a_tag in soup.find_all("a"):
        a_tag.string = a_tag.get_text()

    # Convert HTML to Markdown using markdownify
    md_content = markdownify(str(soup), heading_style="ATX")

    return md_content


# Function to process HTML files in a directory and save Markdown files to the output directory
def process_html_files_in_directory(input_directory, output_directory):
    # Iterate over files in the input directory
    for filename in os.listdir(input_directory):
        filepath = os.path.join(input_directory, filename)

        # Check if the file is a regular file and ends with '.html'
        if os.path.isfile(filepath) and filename.endswith(".html"):
            # Read HTML content from the file
            with open(filepath, "r", encoding="utf-8") as f:
                html_content = f.read()

            # Convert HTML to Markdown
            markdown_content = convert_html_to_md(html_content)

            # Determine output file path
            output_md_file = os.path.join(
                output_directory, os.path.splitext(filename)[0] + ".md"
            )

            # Write Markdown content to the output file
            with open(output_md_file, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            print(f"Conversion complete. Markdown file saved to: {output_md_file}")


# Example usage:
input_directory_path = "/path/to/your/input/directory"
output_directory_path = "/path/to/your/output/directory"
process_html_files_in_directory(input_directory_path, output_directory_path)
