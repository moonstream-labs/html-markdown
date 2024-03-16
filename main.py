import os
import sys
import requests
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter as md
from typing import Tuple, Optional
from urllib.parse import urlparse

class CustomMarkdownConverter(md):
    def convert_code(self, el, text, convert_as_inline):
        # Existing code conversion logic remains unchanged
        if not convert_as_inline:
            language = el.get('class')[0].replace('language-', '') if el.get('class') else None
            code_block = f'```{language}\n{text}\n```' if language else f'```\n{text}\n```'
            return code_block
        return f'`{text}`'
    
    def convert_h1(self, el, text):
        return '\n\n---\n\n# ' + text.strip() + '\n\n'

    def convert_h2(self, el, text):
        return '\n\n---\n\n## ' + text.strip() + '\n\n'

    def convert_h3(self, el, text):
        return '\n\n---\n\n### ' + text.strip() + '\n\n'

    def convert_h4(self, el, text):
        return '\n\n---\n\n#### ' + text.strip() + '\n\n'

    def convert_h5(self, el, text):
        return '\n\n---\n\n##### ' + text.strip() + '\n\n'

    def convert_h6(self, el, text):
        return '\n\n---\n\n###### ' + text.strip() + '\n\n'


def get_input() -> Tuple[str, str, str, str, str, str, str, Optional[str], str]:
    """
    Gets user inputs for the conversion process and returns them as a tuple.

    Returns:
        A tuple containing the following:
        - root_dir: The name of the repository.
        - section_dir: The name of the section within the repository.
        - module_name: The name of the module.
        - module_number: The module number, used in constructing image file titles.
        - media_prepend: Prefix for image file titles.
        - target_div_id: ID of the target div to be converted.
        - notes_element: HTML element type for notes elements.
        - notes_class: Class name for notes elements (optional).
    """
    root_dir = input("Root directory: ").strip()
    section_dir = input("Section directory: ").strip()
    module_name = input("Module name: ").strip()
    module_number = input("Module number: ").strip()
    media_prepend = input("Media prepend: ").strip()
    target_div_id = input("Target div ID: ").strip()
    notes_element = input("Notes element: ").strip()
    notes_class = input("Notes class (leave blank if none): ").strip()

    return (
        root_dir,
        section_dir,
        module_name,
        module_number,
        media_prepend,
        target_div_id,
        notes_element,
        notes_class or None,
    )


def create_directories(root_dir: str, section_dir: str) -> Tuple[str, str, str]:
    """
    Creates necessary directories for the repository and assets based on the provided names.

    Args:
        root_dir: The name of the repository.
        section_dir: The name of the section within the repository.

    Returns:
        A tuple containing paths to the root directory, section directory, and assets directory.
    """
    root_dir = os.path.join(os.getcwd(), root_dir)
    section_dir = os.path.join(root_dir, section_dir)
    assets_dir = os.path.join(root_dir, "Assets", section_dir)

    os.makedirs(root_dir, exist_ok=True)
    os.makedirs(section_dir, exist_ok=True)
    os.makedirs(assets_dir, exist_ok=True)

    return root_dir, section_dir, assets_dir


def download_media(
    soup: BeautifulSoup,
    assets_dir: str,
    media_prepend: str,
    module_number: str,
    section_dir: str,
    base_url: str,
) -> None:
    """
    Downloads media (images, videos, audio) from the HTML content and saves them in the specified assets directory.

    Args:
        soup: BeautifulSoup object containing the parsed HTML.
        assets_dir: The directory where media files should be saved.
        media_prepend: Prefix for naming the media files.
        module_number: Module number to include in the media file names.
        section_dir: Section name for organizing the media files.
        base_url: The base URL of the page to resolve relative media sources.
    """
    media_counter = 1
    media_tags = soup.find_all(["img", "video", "audio"])

    for tag in media_tags:
        # For video and audio tags, prioritize the source tag if present
        src = tag.get("src") or (
            tag.find("source").get("src") if tag.find("source") else None
        )
        if src:
            if not src.startswith(("http:", "https:")):
                src = base_url + src
            response = requests.get(src)

            ext = src.split(".")[-1].split("?")[0]  # Remove URL parameters
            filename = f"{media_prepend}_{module_number}_{media_counter}.{ext}"
            filepath = os.path.join(assets_dir, filename)

            with open(filepath, "wb") as f:
                f.write(response.content)

            # Update the src to the Markdown link format
            new_src = f"![[{filename}]]"
            if tag.name == "img":
                tag["src"] = new_src
            else:
                # For video and audio, update the source tag's src
                if tag.find("source"):
                    tag.find("source")["src"] = new_src
                else:
                    tag["src"] = new_src

            media_counter += 1


def clean_html(
    soup: BeautifulSoup, notes_element: str, notes_class: Optional[str]
) -> None:
    """
    Cleans the HTML content by removing unwanted elements and converting notes to a standard format.

    Args:
        soup: BeautifulSoup object containing the parsed HTML.
        notes_element: The HTML element type for notes.
        notes_class: The class name for notes elements (optional).
    """
    # Iterate over all <a> tags and replace them with their text content
    for tag in soup.find_all("a"):
        tag.replace_with(tag.get_text())

    if notes_class:
        notes = soup.find_all(notes_element, class_=notes_class)
    else:
        notes = soup.find_all(notes_element)

    for note in notes:
        note.name = "blockquote"


def convert_to_markdown(html_string: str, section_dir: str, module_name: str) -> None:
    """
    Converts the provided HTML string to Markdown format using the custom converter
    and saves the result to a file.
    """
    # Using the CustomMarkdownConverter for conversion
    converter = CustomMarkdownConverter()
    md_string = converter.convert(html_string)

    md_filepath = os.path.join(section_dir, f"{module_name}.md")
    with open(md_filepath, "w") as f:
        f.write(md_string)


def main() -> None:
    inputs = get_input()
    root_dir, section_dir, assets_dir = create_directories(inputs[0], inputs[1])

    # Get the URL to scrape from the user
    url = input("Enter the URL to scrape: ").strip()

    # Parse the URL to get the base URL
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    target_div = soup.find(
        "div", id=inputs[5]
    )  # Note: Adjusted index for target_div_id based on corrected get_input order
    if not target_div:
        print("Target div not found.")
        sys.exit(1)

    # Adjusted call to download_media to include base_url
    download_media(target_div, assets_dir, inputs[4], inputs[3], inputs[1], base_url)
    clean_html(target_div, inputs[6], inputs[7], inputs[8])

    convert_to_markdown(str(target_div), section_dir, inputs[2])


if __name__ == "__main__":
    main()
