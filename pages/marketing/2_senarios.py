import datetime
import streamlit as st
from streamlit_modal import Modal
import pandas as pd
from constants import options

"""
### シナリオの作成と実行
"""

# style
st.markdown("""
    <style>
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)
