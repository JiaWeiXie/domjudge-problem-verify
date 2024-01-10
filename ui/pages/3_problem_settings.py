import re
import time
import streamlit as st
import yaml

from utils.file import get_or_create_file, save_file


st.set_page_config(page_title="題目設定", page_icon="ℹ️")
st.sidebar.header("題目設定")
st.title("題目設定")

init_yaml = yaml.dump({"name": ""}, allow_unicode=True)
init_time_limit = "timelimit='1'"
problem_yaml = get_or_create_file("problem.yaml", init_yaml)
domjudge_problem = get_or_create_file("domjudge-problem.ini", init_time_limit)

yaml_value = yaml.load(problem_yaml.encode(), Loader=yaml.FullLoader)
problem_name_default = yaml_value.get("name", "") if yaml_value else ""


time_limit_default = 1
if match := re.search(r"\d+", domjudge_problem):
    time_limit_default = int(match.group())

problem_name = st.text_input(
    "題目名稱",
    key="problem_name",
    value=problem_name_default,
    placeholder="請輸入題目名稱",
)
time_limit = st.number_input(
    "時間限制",
    key="time_limit",
    value=time_limit_default,
    min_value=1,
    format="%d",
)

if st.button("儲存"):
    problem_name_val = yaml.dump({"name": problem_name}, allow_unicode=True)
    time_limit_val = f"timelimit='{time_limit}'"
    with st.spinner("儲存成功"):
        save_file("", "problem.yaml", problem_name_val)
        save_file("", "domjudge-problem.ini", time_limit_val)
        time.sleep(1)
    st.rerun()
