import os
import re
import mammoth
from textblob import TextBlob

def convert_docx_to_html(docx_path):
    with open(docx_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        return result.value

def analyze_and_style_quotes(html_text):
    # Match both “smart quotes” and "regular quotes"
    dialogue_pattern = r'([“"][^”"]+[”"])'
    matches = re.findall(dialogue_pattern, html_text)

    for quote in matches:
        # Clean the quote
        raw = quote.strip('“”"')
        sentiment = TextBlob(raw).sentiment.polarity

        # Choose font based on sentiment
        if sentiment > 0.3:
            style = 'font-family: "Comic Sans MS", cursive; color: green;'
        elif sentiment < -0.3:
            style = 'font-family: "Impact", sans-serif; color: red;'
        else:
            style = 'font-family: "Georgia", serif; color: gray;'

        styled = f'<span style="{style}">{quote}</span>'
        html_text = html_text.replace(quote, styled)

    return html_text

def wrap_html(content, title):
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{title}</title>
</head>
<body>
{content}
</body>
</html>
"""

def process_folder(docx_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(docx_folder):
        if filename.lower().endswith(".docx"):
            docx_path = os.path.join(docx_folder, filename)
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_folder, f"{base_name}.html")

            print(f"Processing: {filename}")
            html = convert_docx_to_html(docx_path)
            styled_html = analyze_and_style_quotes(html)
            full_html = wrap_html(styled_html, base_name)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(full_html)
            print(f"Saved to: {output_path}")



process_folder("/home/fbartolic/Documents/fun/tale-hackathon/books", "/home/fbartolic/Documents/fun/tale-hackathon/html")
