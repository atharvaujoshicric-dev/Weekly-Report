import streamlit as st
import pandas as pd
from pptx import Presentation
import io

st.title("📊 BeyondWalls PPT Report Generator")

# Sidebar setup
st.sidebar.header("Template Setup")
template_file = st.sidebar.file_uploader("Upload your PPTX Template", type="pptx")

if template_file:
    # Everything related to data entry must stay inside this form block
    with st.form("data_entry_form"):
        st.subheader("Enter Weekly Metrics")
        
        col1, col2 = st.columns(2)
        with col1:
            proj = st.text_input("Project Name", value="Aishwaryam Abhimaan")
            leads = st.number_input("Total Leads", value=0)
            spends = st.number_input("Total Spends (with GST)", value=0)
        
        with col2:
            svc = st.number_input("Site Visits Conducted", value=0)
            bookings = st.number_input("Total Bookings", value=0)
            date_range = st.text_input("Date Range", value="1st - 7th Sept")

        # The REQUIRED submit button inside the form
        submitted = st.form_submit_button("Generate PPTX")

    # The logic to process the PPTX only runs AFTER 'submitted' is True
    if submitted:
        prs = Presentation(template_file)
        
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    # Use the same tags you put in your PPT template
                    if "{{PROJECT_NAME}}" in shape.text:
                        shape.text = shape.text.replace("{{PROJECT_NAME}}", proj)
                    if "{{TOTAL_LEADS}}" in shape.text:
                        shape.text = shape.text.replace("{{TOTAL_LEADS}}", str(leads))
                    if "{{TOTAL_SPENDS}}" in shape.text:
                        shape.text = shape.text.replace("{{TOTAL_SPENDS}}", str(spends))
                    if "{{DATE_RANGE}}" in shape.text:
                        shape.text = shape.text.replace("{{DATE_RANGE}}", date_range)
        
        # Save to buffer
        binary_output = io.BytesIO()
        prs.save(binary_output)
        
        st.success("✅ Report Prepared!")
        st.download_button(
            label="📩 Download Processed PPT Report",
            data=binary_output.getvalue(),
            file_name=f"{proj}_Weekly_Report.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
else:
    st.info("Please upload your template in the sidebar to start.")
