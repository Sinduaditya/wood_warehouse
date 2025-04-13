import streamlit as st
from datetime import datetime
from utils import hash_password, check_password
from supabase import create_client, Client
from config import supabase  


# 🌟 Function Login
def login():
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<h1 style='text-align: center;'>🔐 Welcome Back</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #6c757d;'>Login to access your Wood Warehouse account</p>", unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)
            
            user_type = st.radio("Select account type:", ("Customer", "Admin"), horizontal=True)
            email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            login_btn = st.button("🚪 Login", use_container_width=True)
            
            if login_btn:
                with st.spinner("Authenticating..."):
                    table_name = "admin" if user_type == "Admin" else "customers"
                    result = supabase.table(table_name).select("*").eq("email", email).execute()
                    
                    if result.data:
                        user = result.data[0]
                        if "password" not in user:
                            st.error("❌ Error: Password field not found in database!")
                            return

                        if check_password(password, user["password"]):
                            st.success(f"✅ Login successful as {user_type}")
                            st.session_state["user"] = user
                            st.session_state["role"] = user_type
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Incorrect password.")
                    else:
                        st.error("❌ Email not found. Please register.")
# 🌟 Function Register
def register():
    st.title("📝 Register Customer")
    name = st.text_input("Nama Perusahaan")
    contact_person = st.text_input("Nama Pemilik")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    phone = st.text_input("Nomor Telepon")
    address = st.text_area("Alamat")

    if st.button("Register"):
        hashed_password = hash_password(password)  
        data = {
            "name": name,
            "contact_person": contact_person,
            "phone": phone,
            "email": email,
            "address": address,  # Pastikan alamat juga dikirim jika diperlukan
            "created_at": datetime.now().isoformat(),
            "password": hashed_password
        }
        response = supabase.table("customers").insert(data).execute()

        if response.data:
            st.success("✅ Registrasi berhasil! Silakan login.")
            # st.write("Data yang akan dikirim:", data)
        else:
            st.error("❌ Registrasi gagal. Coba lagi.")
# 🚪 Logout Function
def logout():
    st.session_state.pop("user", None)
    st.session_state.pop("role", None)
    st.rerun()
