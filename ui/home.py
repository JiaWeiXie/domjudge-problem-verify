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
目前只能上傳 .zip 檔案，並且只能上傳一個檔案，請確認檔案內容為題目 PDF 檔案。\n
當前支援的功能有：\n
- 從現有 Domjudge 格式 zip 檔題目開始 \n
- 上傳題目 PDF 檔案 \n
- 上傳測資檔案 \n
- 編輯測資檔案 \n
- 新增驗證測資程式 \n
- 批次驗證測資 \n
- 儲存成 Domjudge 格式 zip 檔 \n
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
