import datetime
import streamlit as st
from streamlit_modal import Modal
import pandas as pd
from constants import options
from app.types.project import Project
from services.projects import list, entry

"""
### プロジェクト一覧
"""
projects = []

open_modal = st.button("プロジェクト追加", key="projects-add")

modal = Modal(
    "プロジェクト追加", 
    key="add-project",
    
    # Optional
    padding=20,    # default value
    max_width=744  # default value
)

if open_modal:
    modal.open()

if modal.is_open():
    with modal.container():
        segment =  st.selectbox(
            label="セグメント",
            options=options.segments,
            key="segment"
        )

        title = st.text_input("タイトル", key="project-title")
        description = st.text_input("説明", key="project-description")
        launched_at = st.date_input("開始日", datetime.date.today(), key="project-launched-at")
        completed_at = st.date_input("完了日", datetime.date.today(), key="project-completed-at")
        partner = st.text_input("取引先", key="project-partner")
        status = st.selectbox(
            label="ステータス",
            options=options.project_status,
            key="project-status"
        )
        estimate_sales = st.text_input("売上(計画)", key="project-estimate-sales")
        estimate_cost = st.text_input("原価(計画)", key="project-estimate-cost")
        estimate_profit = st.text_input("損益(計画)", key="project-estimate-profit")
        tax_rate = st.selectbox(
            label="消費税率",
            options=options.tax_rates,
            key="project-tax-rate"
        )

        if st.button("追加"):
            try:
                entry(project=Project(
                    segment=segment,
                    title=title,
                    description=description,
                    launched_at=launched_at,
                    completed_at=completed_at,
                    partner=partner,
                    status=status,
                    estimate_sales=estimate_sales,
                    estimate_cost=estimate_cost,
                    estimate_profit=estimate_profit,
                    tax_rate=tax_rate,
                ))
                modal.close()
                st.toast('プロジェクトを登録しました')
            except Exception as e:
                st.toast(e)
                modal.close()

for project in list():
    projects.append({
        "id": project.id,
        "セグメント": project.segment,
        "タイトル": project.title,
        "説明": project.description,
        "開始日": project.launched_at.strftime('%Y-%m-%d'),
        "完了日": project.completed_at.strftime('%Y-%m-%d'),
        "取引先": project.partner,
        "ステータス": project.status,
        "売上(計画)": project.estimate_sales,
        "原価(計画)": project.estimate_cost,
        "損益(計画)": project.estimate_profit,
        "消費税率": project.tax_rate,
    })

st.dataframe(
    pd.DataFrame(projects),
    width=800,
    height=600,
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
