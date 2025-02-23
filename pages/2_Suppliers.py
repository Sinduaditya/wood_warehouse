import streamlit as st
from config import supabase

st.title("🏢 Supplier Management")

# Tambah supplier
with st.form("add_supplier"):
    name = st.text_input("Nama Supplier")
    contact_person = st.text_input("Contact Person")
    phone = st.text_input("Nomor Telepon")
    email = st.text_input("Email")
    address = st.text_area("Alamat")
    submit = st.form_submit_button("Tambah Supplier")

    if submit:
        data = {
            "name": name,
            "contact_person": contact_person,
            "phone": phone,
            "email": email,
            "address": address
        }
        supabase.table("suppliers").insert(data).execute()
        st.success("Supplier berhasil ditambahkan!")

# Search supplier by name
search_query = st.text_input("Cari Supplier", "")

# Pagination
page = st.number_input("Page", min_value=1, step=1, value=1)
page_size = 10
start = (page - 1) * page_size
# Fetch suppliers with search and pagination
if search_query:
    all_suppliers = supabase.table("suppliers").select("*").ilike("name", f"%{search_query}%").execute()
    suppliers = all_suppliers.data[start:start + page_size]
else:
    suppliers = supabase.table("suppliers").select("*").range(start, start + page_size - 1).execute().data

st.write("### Daftar Supplier")
st.table(suppliers)
