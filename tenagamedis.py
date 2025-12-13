import streamlit as st
import pandas as pd
import pickle
import numpy as np

with open("best_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("feature_list.pkl", "rb") as f:
    feature_list = pickle.load(f)

# CHATBOT TENAGA MEDIS (RULE-BASED) 
def chatbot_medical(query):
    """Rule-based chatbot untuk tenaga medis"""
    query = query.lower().strip()
    df = st.session_state.get("medical_df", None)

    if df is None:
        needs_data = ["ganas", "jinak", "pasien", "berapa", "jumlah", "data", "prediksi", "summary", "ringkas"]
        if any(k in query for k in needs_data):
            return "Silakan unggah file CSV terlebih dahulu agar saya dapat melakukan analisis data pasien Anda."
        else:
            return "Saya siap membantu setelah Anda mengunggah data pasien (CSV)."
    try:
        if "Prediction" not in df.columns:
            if all(feat in df.columns for feat in feature_list):
                df_input = df[feature_list]
                df["Prediction"] = model.predict(df_input)
            else:
                return "Kolom fitur lengkap tidak ditemukan di dataset. Pastikan CSV berisi semua fitur yang dibutuhkan."
    except Exception as e:
        return f"Gagal memproses prediksi otomatis: {e}"

    # Statistik dasar
    total = len(df)
    if total == 0:
        return "Dataset kosong — tidak ada baris pasien yang bisa dianalisis."

    # Toleransi bila label bukan "M"/"B", normalisasikan kalau perlu
    pred_values = df["Prediction"].astype(str)
    ganas = (pred_values == "M").sum()
    jinak = (pred_values == "B").sum()
    # jika model menyimpan label lain (mis. 1/0), coba mapping
    if (ganas + jinak) == 0:
        if set(pred_values.unique()).issubset({"1", "0", "1.0", "0.0"}):
            ganas = (pred_values == "1").sum()
            jinak = (pred_values == "0").sum()

    try:
        persen_ganas = round((ganas / total) * 100, 2)
        persen_jinak = round((jinak / total) * 100, 2)
    except ZeroDivisionError:
        persen_ganas = persen_jinak = 0.0

    # A. PERTANYAAN TENTANG DATA PASIEN
    if ("berapa" in query and "total" in query and "pasien" in query) or ("total pasien" in query):
        return f"Total pasien dalam dataset Anda adalah **{total} pasien**."

    if "jumlah baris" in query or "jumlah data" in query:
        return f"Dataset mengandung **{total} baris data pasien**."

    if "jumlah kolom" in query or "berapa fitur" in query:
        return f"Dataset Anda memiliki **{df.shape[1]} kolom**, termasuk kolom prediksi jika tersedia."

    if "fitur apa saja" in query or "kolom apa saja" in query:
        cols = "\n".join([f"- {col}" for col in df.columns])
        return "Berikut daftar kolom pada dataset Anda:\n\n" + cols

    if "missing" in query or "kosong" in query or "null" in query:
        missing_series = df.isnull().sum()
        total_missing = int(missing_series.sum())
        if total_missing == 0:
            return "Tidak ada missing value pada dataset. Semua data tampak lengkap."
        else:
            top_missing = missing_series[missing_series > 0].sort_values(ascending=False).head(10)
            details = "\n".join([f"- {idx}: {val} nilai kosong" for idx, val in top_missing.items()])
            return f"Terdapat **{total_missing}** nilai kosong. Kolom dengan missing value terbanyak:\n{details}"

    if ("summary" in query) or ("ringkas" in query) or ("rangkuman" in query) or ("jelaskan data" in query) or ("jelaskan data saya" in query):
        return (
            f"Rangkuman singkat dataset Anda:\n\n"
            f"- Total pasien: **{total}**\n"
            f"- Tumor ganas (Malignant): **{ganas} pasien ({persen_ganas}%)**\n"
            f"- Tumor jinak (Benign): **{jinak} pasien ({persen_jinak}%)**\n"
        )

    # B. PERTANYAAN TENTANG ANALISIS PREDIKSI
    if "berapa" in query and "ganas" in query:
        return f"Terdapat **{ganas} pasien** dengan tumor ganas (Malignant)."

    if "berapa" in query and "jinak" in query:
        return f"Terdapat **{jinak} pasien** dengan tumor jinak (Benign)."

    if "persen" in query and "ganas" in query:
        return f"Persentase tumor ganas adalah **{persen_ganas}%** dari total pasien."

    if "persen" in query and "jinak" in query:
        return f"Persentase tumor jinak adalah **{persen_jinak}%** dari total pasien."

    if ("distribusi" in query or "bagaimana distribusi" in query or "plot distribusi" in query):
        return "Saya bisa menampilkan distribusi prediksi di panel jika Anda melihat bagian 'Distribusi Prediksi' setelah upload file."

    if "model apa" in query or "algoritma apa" in query or "pakai model" in query:
        return "Model yang digunakan adalah **Naive Bayes Classifier** — dipilih karena kestabilan dan performanya pada dataset fitur numerik seperti WBCD."

    if ("kenapa" in query or "mengapa" in query) and ("prediksi" in query or "hasil" in query):
        return (
            "Prediksi dihasilkan berdasarkan pola fitur FNA (mis. radius, texture, perimeter, area). "
            "Nilai fitur yang jauh dari rentang normal cenderung mengarah ke klasifikasi ganas."
        )

    # C. PERTANYAAN TENTANG VALIDITAS & EVALUASI MODEL
    if "valid" in query or "validitas" in query or ("akurasi" in query and "model" in query) or "akurasi" in query:
        return (
            "Model Random Forest yang digunakan umumnya memberikan akurasi tinggi pada dataset WBCD (sering di kisaran >90%). "
            "Namun, validitas di konteks Anda bergantung pada kualitas data (missing, distribusi fitur) dan apakah data berasal dari populasi yang sama."
        )

    if "bisa dipercaya" in query or "seberapa yakin" in query or "confidence" in query:
        return (
            "Model cukup dapat dipercaya sebagai alat screening awal. "
            "Untuk kepercayaan klinis, hasil prediksi harus dikonfirmasi oleh pemeriksaan lanjutan (biopsi/mammogram) dan pendapat ahli."
        )

    if "overfitting" in query or "over fit" in query:
        return (
            "Overfitting diatasi dengan pembagian train-test dan parameter tuning (mis. jumlah pohon). "
            "Untuk verifikasi, Anda bisa menjalankan cross-validation dan melihat perbedaan skor train vs test."
        )

    if "dataset apa" in query or "sumber data" in query:
        return "Dataset dasar yang terkait adalah **Wisconsin Breast Cancer Diagnostic (WBCD)** — dataset umum untuk tugas ini."

    # D. RULE TEKNIS (DEFAULT)
    tech_responses = {
        "precision": "Precision menunjukkan ketepatan model dalam memprediksi tumor ganas — dari semua yang diprediksi ganas, berapa yang benar-benar ganas.",
        "recall": "Recall menunjukkan kemampuan model menemukan seluruh kasus ganas (sensitivity).",
        "f1" : "F1 Score adalah rata-rata harmonik antara precision dan recall, cocok untuk dataset imbalance.",
        "random forest": "Random Forest bekerja dengan membuat banyak decision tree dan mengambil hasil voting terbanyak untuk prediksi akhir.",
        "csv": "Pastikan file CSV memiliki fitur numerik sesuai urutan feature_list yang digunakan saat pelatihan.",
        "error": "Kesalahan umum saat upload biasanya format kolom tidak sesuai atau terdapat nilai non-numeric pada kolom fitur."
    }

    for key, val in tech_responses.items():
        if key in query:
            return val
    return "Maaf, saya belum memahami pertanyaan tersebut. Coba tanyakan tentang jumlah pasien, persentase ganas/jinak, missing value, atau validitas model."


# UI CHAT COMPONENT 
def chat_ui(chat_history_key, chatbot_function, title):
    st.subheader(title)

    if chat_history_key not in st.session_state:
        st.session_state[chat_history_key] = []

    for sender, msg in st.session_state[chat_history_key]:
        if sender == "user":
            st.markdown(f"🧑 **Anda:** {msg}")
        else:
            st.markdown(f"🤖 **Chatbot:** {msg}")

    user_input = st.text_input("Ketik pertanyaan Anda di sini:", key=f"input_{chat_history_key}")

    if st.button("Kirim", key=f"send_{chat_history_key}"):
        if user_input:
            st.session_state[chat_history_key].append(("user", user_input))
            reply = chatbot_function(user_input)
            st.session_state[chat_history_key].append(("bot", reply))
            st.rerun()


# Fungsi utama untuk halaman tenaga medis
def run_tenaga_medis():
    st.title("🩺 Sistem Prediksi Kanker Payudara (Breast Cancer Classifier) — Mode Tenaga Medis")
    st.write(
        """
        Silakan unggah file CSV hasil ekstraksi FNA (30 fitur) untuk analisis dan prediksi.
        """
    )

    file = st.file_uploader("Unggah file CSV hasil pemeriksaan FNA", type=["csv"])
    if file is not None:
        try:
            df = pd.read_csv(file)
        except Exception as e:
            st.error(f"Gagal membaca CSV: {e}")
            df = None
            
        if df is not None:
            st.session_state["medical_df"] = df
            st.success("File berhasil dibaca!")
            
            # Memastikan semua fitur ada sebelum prediksi
            if all(feat in df.columns for feat in feature_list):
                try:
                    df_input = df[feature_list]
                    pred = model.predict(df_input)
                    df["Prediction"] = pred
                    df["Pred_Description"] = df["Prediction"].replace({
                        "M": "Malignant (Ganas)",
                        "B": "Benign (Jinak)",
                        1: "Malignant (Ganas)",
                        0: "Benign (Jinak)"
                    })
                except Exception as e:
                    st.error(f"Gagal melakukan prediksi: {e}")
            else:
                st.warning("Beberapa fitur yang dibutuhkan model tidak ditemukan di CSV. Pastikan kolom sesuai feature_list.")
                st.session_state["medical_df"] = df 

            if "Prediction" in df.columns:
                pred_values = df["Prediction"].astype(str)
                ganas = (pred_values == "M").sum()
                jinak = (pred_values == "B").sum()
                if (ganas + jinak) == 0:
                    if set(pred_values.unique()).issubset({"1", "0", "1.0", "0.0"}):
                        ganas = (pred_values == "1").sum()
                        jinak = (pred_values == "0").sum()
                total = len(df)
                st.subheader("📌 Hasil Prediksi")
                st.info(f"Total Pasien yang Diprediksi: **{total}** | **Ganas (Malignant): {ganas}** pasien | **Jinak (Benign): {jinak}** pasien.")
                
            else:
                st.subheader("📌 Hasil Prediksi")
                st.warning("Prediksi belum dapat ditampilkan. Silakan unggah file yang sesuai.")

            if "Prediction" in df.columns:
                st.dataframe(st.session_state["medical_df"])
            
            try:
                csv = st.session_state["medical_df"].to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="💾 Download Hasil Prediksi",
                    data=csv,
                    file_name="hasil_prediksi.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Gagal membuat tombol download: {e}")

            st.subheader("📊 Distribusi Prediksi")
            if "Pred_Description" in st.session_state["medical_df"].columns:
                st.bar_chart(st.session_state["medical_df"]["Pred_Description"].value_counts())
            else:
                st.bar_chart(st.session_state["medical_df"]["Prediction"].value_counts())

    chat_ui("chat_medical", chatbot_medical, "💬 Chatbot Teknis (Untuk Tenaga Medis)")

if __name__ == "__main__":
    run_tenaga_medis()
