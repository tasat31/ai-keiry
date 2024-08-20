import streamlit as st
import pandas as pd
from services.dashboard import leads, sales, expense, sales_expense_leads_by_segment
import plotly.express as px

def currency_format(x):
    return "{:,d}".format(x)

"""
### ダッシュボード

"""
col1, col2, col3, col4 = st.columns(4)

leads_count = leads()
sales_amount = sales()
expense_amount = expense()
profit_amount = sales_amount - expense_amount

with col1.container(height=160):
    st.write("###### 見込み客数")
    st.write("## %s件" % currency_format(leads_count))

with col2.container(height=160):
    st.write("##### 売上高")
    st.write("### %sk円" % currency_format(int(sales_amount/1000.0 + 0.5)))
    st.caption("税込")

with col3.container(height=160):
    st.write("##### 費用")
    st.write("### %sk円" % currency_format(int(expense_amount/1000 + 0.5)))
    st.caption("税込")

with col4.container(height=160):
    st.write("##### 損益")
    st.write("### %sk円" % currency_format(int(profit_amount/1000 + 0.5)))
    st.caption("税込")

df_sales_expense_leads_by_segment = sales_expense_leads_by_segment()

# st.write(df_sales_expense_leads_by_segment)

fig = px.scatter(
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

st.plotly_chart(fig, theme="streamlit", use_container_width=True)