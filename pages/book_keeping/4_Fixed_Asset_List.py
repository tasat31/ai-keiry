import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

"""
### 固定資産台帳
"""
st.write("会計期間: %s - %s" % (st.session_state['fiscal_start_date'].strftime("%Y-%m-%d"), st.session_state['fiscal_end_date'].strftime("%Y-%m-%d")))


# style
st.markdown("""
    <style>
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)
