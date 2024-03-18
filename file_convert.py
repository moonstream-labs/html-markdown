from markdownify import markdownify
from bs4 import BeautifulSoup
import os

# Define the input HTML file path
input_html_file = "path/to/your/input.html"

# Define the output Markdown file path
output_md_file = os.path.expanduser("~/Desktop/output.md")


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


# Read HTML content from the input file
with open(input_html_file, "r", encoding="utf-8") as f:
    html_content = f.read()

# Convert HTML to Markdown
markdown_content = convert_html_to_md(html_content)

# Write Markdown content to the output file
with open(output_md_file, "w", encoding="utf-8") as f:
    f.write(markdown_content)

print(f"Conversion complete. Markdown file saved to: {output_md_file}")
