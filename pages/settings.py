import streamlit as st
import pandas as pd
from services.kittings import fiscal_term_settings

"""
### 各種設定

"""
fiscal_end_date = st.date_input(label="今期の会計期首日", value=st.session_state['fiscal_start_date'], format="YYYY/MM/DD")
st.caption("今期の会計期首日を変更します。会計機能(仕訳検索・入力等)の期首日、期末日が変更されます。")

if st.button(label="設定"):
    try:
        st.session_state['fiscal_start_date'], st.session_state['fiscal_end_date'], st.session_state['fiscal_term'] = fiscal_term_settings(fiscal_end_date)
        st.toast("%s (%s - %s)" % (st.session_state['fiscal_term'], st.session_state['fiscal_start_date'].strftime("%Y-%m-%d"), st.session_state['fiscal_end_date'].strftime("%Y-%m-%d")))
        st.toast("会計期首日を更新しました。")
    except Exception as e:
        st.write(e)
