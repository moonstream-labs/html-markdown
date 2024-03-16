import os
import sys
import requests
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter as md
from typing import Tuple, Optional
from urllib.parse import urlparse

class CustomMarkdownConverter(md):
    def convert_code(self, el, text, convert_as_inline):
        if not convert_as_inline:
            language = el.get("class")[0].replace("language-", "") if el.get("class") else None
            code_block = f"```{language}\n{text}\n```" if language else f"```\n{text}\n```"
            return code_block
        return f"`{text}`"


def get_input() -> Tuple[str, str, str, str, str, str, str, Optional[str], str, str]:
    root_dir = input("Root directory: ").strip()
    section_dir = input("Section directory: ").strip()
    module_name = input("Module name: ").strip()
    module_number = input("Module number: ").strip()
    media_prepend = input("Media prepend: ").strip()
    target_selector = input("Target element or ID: ").strip()
    target_type = input("Is this an element type or an ID? [element/id]: ").strip().lower()
    notes_element = input("Notes element: ").strip()
    notes_class = input("Notes class (leave blank if none): ").strip()

    return (
        root_dir,
        section_dir,
        module_name,
        module_number,
        media_prepend,
        target_selector,
        target_type,
        notes_element,
        notes_class or None,
    )


def create_directories(root_dir: str, section_dir: str) -> Tuple[str, str, str]:
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
):
    media_counter = 1
    media_tags = soup.find_all(["img", "video", "audio"])

    for tag in media_tags:
        src = tag.get("src") or (tag.find("source").get("src") if tag.find("source") else None)
        if src:
            if not src.startswith(("http:", "https:")):
                src = base_url + src
            response = requests.get(src)

            ext = src.split(".")[-1].split("?")[0]
            filename = f"{media_prepend}_{module_number}_{media_counter}.{ext}"
            filepath = os.path.join(assets_dir, filename)

            with open(filepath, "wb") as f:
                f.write(response.content)

            new_src = f"![[{filename}]]"
            if tag.name == "img":
                tag["src"] = new_src
            else:
                if tag.find("source"):
                    tag.find("source")["src"] = new_src
                else:
                    tag["src"] = new_src

            media_counter += 1


def clean_html(
    soup: BeautifulSoup, notes_element: str, notes_class: Optional[str]
):
    for tag in soup.find_all("a"):
        tag.replace_with(tag.get_text())

    if notes_class:
        notes = soup.find_all(notes_element, class_=notes_class)
    else:
        notes = soup.find_all(notes_element)

    for note in notes:
        note.name = "blockquote"


def convert_to_markdown(html_string: str, section_dir: str, module_name: str):
    converter = CustomMarkdownConverter()
    md_string = converter.convert(html_string)

    md_filepath = os.path.join(section_dir, f"{module_name}.md")
    with open(md_filepath, "w") as f:
        f.write(md_string)


def main():
    inputs = get_input()
    root_dir, section_dir, assets_dir = create_directories(inputs[0], inputs[1])

    url = input("Enter the URL to scrape: ").strip()
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    if inputs[6] == "id":
        target = soup.find(id=inputs[5])
    elif inputs[6] == "element":
        target = soup.find(inputs[5])
    else:
        print("Invalid target type specified.")
        sys.exit(1)

    if not target:
        print("Target not found.")
        sys.exit(1)

    download_media(target, assets_dir, inputs[4], inputs[3], inputs[1], base_url)
    clean_html(target, inputs[7], inputs[8])
    convert_to_markdown(str(target), section_dir, inputs[2])


if __name__ == "__main__":
    main()
