import streamlit as st
import pandas as pd
import datetime
import calendar
from services.journals import list

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
    height=600,
    hide_index=True,
)

st.dataframe(
    pd.DataFrame(journals_summary),
    width=800,
    # height=600,
    hide_index=True,
)

st.download_button(
    label=":white_check_mark: 仕訳データCSV ダウンロード",
    data=pd.DataFrame(journals_for_download).to_csv().encode('utf-8'),
    file_name='keiry_journal_data.csv',
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

