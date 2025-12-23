"""
Sekarang, mari kita coba simulasi coding. Anggap saja kita sudah menginstall pandas 
dan mengimpornya dengan kode standar: import pandas as pd

Jika kamu memiliki file data bernama karyawan.csv, kira-kira perintah (fungsi) apa yang disediakan Pandas 
untuk membaca file csv tersebut?
"""

from sympy.simplify.radsimp import numer
import pandas as pd

# Membaca file CSV
# Pintu gerbang utama untuk memuat data dari file teks ke DataFrame.
data = pd.read_csv("karyawan.csv")

# Menampilkan data
# Sangat berguna untuk mengintip 5 baris pertama, terutama jika datanya memiliki jutaan baris.
data.head()

# Menampilkan informasi data
# Memberikan gambaran umum tentang struktur data, termasuk jumlah baris, nama kolom, dan tipe data.
data.info()

# Menampilkan statistik data
# Memberikan ringkasan statistik dari data, termasuk nilai minimum, maksimum, rata-rata, dan variasi.
data.describe()

# Jika kita ingin mengambil kolom 'Gaji' saja dari variabel data, kira-kira bagaimana kodenya?
gaji = data['gaji']

gaji.head()

# Kira-kira, bagaimana kodenya jika kita ingin menampilkan baris data yang nilai kolom 'gaji'-nya lebih besar dari (>) 10000000? Coba tebak logikanya dulu.

gaji_tinggi = data[data['gaji'] > 10_000_000]

gaji_tinggi.head()

"""
Kira-kira, bagaimana idemu untuk menulis kode yang:

    Mengelompokkan data berdasarkan kolom 'Departemen'.

    Lalu menghitung rata-rata (.mean()) untuk setiap kelompoknya?
"""

group = data.groupby('departemen').mean(numeric_only=True)

group.head()