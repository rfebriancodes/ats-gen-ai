import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
import re
import streamlit as st

# Load API Key (Pastikan ini ada di bagian atas app.py)
load_dotenv()
api_key = 'AIzaSyC-VS4pqSohcH5JYhBhRfnY7l-RTsB64Bg'
if not api_key:
    st.error("⚠️ API Key Gemini tidak ditemukan!")
    st.stop()

# Konfigurasi Gemini (Pakai model 1.5 Flash karena super cepat)
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

def extract_skills_with_gemini(job_desc_text):
    """
    Menggunakan Gemini API untuk mengekstrak Hard Skills & Soft Skills 
    secara cerdas dari teks Job Description apa pun (Multi-Konteks).
    """
    
    # Prompt cerdas untuk Gemini agar hasil ekstraksi bersih dan relevan
    prompt = f"""
    Kamu adalah ahli HR Senior dan analisis teks tingkat lanjut.
    Tugasmu adalah membaca teks Job Description berikut dan mengekstrak semua SKILLS (Keahlian) yang relevan, baik Hard Skills maupun Soft Skills.

    Job Description:
    "{job_desc_text}"

    Instruksi Penting:
    1. Ekstrak HANYA kata atau frasa yang merupakan keahlian (contoh: Python, AWS, Manajemen Proyek, Komunikasi, Figma, REST API).
    2. JANGAN ekstrak kata sifat umum (seperti 'excellent', 'strong', 'rapid'), persyaratan umum (seperti 'bachelor degree', 'experience'), atau kata sampah.
    3. Ekstrak skill dalam format huruf kecil.
    4. Kembalikan output HANYA dalam format JSON berupa satu array (list) dari string. Contoh output: ["python", "aws", "manajemen proyek"]
    """
    
    try:
        # Kirim prompt ke Gemini
        response = model.generate_content(prompt)
        
        # Bersihkan text markdown json ```json ... ``` jika ada
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        
        # Parse JSON menjadi list Python
        skills_list = json.loads(clean_text)
        
        # Kembalikan sebagai string yang dipisahkan koma agar cocok dengan visualisasi Streamlit-mu
        return ", ".join(sorted(skills_list))
        
    except json.JSONDecodeError:
        # Jika AI 'halu' dan format JSON-nya berantakan, kita pakai regex sederhana sebagai backup
        st.warning("⚠️ Format JSON dari AI bermasalah, menggunakan ekstraksi cadangan.")
        # Ambil kata-kata di dalam tanda kutip atau yang dipisahkan koma dari teks AI
        alternative_extract = re.findall(r'"([^"]*)"|(\w+(?:\s+\w+)*)', response.text)
        # Flatten list dan bersihkan
        flattened = [item for sublist in alternative_extract for item in sublist if item]
        return ", ".join(sorted(set(flattened)))
        
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat menghubungi Gemini API: {e}")
        return ""