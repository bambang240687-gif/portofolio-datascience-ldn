import pandas as pd 
from sklearn.linear_model import LinearRegression
import joblib # Library untuk menyimpan model ke file
import os

# 1. Buat data simulasi
data = {
    'Jumlah_Pesanan' : [10, 50, 100, 200, 500, 1000], # X (Features)
    'Hari_Pengerjaan': [7, 10, 14, 18, 30, 45], # y (Target)
}

df = pd.DataFrame(data)

# 2. Pisahkan X dan y
X = df[['Jumlah_Pesanan']]
y = df['Hari_Pengerjaan']

# 3. Latih model
model = LinearRegression()
model.fit(X, y)

print("Model berhasil dilatih")
print(f"Contoh prediksi jika jumlah pesanan 250: {model.predict([[250]])[0]}")

# 4. Simpan model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'model_estimasi.sav')

joblib.dump(model, MODELS_DIR)

print("Model berhasil disimpan")

