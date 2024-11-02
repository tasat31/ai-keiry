import datetime
import streamlit as st
from streamlit import session_state as ss
from streamlit_modal import Modal
import pandas as pd
from constants import options
from services.leads import lead_options
from services.quotation_templates import quotation_template_options
from services.quotation_templates import list as quotation_template_list
from services.quotation_templates import bulk_entry as quotation_template_bulk_entry
from services.quotation_templates import delete_by_title as quotation_template_delete_by_title
from app.types.invoice import InvoicePaper
from app.pdfs.invoice_paper import generate_invoice_paper

if 'quotation_template_title' not in ss:
    ss.quotation_template_title = None

if 'quotation_details' not in ss:
    ss.quotation_details = [
        {
            "項目": "",
            "単価": 0,
            "数量": 0,
            "単位": "",
            "税率": 0.1,
        },
    ]

def apply_quotation_template():
    quotation_details = []
    for quotation_template in quotation_template_list(title=ss.quotation_template_title):
        quotation_details.append({
            "項目": quotation_template.item,
            "単価": quotation_template.unit_price,
            "数量": quotation_template.quantity,
            "単位": quotation_template.unit,
            "税率": quotation_template.tax_rate,
        })

    if len(quotation_details) > 0:
        ss.quotation_details = quotation_details
        ss.quotation_details_df = pd.DataFrame(ss.quotation_details)
        ss.df_result = pd.DataFrame({
            "金額": ss.quotation_details_df["単価"] * ss.quotation_details_df["数量"],
            "消費税": ss.quotation_details_df["単価"] * ss.quotation_details_df["数量"] * ss.quotation_details_df["税率"],
        })
    else:
        ss.quotation_details = [
            {
                "項目": "",
                "単価": 0,
                "数量": 0,
                "単位": "",
                "税率": 0.1,
            },
        ]
        ss.df_result = pd.DataFrame(
            {
                "金額": [0],
                "消費税": [0],
            }
        )

"""
### 請求書の発行
"""
apply_quotation_template()

quotation_customer = st.selectbox(
    label="宛先",
    options=lead_options(),
    key="select-customer",
    help="登録された見込み客から選択します。",
    index=None,
    placeholder="選択して下さい",
)

ss.quotation_template_title = st.selectbox(
    label="見積りテンプレート選択",
    options=quotation_template_options(),
    placeholder="選択して下さい",
    index=None,
    key="select-quotation-template",
)

if st.button("テンプレートを適用"):
    apply_quotation_template()

quotation_title = st.text_input(label="件名", value=ss.quotation_template_title)

"""
##### 請求明細
"""

col_editor, col_result = st.columns([0.8, 0.2])

with col_editor:
    ss.quotation_details_df = pd.DataFrame(ss.quotation_details)

    ss.edited_quotation_details_df = st.data_editor(
        ss.quotation_details_df,
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
    ss.df_result = pd.DataFrame({
        "金額": ss.edited_quotation_details_df["単価"] * ss.edited_quotation_details_df["数量"],
        "消費税": ss.edited_quotation_details_df["単価"] * ss.edited_quotation_details_df["数量"] * ss.edited_quotation_details_df["税率"],
    })
    st.dataframe(
        ss.df_result,
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
##### お支払い条件
"""

quotation_delivery_date = st.date_input(label="納期", value=datetime.datetime.today(), key="quatation-delivery-date")

quotation_payment =  st.selectbox(
    label="お支払い条件",
    options=options.payment_conditions,
    key="select-payment-conditions"
)


quotation_remark = st.text_area(label="備考")

col_btn_1, col_btn_2, col_btn_3 = st.columns([0.40, 0.30, 0.30])

with col_btn_1:
    if st.button("請求書PDFプレビュー", use_container_width=True):
        try:
            file_path='/tmp/invoice.pdf'
            generate_invoice_paper(
                invoice_paper=InvoicePaper(
                    issued_at=datetime.datetime.today(),
                    customer=quotation_customer + " 御中",
                    title=quotation_title,
                    delivery_date=quotation_delivery_date,
                    payment=quotation_payment,
                    remark=quotation_remark,
                    account_information=ss.account_information,
                    details=pd.concat(
                        [
                            ss.edited_quotation_details_df,
                            ss.df_result,
                            pd.DataFrame({"備考": [''] * len(ss.edited_quotation_details_df.index)})
                        ], axis=1
                    ),
                    company_name=ss.company_name,
                    company_postal_no=ss.company_postal_no,
                    company_address=ss.company_address,
                    company_tax_no=ss.company_tax_no,
                    company_tel=ss.company_tel,
                    company_mail=ss.company_mail,
                ),
                file_path=file_path
            )

            with open(file_path, "rb") as file:
                st.download_button(
                    label="請求書PDFをダウンロード",
                    data=file,
                    file_name="請求書_%s.pdf" % quotation_title,
                    mime="application/pdf",
                    use_container_width=True,
                )

        except Exception as e:
            st.toast(e)

with col_btn_2:
    if st.button("売掛金計上", type="primary"):
        pass

with col_btn_3:
    pass

# style
st.markdown("""
    <style>
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)
