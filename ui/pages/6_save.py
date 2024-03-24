import streamlit as st

from utils.file import create_zip_file


st.set_page_config(page_title="存檔", page_icon="🎉")
st.title("存檔")

st.subheader("題目資訊顯示")

file_name = ""
if "file_name" in st.session_state:
    file_name = st.session_state["file_name"] or "problem"
    file_name = st.text_input("壓縮檔名稱", value=file_name)
else:
    file_name = st.text_input("壓縮檔名稱")


if file_name and st.button("製作 .zip 檔案"):
    st.session_state["file_name"] = file_name
    download_file = create_zip_file(file_name)
    st.session_state["zip_file"] = download_file
    with open(download_file, "rb") as file:
        st.download_button(
            label="下載 .zip 檔案",
            data=file,
            file_name=f"{file_name}.zip",
            mime="application/zip",
        )
