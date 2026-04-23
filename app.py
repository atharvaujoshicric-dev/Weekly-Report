import streamlit as st
import pandas as pd
from datetime import datetime

# Page Config
st.set_page_config(page_title="BeyondWalls Weekly Reporting", layout="wide")

st.title("📊 Weekly Reporting Dashboard")
st.subheader("Generate Mandate Project Reports")

# Sidebar for Template Selection
report_type = st.sidebar.selectbox(
    "Select Report Template",
    ["CP Aggregator Weekly", "Pre-Sales Review", "Weekly Project Review"]
)

# Shared Header Info
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        project_name = st.text_input("Project Name", value="Aishwaryam Abhimaan")
    with col2:
        report_date = st.date_input("Reporting Week Ending", datetime.now())

st.divider()

# --- TEMPLATE 1: CP AGGREGATOR WEEKLY ---
if report_type == "CP Aggregator Weekly":
    st.header("Channel Partner Performance")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Total Spends (Incl. GST)", st.number_input("Spends", value=0))
        st.metric("Total Leads", st.number_input("Leads", value=0))
    with col_b:
        st.metric("Qualified Leads", st.number_input("Qualified", value=0))
        st.metric("CP Visits", st.number_input("CP SVC", value=0))
    with col_c:
        st.metric("Total Bookings", st.number_input("Bookings", value=0))
        st.metric("CPL", st.number_input("Cost Per Lead", value=0))

    st.subheader("Top Performing CPs")
    cp_data = st.data_editor(pd.DataFrame({
        "CP Firm": ["Discounted Homes", "Enquiry Page"],
        "Visits": [0, 0],
        "Bookings": [0, 0]
    }), num_rows="dynamic")

# --- TEMPLATE 2: PRE-SALES REVIEW ---
elif report_type == "Pre-Sales Review":
    st.header("Pre-Sales Funnel Analysis")
    
    col_ps1, col_ps2 = st.columns(2)
    with col_ps1:
        attempts = st.number_input("Avg Daily Call Attempts (Target: 200)", value=0)
        scheduled = st.number_input("Visits Scheduled", value=0)
    with col_ps2:
        conducted = st.number_input("Visits Conducted", value=0)
        ratio = st.number_input("Lead to SVC Ratio (%)", value=0.0)

    st.subheader("Lead Unqualification Reasons")
    unqual_reasons = st.multiselect("Select Major Reasons", 
        ["Low Budget", "Location Mismatch", "Possession Date Mismatch", "Not Interested", "Postponed"])
    st.text_area("Inferences & Remarks")

# --- TEMPLATE 3: WEEKLY PROJECT REVIEW ---
elif report_type == "Weekly Project Review":
    st.header("Overall Project Health")
    
    tab1, tab2 = st.tabs(["Inventory Status", "Marketing Costs"])
    
    with tab1:
        st.write("Live Inventory Overview")
        st.data_editor(pd.DataFrame({
            "Unit Type": ["1 BHK", "2 BHK", "3 BHK"],
            "Total": [0, 0, 0],
            "Sold": [0, 0, 0],
            "Pending Agreement": [0, 0, 0]
        }))

    with tab2:
        st.number_input("Lifetime Marketing Cost", value=25023100)
        st.number_input("Current Ad Cost %", value=1.21)

# --- SCREENSHOT UPLOADER ---
st.divider()
st.subheader("📸 Report Screenshots")
uploaded_files = st.file_uploader("Upload Call Logs, Visit Lineups, or CRM Screenshots", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.image(uploaded_file, caption=uploaded_file.name, width=400)

# --- DOWNLOADER ---
st.divider()
if st.button("Generate Final Report Summary"):
    # Create a simple text-based summary for now
    summary = f"REPORT: {report_type}\nPROJECT: {project_name}\nDATE: {report_date}\n"
    st.download_button("Download .txt Report", summary, file_name=f"{project_name}_Weekly.txt")
    st.success("Report generated! For full PPT automation, consider adding 'python-pptx' to your workflow.")
