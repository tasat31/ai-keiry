import streamlit as st
import pandas as pd
import datetime
import calendar
from services.trial_balance import output

"""
### 合計残高試算表
"""
st.write("会計期間: %s - %s" % (st.session_state['fiscal_start_date'].strftime("%Y-%m-%d"), st.session_state['fiscal_end_date'].strftime("%Y-%m-%d")))

col1, col2, col3, col4 = st.columns(4)

with col1:
    entried_at_from = st.date_input("計上日カラ",  value=st.session_state['fiscal_start_date'])

with col2:
    current_date =  datetime.date.today()
    last_day = calendar.monthrange(current_date.year, current_date.month)[1]
    entried_at_to = st.date_input("計上日マデ", value=st.session_state['fiscal_end_date'])

with col3:
    pass

with col4:
    pass

sheet = []
for data in output(entried_at_from=entried_at_from, entried_at_to=entried_at_to):
    sheet.append({
        "No": data.display_seq,
        "勘定科目":data.name,
        "項目": data.caption,
        "前期末残高": "",
        "借方": data.credit_actual_total_amount,
        "貸方": data.debit_actual_total_amount,
        "残高": data.balance_actual_amount,
        "借方(予測)": data.credit_predict_total_amount,
        "貸方(予測)": data.debit_predict_total_amount,
        "残高(予測)": data.balance_predict_amount,
        "借方(実績+予測)": data.credit_actual_predict_total_amount,
        "貸方(実績+予測)": data.debit_actual_predict_total_amount,
        "残高(実績+予測)": data.balance_actual_predict_amount,
        # data.credit_actual_total_tax,
        # data.debit_actual_total_tax,
        # data.balance_actual_tax,
        # data.credit_predict_total_tax,
        # data.debit_predict_total_tax,
        # data.balance_predict_tax,
        # data.credit_actual_predict_total_tax,
        # data.debit_actual_predict_total_tax,
        # data.balance_actual_predict_tax
    })

st.dataframe(
    pd.DataFrame(sheet),
    width=800,
    height=600,
    hide_index=True,
)


# style
st.markdown("""
    <style>
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)
