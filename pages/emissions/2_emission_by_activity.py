import datetime
import calendar
import streamlit as st
from streamlit_modal import Modal
import pandas as pd
from constants import options
from services.activities import list as activity_list
from services.journals import list_by_promotion
from services.emissions import bulk_entry as emission_bulk_entry

@st.cache_data
def options_activities():
    activities = []
    for activity in activity_list():
        activities.append(
            [activity.name, activity.emission_source, activity.emission_factor, 'tCo2/'+activity.unit, activity.scope_category, activity.id],
        )

    return activities

"""
### 活動別排出量の算定
"""
st.caption('販売費及び一般管理費の仕訳データをもとに排出量の算定を行います。')

activities_by_promotion = []
emissions_by_promotion = []

col11, col12, col13 = st.columns(3)

with col11:
    entried_at_from = st.date_input("計上日カラ", value=datetime.date.today().replace(day=1))

with col12:
    current_date =  datetime.date.today()
    last_day = calendar.monthrange(current_date.year, current_date.month)[1]
    entried_at_to = st.date_input("計上日マデ", value=current_date.replace(day=last_day))

with col13:
    pass

"""
##### 活動内容の確認(未実施分)
"""

for activity_by_promotion in list_by_promotion(entried_at_from=entried_at_from, entried_at_to=entried_at_to):
    activities_by_promotion.append({
        "check": False,
        "活動内容": None,
        "活動量": 0.0,
        "計上日": activity_by_promotion.entried_at.strftime('%Y-%m-%d'),
        "費目": activity_by_promotion.cost_type,
        "金額(税抜)": activity_by_promotion.amount - activity_by_promotion.tax,
        "摘要": activity_by_promotion.summary,
        "備考": activity_by_promotion.remark,
        "取引先": activity_by_promotion.partner,
        "仕訳id": activity_by_promotion.id,
    })

edited_activities_by_promotion = st.data_editor(
    pd.DataFrame(activities_by_promotion),
    width=800,
    height=300,
    hide_index=True,
    column_config={
        "活動内容": st.column_config.SelectboxColumn(
            "活動内容",
            options=options_activities(),
            width="large"
        ),
        "活動量": st.column_config.NumberColumn(
            "活動量",
            format="%.3f",
        ),
    },
    disabled=["計上日", "費目", "金額(税抜)", "摘要", "備考", "取引先", "仕訳id"],
    key='activity-by-promotion',
)

"""
##### 排出量の算定
"""
if len(edited_activities_by_promotion.query('check == True')) != 0:
    checked_edited_activities_by_promotion = edited_activities_by_promotion.query('check == True')

    checked_edited_activities_by_promotion["活動名称"] = checked_edited_activities_by_promotion["活動内容"].apply(lambda s: s.split(',')[0] if s is not None else None)
    checked_edited_activities_by_promotion["排出源"] = checked_edited_activities_by_promotion["活動内容"].apply(lambda s: s.split(',')[1] if s is not None else None)
    checked_edited_activities_by_promotion["排出係数"] = checked_edited_activities_by_promotion["活動内容"].apply(lambda s: float(s.split(',')[2]) if s is not None else 0.0)
    checked_edited_activities_by_promotion["単位"] = checked_edited_activities_by_promotion["活動内容"].apply(lambda s: s.split(',')[3] if s is not None else None)
    checked_edited_activities_by_promotion["スコープ"] = checked_edited_activities_by_promotion["活動内容"].apply(lambda s: s.split(',')[4] if s is not None else None)
    checked_edited_activities_by_promotion["活動id"] = checked_edited_activities_by_promotion["活動内容"].apply(lambda s: s.split(',')[-1] if s is not None else None)
    checked_edited_activities_by_promotion["排出量tCO2"] = checked_edited_activities_by_promotion["排出係数"] * checked_edited_activities_by_promotion["活動量"]


    df_caluclated = pd.concat([
            checked_edited_activities_by_promotion["check"],
            checked_edited_activities_by_promotion["活動名称"],
            checked_edited_activities_by_promotion["スコープ"],
            checked_edited_activities_by_promotion["排出源"],
            checked_edited_activities_by_promotion["活動量"],
            checked_edited_activities_by_promotion["排出係数"],
            checked_edited_activities_by_promotion["単位"],
            checked_edited_activities_by_promotion["排出量tCO2"],
            checked_edited_activities_by_promotion["計上日"],
            checked_edited_activities_by_promotion["費目"],
            checked_edited_activities_by_promotion["摘要"],
            checked_edited_activities_by_promotion["備考"],
            checked_edited_activities_by_promotion["取引先"],
            checked_edited_activities_by_promotion["活動id"],
            checked_edited_activities_by_promotion["仕訳id"],
        ], axis=1
    )
    st.data_editor(
        df_caluclated,
        width=800,
        height=300,
        hide_index=True,
        disabled=["check", "活動名称", "スコープ", "排出源", "活動量", "排出係数", "排出量tCO2", "計上日", "費目", "摘要", "備考", "取引先", "活動id", "仕訳id"],
        key='edited-activity-by-promotion'
    )
    st.write(df_caluclated[["活動名称", "スコープ", "排出量tCO2"]].groupby(by=["活動名称", "スコープ"]).sum().sort_values("スコープ"))
    st.write("### 排出量 計 = %.6f tCO2" % df_caluclated["排出量tCO2"].sum())
else:
    st.caption("活動内容を選択して下さい。")

if st.button("算定結果を登録する", type="primary"):
    df_caluclated["aggregation_key"] = df_caluclated["活動id"].apply(lambda s: 'promotion' if s is not None else '')
    df_for_bulk_entry = pd.concat(
        [
            df_caluclated["仕訳id"],
            df_caluclated["活動id"],
            df_caluclated["活動量"],
            df_caluclated["排出係数"],
            df_caluclated["排出量tCO2"],
            df_caluclated["aggregation_key"]
        ],
        axis=1
    )

    try:
        emission_bulk_entry(df_for_bulk_entry.to_csv().split('\n'))
        st.toast('算定結果を登録しました')
    except Exception as e:
        st.toast(e)

# style
st.markdown("""
    <style>
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)
