import streamlit as st
from streamlit import session_state as ss
import pandas as pd
from services.statements import list as statements_list

"""
### 財務諸表
"""
balance_sheet_tab, profit_and_loss_tab, cashflow_tab = st.tabs(["貸借対照表", "損益計算書", "キャッシュフロー計算書",])

with balance_sheet_tab:
    st.write("%s (%s - %s)" % (ss.fiscal_term, ss.fiscal_start_date.strftime('%Y年%m月%d日'), ss.fiscal_end_date.strftime('%Y年%m月%d日')))
    balance_sheet = []
    for data in statements_list(fiscal_term=ss.fiscal_term, document_name="貸借対照表"):
        balance_sheet.append({
            "caption": data.item_caption,
            "item": data.item_name,
            "amount": data.amount,
            "display_seq": data.display_seq
        })

    df_balance_sheet = pd.DataFrame(balance_sheet)
    st.dataframe(df_balance_sheet, width=800)

with profit_and_loss_tab:
    st.write("%s (%s - %s)" % (ss.fiscal_term, ss.fiscal_start_date.strftime('%Y年%m月%d日'), ss.fiscal_end_date.strftime('%Y年%m月%d日')))
    profit_and_loss_sheet = []
    for data in statements_list(fiscal_term=ss.fiscal_term, document_name="損益計算書"):
        profit_and_loss_sheet.append({
            "caption": data.item_caption,
            "item": data.item_name,
            "amount": data.amount,
            "display_seq": data.display_seq
        })

    df_profit_and_loss_sheet = pd.DataFrame(profit_and_loss_sheet)
    st.dataframe(df_profit_and_loss_sheet, width=800)

with cashflow_tab:
    pass

# style
st.markdown("""
    <style>
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)
