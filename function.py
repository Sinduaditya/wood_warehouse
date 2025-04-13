import streamlit as st
from supabase import create_client
from config import supabase     # import dari config.py
from datetime import datetime
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from streamlit_option_menu import option_menu

def lihat_pesanan_detail():
    st.subheader("📋 Riwayat Pesanan Anda")

    # Pastikan user sudah login
    if "user" not in st.session_state:
        st.warning("⚠️ Silakan login terlebih dahulu.")
        return

    # Ambil ID customer dari session
    customer_id = st.session_state["user"].get("id")
    if not customer_id:
        st.error("❌ Gagal mengambil data pelanggan.")
        return

    # Ambil data pesanan berdasarkan customer_id
    response = supabase.table("orders").select("*").eq("customer_id", customer_id).order("created_at", desc=True).execute()

    if response.data:
        # Mengubah ke DataFrame dan rename kolom
        df = pd.DataFrame(response.data)
        df = df.rename(columns={
            "id": "Order ID",
            "order_date": "Tanggal Pemesanan",
            "total_price": "Total Harga",
            "status": "Status Pesanan",
            "created_at": "Waktu Dibuat"
        })

        # Format angka di kolom harga agar lebih rapi
        df["Total Harga"] = df["Total Harga"].apply(lambda x: f"Rp. {x:,.0f}".replace(",", "."))

        # Format tanggal agar lebih mudah dibaca
        df["Tanggal Pemesanan"] = pd.to_datetime(df["Tanggal Pemesanan"], errors='coerce').dt.strftime("%d %B %Y")
        df["Waktu Dibuat"] = pd.to_datetime(df["Waktu Dibuat"], errors='coerce').dt.strftime("%d %B %Y  Jam : %H:%M")


        # Pilihan filter status
        status_filter = st.selectbox("Filter Status", ["Semua", "Shipped", "Cancelled", "Pending", "Completed", "Paid"])
        
        # Terapkan filter jika tidak memilih "Semua"
        if status_filter != "Semua":
            df = df[df["Status Pesanan"] == status_filter]

        # Cek apakah df kosong setelah filter
        if df.empty:
            st.info("📭 Tidak ada pesanan dengan status tersebut.")
        else:
            # Inisialisasi session state untuk menyimpan status tampilan detail
            if "show_details" not in st.session_state:
                st.session_state["show_details"] = {}

            # Tampilkan tabel pesanan dengan tombol "Lihat Detail" & "Tutup Detail"
            for _, row in df.iterrows():
                order_id = row["Order ID"]

                with st.container():
                    st.write(f"### Order ID: {order_id}")
                    st.write(f"📅 **Tanggal Pemesanan:** {row['Tanggal Pemesanan']}")
                    st.write(f"💰 **Total Harga:** {row['Total Harga']}")
                    st.write(f"📦 **Status Pesanan:** {row['Status Pesanan']}")

                    # Pastikan setiap order ID memiliki state
                    if order_id not in st.session_state["show_details"]:
                        st.session_state["show_details"][order_id] = False

                    col1, col2 = st.columns([1, 4])  # Buat 2 kolom untuk tombol
                    with col1:
                        if st.button(f"🔍 Lihat Detail", key=f"open_{order_id}"):
                            st.session_state["show_details"][order_id] = True
                            st.rerun()  # 🔄 Refresh UI langsung agar tombol bekerja dalam sekali klik
                    with col2:
                        if st.button(f"🔒 Tutup Detail", key=f"close_{order_id}"):
                            st.session_state["show_details"][order_id] = False
                            st.rerun()  # 🔄 Refresh UI langsung

                    # Tampilkan detail jika state aktif
                    if st.session_state["show_details"][order_id]:
                        tampilkan_detail_pesanan(order_id)

                    st.divider()  # Garis pemisah antar order

    else:
        st.info("📭 Anda belum memiliki pesanan.")

