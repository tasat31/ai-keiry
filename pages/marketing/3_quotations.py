import datetime
import streamlit as st
from streamlit import session_state as ss
from streamlit_modal import Modal
import pandas as pd
from constants import options
from services.leads import lead_options
from app.types.quotation import Quotation
from app.pdfs.quotation import generate_quotation

"""
### 見積書の作成
"""

quoatation_details = [
    {
        "項目": "",
        "単価": 0,
        "数量": 0,
        "単位": "",
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

quotation_title = st.text_input(label="件名")

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

    ss.edited_quotation_details_df = st.data_editor(
        ss.quoatation_details_df,
        key="quotation_details_data_editor",
        column_config={
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
        "金額": ss.edited_quotation_details_df["単価"] * ss.edited_quotation_details_df["数量"],
        "消費税": ss.edited_quotation_details_df["単価"] * ss.edited_quotation_details_df["数量"] * ss.edited_quotation_details_df["税率"],
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

quotation_delivery = st.text_input(label="納期", value="別途調整", key="quatation-delivery")

quotation_payment =  st.selectbox(
    label="お支払い条件",
    options=options.payment_conditions,
    key="select-payment-conditions"
)

quotation_expiry =  st.selectbox(
    label="見積り有効期限",
    options=options.expiries_of_quotation,
    key="select-expiries-of-quotation"
)

quotation_other_conditions = st.multiselect(
    label="その他見積り条件",
    options=options.quatation_conditions,
    placeholder="選択して下さい",
)

quotation_remark = st.text_area(label="備考")

if st.button("見積書PDF作成"):
    try:
        file_path='/tmp/quotation.pdf'
        generate_quotation(
            quotation=Quotation(
                issued_at=datetime.datetime.today(),
                customer=quotation_customer,
                title=quotation_title,
                delivery=quotation_delivery,
                expiry=quotation_expiry,
                payment=quotation_payment,
                other_conditions=quotation_other_conditions,
                remark=quotation_remark,
                departure=quotation_departure,
                arrival=quotation_arrival,
                trip=quotation_trip,
                details=pd.concat([ss.edited_quotation_details_df, df_result], axis=1)
            ),
            file_path=file_path
        )

        with open(file_path, "rb") as file:
            st.download_button(
                label="見積書PDFをダウンロード",
                data=file,
                file_name="御見積書_%s.pdf" % quotation_title,
                mime="application/pdf"
            )

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
