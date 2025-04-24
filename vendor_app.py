import streamlit as st
import pandas as pd
from io import BytesIO
import datetime

st.set_page_config(page_title="Vendor Submission Tool", layout="wide")
st.title("📦 OTM Vendor Submission Tool")

# --- Manual Entry ---
st.subheader("➕ Enter Material Details (Manual Option)")

material_numbers = st.text_input("Material Numbers (separated by comma)", help="Enter multiple material numbers separated by commas")
material_description = st.text_input("Material Description (applies to all if same)")
uom = st.selectbox("UL Base Unit of Measure", options=["EA", "PC", "KG", "LB", "G", "GAL", "L", "FT3", "M3", "IN3"])
packing_unit = st.selectbox("Packing Unit", options=["EA", "PC", "KG", "LB", "G", "GAL", "L", "FT3", "M3", "IN3"])
bun_per_pu = st.number_input("BUN per Packing Unit", min_value=0.0)
gross_weight = st.number_input("Gross Weight", min_value=0.0)
net_weight = st.number_input("Net Weight", min_value=0.0)
weight_unit = st.selectbox("Weight Unit", options=["KG", "LB", "G"])
length = st.number_input("Length (In)", min_value=0.0)
width = st.number_input("Width (In)", min_value=0.0)
height = st.number_input("Height (In)", min_value=0.0)
volume = length * width * height
volume_unit = "IN3"
pallet_units = st.number_input("Packing Units per Pallet", min_value=0)
pallet_unit = "Pallet"

manual_data = []

if material_numbers:
    materials = [m.strip() for m in material_numbers.split(",")]
    for m in materials:
        manual_data.append({
            "Material #": m,
            "Material Description": material_description,
            "UL Base Unit of Measure": uom,
            "Packing Unit": packing_unit,
            "BUN/Packing Unit (Unit)": bun_per_pu,
            "Gross Weight": gross_weight,
            "Net Weight": net_weight,
            "Weight Unit": weight_unit,
            "Length (In)": length,
            "Wide (In)": width,
            "Height (In)": height,
            "Volume OR populate (L-W-H)": volume,
            "Volume Unit": volume_unit,
            "Packing Units per Pallet": pallet_units,
            "Packing Units per Pallet (UOM)": pallet_unit,
            "CHECK": ""
        })

# --- File Upload ---
st.subheader("📤 Or Upload Material List File (Excel or CSV)")

uploaded_file = st.file_uploader("Upload XLSX or CSV", type=["xlsx", "csv"])

file_data = []
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine="openpyxl")

        file_data = df.to_dict(orient="records")
        st.success("File uploaded and parsed successfully.")
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

# --- Combine + Export ---
final_data = manual_data + file_data
if final_data:
    df_final = pd.DataFrame(final_data)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Vendor_Submission_{timestamp}.xlsx"

    def to_excel(dataframe):
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            dataframe.to_excel(writer, index=False, sheet_name="OTM Submission")
        return buffer.getvalue()

    st.download_button(
        label="📥 Download Purple Form Format",
        data=to_excel(df_final),
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