def lihat_pesanan():
    st.subheader("📋 Riwayat Pesanan Anda")

    # Pastikan user sudah login
    if "user" not in st.session_state:
        st.warning("⚠️ Silakan login terlebih dahulu.")
        return

    # Ambil ID customer dari session
    customer_id = st.session_state["user"].get("id")
    if not customer_id:
        st.error("❌ Gagal mengambil data pelanggan.")
        return

    # Ambil data pesanan berdasarkan customer_id
    response = supabase.table("orders").select("id, order_date, total_price, status, created_at").eq("customer_id", customer_id).order("created_at", desc=True).execute()

    if response.data:
        # Mengubah ke DataFrame dan rename kolom
        df = pd.DataFrame(response.data)
        df = df.rename(columns={
            "id": "Order ID",
            "order_date": "Tanggal Pemesanan",
            "total_price": "Total Harga",
            "status": "Status Pesanan",
            "created_at": "Waktu Dibuat"
        })

        # Format angka di kolom harga agar lebih rapi
        df["Total Harga"] = df["Total Harga"].apply(lambda x: f"Rp. {x:,.0f}".replace(",", "."))
        
        # Format tanggal agar lebih mudah dibaca
        df["Tanggal Pemesanan"] = pd.to_datetime(df["Tanggal Pemesanan"], format='ISO8601', errors='coerce').dt.strftime("%d %B %Y")
        df["Waktu Dibuat"] = pd.to_datetime(df["Waktu Dibuat"], format='ISO8601', errors='coerce').dt.strftime("%d %B %Y  Jam : %H:%M")

        # Set indeks ke "Order ID" sebelum styling
        df.set_index("Order ID", inplace=True)

        # Fungsi untuk memberi warna berdasarkan status
        def highlight_status(val):
            warna = {
                "Shipped": "background-color: #a5d6a7; color: black;",  # Hijau
                "Cancelled": "background-color: #ef9a9a; color: black;",  # Merah
                "Pending": "background-color: #fff59d; color: black;",  # Kuning
                "Completed": "background-color: #78C0E0 ; color: black;",  # Biru
                "Paid": "background-color: #79B473; color: black;"  # Hijau
            }
            return warna.get(val, "")  # Mengembalikan style CSS

        status_filter = st.selectbox("Filter Status", ["Semua", "Shipped", "Cancelled", "Pending", "Completed", "Paid"])
        if status_filter != "Semua":
            df = df[df["Status Pesanan"] == status_filter]
        # Terapkan styling pada kolom "Status Pesanan"
        styled_df = df.style.applymap(highlight_status, subset=["Status Pesanan"])

        # Tampilkan tabel
        st.dataframe(styled_df, use_container_width=True)
        
        # Tambahkan fitur pembayaran dan pembatalan
        st.subheader("💰 Bayar atau Batalkan Pesanan")
        
        # Get the raw data for processing payments or cancellations
        raw_data = response.data
        
        # Create payment or cancellation section for each order
        for order in raw_data:
            order_id = order['id']
            total_price = order['total_price']
            status = order['status']
            
            # Only show payment option for orders that are not paid/cancelled
            if status != "Paid" and status != "Cancelled":
                with st.expander(f"Order ID: {order_id} - Total: Rp. {total_price:,.0f}".replace(",", ".")):
                    with st.form(key=f"payment_form_{order_id}"):
                        st.write("### Form Pembayaran")
                        
                        # Payment method dropdown
                        payment_method = st.selectbox(
                            "Metode Pembayaran",
                            ["Cash", "Bank Transfer"],
                            key=f"payment_method_{order_id}"
                        )
                        
                        # Display amount (read-only)
                        st.write(f"**Total Pembayaran:** Rp. {total_price:,.0f}".replace(",", "."))
                        
                        # Payment date
                        payment_date = st.date_input(
                            "Tanggal Pembayaran",
                            datetime.now().date(),
                            key=f"payment_date_{order_id}"
                        )
                        
                        # Submit button
                        submitted = st.form_submit_button("Bayar Sekarang")
                        
                        if submitted:
                            # Create payment record
                            payment_data = {
                                "order_id": order_id,
                                "payment_method": payment_method,
                                "amount": total_price,
                                "payment_status": "Completed",
                                "payment_date": payment_date.strftime("%Y-%m-%d")
                            }
                            
                            try:
                                # Check if payment already exists for this order
                                check_payment = supabase.table("payments").select("*").eq("order_id", order_id).execute()
                                
                                if check_payment.data:
                                    st.warning(f"Pembayaran untuk Order ID {order_id} sudah ada.")
                                else:
                                    # Insert payment record
                                    payment_response = supabase.table("payments").insert(payment_data).execute()
                                    
                                    # Update order status
                                    order_update = supabase.table("orders").update({"status": "Paid"}).eq("id", order_id).execute()
                                    
                                    st.success(f"✅ Pembayaran untuk Order ID {order_id} berhasil! Status telah diperbarui.")
                                    st.balloons()
                                    st.info("💡 Pesanan Anda telah berhasil dibayar. Terima kasih!")
                                    
                                    # Refresh the page
                                    st.rerun()
                                
                            except Exception as e:
                                st.error(f"❌ Terjadi kesalahan: {e}")
            
            # Only show cancel option for orders with status "Pending"
            if status == "Pending":
                if st.button(f"Batalkan Pesanan ID: {order_id}", key=f"cancel_order_{order_id}"):
                    try:
                        # Ambil detail pesanan untuk mengembalikan stok
                        order_details = supabase.table("order_details").select("wood_type_id, quantity").eq("order_id", order_id).execute()
                        
                        if order_details.data:
                            for detail in order_details.data:
                                wood_type_id = detail["wood_type_id"]
                                quantity = detail["quantity"]
                                
                                # Update stok kayu
                                supabase.table("warehouse_stock").update({"quantity": supabase.table("warehouse_stock").select("quantity").eq("id", wood_type_id).execute().data[0]["quantity"] + quantity}).eq("id", wood_type_id).execute()
                        
                        # Hapus pesanan dan detailnya
                        supabase.table("order_details").delete().eq("order_id", order_id).execute()
                        supabase.table("orders").delete().eq("id", order_id).execute()
                        
                        st.success(f"✅ Pesanan ID {order_id} berhasil dibatalkan dan stok telah dikembalikan.")
                        st.info("💡 Pesanan Anda telah berhasil dibatalkan.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Terjadi kesalahan saat membatalkan pesanan: {e}")
    else:
        st.info("📭 Anda belum memiliki pesanan.")

