import streamlit as st
import tenagamedis
import pasien
import base64

st.set_page_config(page_title="Breast Cancer Diagnostic Early Support", layout="wide", page_icon="🩺")
st.sidebar.title("Breast Cancer Early Support App")
menu = st.sidebar.selectbox(
    "Pilih Mode:",
    ["Beranda", "Tenaga Medis", "Pasien"]
)

def show_header():
    st.image("image.png", width="stretch")
    st.markdown("---")

def show_bg():
    with open("image2.png", "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
        """, unsafe_allow_html=True)

def show_homepage():
    st.title("🏥 Breast Cancer Support System")
    show_header()
    st.write("Antarmuka web ini berfungsi sebagai alat bantu bagi tenaga medis untuk prediksi Kanker Payudara berbasis data numerik FNA menggunakan machine learning. Sekaligus menyediakan informasi edukatif yang berguna bagi pasien")
    st.markdown("---")
    st.subheader("🔍 Mode:")
    st.write("**Tenaga Medis**: Upload data CSV FNA untuk prediksi menggunakan model Machine Learning. Dilengkapi Chatbot Teknis berbasis rule-based untuk analisis data dan model")
    st.write("**Pasien**: Menyediakan informasi edukatif (gejala jinak/ganas) dan akses Chatbot Edukasi seputar Kanker Payudara berbasis rule-based.")
    st.markdown("---")
    st.info("Gunakan menu di sebelah kiri untuk memilih mode.")

if menu == "Beranda":
    show_homepage()

elif menu == "Tenaga Medis":
    tenagamedis.run_tenaga_medis() 
    show_bg()

elif menu == "Pasien":
    pasien.run_patient_page()
    show_bg()

