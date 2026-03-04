import pdfplumber
import re
import re
import pdfplumber

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            # Naikkan toleransi x menjadi lebih besar (misal 2.0 atau 3.0)
            extracted = page.extract_text(x_tolerance=2.0) 
            if extracted:
                text += extracted + " "
    
    # Bersihkan enter
    text = text.replace("\n", " ").strip()
    
    # Trik Sakti: Pisahkan huruf kecil yang nempel dengan huruf besar
    # Mengubah "BackendDeveloperIntern" menjadi "Backend Developer Intern"
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    
    return text



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