def status_pembayaran():
    st.subheader("📋 Status Pembayaran Anda")

    # Pastikan user sudah login
    if "user" not in st.session_state:
        st.warning("⚠️ Silakan login terlebih dahulu.")
        return

    # Ambil ID customer dari session
    customer_id = st.session_state["user"].get("id")
    if not customer_id:
        st.error("❌ Gagal mengambil data pelanggan.")
        return

    # Query data payments yang sudah difilter berdasarkan customer_id
    response = supabase.table("payments")\
        .select("id, order_id, payment_method, amount, payment_status, payment_date, orders!inner(customer_id)")\
        .eq("orders.customer_id", customer_id)\
        .order("payment_date", desc=True)\
        .execute()

    if not response.data:
        st.info("📭 Anda belum memiliki pembayaran.")
        return

    # Konversi data ke DataFrame
    df = pd.DataFrame(response.data)

    # Rename kolom agar lebih user-friendly
    df = df.rename(columns={
        "id": "Payment ID",
        "order_id": "Order ID",
        "payment_method": "Metode Pembayaran",
        "amount": "Total Harga",
        "payment_status": "Status Pembayaran",
        "payment_date": "Waktu Pembayaran"
    })

    # Format angka di kolom harga agar lebih rapi
    df["Total Harga"] = df["Total Harga"].apply(lambda x: f"Rp. {x:,.0f}".replace(",", "."))

    # Format tanggal agar lebih mudah dibaca
    df["Waktu Pembayaran"] = pd.to_datetime(df["Waktu Pembayaran"]).dt.strftime("%d %B %Y - %H:%M")
    df.set_index("Order ID", inplace=True)

    # Pilihan filter status pembayaran
    status_filter = st.selectbox("Filter Status", ["Semua", "Pending", "Completed", "Failed"])
    
    # Terapkan filter jika tidak memilih "Semua"
    if status_filter != "Semua":
        df = df[df["Status Pembayaran"] == status_filter]

    if df.empty:
        st.info("📭 Tidak ada pembayaran dengan status tersebut.")
        return

    # Fungsi untuk memberi warna berdasarkan status pembayaran
    def highlight_status(val):
        warna = {
            "Completed": "background-color: #a5d6a7; color: black;",  # Hijau
            "Pending": "background-color: #fff59d; color: black;",  # Kuning
            "Failed": "background-color: #ef9a9a; color: black;",  # Merah
        }
        return warna.get(val, "")

    # Terapkan styling pada kolom "Status Pembayaran"
    styled_df = df.style.applymap(highlight_status, subset=["Status Pembayaran"])

    # Tampilkan tabel
    st.dataframe(styled_df, use_container_width=True)

def status_pengiriman():
    st.subheader("🚚 Status Pengiriman Anda")

    # Pastikan user sudah login
    if "user" not in st.session_state:
        st.warning("⚠️ Silakan login terlebih dahulu.")
        return

    # Ambil ID customer dari session
    customer_id = st.session_state["user"].get("id")
    if not customer_id:
        st.error("❌ Gagal mengambil data pelanggan.")
        return

    # Query data shipments yang sudah difilter berdasarkan customer_id
    response = supabase.table("shipments")\
        .select("id, order_id, tracking_number, shipping_company, estimated_delivery, status, created_at, orders!inner(customer_id)")\
        .eq("orders.customer_id", customer_id)\
        .order("created_at", desc=True)\
        .execute()

    if not response.data:
        st.info("📭 Anda belum memiliki pengiriman.")
        return

    # Konversi data ke DataFrame
    df = pd.DataFrame(response.data)

    # Rename kolom agar lebih user-friendly
    df = df.rename(columns={
        "id": "Shipment ID",
        "order_id": "Order ID",
        "tracking_number": "Nomor Resi",
        "shipping_company": "Ekspedisi",
        "estimated_delivery": "Estimasi Tiba",
        "status": "Status Pengiriman",
        "created_at": "Waktu Pengiriman"
    })

    # Format tanggal agar lebih mudah dibaca
    df["Estimasi Tiba"] = pd.to_datetime(df["Estimasi Tiba"]).dt.strftime("%d %B %Y")
    df["Waktu Pengiriman"] = pd.to_datetime(df["Waktu Pengiriman"]).dt.strftime("%d %B %Y - %H:%M")

    # Pilihan filter status pengiriman
    status_filter = st.selectbox("Filter Status Pengiriman", ["Semua", "In Transit", "Delivered", "Failed"])
    df.set_index("Order ID", inplace=True)
    # Terapkan filter jika tidak memilih "Semua"
    if status_filter != "Semua":
        df = df[df["Status Pengiriman"] == status_filter]

    if df.empty:
        st.info("📭 Tidak ada pengiriman dengan status tersebut.")
        return

    # Fungsi untuk memberi warna berdasarkan status pengiriman
    def highlight_status(val):
        warna = {
            "Delivered": "background-color: #a5d6a7; color: black;",  # Hijau
            "In Transit": "background-color: #fff59d; color: black;",  # Kuning
            "Failed": "background-color: #ef9a9a; color: black;",  # Merah
        }
        return warna.get(val, "")

    # Terapkan styling pada kolom "Status Pengiriman"
    styled_df = df.style.applymap(highlight_status, subset=["Status Pengiriman"])

    # Tampilkan tabel
    st.dataframe(styled_df, use_container_width=True)

