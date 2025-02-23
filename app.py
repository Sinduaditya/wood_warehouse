import streamlit as st
from supabase import create_client
import bcrypt
from config import supabase  
from datetime import datetime
import streamlit as st

hide_menu_style = """
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    </style>
"""

st.markdown(hide_menu_style, unsafe_allow_html=True)


# 🔑 Fungsi Hash & Verifikasi Password
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode("utf-8")

def check_password(password, hashed_password):
    try:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
    except Exception as e:
        st.error(f"⚠️ Error saat memverifikasi password: {e}")
        return False

# 🌟 Login Function
def login():
    st.title("🔐 Login Wood Warehouse")

    user_type = st.radio("Login sebagai:", ("Admin", "Customer"))
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if user_type == "Admin":
            result = supabase.table("admin").select("*").eq("email", email).execute()
        else:
            result = supabase.table("customers").select("*").eq("email", email).execute()
        
        if result.data:
            user = result.data[0]
            
            if "password" not in user:
                st.error("❌ Error: Tidak ada password di database!")
                return

            if check_password(password, user["password"]):
                st.success(f"✅ Login berhasil sebagai {user_type}")
                st.session_state["user"] = user
                st.session_state["role"] = user_type
                st.rerun()
            else:
                st.error("❌ Password salah")
        else:
            st.error("❌ Email tidak ditemukan")

# 🆕 Register Function (Customer)
def register():
    st.title("📝 Register Customer")
    name = st.text_input("Nama Perusahaan")
    contact_person = st.text_input("Nama Pemilik")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    phone = st.text_input("Nomor Telepon")
    address = st.text_area("Alamat")

    if st.button("Register"):
        hashed_password = hash_password(password)  # Simpan password dalam bentuk hash
        data = {
            "name": name,
            "contact_person": contact_person,
            "phone": phone,
            "email": email,
            "created_at": datetime.now().isoformat(),
            "password": hashed_password
        }
        response = supabase.table("customers").insert(data).execute()

        if response.data:
            st.success("✅ Registrasi berhasil! Silakan login.")
        else:
            st.error("❌ Registrasi gagal. Coba lagi.")

# 🚪 Logout Function
def logout():
    st.session_state.pop("user", None)
    st.session_state.pop("role", None)
    st.rerun()


# Main CRUD Disini sesuaikan loginnya admin atau customers
# 📌 Dashboard
def dashboard():
    if "user" not in st.session_state:
        st.warning("⚠️ Silakan login terlebih dahulu.")
        return
    
    role = st.session_state["role"]

    if role == "Admin":
        st.sidebar.title("📌 Admin Dashboard")
        menu = st.sidebar.radio("Menu", ["Kelola Stok", "Kelola Orders", "Kelola Pengguna"])
        
        if menu == "Kelola Stok":
            st.subheader("📦 Manajemen Stok Kayu")
            st.write("🚧 Fitur dalam pengembangan...")

        elif menu == "Kelola Orders":
            st.subheader("📜 Manajemen Pesanan")
            st.write("🚧 Fitur dalam pengembangan...")

        elif menu == "Kelola Pengguna":
            st.subheader("👤 Manajemen Pengguna")
            customers = supabase.table("customers").select("id, name, email").execute()
            if customers.data:
                st.table(customers.data)
            else:
                st.write("Tidak ada pengguna yang terdaftar.")

    else:
        st.sidebar.title("🛍️ Customer Dashboard")
        menu = st.sidebar.radio("Menu", ["Pesan Kayu", "Lihat Pesanan"])

        if menu == "Pesan Kayu":
            st.subheader("📥 Pesan Kayu Baru")
            st.write("🚧 Fitur dalam pengembangan...")

        elif menu == "Lihat Pesanan":
            st.subheader("📋 Riwayat Pesanan")
            st.write("🚧 Fitur dalam pengembangan...")

    # 🚪 Tombol Logout
    if st.sidebar.button("Logout ❌"):
        logout()
# END Main CRUD Disini sesuaikan loginnya admin atau customers

# 🎯 Main App
def main():
    st.sidebar.title("🌲 Wood Warehouse")

    if "user" in st.session_state:
        dashboard()
    else:
        menu = st.sidebar.radio("Navigasi", ["Login", "Register"])
        if menu == "Login":
            login()
        elif menu == "Register":
            register()

if __name__ == "__main__":
    main()
