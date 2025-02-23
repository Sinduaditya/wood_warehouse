# Wood Warehouse Management System

Wood Warehouse Management System adalah aplikasi berbasis web yang dikembangkan menggunakan **Streamlit** untuk mengelola inventaris kayu, supplier, pelanggan, dan pesanan dalam gudang.

## 📌 Fitur Utama
- **Dashboard**: Menampilkan ringkasan data warehouse.
- **Suppliers**: Mengelola daftar supplier kayu.
- **Customers**: Menyimpan data pelanggan yang melakukan pemesanan.
- **Warehouse Stock**: Melacak stok kayu yang tersedia.
- **Customer Dashboard**: Antarmuka khusus untuk pelanggan yang ingin melakukan pemesanan.

## 🚀 Instalasi
1. **Clone Repository**
```bash
   git clone <https://github.com/Sinduaditya/wood_warehouse.git>
   cd wood_warehouse
```
2. **Buat Virtual Environment (Opsional, tetapi disarankan)**
```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Mac/Linux
   venv\Scripts\activate     # Untuk Windows
```
3. **Install Dependensi**
```bash
   pip install -r requirements.txt
```
4. **Jalankan Aplikasi**
```bash
   streamlit run app.py
```

## 📂 Struktur Direktori
```
📁 wood-warehouse-management
│── 📁 pages
│   ├── 1_Dashboard.py
│   ├── 2_Suppliers.py
│   ├── 3_Customers.py
│   ├── 5_Warehouse_Stock.py
|   ├── ( untuk setiap menu selanjutnya, cth: 5_Payments.py) FORMAT WAJIB SAMA.
│── app.py
│── config.py
│── readme.md
│── requirements.txt
```
## 🔐 Auth
- admin : admin@admin.com 
    ( pass : sindu )
- user : nduujanadi51@gmail.com
    ( pass : sindu )


## 🔧 Konfigurasi
File `config.py` digunakan untuk mengatur parameter koneksi database dan konfigurasi lainnya.

## 🛠 Teknologi yang Digunakan
- **Python** (Streamlit, PostgreSQL, Pandas)
- **PostgreSQL** sebagai database backend
- **Supabase/PostgREST** untuk API database

## 📌 Catatan
Jika ada kendala terkait **akses menu yang tidak diinginkan**, pastikan untuk menggunakan **Streamlit navigation control**, misalnya dengan **menyembunyikan sidebar tertentu** di dalam `app.py`:
```python
import streamlit as st
st.set_page_config(layout='wide', initial_sidebar_state='collapsed')
```

## 📝 Lisensi
Proyek ini bersifat open-source. Silakan gunakan dan modifikasi sesuai kebutuhan.

---
Selamat mencoba! 🚀

