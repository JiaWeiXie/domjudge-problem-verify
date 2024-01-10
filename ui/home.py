# app.py
import zipfile
import streamlit as st

from pathlib import Path
from utils.file import get_tmp_folder, remove_tmp_folder

st.set_page_config(
    page_title="首頁",
    page_icon="👋",
)
st.sidebar.header("首頁")
st.title("出題助手")


def clear_state():
    remove_tmp_folder()
    st.session_state.clear()


st.sidebar.button("清除暫存資料", on_click=clear_state)

content = """
一些說明 .....
....
....
"""

st.write(content)


st.write("## 從現有題目開始")
uploaded_problem_zip = st.file_uploader("開啟題目 .zip 檔案", type="zip")

if uploaded_problem_zip is not None:
    file_name = str(uploaded_problem_zip.name).split(".")[0]
    st.write(file_name)
    # unzip files and folder to temp folder and save to session state
    tmp_folder = get_tmp_folder()
    uploaded_problem_zip.seek(0)
    with zipfile.ZipFile(uploaded_problem_zip, "r") as zip_ref:
        zip_ref.extractall(tmp_folder)

    st.session_state["problem_pdf"] = str(Path(tmp_folder) / "problem.pdf")
    st.session_state["file_name"] = file_name
