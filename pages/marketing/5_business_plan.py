import datetime
import streamlit as st
from streamlit_modal import Modal
import pandas as pd
from constants import options

"""
### 事業計画

当年度の月別、年間
- 当初計画
- 実績見込み
- 実績
- 当初計画との差異

年間の場合は、3カ年計画を表示

"""

# style
st.markdown("""
    <style>
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)
