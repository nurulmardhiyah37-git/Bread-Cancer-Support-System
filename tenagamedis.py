import streamlit as st
import pandas as pd
import pickle
import numpy as np

try:
    with open("best_model.pkl", "rb") as f:
        best_model = pickle.load(f)
    with open("feature_list.pkl", "rb") as f:
        feature_list = pickle.load(f)
except FileNotFoundError:
    st.error("File model atau feature_list tidak ditemukan!")
    st.stop()

def run_tenaga_medis():
    st.title("🩺 Sistem Prediksi Kanker Payudara")
    file = st.file_uploader("Unggah file CSV hasil pemeriksaan FNA", type=["csv"])
    if file is not None:
        try:
            df = pd.read_csv(file)
            # Pengecekan fitur
            if all(feat in df.columns for feat in feature_list):
                df_input = df[feature_list]
                pred = best_model.predict(df_input)
                df["Prediction"] = pred
                df["Pred_Description"] = df["Prediction"].replace({
                    "M": "Malignant", "B": "Benign", 
                    1: "Malignant", 0: "Benign",
                    "1.0": "Malignant", "0.0": "Benign"
                })
                st.session_state["medical_df"] = df
                st.success("File Berhasil Dibaca!")
            else:
                st.error("Kolom CSV tidak sesuai dengan fitur yang dibutuhkan model.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

    # menampilkan hasil
    if "medical_df" in st.session_state:
        df_show = st.session_state["medical_df"]
        st.write("### Pratinjau Data & Hasil")
        st.dataframe(df_show.head())
        # Grafik
        if "Pred_Description" in df_show.columns:
            st.bar_chart(df_show["Pred_Description"].value_counts())

    st.divider()
    chat_ui("chat_medical", chatbot_medical, "💬 Chatbot Tenaga Medis (Rule Based)")
    
# CHATBOT TENAGA MEDIS (RULE-BASED) 
def chatbot_medical(query):
    query = query.lower().strip()
    df = st.session_state.get("medical_df", None)
    if df is None:
        needs_data = []
        if any(k in query for k in needs_data):
            return "Silakan unggah file CSV terlebih dahulu agar saya dapat melakukan analisis data pasien Anda."
        else:
            return "Saya siap membantu setelah Anda mengunggah data pasien (CSV)."
    if "Prediction" not in df.columns:
        return "Data belum diprediksi. Pastikan format CSV Anda benar (memiliki fitur yang sesuai) agar saya bisa menganalisisnya."

    total = len(df)
    if total == 0:
        return "Dataset kosong — tidak ada baris pasien yang bisa dianalisis."

    # Perhitungan statistik dari kolom yang sudah ada
    pred_values = df["Prediction"].astype(str)
    ganas = (pred_values.isin(["M", "1", "1.0"])).sum()
    jinak = (pred_values.isin(["B", "0", "0.0"])).sum()
    try:
        persen_ganas = round((ganas / total) * 100, 2)
        persen_jinak = round((jinak / total) * 100, 2)
    except ZeroDivisionError:
        persen_ganas = persen_jinak = 0.0

    # Logika Jawaban 
    if ("berapa" in query and "total" in query and "pasien" in query) or ("total pasien" in query) or \
       ("jumlah baris" in query) or ("jumlah data" in query):
        return f"Total pasien dalam dataset Anda adalah **{total} pasien** (atau {total} baris data)."
    elif "ringkas" in query or "summary" in query or "rangkuman" in query:
        return (
            f"Rangkuman singkat dataset Anda:\n\n"
            f"- Total pasien: **{total}**\n"
            f"- Tumor ganas (Malignant): **{ganas} pasien ({persen_ganas}%)**\n"
            f"- Tumor jinak (Benign): **{jinak} pasien ({persen_jinak}%)**\n"
        )
    elif "missing" in query or "kosong" in query or "null" in query:
        missing_series = df.isnull().sum()
        total_missing = int(missing_series.sum())
        if total_missing == 0:
            return "Tidak ada missing value pada dataset. Semua data tampak lengkap."
        else:
            top_missing = missing_series[missing_series > 0].sort_values(ascending=False).head(10)
            details = "\n".join([f"- {idx}: {val} nilai kosong" for idx, val in top_missing.items()])
            return f"Terdapat **{total_missing}** nilai kosong. Kolom dengan missing value terbanyak:\n{details}"
    elif ("berapa" in query and "ganas" in query) or ("jumlah ganas" in query):
        return f"Terdapat **{ganas} pasien** dengan tumor ganas (Malignant)."
    elif ("berapa" in query and "jinak" in query) or ("jumlah jinak" in query):
        return f"Terdapat **{jinak} pasien** dengan tumor jinak (Benign)."
    elif "persen" in query and "ganas" in query:
        return f"Persentase tumor ganas adalah **{persen_ganas}%** dari total pasien."
    elif "persen" in query and "jinak" in query:
        return f"Persentase tumor jinak adalah **{persen_jinak}%** dari total pasien."
    elif "valid" in query or "validitas" in query or ("akurasi" in query and "model" in query) or "akurasi" in query:
        return (
            "Model Naive Bayes yang digunakan umumnya memberikan akurasi tinggi pada dataset WBCD (sering di kisaran >90%). "
            "Namun, validitas di konteks Anda bergantung pada kualitas data (missing, distribusi fitur) dan apakah data berasal dari populasi yang sama."
        )
    elif "overfitting" in query or "over fit" in query:
        return (
            "Overfitting diatasi dengan pembagian train-test dan parameter tuning (mis. jumlah pohon). "
            "Untuk verifikasi, Anda bisa menjalankan cross-validation dan melihat perbedaan skor train vs test."
        )
    else:
        return "Maaf, saya belum memahami pertanyaan tersebut. Coba tanyakan tentang jumlah pasien, persentase ganas/jinak, atau ringkasan data."

# UI CHAT COMPONENT 
def chat_ui(chat_history_key, chatbot_function, title):
    st.subheader(title)

    if chat_history_key not in st.session_state:
        st.session_state[chat_history_key] = []

    chat_container = st.container()
    with chat_container:
        for sender, msg in st.session_state[chat_history_key]:
            if sender == "user":
                st.markdown(f"🧑 **Anda:** {msg}")
            else:
                st.markdown(f"🤖 **Chatbot:** {msg}")

    with st.form(key=f"form_{chat_history_key}", clear_on_submit=True):
        user_input = st.text_input("Ketik pertanyaan Anda di sini:")
        submit_button = st.form_submit_button("Kirim")

        if submit_button and user_input:
            st.session_state[chat_history_key].append(("user", user_input))
            reply = chatbot_function(user_input)
            st.session_state[chat_history_key].append(("bot", reply))
            st.rerun()

if __name__ == "__main__":
    run_tenaga_medis()