def tampilkan_detail_pesanan(order_id):
    """Menampilkan detail pesanan berdasarkan Order ID"""
    st.subheader(f"📜 Detail Pesanan - Order ID: {order_id}")

    # Ambil detail order dari database
    response = supabase.table("order_details").select("*").eq("order_id", order_id).execute()

    if response.data:
        df_detail = pd.DataFrame(response.data)

        # Rename kolom agar lebih user-friendly
        df_detail = df_detail.rename(columns={
            "order_id":"ID Order",
            "wood_type_id": "Tipe Kayu",
            "quantity": "Jumlah Kayu",
            "unit_price": "Harga Satuan",
            "subtotal": "Total Harga"
        })

        # Format harga
        df_detail["Harga Satuan"] = df_detail["Harga Satuan"].apply(lambda x: f"Rp. {x:,.0f}".replace(",", "."))
        df_detail = df_detail.drop(columns=["id"])
        # Hitung total per item
        df_detail.set_index("ID Order", inplace=True)

        # Tampilkan tabel detail pesanan
        st.dataframe(df_detail, use_container_width=True)

    else:
        st.info("📭 Tidak ada detail pesanan untuk Order ID ini.")

def tampilkan_supplier():
    st.subheader("📦 Daftar Supplier")

    # Query untuk mengambil semua data supplier
    response = supabase.table("suppliers")\
        .select("id, name, contact_person, phone, email, address, created_at")\
        .order("created_at", desc=True)\
        .execute()

    if not response.data:
        st.info("📭 Belum ada data supplier.")
        return

    # Konversi data ke DataFrame
    df = pd.DataFrame(response.data)

    # Rename kolom agar lebih user-friendly
    df = df.rename(columns={
        "id": "ID Supplier",
        "name": "Nama Supplier",
        "contact_person": "Kontak Person",
        "phone": "Telepon",
        "email": "Email",
        "address": "Alamat",
        "created_at": "Tanggal Ditambahkan"
    })

    # Format tanggal agar lebih mudah dibaca
    df["Tanggal Ditambahkan"] = pd.to_datetime(df["Tanggal Ditambahkan"], format='ISO8601').dt.strftime("%d %B %Y - %H:%M")
    df.set_index("ID Supplier", inplace=True)
    # Tampilkan tabel
    st.dataframe(df, use_container_width=True)

def tampilkan_jenis_kayu():
    st.subheader("🪵 Daftar Jenis Kayu")

    # Query untuk mengambil semua jenis kayu
    response = supabase.table("wood_types")\
        .select("id, wood_name, category, description, created_at")\
        .order("created_at", desc=True)\
        .execute()

    if not response.data:
        st.info("📭 Belum ada data jenis kayu.")
        return

    # Konversi data ke DataFrame
    df = pd.DataFrame(response.data)

    # Rename kolom agar lebih user-friendly
    df = df.rename(columns={
        "id": "ID Kayu",
        "wood_name": "Nama Kayu",
        "category": "Kategori",
        "description": "Deskripsi",
        "created_at": "Tanggal Ditambahkan"
    })

    # Format tanggal agar lebih mudah dibaca
    df["Tanggal Ditambahkan"] = pd.to_datetime(df["Tanggal Ditambahkan"], format='ISO8601').dt.strftime("%d %B %Y - %H:%M")

    # Mapping kategori kayu dengan emoji
    kategori_emoji = {
        "Hardwood": " Hardwood",
        "Softwood": " Softwood",
        "Plywood": " Plywood",
        "Others": " Others"
    }

    # Ganti nilai kategori dengan emoji yang sesuai
    df["Kategori"] = df["Kategori"].map(kategori_emoji)
    df.set_index("ID Kayu", inplace=True)
    # Tambahkan filter berdasarkan kategori kayu
    kategori_filter = st.selectbox("Filter Kategori Kayu", ["Semua", "Hardwood", "Softwood", "Plywood", "Others"])
    if kategori_filter != "Semua":
        df = df[df["Kategori"].str.contains(kategori_filter, case=False, na=False)]

    if df.empty:
        st.info("📭 Tidak ada jenis kayu dengan kategori tersebut.")
        return

    # Tampilkan tabel
    st.dataframe(df, use_container_width=True)

