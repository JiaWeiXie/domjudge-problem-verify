import os
import time
import streamlit as st

from streamlit_ace import st_ace

from utils.file import (
    list_folder,
    open_file,
    save_file,
    delete_file,
    create_folder,
    folder_exists,
    pair_files,
    get_next_filename,
)
from utils.text import normalization_text

st.set_page_config(page_title="測資編輯", page_icon="📝")
st.sidebar.header("測資編輯")
st.title("測資編輯")

with st.sidebar:
    if not folder_exists("data/sample"):
        st.button("新增範例測資", on_click=lambda: create_folder("data/sample"))
        
    if not folder_exists("data/secret"):
        st.button("新增隱藏測資", on_click=lambda: create_folder("data/secret"))


folder_option = st.selectbox("選擇測資類型", list_folder("data"))


def delete_testcase(*paths):
    with st.spinner("刪除成功"):
        for path in paths:
            delete_file(path)
        time.sleep(1)
    st.rerun()


if folder_option is not None:
    data_folder = os.path.join("data", folder_option)
    st.write(data_folder)
    files = list_folder(data_folder)

    testcases = dict()
    for infile, ansfile in pair_files(files):
        st.divider()
        input_col, ans_col = st.columns(2)
        indata = open_file(data_folder, infile)
        ansdata = open_file(data_folder, ansfile)
        inpath_name = f"{data_folder}/{infile}"
        anspath_name = f"{data_folder}/{ansfile}"
        height = int((len(indata.splitlines()) + 1) * 20)
        height = max(height, 200)
        with input_col:
            st.write(inpath_name)
            testcases[inpath_name] = st_ace(
                indata,
                height=height,
                key=inpath_name,
                auto_update=True,
            )
            st.button(
                "刪除測資",
                on_click=delete_testcase,
                args=(inpath_name, anspath_name),
                key=f"{infile}_{ansfile}",
            )
        with ans_col:
            st.write(anspath_name)
            testcases[anspath_name] = st_ace(
                ansdata,
                height=height,
                key=anspath_name,
                auto_update=True,
            )

    if st.button("儲存"):
        with st.spinner("儲存中"):
            for path_name, data in testcases.items():
                save_file("", path_name, normalization_text(data))
            time.sleep(1)

        st.success("儲存成功")

    in_f, ans_f = get_next_filename(files, data_folder)
    st.divider()
    st.markdown("## 新增測資")
    input_col, ans_col = st.columns(2)
    with input_col:
        st.write(in_f)
        in_data = st_ace(
            height=200,
            key=in_f,
            auto_update=True,
        )

    with ans_col:
        st.write(ans_f)
        ans_data = st_ace(
            height=200,
            key=ans_f,
            auto_update=True,
        )

    if st.button("新增"):
        with st.spinner("新增中"):
            save_file("", in_f, in_data)
            save_file("", ans_f, ans_data)
            time.sleep(1)
            st.success("新增成功")
        st.rerun()
