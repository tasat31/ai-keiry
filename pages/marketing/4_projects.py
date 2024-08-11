import datetime
import streamlit as st
from streamlit_modal import Modal
import pandas as pd
from constants import options

"""
### プロジェクト一覧
"""
open_modal = st.button("プロジェクト追加", key="projects-add")

modal = Modal(
    "プロジェクト追加", 
    key="add-project",
    
    # Optional
    padding=20,    # default value
    max_width=744  # default value
)

if open_modal:
    modal.open()

if modal.is_open():
    with modal.container():
        segment =  st.selectbox(
            label="セグメント",
            options=options.segments,
            key="segment"
        )

        title = st.text_input("タイトル", key="projects-title")

        description = st.text_input("説明", key="projects-description")

        loanched_at = st.date_input("開始日", datetime.date.today(), key="projects-loanched_at")

        partner = st.text_input("取引先", key="projects-partner")

        if st.button("追加"):
            modal.close()

# style
st.markdown("""
    <style>
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)
