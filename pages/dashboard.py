import streamlit as st
import pandas as pd
from services.dashboard import leads, sales, expense, sales_expense_leads_by_segment, leads_by_rank, expense_by_cost_type
import plotly.express as px
from plotly import graph_objects as go

def currency_format(x):
    return "{:,d}".format(x)

"""
### ダッシュボード

"""

st.write("会計期間: %s - %s" % (st.session_state['fiscal_start_date'].strftime("%Y-%m-%d"), st.session_state['fiscal_end_date'].strftime("%Y-%m-%d")))

col11, col12, col13, col14 = st.columns(4)

leads_count = leads()
sales_amount = sales(entried_at_from=st.session_state['fiscal_start_date'], entried_at_to=st.session_state['fiscal_end_date'])
expense_amount = expense(entried_at_from=st.session_state['fiscal_start_date'], entried_at_to=st.session_state['fiscal_end_date'])
profit_amount = sales_amount - expense_amount

with col11.container(height=160):
    st.write("###### 見込み客数")
    st.write("## %s件" % currency_format(leads_count))

with col12.container(height=160):
    st.write("###### 売上高(千円)")
    st.write("## %s" % currency_format(int(sales_amount/1000.0 + 0.5)))

with col13.container(height=160):
    st.write("###### 費用(千円)")
    st.write("## %s" % currency_format(int(expense_amount/1000 + 0.5)))

with col14.container(height=160):
    st.write("###### 損益(千円)")
    st.write("## %s" % currency_format(int(profit_amount/1000 + 0.5)))


st.caption("金額は税込")

# st.write(df_sales_expense_leads_by_segment)

col21, col22 = st.columns([0.5, 0.5])

with col21.container():
    st.write("見込み客の内訳")
    colors = ["gold", "gold", "lightgreen", "lavender"]
    df_leads_by_rank = leads_by_rank()
    fig_leads_by_rank = px.pie(df_leads_by_rank, values='見込み客数', names='ランク')
    st.plotly_chart(fig_leads_by_rank, theme="streamlit", use_container_width=True)

with col22.container():
    st.write("販売費及び一般管理費の内訳")
    graph_data = expense_by_cost_type()

    fig_expense_by_cost_type = go.Figure(
        go.Funnelarea(
            title="費目別の割合",
            labels=graph_data["labels"],
            values=graph_data["values"],
            textfont_size=20,
            # marker=dict(colors=colors,pattern=dict(shape=["", "/", "", ""])),
        )
    )

    st.plotly_chart(fig_expense_by_cost_type, theme="streamlit", use_container_width=True)

df_sales_expense_leads_by_segment = sales_expense_leads_by_segment()
fig__sales_expense_leads_by_segment = px.scatter(
    df_sales_expense_leads_by_segment,
    title="見込み客規模 vs 売上実績チャート",
    x="売上高(税込)",
    y="売上利益(税込)",
    size="見込み客数",
    color="セグメント",
    hover_name="セグメント",
    log_x=False,
    size_max=60,
    orientation="h",
)

st.plotly_chart(fig__sales_expense_leads_by_segment, theme="streamlit", use_container_width=True)
