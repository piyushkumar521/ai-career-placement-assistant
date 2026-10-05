import re

def clean_resume_text(text):
    # remove extra spaces
    text = re.sub(r"[ \t]+", "\n\n", text)
    
    # remove excessive blanks lines
    text=re.sub(r"\n\s*\n+", "\n\n", text)
    
    # remove leading/trailing spaces from each line
    text="\n".join(line.strip() for line in text.splitlines())
    
    # remove leading/trailing whitespace
    text=text.strip()
    
    return text