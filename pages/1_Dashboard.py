import streamlit as st
from config import supabase

st.title("🏠 Dashboard")
st.write("Ringkasan Data Warehouse")

# Hitung jumlah data
total_suppliers = supabase.table("suppliers").select("*", count="exact").execute().count
total_customers = supabase.table("customers").select("*", count="exact").execute().count
total_orders = supabase.table("orders").select("*", count="exact").execute().count

st.metric(label="Total Suppliers", value=total_suppliers)
st.metric(label="Total Customers", value=total_customers)
st.metric(label="Total Orders", value=total_orders)
