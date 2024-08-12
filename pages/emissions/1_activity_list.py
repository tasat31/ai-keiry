import datetime
import streamlit as st
from streamlit_modal import Modal
import pandas as pd
from constants import options
from app.types.activity import Activity
from services.activities import list, entry

"""
### 活動内容(排出源と係数)の設定
"""
activities = []

open_modal = st.button("活動内容を追加", key="activity-add")

modal = Modal(
    "活動内容追加", 
    key="add-activity",
    
    padding=20,
    max_width=800,
)

if open_modal:
    modal.open()

if modal.is_open():
    with modal.container():
        activity_name = st.text_input("活動名称", key="activity-name")
        activity_emission_source =  st.selectbox(
            label="排出源",
            options=options.emission_sources,
            key="activity-emission-source"
        )
        activity_unit = st.text_input("単位", key="activity-unit")
        activity_emission_factor = st.text_input("単位あたりのtCo2", key="activity-emission-factor")
        activity_scope_category =  st.selectbox(
            label="スコープ・カテゴリ",
            options=options.scope_categories,
            key="activity-scope-category"
        )
        activity_basis_of_emission_factor = st.text_input("排出係数の根拠", key="activity-basis-of-emission_factor")
        activity_description = st.text_input("説明", key="activity-description")

        if st.button("追加"):
            activity = Activity(
                name=activity_name,
                emission_source=activity_emission_source,
                unit=activity_unit,
                emission_factor=activity_emission_factor,
                scope_category=activity_scope_category,
                basis_of_emission_factor=activity_basis_of_emission_factor,
                description=activity_description
            )
            entry(activity=activity)
            modal.close()


for activity in list():
    activities.append({
        "活動名称": activity.name,
        "排出源": activity.emission_source,
        "単位": activity.unit,
        "単位あたりのtCo2": str(activity.emission_factor),
        "スコープ・カテゴリ": activity.scope_category,
        "排出係数の根拠": activity.basis_of_emission_factor,
        "説明": activity.description,
    })

st.dataframe(
    pd.DataFrame(activities),
    width=800,
    height=600,
    column_config={
        "排出係数の根拠": st.column_config.LinkColumn(
            validate="^http",
            max_chars=256,
        ),
    },
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
