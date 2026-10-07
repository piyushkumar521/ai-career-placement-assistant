from src.utils.text_utils import clean_resume_text


def process_job_description(text):
    cleaned_text = clean_resume_text(text)

    return cleaned_text