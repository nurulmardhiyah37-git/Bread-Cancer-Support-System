import streamlit as st

def run_patient_page():

    st.title("Informasi Edukatif Kanker Payudara - Mode Pasien")

    st.header("Gejala Umum Kanker Payudara Ganas")
    st.markdown("""
    Berikut adalah beberapa **gejala kanker payudara ganas** menurut badan kesehatan dunia:

    - Benjolan keras yang tidak terasa nyeri  
    - Perubahan bentuk atau ukuran payudara  
    - Perubahan tekstur kulit (mengkerut seperti kulit jeruk)  
    - Bentuk cenderung tertarik masuk ke dalam  
    - Keluar cairan abnormal   
    - Pembengkakan atau kemerahan yang tidak biasa  
    - Nyeri payudara atau nyeri pada ketiak yang tidak hilang  

    **Sumber resmi:**
    - WHO-Breast Cancer Overview: https://www.who.int/news-room/fact-sheets/detail/breast-cancer  
    - CDC-Breast Cancer Symptoms: https://www.cdc.gov/cancer/breast/basic_info/symptoms.htm  
    - Kemenkes RI-Informasi Kanker Payudara: https://www.kemkes.go.id/id/layanan/kerangka-kerja-pencegahan-dan-pengendalian-kanker 
    """)

    st.header("Gejala Umum Kanker Payudara Jinak")
    st.markdown("""
    Ciri-ciri yang **umumnya ditemukan pada Kanker Payudara jinak**:

    - Benjolan lunak dan dapat digerakkan  
    - Nyeri yang muncul sebelum atau selama menstruasi  
    - Ukuran benjolan berubah-ubah  
    - Tidak menyebabkan perubahan kulit  
    - Jarang menyebabkan keluarnya cairan abnormal   

    **Sumber tambahan:**
    - Mayo Clinic, Benign Breast Conditions: https://www.mayoclinic.org  
    - Johns Hopkins Medicine-Non-cancerous Breast Lumps: https://www.hopkinsmedicine.org  
    """)

    st.warning("⚠️ Informasi ini bersifat edukatif dan **bukan diagnosis medis**. Untuk kepastian diagnosis, konsultasikan dengan tenaga kesehatan profesional.")

    st.header("Chatbot Edukatif Tanya Jawab Seputar Kanker Payudara")
    user_q = st.text_input("Masukkan pertanyaan Anda:")

    responses = {
        "apa itu kanker payudara": "Kanker payudara adalah pertumbuhan sel abnormal pada jaringan payudara yang bersifat ganas. " "(Sumber: MSD Manuals, 2025)",
        "gejala kanker": "Beberapa gejala meliputi benjolan keras, perubahan kulit, puting tertarik ke dalam, dan cairan abnormal."  "(Sumber: WHO Fact Sheet 2024, MSD Manuals)",
        "ciri ciri kanker": "Ciri-cirinya meliputi benjolan yang keras, tidak nyeri, kulit mengerut seperti kulit jeruk, perubahan bentuk payudara, atau puting masuk ke dalam serta adanya cairan yang keluar abnormal"  "(Sumber: WHO & CDC Breast Cancer Symptoms, 2024)",
        "gejala awal": "Pada tahap awal, kanker payudara sering tidak menimbulkan gejala. Benjolan kecil yang tidak terasa sakit adalah tanda paling umum."  "(Sumber: MSD Manuals,  Early Breast Cancer, 2025)",
        "apakah kanker payudara sakit": "Tidak selalu. Banyak benjolan kanker tidak menimbulkan rasa sakit pada tahap awal." "(Sumber: CDC Breast Cancer Basic Facts, 2024)",
        "periksa dimana": "Pemeriksaan dapat dilakukan di puskesmas, rumah sakit, atau layanan deteksi dini kanker terdekat." "(Sumber: Kemenkes RI, Deteksi Dini Kanker Payudara, 2024)",
        "penyebab": "Kanker payudara memiliki banyak faktor risiko seperti genetik, hormonal, usia, dan gaya hidup." "(Sumber: LWW Journal, Epidemiology & Risk Factors of Breast Cancer, 2024)",
        "faktor risiko": "Faktor risiko termasuk usia di atas 40, riwayat keluarga, mutasi gen BRCA1/BRCA2, obesitas, alkohol, dan terapi hormon jangka panjang."  "(Sumber: WJ Breast Cancer Review 2024; WHO 2024)",
        "apakah keturunan": "Ya, sekitar 5 sampai 10% kasus kanker payudara dipengaruhi faktor genetik seperti mutasi BRCA1/BRCA2."  "(Sumber: WJSO, Familial Breast Cancer Review, 2024)",
        "apakah saya kena kanker": "Saya tidak bisa memberikan diagnosis. Untuk kepastian, silakan periksa ke tenaga medis dan lakukan pemeriksaan lanjutan."  "(Sumber: CDC & WHO Breast Cancer Screening Guidelines)",
        "apakah benjolan saya kanker": "Tidak semua benjolan adalah kanker. Pemeriksaan medis seperti USG atau biopsi diperlukan untuk memastikan."   "(Sumber: MSD Manuals, Diagnosis Breast Masses, 2025)",
        "bagaimana cara mengobati": "Pengobatan tergantung kondisi pasien dan dapat berupa operasi, kemoterapi, radioterapi, terapi hormon, atau terapi target." "(Sumber: BMJ Breast Cancer Treatment Overview, 2023)",
        "apakah bisa sembuh": "Peluang sembuh tinggi jika terdeteksi pada tahap awal. Survival rate meningkat dengan deteksi dini. " "(Sumber: WHO Global Breast Cancer Report 2024)",
        "bagaimana mencegah": "Beberapa langkah pencegahan termasuk menjaga berat badan sehat, olahraga rutin, batasi alkohol, dan lakukan pemeriksaan rutin." "(Sumber: Kemenkes RI & WHO Prevention Guidelines, 2024)",
        "apakah bisa dicegah": "Tidak semuanya dapat dicegah, tetapi risiko bisa dikurangi dengan gaya hidup sehat dan deteksi dini."  "(Sumber: WHO Breast Cancer Prevention, 2024)",
    
        "default":"Maaf, saya belum memiliki informasi untuk pertanyaan tersebut. Coba ajukan dengan kata kunci yang lebih sederhana ya."
    }

    if user_q:
        key = user_q.lower().strip()
        found = None
        for k in responses:
            if k in key:
                found = responses[k]
                break

        if found:
            st.success(found)
        else:
            st.info(responses["default"])


if __name__ == "__main__":
    run_patient_page()