def tampilkan_stok_gudang():    
    st.subheader("🏢 Stok Gudang")

    # Query untuk mengambil data stok dengan join ke tabel kayu dan supplier
    response = supabase.table("warehouse_stock")\
        .select("id, wood_types!inner(wood_name, category), suppliers!inner(name), quantity, unit, price_per_unit, received_date, status, created_at")\
        .order("created_at", desc=True)\
        .execute()

    if not response.data:
        st.info("📭 Belum ada data stok kayu.")
        return

    # Konversi data ke DataFrame
    df = pd.DataFrame(response.data)

    # Mengurai JSON object dari kolom wood_types dan suppliers
    df["Nama Kayu"] = df["wood_types"].apply(lambda x: x["wood_name"] if isinstance(x, dict) else None)
    df["Kategori"] = df["wood_types"].apply(lambda x: x["category"] if isinstance(x, dict) else None)
    df["Nama Supplier"] = df["suppliers"].apply(lambda x: x["name"] if isinstance(x, dict) else None)

    # Rename kolom agar lebih user-friendly
    df = df.rename(columns={
        "id": "ID Stok",
        "quantity": "Jumlah",
        "unit": "Satuan",
        "price_per_unit": "Harga per Unit",
        "received_date": "Tanggal Diterima",
        "status": "Status",
        "created_at": "Tanggal Ditambahkan"
    })

    # Format tanggal agar lebih mudah dibaca
    df["Tanggal Diterima"] = pd.to_datetime(df["Tanggal Diterima"], format='mixed', errors='coerce').dt.strftime("%d %B %Y")
    df["Tanggal Ditambahkan"] = pd.to_datetime(df["Tanggal Ditambahkan"], format='mixed', errors='coerce').dt.strftime("%d %B %Y - %H:%M")

    # Hapus kolom JSON yang sudah diurai
    df.drop(columns=["wood_types", "suppliers"], inplace=True)

    # Set ID sebagai index
    df.set_index("ID Stok", inplace=True)

    # Filter status stok
    status_filter = st.selectbox("🔍 Filter Status", ["Semua", "Available", "Reserved", "Sold"], key="status_filter")
    if status_filter != "Semua":
        df = df[df["Status"] == status_filter]

    if df.empty:
        st.info("📭 Tidak ada stok dengan status tersebut.")
        return

    # Tampilkan tabel dengan styling
    st.dataframe(
        df.style.format({
            "Harga per Unit": "Rp {:,.2f}".format
        }).background_gradient(cmap="Blues", subset=["Jumlah"]),
        use_container_width=True
    )

    # Tambahkan tombol edit untuk setiap baris
    for index, row in df.iterrows():
        if st.button(f"✏️ Edit Stok ID: {index}", key=f"edit_button_{index}"):
            with st.container():
                st.write(f"### 🛠️ Edit Detail Stok ID: {index}")
                with st.form(f"edit_form_{index}"):
                    new_quantity = st.number_input("Jumlah", value=row["Jumlah"], min_value=0, step=1, key=f"quantity_{index}")
                    new_unit = st.text_input("Satuan", value=row["Satuan"], key=f"unit_{index}")
                    new_price_per_unit = st.number_input("Harga per Unit", value=row["Harga per Unit"], min_value=0.0, step=0.01, key=f"price_{index}")
                    new_status = st.selectbox("Status", ["Available", "Reserved", "Sold"], index=["Available", "Reserved", "Sold"].index(row["Status"]), key=f"status_{index}")
                    submitted = st.form_submit_button("💾 Simpan Perubahan")

                    if submitted:
                        try:
                            # Update data di Supabase
                            supabase.table("warehouse_stock").update({
                                "quantity": new_quantity,
                                "unit": new_unit,
                                "price_per_unit": new_price_per_unit,
                                "status": new_status
                            }).eq("id", index).execute()
                            st.success(f"✅ Stok ID {index} berhasil diperbarui!")
                            st.experimental_rerun()  # Refresh halaman
                        except Exception as e:
                            st.error(f"❌ Terjadi kesalahan: {e}")

def tampilkan_orders():
    st.subheader("📦 Daftar Pesanan (Orders)")

    # Query untuk mengambil semua orders dengan customer
    response = supabase.table("orders")\
        .select("id, customer_id, order_date, total_price, status, created_at")\
        .order("created_at", desc=True)\
        .execute()

    if not response.data:
        st.info("📭 Belum ada data pesanan.")
        return

    # Konversi ke DataFrame
    df = pd.DataFrame(response.data)

    # Rename kolom agar lebih user-friendly
    df = df.rename(columns={
        "id": "ID Order",
        "customer_id": "ID Customer",
        "order_date": "Tanggal Order",
        "total_price": "Total Harga",
        "status": "Status",
        "created_at": "Tanggal Ditambahkan"
    })

    # Format tanggal
    df["Tanggal Order"] = pd.to_datetime(df["Tanggal Order"], format='mixed', errors='coerce').dt.strftime("%d %B %Y")
    df["Tanggal Ditambahkan"] = pd.to_datetime(df["Tanggal Ditambahkan"], format='mixed', errors='coerce').dt.strftime("%d %B %Y - %H:%M")

    df.set_index("ID Order", inplace=True)
    # Filter status order
    status_filter = st.selectbox("Filter Status Order", ["Semua", "Pending", "Paid", "Shipped", "Completed", "Cancelled"])
    if status_filter != "Semua":
        df = df[df["Status"] == status_filter]

    if df.empty:
        st.info("📭 Tidak ada pesanan dengan status tersebut.")
        return

    # Tampilkan tabel
    st.dataframe(df, use_container_width=True)

def tampilkan_pembayaran():
    st.subheader("💳 Daftar Pembayaran")

    # Query untuk mengambil data pembayaran
    response = supabase.table("payments")\
        .select("id, order_id, payment_method, amount, payment_status, payment_date")\
        .order("payment_date", desc=True)\
        .execute()

    if not response.data:
        st.info("📭 Belum ada data pembayaran.")
        return

    # Konversi ke DataFrame
    df = pd.DataFrame(response.data)

    # Rename kolom agar lebih user-friendly
    df = df.rename(columns={
        "id": "ID Pembayaran",
        "order_id": "ID Order",
        "payment_method": "Metode Pembayaran",
        "amount": "Jumlah",
        "payment_status": "Status Pembayaran",
        "payment_date": "Tanggal Pembayaran"
    })

    # Format tanggal
    df["Tanggal Pembayaran"] = pd.to_datetime(df["Tanggal Pembayaran"]).dt.strftime("%d %B %Y - %H:%M")
    df.set_index("ID Pembayaran", inplace=True)
    # Filter status pembayaran
    status_filter = st.selectbox("Filter Status Pembayaran", ["Semua", "Pending", "Completed", "Failed"])
    if status_filter != "Semua":
        df = df[df["Status Pembayaran"] == status_filter]

    if df.empty:
        st.info("📭 Tidak ada pembayaran dengan status tersebut.")
        return

    # Tampilkan tabel
    st.dataframe(df, use_container_width=True)

