# FILE KONFIGURASI DATABASE
from supabase import create_client
import streamlit as st

SUPABASE_URL = "https://uxoderburyhwzippkbgo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV4b2RlcmJ1cnlod3ppcHBrYmdvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDAyMjIxMDcsImV4cCI6MjA1NTc5ODEwN30.emn097vXFUNiNJpUcmx_9CysNcNyg-FU8s02h_pHX74"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

