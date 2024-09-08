import datetime
import calendar
import streamlit as st
from streamlit import session_state as ss
from streamlit_modal import Modal
import pandas as pd
from constants import options
from app.types.emission import EmissionDetail
from services.emissions import aggregate_by_scope, aggregate_by_scope_and_month
from services.emissions import list as emission_list

"""
### レポート出力
"""

col11, col12, col13 = st.columns(3)

with col11:
    entried_at_from = st.date_input("計上日カラ", value=ss.fiscal_start_date)

with col12:
    current_date =  datetime.date.today()
    last_day = calendar.monthrange(current_date.year, current_date.month)[1]
    entried_at_to = st.date_input("計上日マデ", value=current_date.replace(day=last_day))

with col13:
    pass

"""
##### Scope別排出量
"""
df_aggregate_by_scope = pd.DataFrame(aggregate_by_scope(entried_at_from=entried_at_from, entried_at_to=entried_at_to))
st.dataframe(
    df_aggregate_by_scope,
    column_config={
        "scope_category": "スコープカテゴリ",
        "activity_name": "活動名",
        "emission_source": "排出源",
        "unit": "単位",
        "total_activity": "活動量",
        "total_emission": "排出量",
    },
    hide_index=True
)

"""
##### 月別排出量内訳
"""
df_aggregate_by_scope_and_month = pd.DataFrame(aggregate_by_scope_and_month(entried_at_from=entried_at_from, entried_at_to=entried_at_to))
st.dataframe(
    df_aggregate_by_scope_and_month,
    column_config={
        "month": "年月",
        "scope_category": "スコープカテゴリ",
        "activity_name": "活動名",
        "emission_source": "排出源",
        "unit": "単位",
        "total_activity": "活動量",
        "total_emission": "排出量",
    },
    hide_index=True
)

"""
##### 排出量明細
"""

emission_details = []
for emission_detail in emission_list(entried_at_from=entried_at_from, entried_at_to=entried_at_to):
    emission_details.append({
        "日付": emission_detail.journal_entried_at.strftime('%Y-%m-%d'),
        "活動名": emission_detail.activity_name,
        "スコープカテゴリ": emission_detail.scope_category,
        "活動量": emission_detail.activity,
        "単位": emission_detail.activity_unit,
        "排出係数": emission_detail.emission_factor,
        "排出量": emission_detail.emission,
        "摘要": emission_detail.journal_summary,
        "備考": emission_detail.journal_remark,
        "活動id": emission_detail.activity_id,
        "仕訳id": emission_detail.journal_id,
    })

df_emission_details = pd.DataFrame(emission_details)
st.dataframe(df_emission_details, hide_index=True)

# style
st.markdown("""
    <style>
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)
