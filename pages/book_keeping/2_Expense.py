import streamlit as st
import pandas as pd
import datetime
from constants import options, segments
from app.types.journal import Journal
from services.journals import entry

"""
### 販管費及び一般管理費
"""

cost_type = st.selectbox(
    label="費目",
    options=options.cost_types,
    key="cost-type"
)

summary = st.text_input("摘要")

entried_at = st.date_input("計上日", datetime.date.today())

amount_inc_tax = st.text_input("金額(総額・税込み)")

tax = st.text_input("消費税")

tax_rate = st.selectbox(
    label="消費税率",
    options=("0.10", "0.08", "0.00"),
    key="tax-rate"
)

paid = st.selectbox(
    label="支払い",
    options=("現金", "未払金"),
    key="paid"
)

partner = st.text_input("取引先")

remark = st.text_input("備考")

if st.button("記帳", type="primary"):
    if paid == "現金":
        debit = "現金及び預金"
        cash_out = int(amount_inc_tax)
        tax_out = int(tax)
    else:
        debit = "未払金"
        cash_out = 0
        tax_out = 0

    try:
        entry(journal=Journal(
            entried_at=entried_at,
            credit="販売費及び一般管理費",
            debit=debit,
            amount=int(amount_inc_tax) - int(tax),
            tax_rate=float(tax_rate),
            tax=int(tax),
            summary=summary,
            remark=remark,
            partner=partner,
            cash_in=0,
            cash_out=cash_out,
            tax_in=0,
            tax_out=tax_out,
            cost_type=cost_type,
            segment=segments.segments["others"],
            project_code="",
            fiscal_term="2025年6月期",
            month=entried_at.strftime('%Y%m'),
            closed=True
        ))
        st.toast('記帳しました')
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

