from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import os

# Caching translated words
translation_cache = {}

def is_russian(text):
    # Finding words on the page
    return any('\u0400' <= char <= '\u04FF' for char in text)

# In this function paste the language you want to translate the text
def translate_text(text, target_lang='de'):
    # returning already translated words
    if text in translation_cache:
        return translation_cache[text]
    try:
        translator = GoogleTranslator(target=target_lang)
        translated_text = translator.translate(text)

        # saving translated words
        translation_cache[text] = translated_text

        return translated_text
    except Exception as e:
        print(f"Translation issue: {e}")
        return text

def main():
    # Path to HTML file
    input_file_path = r'...yourpath\index.html'

    # Opening HTML file
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
    except FileNotFoundError:
        print(f"File is not found: {input_file_path}")
        return
    except IOError as io_err:
        print(f"in-out error: {io_err}")
        return

    # Parsing HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Translating&Replacing
    for element in soup.find_all(string=True):
        if element.strip() and is_russian(element):
            # Attention on the spaces
            leading_spaces = len(element) - len(element.lstrip())
            trailing_spaces = len(element) - len(element.rstrip())

            translated_text = translate_text(element.strip())
            if translated_text:
                translated_text = ' ' * leading_spaces + translated_text + ' ' * trailing_spaces
                element.replace_with(translated_text)

    # Saving
    save_directory = r'...path_to_your_project'
    file_path = os.path.join(save_directory, 'translated_page.html')

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Translated page saved to the: {file_path}")
    except IOError as io_err:
        print(f"Writing issue caused: {io_err}")


if __name__ == "__main__":
    main()