def tampilkan_pengiriman():
    st.subheader("🚚 Daftar Pengiriman")

    # Query untuk mengambil data shipments
    response = supabase.table("shipments")\
        .select("id, order_id, tracking_number, shipping_company, estimated_delivery, status, created_at")\
        .order("created_at", desc=True)\
        .execute()

    if not response.data:
        st.info("📭 Belum ada data pengiriman.")
        return

    # Konversi ke DataFrame
    df = pd.DataFrame(response.data)

    # Rename kolom agar lebih user-friendly
    df = df.rename(columns={
        "id": "ID Pengiriman",
        "order_id": "ID Order",
        "tracking_number": "No. Resi",
        "shipping_company": "Perusahaan Pengiriman",
        "estimated_delivery": "Estimasi Tiba",
        "status": "Status",
        "created_at": "Tanggal Ditambahkan"
    })

    # Format tanggal
    df["Estimasi Tiba"] = pd.to_datetime(df["Estimasi Tiba"]).dt.strftime("%d %B %Y")
    df["Tanggal Ditambahkan"] = pd.to_datetime(df["Tanggal Ditambahkan"]).dt.strftime("%d %B %Y - %H:%M")
    df.set_index("ID Pengiriman", inplace=True)
    # Filter status pengiriman
    status_filter = st.selectbox("Filter Status Pengiriman", ["Semua", "In Transit", "Delivered", "Failed"])
    if status_filter != "Semua":
        df = df[df["Status"] == status_filter]

    if df.empty:
        st.info("📭 Tidak ada pengiriman dengan status tersebut.")
        return

    # Tampilkan tabel
    st.dataframe(df, use_container_width=True)

def get_category_quantity():
    # Query ke Supabase untuk mendapatkan total quantity berdasarkan kategori kayu
    response = supabase.table("warehouse_stock")\
        .select("wood_type_id, quantity")\
        .execute()
    
    # Jika tidak ada data, kembalikan DataFrame kosong
    if not response.data:
        return pd.DataFrame(columns=["category", "total_quantity"])

    # Konversi hasil ke DataFrame
    df_stock = pd.DataFrame(response.data)

    # Query untuk mendapatkan kategori kayu dari wood_types
    response_types = supabase.table("wood_types")\
        .select("id, category")\
        .execute()
    
    if not response_types.data:
        return pd.DataFrame(columns=["category", "total_quantity"])

    df_types = pd.DataFrame(response_types.data)

    # Gabungkan kedua DataFrame berdasarkan wood_type_id
    df_merged = df_stock.merge(df_types, left_on="wood_type_id", right_on="id", how="left")

    # Hitung total quantity berdasarkan kategori kayu
    df_result = df_merged.groupby("category")["quantity"].sum().reset_index()
    df_result = df_result.rename(columns={"quantity": "total_quantity"})

    return df_result

# Fungsi untuk menampilkan diagram batang
def tampilkan_grafik_stok():
    st.subheader("📊 Inventory Visualization")

    # Ambil data dari Supabase
    df = get_category_quantity()

    if df.empty:
        st.warning("⚠️ No wood stock data available.")
        return

    # Create tabs for different visualization options
    tab1, tab2 = st.tabs(["📊 Bar Chart", "🥧 Pie Chart"])
    
    with tab1:
        # Use a more modern color palette
        colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
        
        # Create Bar Chart with enhanced styling
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(
            df["category"], 
            df["total_quantity"], 
            color=colors[:len(df)],
            width=0.6,
            edgecolor='white',
            linewidth=1,
            alpha=0.8
        )
        
        # Add data labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2., 
                height + 0.1,
                f'{int(height)}',
                ha='center', 
                va='bottom',
                fontweight='bold'
            )

        # Enhanced styling
        ax.set_xlabel("Wood Category", fontsize=12, fontweight='bold')
        ax.set_ylabel("Total Quantity", fontsize=12, fontweight='bold')
        ax.set_title("Warehouse Stock by Category", fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(df["category"])))
        ax.set_xticklabels(df["category"], rotation=30)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add background color
        fig.patch.set_facecolor('#f5f5f5')
        ax.set_facecolor('#f5f5f5')
        
        plt.tight_layout()
        
        # Display chart
        st.pyplot(fig)
        
        # Add insights section
        if len(df) > 0:
            total_stock = df["total_quantity"].sum()
            max_category = df.loc[df["total_quantity"].idxmax(), "category"]
            
            st.markdown(f"""
            ### 📈 Inventory Insights
            - **Total stock**: {int(total_stock)} units
            - **Highest inventory**: {max_category} ({int(df["total_quantity"].max())} units)
            - **Categories**: {len(df)} wood types
            """)
    
    with tab2:
        # Create Pie Chart for percentage distribution
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Calculate percentages
        df['percentage'] = df['total_quantity'] / df['total_quantity'].sum() * 100
        
        # Create pie chart with enhanced styling
        wedges, texts, autotexts = ax.pie(
            df['total_quantity'], 
            labels=df['category'],
            autopct='%1.1f%%',
            startangle=90,
            shadow=False,
            colors=colors[:len(df)],
            wedgeprops={'edgecolor': 'white', 'linewidth': 2, 'antialiased': True},
            textprops={'fontsize': 12, 'fontweight': 'bold'}
        )
        
        # Style the percentage texts
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
            
        ax.set_title('Stock Distribution by Category', fontsize=14, fontweight='bold')
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        plt.tight_layout()
        
        # Display pie chart
        st.pyplot(fig)
        
        # Display data table with percentages
        st.markdown("#### Detailed Breakdown")
        display_df = df[['category', 'total_quantity', 'percentage']].copy()
        display_df.columns = ['Category', 'Quantity', 'Percentage (%)']
        display_df['Percentage (%)'] = display_df['Percentage (%)'].round(1)
        
        st.dataframe(
            display_df.style.background_gradient(cmap='Blues', subset=['Quantity']),
            use_container_width=True
        )

