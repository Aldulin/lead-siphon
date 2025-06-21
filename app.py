import streamlit as st
import pandas as pd
from scraper import scrape_gmaps
from email_extractor import extract_emails
import os

st.set_page_config(page_title="Lead Siphon", layout="centered")
st.title("🔍 Lead Siphon - Google Maps Scraper")

# Basic auth gate
PASSWORD = os.getenv("LEAD_SIPHON_PASSWORD", "demo123")
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    pw = st.text_input("Enter access password:", type="password")
    if pw == PASSWORD:
        st.session_state.auth = True
        st.experimental_rerun()
    else:
        st.stop()

# Tabs
tabs = st.tabs(["🗺️ Scrape GMaps", "📧 Email Extractor"])

# --- GMaps Scraper Tab ---
with tabs[0]:
    st.header("🗺️ Google Maps Lead Scraper")
    query = st.text_input("Business type (e.g. dentist)")
    city = st.text_input("City (e.g. Iasi)")
    max_results = st.slider("Max results", 10, 100, 30)

    if st.button("Scrape Leads"):
        with st.spinner("Scraping Google Maps..."):
            df = scrape_gmaps(f"{query} in {city}", max_results)
            if df.empty:
                st.error("No results found. Try again or check location/keyword.")
            else:
                st.success(f"Found {len(df)} leads")
                st.dataframe(df)
                df.to_csv("leads.csv", index=False)
                st.download_button("📥 Download CSV", data=df.to_csv(index=False), file_name="leads.csv")

# --- Email Extractor Tab ---
with tabs[1]:
    st.header("📧 Website Email Extractor")
    uploaded_file = st.file_uploader("Upload CSV with Website column", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if "Website" not in df.columns:
            st.error("CSV must contain a 'Website' column")
        else:
            with st.spinner("Extracting emails from websites..."):
                df = extract_emails(df)
                st.success("Done extracting emails")
                st.dataframe(df)
                st.download_button("📥 Download CSV with Emails", data=df.to_csv(index=False), file_name="leads_with_emails.csv")
