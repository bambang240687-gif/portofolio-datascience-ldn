import streamlit as st
import pdfplumber
import pandas as pd
import re
from io import BytesIO

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Ekstraktor Invoice Otomatis", page_icon="📄")

st.title("📄 Aplikasi OCR Invoice & SPH")
st.markdown("Upload file PDF Invoice/SPH Anda, dan biarkan AI mengekstrak data pentingnya ke Excel.")

# --- Upload File ---
uploaded_files = st.file_uploader("Upload File PDF (Bisa Banyak Sekaligus)", type="pdf", accept_multiple_files=True)

# --- Fungsi bantu: normalisasi angka ---
def normalisasi_angka(teks):
    if not teks:
        return 0
    teks = teks.strip()
    teks = teks.replace(" ", "").replace(".", "").replace(",", "")
    return int(teks) if teks.isdigit() else 0

# Tombol Eksekusi
if st.button("Ekstrak Data 🚀") and uploaded_files:
    
    data_hasil = []
    progress_bar = st.progress(0)
    
    for i, file_pdf in enumerate(uploaded_files):
        with pdfplumber.open(file_pdf) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text() or ""

            # --- pembersih duplikasi huruf / angka (SPH bold palsu) ---
            if len(re.findall(r'([A-Za-z0-9])\1', text)) / max(len(text), 1) > 0.1:
                text = re.sub(r'([A-Za-z0-9\.\-/,:;%])\1', r'\1', text)

            # --- Nomor Dokumen ---
            # --- Nomor Dokumen (lebih ketat, hindari angka nyasar) ---
            no_surat = "Tidak Ditemukan"

            # Cari pola “No:” atau “Nomor:” tapi pastikan setelahnya bukan angka tunggal
            m_no = re.search(
                r'\b(?:Nomor|No\.?)\b\s*[:\-]?\s*([A-Za-z]{2,}[/A-Za-z0-9.\-]+)',
                text, re.IGNORECASE
            )

            # Kalau belum ketemu, cari kode dengan awalan APP atau SPH
            if m_no:
                no_surat = m_no.group(1).strip()
            else:
                m_alt = re.search(r'\b(APP|SPH)[/\-A-Za-z0-9]+', text)
                if m_alt:
                    no_surat = m_alt.group(0).strip()

            # --- Tanggal ---
            tanggal = "Tidak Ditemukan"
            m_tgl = re.search(
                r'(?:Jakarta,?\s*)?(\d{1,2}\s+(?:Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)\s+\d{4})',
                text, re.IGNORECASE)
            if m_tgl:
                tanggal = m_tgl.group(1)

            # --- Total Harga ---
            total_bersih = "0"
            m_total = re.search(r'Grand\s*Total[^R]*Rp[^\d]*([\d\.,]+)', text, re.IGNORECASE)
            if m_total:
                total_raw = m_total.group(1)
            else:
                semua = re.findall(r'Rp[^\d]*([\d\.,]+)', text)
                total_raw = max(semua, key=lambda x: normalisasi_angka(x)) if semua else "0"

            angka_bersih = normalisasi_angka(total_raw)
            if angka_bersih:
                total_bersih = f"{angka_bersih:,}".replace(",", ".")

            # --- SPH Mode ---
            if "SPH" in no_surat.upper() or "PENAWARAN" in text.upper():
                total_bersih = "0"

            # --- Simpan hasil ---
            data_hasil.append({
                "Nama File": file_pdf.name,
                "Nomor Dokumen": no_surat,
                "Tanggal": tanggal,
                "Total Nilai (Rp)": total_bersih
            })

        progress_bar.progress((i + 1) / len(uploaded_files))

    # --- TAMPILKAN HASIL ---
    st.success("✅ Ekstraksi Selesai!")
    df = pd.DataFrame(data_hasil)
    st.dataframe(df)

    # --- DOWNLOAD KE EXCEL ---
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data Ekstraksi')

    st.download_button(
        label="📥 Download Hasil ke Excel",
        data=buffer.getvalue(),
        file_name="Rekap_Data_Invoice.xlsx",
        mime="application/vnd.ms-excel"
    )

elif not uploaded_files:
    st.info("Silakan upload file PDF terlebih dahulu.")
