import datetime
import streamlit as st
from streamlit_modal import Modal
import pandas as pd
import datetime
import calendar
from constants import options
from services.leads import list, cluster_options

"""
### シナリオの作成と実行
"""
leads = []

senario_title = st.text_input(label="シナリオタイトル(キャンペーンメール件名)")

col1, col2, col3, col4 = st.columns([0.20, 0.30, 0.25, 0.25])

with col1:
    segment_selected = st.selectbox(
        label="セグメント",
        options=options.segments,
        key="senario-segments",
        index=None
    )

with col2:
    cluster_selected = st.selectbox(
        label="クラスター",
        options=cluster_options(),
        key="senario-clusters",
        index=None
    )

with col3:
    last_contacted_at_from = st.date_input("直近のコンタクト日カラ", value=datetime.date.today().replace(day=1))

with col4:
    current_date =  datetime.date.today()
    last_day = calendar.monthrange(current_date.year, current_date.month)[1]
    last_contacted_at_to = st.date_input("直近のコンタクト日マデ", value=current_date.replace(day=last_day))

for lead in list(
    segment=segment_selected,
    cluster=cluster_selected,
    last_contacted_at_from=last_contacted_at_from,
    last_contacted_at_to=last_contacted_at_to,
):
    leads.append({
        "check": False,
        "セグメント": lead.segment,
        "クラスター": lead.cluster,
        "取引状況": lead.trade_status,
        "ランク":  lead.rank,
        "担当者・メールアドレス":  lead.partner_mail_address,
        "宛先会社": lead.name,
        "宛先担当者":  lead.partner_role + '  ' + lead.partner_name + '様',
        "説明":  lead.description,
        "直近のコンタクト日":  lead.last_contacted_at.strftime('%Y-%m-%d') if lead.last_contacted_at is not None else '',
        "法人/個人": lead.entity,
        "郵便番号": lead.postal_no,
        "都道府県": lead.prefecture,
        "市区町村": lead.city,
        "番地・建物等": lead.address,
        "URL": lead.url,
        "TEL":  lead.tel,
        "担当者・電話番号1":  lead.partner_tel_1,
        "担当者・電話番号2":  lead.partner_tel_2,
        "id": lead.id,
    })

"""
##### シナリオ候補の見込み客
"""

edited_leads = st.data_editor(
    pd.DataFrame(leads),
    width=800,
    height=300,
    column_config={
        "URL": st.column_config.LinkColumn(
            validate="^http",
            max_chars=256,
        ),
    },
    hide_index=True,
    key='senario-workspace',
)

"""
##### シナリオ適用見込み客
"""

if len(edited_leads) != 0:
    st.data_editor(
        edited_leads.query('check == True'),
        width=800,
        height=300,
        column_config={
            "URL": st.column_config.LinkColumn(
                validate="^http",
                max_chars=256,
            ),
        },
        hide_index=True,
        key='lead-selected'
    )
else:
    st.caption("見込み客を選択して下さい。")

senario_mail_content = st.text_area(
    label="キャンペーンメール内容",
    height=400
)

st.button("キャンペーンメール送信", type="primary")

# style
st.markdown("""
    <style>
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)
