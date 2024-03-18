from markdownify import markdownify
from bs4 import BeautifulSoup
import os
import re


def convert_html_to_md(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    for figure in soup.find_all("figure"):
        figure.extract()
    for style_tag in soup.find_all("style"):
        style_tag.extract()
    for a_tag in soup.find_all("a"):
        a_tag.string = a_tag.get_text()
    md_content = markdownify(str(soup), heading_style="ATX", wrap=True)
    md_content = re.sub(r"\*{3,}", "**", md_content)
    return md_content


def remove_excessive_line_breaks(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()
    pattern = r"\n{2,}"
    updated_content = re.sub(pattern, "\n\n", markdown_content)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(updated_content)


def process_html_files_in_directory(input_directory, output_directory):
    for filename in os.listdir(input_directory):
        filepath = os.path.join(input_directory, filename)
        if os.path.isfile(filepath) and filename.endswith(".html"):
            with open(filepath, "r", encoding="utf-8") as f:
                html_content = f.read()
            markdown_content = convert_html_to_md(html_content)
            output_md_file = os.path.join(
                output_directory, os.path.splitext(filename)[0] + ".md"
            )
            with open(output_md_file, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            print(f"Markdown file saved to: {output_md_file}")
            # New Step: Clean-up excessive line breaks right after file creation
            remove_excessive_line_breaks(output_md_file)
            print(f"Cleaned up excessive line breaks in: {output_md_file}")


# Example usage
input_directory_path = input("Enter the path to your input directory: ")
output_directory_path = input("Enter the path to your output directory: ")
process_html_files_in_directory(input_directory_path, output_directory_path)
