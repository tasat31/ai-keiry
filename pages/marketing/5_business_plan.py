import datetime
import streamlit as st
from streamlit import session_state as ss
from streamlit_modal import Modal
import pandas as pd
import calendar
from constants import options
from app.types.business_plan import GeneralCostPlan, SalesPlan
from services.business_plan import general_cost_plan_list, sales_plan_list

"""
### 事業計画
"""

st.write("会計期間: %s - %s" % (ss.fiscal_start_date.strftime("%Y-%m-%d"), ss.fiscal_end_date.strftime("%Y-%m-%d")))

col11, col12, col13, col14 = st.columns(4)

with col11:
    entried_at_from = st.date_input("計画開始", value=ss.fiscal_start_date)

with col12:
    entried_at_to = st.date_input("計画終了", value=ss.fiscal_end_date)

with col13:
    pass

with col14:
    pass

col21, col22, col23, col24 = st.columns(4)

with col21:
    show_annual_summary= st.toggle(
        label="年別集計",
        key="show-annual-summary",
    )

with col22:
    show_closed_only = st.toggle(
        label="実績のみ表示",
        key="show-closed-only",
    )

with col23:
    pass

with col24:
    pass


general_cost_plans = []
for data in general_cost_plan_list(entried_at_from=entried_at_from, entried_at_to=entried_at_to, closed=True if show_closed_only else None):
    general_cost_plans.append(data.dict())

df_general_cost_plans = pd.DataFrame(general_cost_plans)

month_list = list(df_general_cost_plans.groupby('month').groups.keys())
df_general_cost_plans_monthly_transition = df_general_cost_plans[df_general_cost_plans['month'] == month_list[0]][['cost_type', 'amount_inc_tax']].rename(columns={'amount_inc_tax': month_list[0]})

for month in month_list[1:]:
    df_general_cost_plans_monthly_transition = pd.merge(
        df_general_cost_plans_monthly_transition,
        df_general_cost_plans[df_general_cost_plans['month'] == month][['cost_type', 'amount_inc_tax']].rename(columns={'amount_inc_tax': month}),
        how='outer',
        on='cost_type'
    )

"""
#### 販売費及び一般管理費の見通し
"""
st.dataframe(
    pd.DataFrame(df_general_cost_plans_monthly_transition),
    width=800,
    # height=600,
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
