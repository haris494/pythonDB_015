import tkinter as tk
import sqlite3

# Fungsi untuk mendapatkan prediksi fakultas berdasarkan nilai tertinggi
def prediksi_fakultas(nilai_biologi, nilai_fisika, nilai_inggris):
    if nilai_biologi > nilai_fisika and nilai_biologi > nilai_inggris:
        return "Kedokteran"
    elif nilai_fisika > nilai_biologi and nilai_fisika > nilai_inggris:
        return "Teknik"
    elif nilai_inggris > nilai_biologi and nilai_inggris > nilai_fisika:
        return "Bahasa"
    else:
        return "Tidak dapat memprediksi"

# Fungsi untuk menyimpan data ke SQLite
def simpan_ke_database(nama_siswa, nilai_biologi, nilai_fisika, nilai_inggris):
    conn = sqlite3.connect("data_siswa.db")
    cursor = conn.cursor()

    # Mengecek apakah tabel sudah ada, jika belum maka membuat tabel
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')

    # Mendapatkan prediksi fakultas
    prediksi = prediksi_fakultas(nilai_biologi, nilai_fisika, nilai_inggris)

    # Menyimpan data ke database
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama_siswa, nilai_biologi, nilai_fisika, nilai_inggris, prediksi))

    conn.commit()
    conn.close()

# Fungsi yang akan dijalankan ketika tombol "Hasil Prediksi" ditekan
def hasil_prediksi():
    # Mengambil nilai dari entry
    nilai_pelajaran = [float(entry.get()) for entry in input_nilai]
    nama_siswa = entry_nama.get()

    # Memisahkan nilai untuk setiap mata pelajaran
    nilai_biologi = nilai_pelajaran[0]
    nilai_fisika = nilai_pelajaran[1]
    nilai_inggris = nilai_pelajaran[2]

    # Menyimpan data ke database
    simpan_ke_database(nama_siswa, nilai_biologi, nilai_fisika, nilai_inggris)

    # Mendapatkan prediksi fakultas
    prediksi = prediksi_fakultas(nilai_biologi, nilai_fisika, nilai_inggris)

    # Menampilkan hasil prediksi
    luaran_hasil.config(text=f"Prodi yang direkomendasikan: {prediksi}")

# Membuat GUI Tkinter
root = tk.Tk()
root.title("Aplikasi Prediksi Prodi Pilihan")
root.geometry('500x500')
root.resizable(False, False)
root.config(background='blue')

# Menambahkan entry dan label untuk nama siswa
label_nama = tk.Label(root, text="Nama Siswa:")
label_nama.grid(row=0, column=0, pady=5, padx=10)

entry_nama = tk.Entry(root)
entry_nama.grid(row=0, column=1, pady=5, padx=10)

# Menambahkan input nilai mata pelajaran
input_nilai = []
mata_pelajaran = ["Biologi", "Fisika", "Inggris"]

for i, mata_pelajaran_label in enumerate(mata_pelajaran):
    label = tk.Label(root, text=f"Nilai {mata_pelajaran_label}:")
    label.grid(row=i + 1, column=0, pady=5, padx=10)

    entry = tk.Entry(root)
    entry.grid(row=i + 1, column=1, pady=5, padx=10)
    input_nilai.append(entry)

# Menambahkan tombol "Hasil Prediksi"
hasil_button = tk.Button(root, text="Hasil Prediksi", command=hasil_prediksi)
hasil_button.grid(row=len(mata_pelajaran) + 1, column=0, columnspan=2, pady=10)

# Menambahkan label luaran hasil prediksi
luaran_hasil = tk.Label(root, text="", font=("Times New Roman", 14))
luaran_hasil.grid(row=len(mata_pelajaran) + 2, column=0, columnspan=4, pady=10)

# Menjalankan loop Tkinter
root.mainloop()