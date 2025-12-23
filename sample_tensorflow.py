import tensorflow as tf

model = tf.keras.models.Sequential([
    # 1. Input Layer: Mendatarkan gambar 28x28 piksel menjadi satu garis lurus (784 angka)
    tf.keras.layers.Flatten(input_shape=(28, 28)),

    # 2. Hidden Layer: Lapisan "berpikir" dengan 128 neuron
    tf.keras.layers.Dense(128, activation='relu'),

    # 3. Output Layer: Lapisan penebak hasil
    tf.keras.layers.Dense(10, activation='softmax')
])
"""
💡 Info Penting: Fungsi softmax di akhir bertugas mengubah angka-angka aneh menjadi persentase 
probabilitas. Contoh: "Saya 90% yakin ini angka 7, tapi 10% yakin ini angka 1."
"""

model.compile(
    optimizer='adam', # Algoritma optimasi standar yang sangat populer
    loss='sparse_categorical_crossentropy', # Cara hitung error untuk klasifikasi banyak kelas (0-9)
    metrics=['accuracy'] # Kita ingin memantau akurasi
)

# Berlatih selama 5 putaran (epochs)
model.fit(X_train, y_train, epochs=5)
"""
Langkah Terakhir: Training (Latihan) 🏋️‍♂️
Saatnya model kita masuk "gym" untuk berlatih. Di TensorFlow, perintahnya mirip dengan Scikit-Learn,
yaitu .fit(). Namun, ada satu parameter baru yang penting bernama Epochs.
Satu epoch artinya model sudah melihat seluruh data latihan satu kali putaran penuh.
"""

test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"Akurasi pada data ujian: {test_acc}")

