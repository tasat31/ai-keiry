import datetime
import streamlit as st
from streamlit_modal import Modal
import pandas as pd
from constants import options
from app.types.project import Project
from services.projects import list, entry, bulk_update

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
        "edit": False,
        "セグメント": project.segment,
        "タイトル": project.title,
        "説明": project.description,
        "開始日": project.launched_at,
        "完了日": project.completed_at,
        "取引先": project.partner,
        "ステータス": project.status,
        "売上(計画)": project.estimate_sales,
        "原価(計画)": project.estimate_cost,
        "損益(計画)": project.estimate_profit,
        "売上(実績)": project.actual_sales,
        "原価(実績)": project.actual_cost,
        "損益(実績)": project.actual_profit,
        "売上(残)": project.diff_sales,
        "原価(残)": project.diff_cost,
        "損益(残)": project.diff_profit,
        "消費税率": project.tax_rate,
        "id": project.id,
    })

projects_edited = st.data_editor(
    pd.DataFrame(projects),
    width=800,
    height=600,
    column_config={
        "セグメント": st.column_config.SelectboxColumn(
            "セグメント",
            options=options.segments,
        ),
        "開始日": st.column_config.DateColumn(
            "開始日",
        ),
        "完了日": st.column_config.DateColumn(
            "完了日",
        ),
        "ステータス": st.column_config.SelectboxColumn(
            "ステータス",
            options=options.project_status,
        ),
        "消費税率": st.column_config.SelectboxColumn(
            "消費税率",
            options=options.tax_rates,
        ),
    },
    disabled=["id"],
    hide_index=True,
)

if st.button("チェックした行を更新", type="primary"):
    res = bulk_update(projects_edited.query('edit == True'))
    st.toast(res["message"])

# style
st.markdown("""
    <style>
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)
