import streamlit as st
from streamlit_modal import Modal
import pandas as pd
import datetime
import calendar
from constants import options
from app.types.journal import Journal
from services.journals import list, credit_options, debit_options, bulk_entry, delete_all_expense_budget
from utils.datetime import list_by_month

@st.cache_data
def credit_options_cached():
    return credit_options()

@st.cache_data
def debit_options_cached():
    return debit_options()

"""
### 予算の作成と管理(費用)
"""
st.caption("実績をもとに予算の作成を行います。")
st.caption("売上高・売上原価の見込みはプロジェクト一覧で入力します。減価償却費については固定資産台帳をもとに計算されます。")

journals = []
journals_summary = []

st.write("会計期間: %s - %s" % (st.session_state['fiscal_start_date'].strftime("%Y-%m-%d"), st.session_state['fiscal_end_date'].strftime("%Y-%m-%d")))


"""
#### 1. 算定基礎データ抽出
"""
st.caption("仕訳の実績データを算定基礎データとします。計上日と勘定項目を指定し、予算案表を編集して下さい。")

col11, col12, col13, col14 = st.columns(4)

with col11:
    entried_at_from = st.date_input("計上日カラ", value=st.session_state['fiscal_start_date'])

with col12:
    current_date =  datetime.date.today()
    last_day = calendar.monthrange(current_date.year, current_date.month)[1]
    entried_at_to = st.date_input("計上日マデ", value=current_date.replace(day=last_day))

with col13:
    credit_selected = st.selectbox(
        label="借方",
        options=['ALL'] + credit_options_cached(),
        key="credit"
    )

with col14:
    debit_selected = st.selectbox(
        label="貸方",
        options=['ALL'] + debit_options_cached(),
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
    if journal.credit == '販売費及び一般管理費' and journal.cost_type != '減価償却費' and journal.closed == True:
        journals.append({
            "年月": journal.entried_at.strftime("%Y-%m"),
            "摘要": journal.summary,
            "現金支出": journal.cash_out,
            "現金収入": journal.cash_in,
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
            "日付": journal.entried_at,
            "id": journal.id,
        })

df_journals_edited = st.data_editor(
    pd.DataFrame(journals),
    width=800,
    height=600,
    column_config={
        "日付": st.column_config.DateColumn(
            "日付",
        ),
        "セグメント": st.column_config.SelectboxColumn(
            "セグメント",
            options=options.segments,
        ),
        "消費税率": st.column_config.SelectboxColumn(
            "消費税率",
            options=options.tax_rates,
        ),
    },
    disabled=["id"],
    hide_index=True,
    num_rows="dynamic"
)

journals_summary.append({
    # "日付": "合計",
    "期間(件数)": "%s 〜 %s (%s 件)" % (df_journals_edited["年月"].min(), df_journals_edited["年月"].max(), str(len(df_journals_edited))),
    "現金支出": df_journals_edited["現金支出"].sum(),
    "現金収入": df_journals_edited["現金収入"].sum(),
    "現金収入-支出": df_journals_edited["現金収入"].sum() - df_journals_edited["現金支出"].sum(),
    "仮受消費税": df_journals_edited["仮受消費税"].sum(),
    "支払消費税": df_journals_edited["支払消費税"].sum(),
    "仮受-支払": df_journals_edited["仮受消費税"].sum() - df_journals_edited["支払消費税"].sum(),
})

st.dataframe(
    pd.DataFrame(journals_summary),
    width=800,
    # height=600,
    hide_index=True,
)


"""
#### 2. 予算案(月割)の作成
"""

months = len(df_journals_edited.groupby("年月"))

df_budget_draft_per_month = (df_journals_edited[["費目", "摘要", "現金支出"]].groupby(["費目", "摘要"]).sum() / months).round(0)
df_tax_rate = df_journals_edited[["費目", "摘要", "消費税率"]].groupby(["費目", "摘要"]).max()

df_budget_draft_per_month = pd.concat([df_budget_draft_per_month, df_tax_rate], axis=1)

df_budget_draft_summary = df_journals_edited[["費目", "現金支出"]].groupby(["費目"]).sum() / months

st.write("##### 予算案(月割)合計: %s円" % "{:,}".format(int(df_budget_draft_per_month["現金支出"].sum())))

st.dataframe(
    df_budget_draft_per_month,
    width=800,
    # height=600,
    hide_index=False,
)

"""
#### 予算案(月割)の適用
"""
col21, col22 = st.columns(2)

with col21:
    current_date =  datetime.date.today()
    apply_start_date = datetime.datetime(current_date.year, current_date.month, 1)
    budget_entried_at_from = st.date_input("適用期間カラ", value=apply_start_date)

with col22:
    budget_entried_at_to = st.date_input("適用期間マデ", value=st.session_state['fiscal_end_date'])

if st.button("予算案(月割)を反映", type="primary", use_container_width=True):
    dict_budget = []
    apply_date_by_month_list = list_by_month(start_date=budget_entried_at_from, end_date=budget_entried_at_to)
    for index, row in df_budget_draft_per_month.reset_index().iterrows():
        for entried_at in apply_date_by_month_list:
            dict_budget.append({
                "entried_at": entried_at,
                "credit": "販売費及び一般管理費",
                "debit": "現金及び預金",
                "amount": row["現金支出"] - int(row["現金支出"] * row["消費税率"] + 0.5),
                "tax_rate": row["消費税率"],
                "tax": int(row["現金支出"] * row["消費税率"] + 0.5),
                "summary": row["摘要"],
                "remark": "月割り予算",
                "partner": "",
                "cash_in": 0,
                "cash_out": row["現金支出"],
                "cost_type": row["費目"],
                "project_id": None,
                "fiscal_term": st.session_state['fiscal_term'],
                "month": entried_at.strftime('%Y%m'),
                "closed": False
            })

    st.write(pd.DataFrame(dict_budget))

    delete_all_expense_budget()
    res = bulk_entry(pd.DataFrame(dict_budget))
    st.toast(res["message"])

# style
st.markdown("""
    <style>
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

