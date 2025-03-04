import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO

st.set_page_config(page_title="Fancy File Converter", layout="wide")
st.title("Fancy File Converter & Cleaner")
st.write("Smart Data Transformer for cleaning and converting CSV & Excel files")

# Allow multiple file uploads
files = st.file_uploader("Upload your file(s)", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = Path(file.name).suffix.lower()

        if ext == ".csv":
            df = pd.read_csv(file)
        elif ext == ".xlsx":
            df = pd.read_excel(file, engine="openpyxl")
        else:
            st.error(f"Unsupported file format: {ext}")
            continue

        st.subheader(f"Preview: {file.name}")
        st.dataframe(df.head())

        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates Removed")
            st.dataframe(df.head())

        if st.checkbox(f"Clean Data - {file.name}"):
            df = df.fillna(df.select_dtypes(include=["number"]).mean())
            st.success('Missing values filled with means')
            st.dataframe(df.head())

        selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include=["number"]).empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        format_choice = st.radio(f"Convert {file.name} to:", ["csv", "Excel"], key=file.name)

        if st.button(f"Download {file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == "csv":
                df.to_csv(output, index=False)
                mime_type = "text/csv"
                new_name = file.name.replace(ext, ".csv")
            else:
                df.to_excel(output, index=False, engine='openpyxl')
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, ".xlsx")

            output.seek(0)
            st.download_button(
                label="Download File",
                data=output,
                file_name=new_name,
                mime=mime_type
            )
            st.success("Processing Complete!")