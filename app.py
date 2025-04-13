import streamlit as st
from supabase import create_client
from config import supabase     # import dari config.py
from datetime import datetime
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from streamlit_option_menu import option_menu
from auth import login, register, logout  # impoer dari auth.py
from function import lihat_pesanan,lihat_pesanan_detail,status_pembayaran,status_pengiriman,shipment_form,add_shipment,get_suppliers,tambah_supplier,update_stock,tampilkan_stok_gudang,tampilkan_supplier,warehouse_stock_form,add_warehouse_stock,tampilkan_grafik_stok,order_form,add_order,add_order_details,get_orders,tampilkan_orders,tampilkan_detail_pesanan,tambah_kayu,tampilkan_pembayaran,tampilkan_jenis_kayu,tampilkan_pengiriman,manajemen_user
# Custom theme and styling
st.set_page_config(
    page_title="Wood Warehouse Management",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css(file_name):
    with open(file_name, "r") as f:
        return f"<style>{f.read()}</style>"

st.markdown(load_css("style.css"), unsafe_allow_html=True)


# 📌 Dashboard
def dashboard():
    if "user" not in st.session_state:
        st.warning("⚠️ Silakan login terlebih dahulu.")
        return
    
    role = st.session_state["role"]
    user = st.session_state["user"]
    
    # Enhanced sidebar with user info card
    with st.sidebar:
        # User profile section
        with st.container():
            st.markdown(f"""
            <div style="padding: 10px; border-radius: 10px; background-color: rgba(255,255,255,0.1); margin-bottom: 20px">
                <h3 style="margin:0;">👋 Welcome, {user.get('name', user.get('email', 'User'))}</h3>
                <p style="opacity:0.8; margin:0; font-size:14px">{role}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Dashboard header with KPIs
    current_date = datetime.now().strftime("%d %B %Y")
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px">
        <h1 style="margin: 0;">🌲 Wood Warehouse Dashboard</h1>
        <p style="color: #888; margin: 0">{current_date}</p>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    if role == "Admin":
        # Admin dashboard with organized sections
        with st.sidebar:
            st.markdown("### 📌 Admin Navigation")            
            menu = st.radio("Pilih Menu", [
            # Inventory Monitoring
            "Stok Gudang", "Grafik Stock", "Jenis Kayu", "Daftar Supplier",
            # Data Input
            "Input Stock Gudang", "Input Jenis Kayu", "Input Supplier",
            # Order Processing
            "Orders", "Daftar Pembayaran", "Daftar Pengiriman", "Input Pengiriman",
            # Administration
            "Manajemen Pengguna"
        ])

       
        # Display content based on menu selection
        if menu == "Daftar Supplier":
            with st.container():
                tampilkan_supplier()
        elif menu == "Jenis Kayu":
            with st.container():
                tampilkan_jenis_kayu()
        elif menu == "Stok Gudang":
            with st.container():
                tampilkan_stok_gudang()
        elif menu == "Daftar Pengiriman":
            with st.container():
                tampilkan_pengiriman()
        elif menu == "Daftar Pembayaran":
            with st.container():
                tampilkan_pembayaran()
        elif menu == "Orders":
            with st.container():
                tampilkan_orders()
        elif menu == "Grafik Stock":
            col1, col2 = st.columns([2, 1])
            with col1:
                tampilkan_grafik_stok()
            with col2:
                # Quick stats card
                st.markdown("""
                <div style="padding: 20px; border-radius: 10px; background-color: #f0f2f6; margin-bottom: 20px">
                    <h4 style="margin-top:0">📈 Inventory Overview</h4>
                    <p style="color: #000000;">View your warehouse stock visualization and monitor inventory levels by category.</p>
                </div>
                """, unsafe_allow_html=True)
        elif menu == "Input Supplier":
            with st.container():
                tambah_supplier()
        elif menu == "Input Jenis Kayu":
            with st.container():
                tambah_kayu()
        elif menu == "Input Stock Gudang":
            with st.container():
                warehouse_stock_form()
        elif menu == "Input Pengiriman":
            with st.container():
                shipment_form()
        elif menu == "Manajemen Pengguna":
            with st.container():
                manajemen_user()
    else:  # Customer Dashboard
        # Enhanced customer sidebar navigation
        with st.sidebar:
            st.markdown("### 🛍️ Customer Navigation")
            selected = option_menu(
                menu_title=None,
                options=["Pesan Kayu", "Detail Pesanan", "Status Pesanan", "Status Pembayaran", "Status Pengiriman"],
                icons=["basket", "receipt", "list-check", "credit-card", "truck"],
                default_index=0,
            )
            menu = selected
        
        # Display customer dashboard based on selection
        if menu == "Pesan Kayu":
            # Add a nice intro card before the form
            st.markdown("""
            <div style="padding: 15px; border-radius: 10px; background: linear-gradient(to right, #4CAF50, #2E7D32); color: white; margin-bottom: 20px">
                <h2 style="margin:0">🌲 Order Wood Products</h2>
                <p>Select from our high-quality wood inventory and place your order</p>
            </div>
            """, unsafe_allow_html=True)
            order_form()

        elif menu == "Detail Pesanan":
            st.markdown("""
            <div style="padding: 15px; border-radius: 10px; background: linear-gradient(to right, #1976D2, #0D47A1); color: white; margin-bottom: 20px">
                <h2 style="margin:0">📋 Order Details</h2>
                <p>View the complete details of your orders</p>
            </div>
            """, unsafe_allow_html=True)
            lihat_pesanan_detail()   

        elif menu == "Status Pesanan":
            st.markdown("""
            <div style="padding: 15px; border-radius: 10px; background: linear-gradient(to right, #7B1FA2, #4A148C); color: white; margin-bottom: 20px">
                <h2 style="margin:0">📊 Order Status</h2>
                <p>Track the current status of your orders</p>
            </div>
            """, unsafe_allow_html=True)
            lihat_pesanan()
        
        elif menu == "Status Pembayaran":
            st.markdown("""
            <div style="padding: 15px; border-radius: 10px; background: linear-gradient(to right, #FF9800, #E65100); color: white; margin-bottom: 20px">
                <h2 style="margin:0">💳 Payment Status</h2>
                <p>Monitor your payment status and history</p>
            </div>
            """, unsafe_allow_html=True)
            status_pembayaran()
        
        elif menu == "Status Pengiriman":
            st.markdown("""
            <div style="padding: 15px; border-radius: 10px; background: linear-gradient(to right, #F44336, #B71C1C); color: white; margin-bottom: 20px">
                <h2 style="margin:0">🚚 Shipping Status</h2>
                <p>Track your shipments in real-time</p>
            </div>
            """, unsafe_allow_html=True)
            status_pengiriman()

    # Enhanced logout button
    with st.sidebar:
        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button("🚪 Logout", type="primary", use_container_width=True):
            logout()

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
