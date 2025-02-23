import streamlit as st
from config import supabase

st.title("👥 Customer Management")

with st.form("add_customer"):
    name = st.text_input("Nama Customer")
    contact_person = st.text_input("Contact Person")
    phone = st.text_input("Nomor Telepon")
    email = st.text_input("Email")
    address = st.text_area("Alamat")
    submit = st.form_submit_button("Tambah Customer")

    if submit:
        data = {
            "name": name,
            "contact_person": contact_person,
            "phone": phone,
            "email": email,
            "address": address
        }
        supabase.table("customers").insert(data).execute()
        st.success("Customer berhasil ditambahkan!")

customers = supabase.table("customers").select("*").execute()
st.write("### Daftar Customers")
st.table(customers.data)
