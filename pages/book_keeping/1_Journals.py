import streamlit as st
from streamlit_modal import Modal
import pandas as pd
import datetime
import calendar
from constants import options, segments
from app.types.journal import Journal
from services.journals import entry
from services.journals import list


expense_modal = Modal(
    ":pencil: 販管費及び一般管理費を記帳", 
    key="entry-expense-modal",
    
    padding=20,
    max_width=800,
)

sales_and_purchase_modal = Modal(
    ":pencil: 売上高と仕入れを記帳", 
    key="entry-sales-and-purchase-modal",
    
    padding=20,
    max_width=800,
)

if expense_modal.is_open():
    with expense_modal.container():

        expense_cost_type = st.selectbox(
            label="費目",
            options=options.cost_types,
            key="expense-cost-type"
        )

        expense_summary = st.text_input("摘要", key="expense-summary")
        expense_entried_at = st.date_input("計上日", datetime.date.today(), key="expense-entried-at")
        expense_amount_inc_tax = st.text_input("金額(総額・税込み)", key="expense-amount-inc-tax")
        expense_tax = st.text_input("消費税", key="expense-tax")
        expense_tax_rate = st.selectbox(
            label="消費税率",
            options=("0.10", "0.08", "0.00"),
            key="expense-tax-rate"
        )
        expense_paid = st.selectbox(
            label="支払い",
            options=("現金", "未払金"),
            key="expense-paid"
        )
        expense_partner = st.text_input("取引先", key="expense-partner")
        expense_remark = st.text_input("備考", key="expense-remark")
        
        if st.button("記帳", type="primary", key="entry-expense-button"):
            expense_modal.close()
            if expense_paid == "現金":
                expense_debit = "現金及び預金"
                expense_cash_out = int(expense_amount_inc_tax)
                expense_tax_out = int(expense_tax)
            else:
                expense_debit = "未払金"
                expense_cash_out = 0
                expense_tax_out = 0

            try:
                entry(journal=Journal(
                    entried_at=expense_entried_at,
                    credit="販売費及び一般管理費",
                    debit=expense_debit,
                    amount=int(expense_amount_inc_tax) - int(expense_tax),
                    tax_rate=float(expense_tax_rate),
                    tax=int(expense_tax),
                    summary=expense_summary,
                    remark=expense_remark,
                    partner=expense_partner,
                    cash_in=0,
                    cash_out=expense_cash_out,
                    tax_in=0,
                    tax_out=expense_tax_out,
                    cost_type=expense_cost_type,
                    segment=segments.segments["others"],
                    project_code="",
                    fiscal_term="2025年6月期",
                    month=expense_entried_at.strftime('%Y%m'),
                    closed=True
                ))
                st.toast('販売費及び一般管理費を記帳しました')
            except Exception as e:
                st.toast(e)
                expense_modal.close()

if sales_and_purchase_modal.is_open():
    with sales_and_purchase_modal.container():
        sales_tab, purchase_tab = st.tabs(["売上", "仕入れ"])

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

        sales_partner = st.text_input("取引先", key="sales-partner")

        sales_remark = st.text_input("備考", key="sales-remark")

        if st.button("売上高記帳", type="primary", key="booking-sales"):
            sales_and_purchase_modal.close()
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
     

"""
### 仕訳と元帳
"""

journals = []
journals_for_download = []
journals_summary = []
total_cash_out = 0
total_cash_in = 0
total_ammount = 0
total_tax = 0
total_amount_include_tax = 0
total_tax_in = 0
total_tax_out = 0
entried_at_from = None
entried_at_to = None
count = 0
credit_options = []
debit_options = []

col11, col12, col13, col14 = st.columns(4)

with col11:
    entried_at_from = st.date_input("計上日カラ", value=datetime.date.today().replace(day=1))

with col12:
    current_date =  datetime.date.today()
    last_day = calendar.monthrange(current_date.year, current_date.month)[1]
    entried_at_to = st.date_input("計上日マデ", value=current_date.replace(day=last_day))

