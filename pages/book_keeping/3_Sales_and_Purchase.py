import streamlit as st
from streamlit_modal import Modal
import pandas as pd
import datetime
from constants import options, segments
from app.types.journal import Journal
from services.journals import entry

"""
### 売上と仕入れ

"""

sales_tab, purchase_tab, projects_tab = st.tabs(["売上", "仕入れ", "プロジェクト一覧",])

with sales_tab:
    sales_segment = st.selectbox(
        label="セグメント",
        options=options.segments,
        key="sales-segment"
    )

    sales_project_code = ""
    # project_code = st.selectbox(
    #    label="プロジェクトコード",
    #    options=options.segments,
    #    key="project-code"
    #)

    sales_summary = st.text_input("摘要", key="sales-summary")

    sales_entried_at = st.date_input("計上日", datetime.date.today(), key="sales-entried-at")

    sales_amount_inc_tax = st.text_input("金額(総額・税込み)", key="sales-amount-inc-tax")

    sales_tax = st.text_input("消費税")

    sales_tax_rate = st.selectbox(
        label="消費税率",
        options=("0.10", "0.08", "0.00"),
        key="tax-rate"
    )

    sales_paid = st.selectbox(
        label="支払い",
        options=("現金", "売掛金"),
        key="paid"
    )

    sales_partner = st.text_input("取引先")

    sales_remark = st.text_input("備考")

    if st.button("売上高記帳", type="primary", key="booking-sales"):
        if sales_paid == "現金":
            sales_credit = "現金及び預金"
            sales_cash_in = int(sales_amount_inc_tax)
            sales_tax_in = int(sales_tax)
        else:
            sales_credit= "売掛金"
            sales_cash_in = 0
            sales_tax_in = 0

        try:
            entry(journal=Journal(
                entried_at=sales_entried_at,
                credit=sales_credit,
                debit="売上高",
                amount=int(sales_amount_inc_tax) - int(sales_tax),
                tax_rate=float(sales_tax_rate),
                tax=int(sales_tax),
                summary=sales_summary,
                remark=sales_remark,
                partner=sales_partner,
                cash_in=sales_cash_in,
                cash_out=0,
                tax_in=sales_tax_in,
                tax_out=0,
                cost_type="",
                segment=sales_segment,
                project_code="",
                fiscal_term="2025年6月期",
                month=sales_entried_at.strftime('%Y%m'),
                closed=True
            ))
            st.toast('売上高を記帳しました')
        except Exception as e:
            st.toast(e)

with purchase_tab:
    purchase_segment = st.selectbox(
        label="セグメント",
        options=options.segments,
        key="purchase-segment"
    )

    purchase_project_code = ""
    # project_code = st.selectbox(
    #    label="プロジェクトコード",
    #    options=options.segments,
    #    key="project-code"
    #)

    purchase_summary = st.text_input("摘要", key="purchase-summary")

    purchase_entried_at = st.date_input("計上日", datetime.date.today(), key="purchase-entried-at")

    purchase_amount_inc_tax = st.text_input("金額(総額・税込み)", key="purchase-amount-inc-tax")

    purchase_tax = st.text_input("消費税", key="purchase-tax")

    purchase_tax_rate = st.selectbox(
        label="消費税率",
        options=("0.10", "0.08", "0.00"),
        key="purchase-tax-rate"
    )

    purchase_paid = st.selectbox(
        label="支払い",
        options=("現金", "買掛金"),
        key="purchase-paid"
    )

    purchase_partner = st.text_input("取引先", key="purchase-partner")

    purchase_remark = st.text_input("備考", key="purhchase-remark")

    if st.button("仕入れ記帳", type="primary", key="booking-purchase"):
        if purchase_paid == "現金":
            purchase_debit = "現金及び預金"
            purchase_cash_out = int(purchase_amount_inc_tax)
            purchase_tax_out = int(purchase_tax)
        else:
            purchase_debit= "買掛金"
            purchase_cash_out = 0
            purchase_tax_out = 0

        try:
            entry(journal=Journal(
                entried_at=purchase_entried_at,
                credit="売上原価",
                debit=purchase_debit,
                amount=int(purchase_amount_inc_tax) - int(purchase_tax),
                tax_rate=float(purchase_tax_rate),
                tax=int(purchase_tax),
                summary=purchase_summary,
                remark=purchase_remark,
                partner=purchase_partner,
                cash_in=0,
                cash_out=purchase_cash_out,
                tax_in=0,
                tax_out=purchase_tax_out,
                cost_type="",
                segment=purchase_segment,
                project_code="",
                fiscal_term="2025年6月期",
                month=purchase_entried_at.strftime('%Y%m'),
                closed=True
            ))
            st.toast('記帳しました')
        except Exception as e:
            st.toast(e)

with projects_tab:
    modal = Modal(
        "プロジェクト追加", 
        key="add-project",
    
        # Optional
        padding=20,    # default value
        max_width=744  # default value
    )

    open_modal = st.button("プロジェクト追加")
    if open_modal:
        modal.open()

    if modal.is_open():
        with modal.container():
            segment =  st.selectbox(
                label="セグメント",
                options=options.segments,
                key="segment"
            )

            title = st.text_input("タイトル")

            description = st.text_input("説明")

            loanched_at = st.date_input("開始日", datetime.date.today())

            partner = st.text_input("取引先")

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

