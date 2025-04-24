import streamlit as st
import pandas as pd
from conversion_logic import convert_units

st.set_page_config(page_title="Analyst Conversion Tool", layout="wide")

st.title("📊 OTM Analyst Validation Tool")
st.markdown("Convert units to SAP base and export validated records for reporting.")

# --- Upload Data ---
uploaded_file = st.file_uploader("📁 Upload vendor file (.xlsx or .csv)", type=["xlsx", "csv"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File uploaded successfully!")
        st.dataframe(df)

        # --- Analyst enters SAP base unit to validate against ---
        st.markdown("### 🔄 Select Target SAP Unit")
        base_unit = st.text_input("Enter SAP base unit for conversion (e.g., KG, L, CM)")

        if base_unit and "Value" in df.columns and "Unit" in df.columns:
            df["Converted to SAP Base"] = df.apply(
                lambda row: convert_units(row["Value"], row["Unit"], base_unit), axis=1
            )
            df["Validated SAP Unit"] = base_unit
            st.success("Validation and conversion successful!")
            st.dataframe(df)

            # --- Download Option ---
            st.markdown("### 📤 Download Final Validated File")
            final_excel = df.to_excel(index=False, engine="openpyxl")
            st.download_button(
                label="⬇️ Download Excel",
                data=final_excel,
                file_name="analyst_validated_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        elif base_unit:
            st.error("Missing required columns: 'Value' and 'Unit'.")

    except Exception as e:
        st.error(f"Error reading file: {e}")
