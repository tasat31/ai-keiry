import streamlit as st
import datetime
from app.types.journal import Journal
from services.journals import entry

"""
### 決算整理仕訳
"""

receivables_tab, debt_tab, allowance_tab, other_tab = st.tabs(["債権管理", "債務管理", "引当金", "その他",])

with receivables_tab:
    pass

with debt_tab:
    pass

with allowance_tab:
    pass

with other_tab:
    other_credit = st.text_input("借方", key="other-credit")
    other_debit= st.text_input("貸方", key="other-debit")

    other_summary = st.text_input("摘要", key="other-summary")

    other_entried_at = st.date_input("計上日", datetime.date.today(), key="other-entried-at")

    other_amount_inc_tax = st.text_input("金額(総額・税込み)", key="other-amount-inc-tax")

    other_tax = st.text_input("消費税", key="other-tax")

    other_tax_rate = st.selectbox(
        label="消費税率",
        options=("0.10", "0.08", "0.00"),
        key="other-tax-rate"
    )

    other_partner = st.text_input("取引先", key="other-partner")

    other_remark = st.text_input("備考", key="other-remark")

    other_cash_in = st.text_input("Cash IN", key="other-cash-in")
    other_cash_out = st.text_input("Cash Out", key="other-cash-out")
    other_tax_in = st.text_input("Tax IN", key="other-tax-in")
    other_tax_out = st.text_input("Tax Out", key="other-tax-out")

    if st.button("記帳", type="primary", key="booking-other"):

        try:
            entry(journal=Journal(
                entried_at=other_entried_at,
                credit=other_credit,
                debit=other_debit,
                amount=int(other_amount_inc_tax) - int(other_tax),
                tax_rate=float(other_tax_rate),
                tax=int(other_tax),
                summary=other_summary,
                remark=other_remark,
                partner=other_partner,
                cash_in=other_cash_in,
                cash_out=other_cash_out,
                tax_in=other_tax_in,
                tax_out=other_tax_out,
                cost_type="",
                segment="",
                project_code="",
                fiscal_term="2025年6月期",
                month=other_entried_at.strftime('%Y%m'),
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