# Main CRUD Disini sesuaikan loginnya admin atau customers
def tambah_supplier():
    st.subheader("➕ Tambah Supplier")

    # Form input data
    with st.form("form_tambah_supplier", clear_on_submit=True):
        name = st.text_input("Nama Supplier", placeholder="Masukan Nama PT Supplier")
        contact_person = st.text_input("Contact Person", placeholder="Masukan Nama Owner")
        phone = st.text_input("Nomor Telepon", placeholder="Masukan Nomor Telepon")
        email = st.text_input("Email", placeholder="Masukan Email")
        address = st.text_area("Alamat", placeholder="Masukan Alamat")

        submitted = st.form_submit_button("Tambah Supplier")
        if submitted:
            if not name:
                st.warning("⚠️ Nama Supplier wajib diisi!")
            else:
                # Data yang akan disimpan ke Supabase
                data = {
                    "name": name,
                    "contact_person": contact_person,
                    "phone": phone,
                    "email": email,
                    "address": address
                }

                # Kirim data ke Supabase
                try:
                    response = supabase.table("suppliers").insert(data).execute()
                    if response:
                        st.success(f"✅ Supplier **{name}** berhasil ditambahkan!")
                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan: {e}")

def tambah_kayu():
    st.subheader("🌲 Tambah Data Kayu")

    # Form input
    with st.form("form_tambah_kayu"):
        wood_name = st.text_input("Nama Kayu", placeholder="Contoh: Merbau Type 0566")
        category = st.selectbox("Kategori", ["Hardwood", "Softwood", "Plywood", "Others"])
        description = st.text_area("Deskripsi", placeholder="Kayu Kualiatas : A/B/C")

        # Tombol submit
        submit_button = st.form_submit_button("Tambah Kayu")

        if submit_button:
            # Validasi input
            if not wood_name.strip():
                st.warning("⚠️ Nama kayu tidak boleh kosong.")
                return
            
            # Proses insert data
            data = {
                "wood_name": wood_name,
                "category": category,
                "description": description
            }

            try:
                response = supabase.table("wood_types").insert(data).execute()
                if response.data:
                    st.success(f"✅ Kayu **{wood_name}** berhasil ditambahkan!")
                else:
                    st.error("❌ Gagal menambahkan data kayu.")
            except Exception as e:
                st.error(f"🚨 Terjadi kesalahan: {e}")

def get_wood_types():
    response = supabase.table('wood_types').select("id, wood_name").execute()
    return {item['wood_name']: item['id'] for item in response.data}

def get_suppliers():
    response = supabase.table('suppliers').select("id, name").execute()
    return {item['name']: item['id'] for item in response.data}

def add_warehouse_stock(data):
    try:
        supabase.table('warehouse_stock').insert(data).execute()
        st.success(f"Stok berhasil ditambahkan!")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")


def warehouse_stock_form():
    st.title("📦 Tambah Stok Gudang")

    wood_types = get_wood_types()
    suppliers = get_suppliers()

    # Pencarian untuk Jenis Kayu
    wood_search = st.text_input("🔍 Cari Jenis Kayu").strip().lower()
    filtered_wood_types = {k: v for k, v in wood_types.items() if wood_search in k.lower()}

    # Pencarian untuk Supplier
    supplier_search = st.text_input("🔍 Cari Supplier").strip().lower()
    filtered_suppliers = {k: v for k, v in suppliers.items() if supplier_search in k.lower()}

    with st.form("warehouse_stock_form"):
        wood_type_id = st.selectbox("Jenis Kayu", list(filtered_wood_types.keys()) if filtered_wood_types else ["Tidak ditemukan"])
        supplier_id = st.selectbox("Supplier", list(filtered_suppliers.keys()) if filtered_suppliers else ["Tidak ditemukan"])

        quantity = st.number_input("Kuantitas", min_value=1, step=1)
        unit = st.text_input("Satuan", placeholder="Contoh: meter, kg, liter")
        price_per_unit = st.number_input("Harga per Unit", min_value=0.0, step=0.01)
        received_date = st.date_input("Tanggal Diterima")
        status = st.selectbox("Status", ["Available", "Reserved", "Sold"])
        submit_button = st.form_submit_button("Tambah Stok")

        if submit_button:
            if wood_type_id != "Tidak ditemukan" and supplier_id != "Tidak ditemukan":
                data = {
                    "wood_type_id": wood_types[wood_type_id],
                    "supplier_id": suppliers[supplier_id],
                    "quantity": quantity,
                    "unit": unit,
                    "price_per_unit": price_per_unit,
                    "received_date": received_date.strftime("%Y-%m-%d"),
                    "status": status
                }
                add_warehouse_stock(data)
                st.success("✅ Stok berhasil ditambahkan!")
            else:
                st.error("❌ Jenis kayu atau supplier tidak valid.")

