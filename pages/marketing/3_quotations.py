import datetime
import streamlit as st
from streamlit import session_state as ss
from streamlit_modal import Modal
import pandas as pd
from constants import options
from services.leads import lead_options
from app.pdfs.quotation import generate_quotation

"""
### 見積書の作成
"""

quoatation_details = [
    {
        "見出し": "",
        "項目": "",
        "単価": 0,
        "単位": "",
        "数量": 0,
        "税率": 0.1,
    },
]

quotation_customer = st.selectbox(
    label="宛先",
    options=lead_options(),
    key="select-customer",
    help="登録された見込み客から選択します。",
    index=None,
    placeholder="選択して下さい",
)

quotation_customer = st.text_input(label="件名")

quotation_template = st.selectbox(
    label="見積りテンプレート選択",
    options=('コミュニティFM局', '1.2GHz送信機', 'スマートPVプラス'),
    placeholder="選択して下さい",
    index=None,
    key="select-quotation-template",
)

"""
##### 見積り明細
"""

col_editor, col_result = st.columns([0.8, 0.2])

with col_editor:
    ss.quoatation_details_df = pd.DataFrame(quoatation_details)

    ss.edited_df = st.data_editor(
        ss.quoatation_details_df,
        key="quotation_details_data_editor",
        column_config={
            "見出し": st.column_config.SelectboxColumn(
                "見出し",
                options=options.quotation_captions,
            ),
            "単価": st.column_config.NumberColumn(
                "単価",
                format="%d",
            ),
            "数量": st.column_config.NumberColumn(
                "数量",
                format="%d",
            ),
            "税率": st.column_config.SelectboxColumn(
                "税率",
                options=options.tax_rates,
                required=True,
            )
        },
        width=800,
        height=600,
        hide_index=True,
        num_rows="dynamic"
    )

with col_result:
    df_result = pd.DataFrame({
        "金額": ss.edited_df["単価"] * ss.edited_df["数量"],
        "消費税": ss.edited_df["単価"] * ss.edited_df["数量"] * ss.edited_df["税率"],
    })
    st.dataframe(
        df_result,
        height=600,
        hide_index=True,
        use_container_width=True
    )

"""
##### 出張費
"""
col_departure, col_arrival, col_trip = st.columns(3)

with col_departure:
    quotation_departure =  st.selectbox(
        label="出発地",
        options=('鹿児島県霧島市', '長崎県佐世保市'),
        key="select-quotation-departure"
    )

with col_arrival:
    quotation_arrival =  st.selectbox(
        label="到着地",
        options=('鹿児島県霧島市', '長崎県佐世保市'),
        key="select-quotation-arrival"
    )

with col_trip:
    quotation_trip = st.radio(
        label="行程",
        options=('往復', '片道', 'なし'),
        horizontal=True,
        key="radio-quotation-trip"
    )

"""
##### 見積り条件
"""

quotation_expiry =  st.selectbox(
    label="見積り有効期限",
    options=options.expiries_of_quotation,
    key="select-expiries-of-quotation"
)

quotation_payment =  st.selectbox(
    label="お支払い条件",
    options=options.payment_conditions,
    key="select-payment-conditions"
)

quotation_conditions = st.multiselect(
    label="その他見積り条件",
    options=options.quatation_conditions,
    placeholder="選択して下さい",
)

quotation_remark =  st.text_input(label="備考")

if st.button("見積書作成"):
    generate_quotation()

# style
st.markdown("""
    <style>
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)
