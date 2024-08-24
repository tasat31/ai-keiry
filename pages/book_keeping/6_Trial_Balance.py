import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import datetime
import calendar
from services.trial_balance import output
from services.statements import delete_by_fiscal_term as delete_statements_by_fiscal_term
from services.statements import bulk_entry as statements_bulk_entry

"""
### 合計残高試算表
"""
st.write("会計期間: %s - %s" % (st.session_state['fiscal_start_date'].strftime("%Y-%m-%d"), st.session_state['fiscal_end_date'].strftime("%Y-%m-%d")))

col1, col2, col3, col4 = st.columns(4)

with col1:
    entried_at_from = st.date_input("計上日カラ",  value=st.session_state['fiscal_start_date'], disabled=True)

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
        "前期末残高": data.balance_actual_last_fiscal_year,
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

if st.button("財務諸表作成", type="primary"):
    df_sheet = pd.DataFrame(sheet)

    # 貸借対照表
    df_balance_sheet = df_sheet.query("項目 != '(7)損益'")[["勘定科目", "項目", "No", "残高"]]
    df_statment_balance_sheet = pd.concat([
        pd.DataFrame({"期首日": [ss.fiscal_start_date] * len(df_balance_sheet)}),
        pd.DataFrame({"期末日": [ss.fiscal_end_date] * len(df_balance_sheet)}),
        pd.DataFrame({"会計期": [ss.fiscal_term] * len(df_balance_sheet)}),
        pd.DataFrame({"書類名": ['貸借対照表'] * len(df_balance_sheet)}),
        df_balance_sheet,
    ], axis=1)

    # 損益計算書
    df_profit_and_loss_sheet = df_sheet.query("項目 == '(7)損益'")[["勘定科目", "項目", "No", "残高"]]
    df_profit_and_loss_sheet.reset_index(drop=True, inplace=True)

    df_statement_profit_and_loss_sheet = pd.concat([
        pd.DataFrame({"期首日": [ss.fiscal_start_date] * len(df_profit_and_loss_sheet)}),
        pd.DataFrame({"期末日": [ss.fiscal_end_date] * len(df_profit_and_loss_sheet)}),
        pd.DataFrame({"会計期": [ss.fiscal_term] * len(df_profit_and_loss_sheet)}),
        pd.DataFrame({"書類名": ['損益計算書'] * len(df_profit_and_loss_sheet)}),
        df_profit_and_loss_sheet,
    ], axis=1)

    try:
        delete_statements_by_fiscal_term(fiscal_term=ss.fiscal_term)

        msg_balance_sheet = statements_bulk_entry(df_statment_balance_sheet.to_csv().split('\n'))
        msg_profit_and_loss_sheet = statements_bulk_entry(df_statement_profit_and_loss_sheet.to_csv().split('\n'))

        st.toast("貸借対照表:" + msg_balance_sheet["message"])
        st.toast("損益計算書:" + msg_profit_and_loss_sheet["message"])
    except Exception as e:
        st.toast(e)

# style
st.markdown("""
    <style>
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)