# Fungsi mendapatkan data order (dengan pagination untuk data besar)
def get_orders():
    # Simulasi data order dari database dengan lebih dari 1000 data
    response = supabase.table('orders').select("id").execute()
    return {item['id']: item['id'] for item in response.data}

def add_shipment(data):
    try:
        # Insert data into the "shipments" table
        response = supabase.table("shipments").insert(data).execute()
        if response.data:
            st.success(f"✅ Data berhasil ditambahkan: {data}")
        else:
            st.error("❌ Gagal menambahkan data ke database.")
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan: {e}")

def shipment_form():
    st.title("🚚 Tambah Pengiriman")

    orders = get_orders()

    with st.form("shipment_form"):
        order_id = st.selectbox(
            "Order ID", 
            list(orders.keys()), 
            index=0, 
            format_func=lambda x: x, 
            placeholder="Cari Order ID..."
        )
        # Generate tracking number dynamically based on selected order ID
        tracking_number = st.text_input("Nomor Resi", value="TRK000", placeholder="Masukkan nomor resi")

        # Select shipping company from predefined options
        shipping_company = st.selectbox("Perusahaan Pengiriman", ["POS Indonesia", "JNE", "TIKI"])
        estimated_delivery = st.date_input("Perkiraan Tanggal Tiba")
        status = st.selectbox("Status", ["In Transit", "Delivered", "Failed"])
        submit_button = st.form_submit_button("Tambah Pengiriman")

        if submit_button:
            data = {
                "order_id": orders[order_id],
                "tracking_number": tracking_number,
                "shipping_company": shipping_company,
                "estimated_delivery": estimated_delivery.strftime("%Y-%m-%d"),
                "status": status
            }
            add_shipment(data)

# Fungsi untuk mendapatkan daftar kayu yang tersedia
def get_available_wood():
    response = supabase.table('warehouse_stock')\
        .select("id, wood_type_id, quantity, price_per_unit, wood_types(wood_name)")\
        .eq("status", "Available")\
        .execute()

    return {
        item['wood_types']['wood_name']: item for item in response.data
    }

# Fungsi untuk menambah pesanan
def add_order(data):
    response = supabase.table('orders').insert(data).execute()
    return response.data[0]['id']  # Ambil ID pesanan yang baru dibuat

# Fungsi untuk menambah detail pesanan
def add_order_details(data):
    supabase.table('order_details').insert(data).execute()

# Fungsi untuk memperbarui stok kayu
def update_stock(wood_id, new_quantity):
    supabase.table('warehouse_stock')\
        .update({"quantity": new_quantity})\
        .eq("id", wood_id)\
        .execute()

import streamlit as st
from datetime import date

def order_form():
    st.title("🛒 Tambah Pesanan")

    # Cek apakah pengguna sudah login
    customer_id = st.session_state["user"].get("id")
    if not customer_id:
        st.error("❌ Gagal mengambil data pelanggan.")
        return

    # Ambil data kayu dan simpan di session_state
    if "wood_options" not in st.session_state or st.button("🔄 Refresh Data"):
        st.session_state["wood_options"] = get_available_wood()

    wood_options = st.session_state["wood_options"]

    if "selected_wood" not in st.session_state:
        st.session_state["selected_wood"] = list(wood_options.keys())[0]

    with st.form("order_form"):
        order_date = st.date_input("Tanggal Pesanan", value=date.today())

        st.subheader("Detail Pesanan")
        selected_wood = st.selectbox(
            "Jenis Kayu",
            list(wood_options.keys()),
            index=list(wood_options.keys()).index(st.session_state["selected_wood"]),
            key="selected_wood"
        )

        # Ambil data stok dan harga sesuai pilihan
        selected_wood_data = wood_options[selected_wood]
        stock = selected_wood_data['quantity']
        unit_price = selected_wood_data['price_per_unit']

        st.write(f"📦 **Stok Tersedia:** {stock}")

        quantity = st.number_input("Kuantitas", min_value=1, max_value=stock, step=1)

        # **Hitung Total Harga Secara Otomatis**
        subtotal = quantity * unit_price
        st.write(f"💰 **Subtotal:** Rp{subtotal:,.2f}")

        # **Tampilkan Total Harga Otomatis**
        st.write(f"🛒 **Total Harga:** Rp{subtotal:,.2f}")

        submit_button = st.form_submit_button("Tambah Pesanan")
        refresh_button = st.form_submit_button("Refresh")

        if refresh_button:
            st.success("✅ Data telah diperbarui!")

        if submit_button:
            if quantity > stock:
                st.error("❌ Stok tidak mencukupi untuk pesanan ini.")
                return

            # **Simpan pesanan ke database**
            order_data = {
                "customer_id": customer_id,
                "order_date": order_date.strftime("%Y-%m-%d"),
                "total_price": subtotal,  # **Gunakan subtotal sebagai total harga**
                "status": "Pending"
            }
            order_id = add_order(order_data)

            order_detail_data = {
                "order_id": order_id,
                "wood_type_id": selected_wood_data['id'],
                "quantity": quantity,
                "unit_price": unit_price,
                "subtotal": subtotal
            }
            add_order_details(order_detail_data)

            # Update stok kayu
            new_stock = stock - quantity
            update_stock(selected_wood_data['id'], new_stock)

            st.success("✅ Pesanan berhasil ditambahkan!")

