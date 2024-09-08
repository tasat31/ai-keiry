import streamlit as st
import pandas as pd
from services.kittings import fiscal_term_settings, company_profile_settings, account_information_settings, background_image_url_settings

"""
### 各種設定
"""

"""
#### 1. 会計期首日
"""

fiscal_end_date = st.date_input(label="今期の会計期首日", value=st.session_state['fiscal_start_date'], format="YYYY/MM/DD")
st.caption("今期の会計期首日を変更します。会計機能(仕訳検索・入力等)の期首日、期末日が変更されます。")

if st.button(label="設定", key="set-fiscal-start-date"):
    try:
        st.session_state['fiscal_start_date'], st.session_state['fiscal_end_date'], st.session_state['fiscal_term'] = fiscal_term_settings(fiscal_end_date)
        st.toast("%s (%s - %s)" % (st.session_state['fiscal_term'], st.session_state['fiscal_start_date'].strftime("%Y-%m-%d"), st.session_state['fiscal_end_date'].strftime("%Y-%m-%d")))
        st.toast("会計期首日を変更しました。")
    except Exception as e:
        st.write(e)

"""
#### 2. インボイス表示内容
"""

company_name = st.text_input(label="会社名", value=st.session_state['company_name'])
company_postal_no = st.text_input(label="郵便番号", value=st.session_state['company_postal_no'])
company_address = st.text_input(label="住所", value=st.session_state['company_address'])
company_tax_no = st.text_input(label="登録番号", value=st.session_state['company_tax_no'])
company_tel = st.text_input(label="TEL", value=st.session_state['company_tel'])
company_mail = st.text_input(label="Mail", value=st.session_state['company_mail'])

if st.button(label="設定", key="set-company-profile"):
    try:
        st.session_state['company_name'], st.session_state['company_postal_no'], st.session_state['company_address'], st.session_state['company_tax_no'], st.session_state['company_tel'], st.session_state['company_mail'] = company_profile_settings(company_name=company_name, company_postal_no=company_postal_no, company_address=company_address, company_tax_no=company_tax_no, company_tel=company_tel, company_mail=company_mail)
        st.toast("インボイス表示内容を更新しました。")
    except Exception as e:
        st.write(e)

"""
#### 3. 入金口座情報
"""
account_information = st.text_input(label="入金口座情報", value=st.session_state['account_information'])

if st.button(label="設定", key="set-account-information"):
    try:
        st.session_state['account_information'] = account_information_settings(account_information=account_information)
        st.toast("入金口座情報を更新しました。")
    except Exception as e:
        st.write(e)

"""
#### 4. 壁紙URL
"""
background_image_url = st.text_input(label="壁紙URL", value=st.session_state['background_image_url'])

if st.button(label="設定", key="set-background-image-url"):
    try:
        st.session_state['background_image_url'] = background_image_url_settings(background_image_url=background_image_url)
        st.toast("壁紙URLを更新しました。")
    except Exception as e:
        st.write(e)
