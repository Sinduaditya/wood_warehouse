import streamlit as st
from config import supabase

st.title("📦 Warehouse Stock Management")

with st.form("add_stock"):
    wood_type_id = st.number_input("Wood Type ID", min_value=1)
    supplier_id = st.number_input("Supplier ID", min_value=1)
    quantity = st.number_input("Quantity", min_value=1)
    unit = st.selectbox("Unit", ["m³", "pcs"])
    price_per_unit = st.number_input("Price per Unit", min_value=0.01)
    received_date = st.date_input("Received Date")
    status = st.selectbox("Status", ["Available", "Reserved", "Sold"])
    submit = st.form_submit_button("Tambah Stok")

    if submit:
        data = {
            "wood_type_id": wood_type_id,
            "supplier_id": supplier_id,
            "quantity": quantity,
            "unit": unit,
            "price_per_unit": price_per_unit,
            "received_date": str(received_date),
            "status": status
        }
        supabase.table("warehouse_stock").insert(data).execute()
        st.success("Stok berhasil ditambahkan!")

stocks = supabase.table("warehouse_stock").select("*").execute()
st.write("### Daftar Stok Gudang")
st.table(stocks.data)
