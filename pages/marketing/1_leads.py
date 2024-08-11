import datetime
import streamlit as st
from streamlit_modal import Modal
import pandas as pd
from constants import options
from app.types.lead import Lead
from services.leads import list, entry

"""
### 見込み客リスト

"""
leads = []

open_modal = st.button("見込み客追加", key="leads-add")

modal = Modal(
    "見込み客追加", 
    key="add-lead",
    
    padding=20,
    max_width=800,
)

if open_modal:
    modal.open()

if modal.is_open():
    with modal.container():
        lead_name = st.text_input("名称", key="leads-title")
        lead_entity =  st.selectbox(
            label="法人/個人",
            options=options.lead_entities,
            key="lead-entities"
        )
        lead_postal_no = st.text_input("郵便番号", key="lead-postal-no")
        lead_prefecture = st.text_input("都道府県", key="lead-prefecture")
        lead_city = st.text_input("市区町村", key="lead-city")
        lead_address = st.text_input("番地・建物等", key="lead-address")
        lead_url = st.text_input("URL", key="lead-url")
        lead_tel = st.text_input("TEL", key="lead-tel")
        lead_segment =  st.selectbox(
            label="セグメント",
            options=options.segments,
            key="lead-segment"
        )
        lead_cluster = st.text_input("クラスタ", key="lead-cluster")
        lead_trade_status =  st.selectbox(
            label="取引状況",
            options=options.lead_trade_status,
            key="lead-trade-status"
        )
        lead_rank =  st.selectbox(
            label="ランク",
            options=options.lead_ranks,
            key="lead-rank"
        )
        lead_first_contacted_at = st.date_input("初回コンタクト日", value=None, key="lead-first-contacted-at")
        lead_first_contacted_media = st.selectbox(
            label="初回コンタクト手段",
            options=options.lead_contacted_media,
            key="lead-first-contacted-media"
        )
        lead_last_contacted_at = st.date_input("直近のコンタクト日", value=None, key="lead-last-contacted-at")
        lead_description = st.text_input("説明", key="leads-description")
        lead_partner_name = st.text_input("担当者氏名", key="lead-partner-name")
        lead_partner_role = st.text_input("担当者部署・役職", key="lead-partner-role")
        lead_partner_tel_1 = st.text_input("担当者・電話番号1", key="lead-partner-tel-1")
        lead_partner_tel_2 = st.text_input("担当者・電話番号2", key="lead-partner-tel-2")
        lead_partner_mail_address = st.text_input("担当者・メールアドレス", key="lead-partner-mail-address")

        if st.button("追加"):
            lead = Lead(
                name=lead_name,
                entity=lead_entity,
                postal_no=lead_postal_no,
                prefecture=lead_prefecture,
                city=lead_city,
                address=lead_address,
                url=lead_url,
                tel=lead_tel,
                segment=lead_segment,
                clusterr=lead_cluster,
                trade_status=lead_trade_status,
                rank=lead_rank,
                first_contacted_at=lead_first_contacted_at,
                first_contacted_media=lead_first_contacted_media,
                last_contacted_at=lead_last_contacted_at,
                description=lead_description,
                partner_name=lead_partner_name,
                partner_role=lead_partner_role,
                partner_tel_1=lead_partner_tel_1,
                partner_tel_2=lead_partner_tel_2,
                partner_mail_address=lead_partner_mail_address,
            )
            entry(lead=lead)
            modal.close()


for lead in list():
    leads.append({
        "名称": lead.name,
        "法人/個人": lead.entity,
        "郵便番号": lead.postal_no,
        "都道府県": lead.prefecture,
        "市区町村": lead.city,
        "番地・建物等": lead.address,
        "URL": lead.url,
        "TEL":  lead.tel,
        "セグメント":  lead.segment,
        "クラスター":  lead.cluster,
        "取引状況": lead.trade_status,
        "ランク":  lead.rank,
        "初回コンタクト日":  lead.first_contacted_at,
        "初回コンタクト手段":  lead.first_contacted_media,
        "直近のコンタクト日":  lead.last_contacted_at,
        "説明":  lead.description,
        "担当者氏名":  lead.partner_name,
        "担当者部署・役職":  lead.partner_role,
        "担当者・電話番号1":  lead.partner_tel_1,
        "担当者・電話番号2":  lead.partner_tel_2,
        "担当者・メールアドレス":  lead.partner_mail_addres,
    })

st.dataframe(
    pd.DataFrame(leads),
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
