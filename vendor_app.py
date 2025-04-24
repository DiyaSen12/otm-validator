import streamlit as st
import pandas as pd
from io import BytesIO

# Page config
st.set_page_config(page_title="Vendor Submission - OTM Validator", layout="wide")
st.title("📦 Vendor Submission Portal – OTM Validator")

# Unit dropdown options
weight_units = ["KG", "LB", "GM"]
dimension_units = ["CM", "MM", "IN"]

# Storage for entered materials
if "material_data" not in st.session_state:
    st.session_state["material_data"] = []

# Manual entry form
with st.expander("➕ Manual Entry (One Material at a Time)"):
    with st.form("manual_entry_form"):
        col1, col2, col3 = st.columns(3)
        material_number = col1.text_input("Material Number")
        description = col2.text_input("Material Description")
        base_uom = col3.selectbox("Base Unit of Measure", weight_units)

        col4, col5, col6 = st.columns(3)
        net_weight = col4.number_input("Net Weight", min_value=0.0, step=0.01)
        gross_weight = col5.number_input("Gross Weight", min_value=0.0, step=0.01)
        weight_unit = col6.selectbox("Weight Unit", weight_units)

        col7, col8, col9 = st.columns(3)
        length = col7.number_input("Length", min_value=0.0, step=0.1)
        width = col8.number_input("Width", min_value=0.0, step=0.1)
        height = col9.number_input("Height", min_value=0.0, step=0.1)

        dimension_unit = st.selectbox("Dimension Unit", dimension_units)

        submit = st.form_submit_button("Add Material")

        if submit:
            # Check required fields
            if not material_number or not description:
                st.warning("Material number and description are required.")
            elif net_weight > gross_weight:
                st.warning("Net weight cannot be greater than gross weight.")
            else:
                volume = length * width * height
                st.session_state["material_data"].append({
                    "Material Number": material_number,
                    "Description": description,
                    "Base UoM": base_uom,
                    "Net Weight": net_weight,
                    "Gross Weight": gross_weight,
                    "Weight Unit": weight_unit,
                    "Length": length,
                    "Width": width,
                    "Height": height,
                    "Dimension Unit": dimension_unit,
                    "Volume": volume
                })
                st.success("Material added!")

# Display current material list
if st.session_state["material_data"]:
    st.subheader("📋 Materials Entered")
    df = pd.DataFrame(st.session_state["material_data"])
    st.dataframe(df)

    def convert_df(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Vendor_Data')
        return output.getvalue()

    st.download_button(
        label="📥 Download Submission File",
        data=convert_df(df),
        file_name="Vendor_OTM_Submission.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Bulk upload section
with st.expander("📤 Bulk Upload via Excel/CSV"):
    uploaded_file = st.file_uploader("Upload Excel or CSV", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                bulk_df = pd.read_csv(uploaded_file)
            else:
                bulk_df = pd.read_excel(uploaded_file)

            # Expected columns
            required_cols = ["Material Number", "Description", "Base UoM",
                             "Net Weight", "Gross Weight", "Weight Unit",
                             "Length", "Width", "Height", "Dimension Unit"]

            if not all(col in bulk_df.columns for col in required_cols):
                st.error("Missing columns in file. Please check the template.")
            else:
                bulk_df["Volume"] = bulk_df["Length"] * bulk_df["Width"] * bulk_df["Height"]
                st.dataframe(bulk_df)

                st.download_button(
                    label="📥 Download Converted Bulk File",
                    data=convert_df(bulk_df),
                    file_name="OTM_Bulk_Submission.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except Exception as e:
            st.error(f"Error: {e}")
