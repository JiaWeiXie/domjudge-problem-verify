import base64
import streamlit as st

from utils.file import save_pdf, open_pdf


st.set_page_config(page_title="題目預覽", page_icon="📄")
st.sidebar.header("題目預覽")

problem_pdf = st.sidebar.file_uploader("上傳題目", type="pdf", help="請上傳題目 PDF 檔案")
redner_option = st.sidebar.radio("PDF 顯示方式", ["Embedded", "Iframe"])


def init_pdf(pdf_file):
    if pdf_file is not None:
        return pdf_file.read()

    if "problem_pdf" not in st.session_state:
        return None

    if st.session_state["problem_pdf"] is not None:
        return open_pdf(st.session_state["problem_pdf"])
    return None


def display_pdf(file_bytes, pdf_redner):
    base64_pdf = base64.b64encode(file_bytes).decode("utf-8")

    if pdf_redner == "Iframe":
        pdf_display = f"""
        <iframe src="data:application/pdf;base64,{base64_pdf}" 
        width="700" height="1000" 
        type="application/pdf"></iframe>
        """
    else:
        pdf_display = f"""<embed
        class="pdfobject"
        type="application/pdf"
        title="Embedded PDF"
        src="data:application/pdf;base64,{base64_pdf}"
        style="overflow: auto; width: 100%; height: 90vh;">
        """
    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


if pdf := init_pdf(problem_pdf):
    save_pdf(pdf)
    display_pdf(pdf, redner_option)