with col13:
    credit_selected = st.selectbox(
        label="借方",
        options=['ALL'] + credit_options,
        key="credit"
    )

with col14:
    debit_selected = st.selectbox(
        label="貸方",
        options=['ALL'] + debit_options,
        key="debit"
    )

col21, col22 = st.columns(2)

with col21:
    summary_input = st.text_input("摘要")

with col22:
    partner_input = st.text_input("取引先")

for journal in list(
    entried_at_from=entried_at_from,
    entried_at_to=entried_at_to,
    credit_selected=credit_selected,
    debit_selected=debit_selected,
    summary_input=summary_input,
    partner_input=partner_input
):
    journals.append({
        "日付": journal.entried_at.strftime('%Y-%m-%d'),
        "摘要": journal.summary,
        "支出": journal.cash_out,
        "収入": journal.cash_in,
        "借方": journal.credit,
        "貸方": journal.debit,
        "金額(税抜)": journal.amount,
        "消費税率":  journal.tax_rate,
        "消費税":  journal.tax,
        "金額(税込)": journal.amount + journal.tax,
        "備考":  journal.remark,
        "取引先":  journal.partner,
        "費目":  journal.cost_type,
        "セグメント":  journal.segment,
        "仮受消費税": journal.tax_in,
        "支払消費税": journal.tax_out,
    })

    if entried_at_from is None:
        entried_at_from = journal.entried_at
    
    total_cash_out = total_cash_out + journal.cash_out
    total_cash_in = total_cash_in + journal.cash_in
    total_ammount = total_ammount + journal.amount
    total_tax = total_tax + journal.tax
    total_amount_include_tax = total_amount_include_tax + (journal.amount + journal.tax)
    total_tax_in = total_tax_in + journal.tax_in
    total_tax_out = total_tax_out + journal.tax_out
    entried_at_to = journal.entried_at
    count = count + 1

    journals_for_download.append(journal.dict())

journals_summary.append({
    # "日付": "合計",
    "期間(件数)": "%s 〜 %s (%s 件)" % (entried_at_from.strftime('%Y-%m-%d'), entried_at_to.strftime('%Y-%m-%d'), str(count)),
    "支出": total_cash_out,
    "収入": total_cash_in,
    "収入 - 支出": total_cash_in - total_cash_out,
    # "借方": "",
    # "貸方": "",
    # "金額(税抜)": total_ammount,
    # "消費税率":  "",
    # "消費税":  total_tax,
    # "金額(税込)": total_amount_include_tax,
    # "備考":  "",
    # "取引先":  "",
    # "費目":  "",
    # "セグメント":  "",
    "仮受消費税": total_tax_in,
    "支払消費税": total_tax_out,
    "仮受-支払": total_tax_in - total_tax_out,
})

st.dataframe(
    pd.DataFrame(journals),
    width=800,
    height=400,
    hide_index=True,
)

st.dataframe(
    pd.DataFrame(journals_summary),
    width=800,
    # height=600,
    hide_index=True,
)


col_btn_1, col_btn_2, col_btn_3 = st.columns(3)

with col_btn_1:
    open_expense_modal = st.button(
        ":pencil: 販管費及び一般管理費",
        type="secondary",
        use_container_width=True,
        key="open-entry-expense-modal"
    )

    if open_expense_modal:
        expense_modal.open()

with col_btn_2:
    open_sales_and_purchase_modal = st.button(
        ":pencil: 売上と仕入れ",
        type="secondary",
        use_container_width=True,
        key="entry-sales-and-purchase-modal"
    )

    if open_sales_and_purchase_modal:
        sales_and_purchase_modal.open()

with col_btn_3:
    st.download_button(
        label=":white_check_mark: CSV ダウンロード",
        data=pd.DataFrame(journals_for_download).to_csv().encode('utf-8'),
        file_name='keiry_journal_data.csv',
        use_container_width=True, 
        mime='text/csv',
    )

# style
st.markdown("""
    <style>
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

