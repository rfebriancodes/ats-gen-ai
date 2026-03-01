import pdfplumber
import re
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + " "
    return text.strip()



def extract_contact_info(text):

    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    phone_pattern = r'(\+62|0)[0-9]{8,13}'
    linkedin_pattern = r'linkedin\.com\/[a-zA-Z0-9\-\/]+'
    github_pattern = r'github\.com\/[a-zA-Z0-9\-\/]+'

    email = re.findall(email_pattern, text)
    phone = re.findall(phone_pattern, text)
    linkedin = re.findall(linkedin_pattern, text)
    github = re.findall(github_pattern, text)

    return {
        "email": email[0] if email else None,
        "phone": phone[0] if phone else None,
        "linkedin": linkedin[0] if linkedin else None,
        "github": github[0] if github else None
    }