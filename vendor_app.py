import streamlit as st
import pandas as pd
from conversion_logic import convert_units

st.set_page_config(page_title="Vendor Submission Tool", layout="wide")

st.title("📦 OTM Vendor Submission Tool")
st.markdown("Upload multiple materials and auto-convert to SAP base units with Excel-ready output.")

# --- Step 1: Upload Material Data ---
uploaded_file = st.file_uploader("📁 Upload your material Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File uploaded successfully!")
        st.dataframe(df)

        # --- Step 2: Enter SAP Base Unit for Each Material ---
        st.markdown("### 🧾 Enter SAP Base Unit of Measure (UoM) for Each Material")
        base_unit = st.text_input("Enter the SAP base unit (e.g., KG, L, CM)", max_chars=5)

        if base_unit:
            if "Unit" in df.columns and "Value" in df.columns:
                df["Converted to SAP Base Unit"] = df.apply(
                    lambda row: convert_units(row["Value"], row["Unit"], base_unit), axis=1
                )
                df["SAP Base Unit"] = base_unit
                st.success("Conversion complete!")
                st.dataframe(df)
            else:
                st.error("❗ The file must contain 'Value' and 'Unit' columns for conversion.")

            # --- Step 3: Export to Excel ---
            st.markdown("### 📤 Download Final Output")
            final_excel = df.to_excel(index=False, engine="openpyxl")
            st.download_button(
                label="⬇️ Download Excel",
                data=final_excel,
                file_name="converted_vendor_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Error processing file: {e}")
