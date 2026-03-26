from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Fungsi untuk menghubungkan ke database
def get_db_connection():
    conn = sqlite3.connect('toko.db')
    conn.row_factory = sqlite3.Row # Agar data bisa diakses seperti dictionary
    return conn

# Membuat tabel jika belum ada saat aplikasi pertama kali dijalankan
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS produk (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_barang TEXT NOT NULL,
            harga INTEGER NOT NULL,
            kuantitas INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inisialisasi Database
init_db()

# 1. Halaman Utama (Menampilkan file HTML)
@app.route('/')
def index():
    return render_template('index.html')

# 2. Mengambil Semua Data Barang (Read)
@app.route('/api/produk', methods=['GET'])
def get_produk():
    conn = get_db_connection()
    produk = conn.execute('SELECT * FROM produk').fetchall()
    conn.close()
    return jsonify([dict(p) for p in produk])

# 3. Menambah Barang Baru (Create)
@app.route('/api/produk', methods=['POST'])
def add_produk():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO produk (nama_barang, harga, kuantitas) VALUES (?, ?, ?)',
                   (data['nama_barang'], 0, 0)) # Default harga & stok 0
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({"id": new_id, "pesan": "Berhasil ditambahkan!"})

# 4. Mengubah Harga / Kuantitas (Update)
@app.route('/api/produk/<int:id>', methods=['PUT'])
def update_produk(id):
    data = request.json
    conn = get_db_connection()
    conn.execute('UPDATE produk SET harga = ?, kuantitas = ? WHERE id = ?',
                 (data['harga'], data['kuantitas'], id))
    conn.commit()
    conn.close()
    return jsonify({"pesan": "Berhasil diperbarui!"})

# 5. Menghapus Barang (Delete)
@app.route('/api/produk/<int:id>', methods=['DELETE'])
def delete_produk(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM produk WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"pesan": "Berhasil dihapus!"})

if __name__ == '__main__':
    # Berjalan di mode debug agar gampang mendeteksi error
    app.run(debug=True)