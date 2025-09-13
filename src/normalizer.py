
import re
import unicodedata

def to_inline_mode(latex_str):
    content = latex_str
    boxed_match = re.search(r'\\boxed\{(.*)\}', content, re.DOTALL)
    if boxed_match:
        content = boxed_match.group(1)
    content = re.sub(r'^\$\$?|\$\$?$', '', content).strip()
    return f"${content}$"

def normalize_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'\$\$|\$', '', text)
    text = re.sub(r'\\boxed{([^}]*)}', r'\1', text)
    text = re.sub(r'\\text{([^}]*)}', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+', ' ', text)
    text = text.lower()
    nfkd_form = unicodedata.normalize('NFD', text)
    text = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
