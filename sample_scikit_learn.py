# Features (Huruf X besar, karena biasanya terdiri dari banyak kolom/matriks)
X = data[['Lama Bekerja', 'Level Pendidikan']]

# Target (huruf y kecil, karena biasanya satu kolom/vektor)
y = data['Gaji']

from sklearn.model_selection import train_test_split

# test_size=0.2 artinya kita menyisihkan 20% data untuk ujian
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

from sklearn.linear_model import LinearRegression

# 1. Pilih model
model = LinearRegression()

# 2. Latih model dengan data latihan (Training)
model.fit(X_train, y_train)

from sklearn.metrics import mean_absolute_error

# Lakukan prediksi
y_pred = model.predict(X_test)

# Hitung Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test, y_pred)

print(f"MAE: {mae}")

"""
🎉 Misi Selesai: Deep Learning (Intro)

Kamu baru saja memahami alur kerja (pipeline) utama seorang AI Engineer:

    Arsitektur: Menyusun lapisan neuron (Input -> Hidden -> Output).

    Compile: Menentukan cara belajar (Optimizer) dan cara menilai (Loss/Metrics).

    Training: Melatih model di "gym" (Fit) dengan menjaga agar tidak overfitting.

    Evaluasi: Menguji dengan data asing (Evaluate).
"""
