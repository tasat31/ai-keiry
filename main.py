import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from services.kittings import fiscal_term_settings, company_profile_settings, account_information_settings, background_image_url_settings

st.session_state['background_image_url'] = ''
st.set_page_config(page_title="AI-keiry")

with open('.streamlit/credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# print(stauth.Hasher.hash_passwords(config['credentials']))

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized'],
    auto_hash=False
)

authenticator.login('main', key="login")

if st.session_state['authentication_status'] is True:
    authenticator.logout('logout', 'sidebar')

    # set st.session_state
    st.session_state['fiscal_start_date'], st.session_state['fiscal_end_date'], st.session_state['fiscal_term'] = fiscal_term_settings()
    st.session_state['company_name'], st.session_state['company_postal_no'], st.session_state['company_address'], st.session_state['company_tax_no'], st.session_state['company_tel'], st.session_state['company_mail'] = company_profile_settings()
    st.session_state['account_information'] = account_information_settings()
    st.session_state['background_image_url'] = background_image_url_settings()

    st.sidebar.title("AI-Keiry Insight")
    st.sidebar.caption("Heart Musen LLC 2024")

    pg = st.navigation({
        "Home": [
            st.Page("pages/dashboard.py", title="dashboard", icon=":material/home:"),
            st.Page("pages/marketing/5_business_plan.py", title="事業計画", icon=":material/extension:"),
            st.Page("pages/settings.py", title="設定", icon=":material/settings:"),
            st.Page("pages/chatbot.py", title="チャットボット(お試し)", icon=":material/robot:"),
        ],
        "Marketing":[
            st.Page("pages/marketing/1_leads.py", title="見込み客", icon=":material/add_circle:"),
            st.Page("pages/marketing/6_leads_threads.py", title="見込み客スレッド", icon=":material/add_circle:"),
            st.Page("pages/marketing/2_senarios.py", title="シナリオの作成と実行", icon=":material/extension:"),
            st.Page("pages/marketing/4_projects.py", title="プロジェクト一覧", icon=":material/add_circle:"),
            st.Page("pages/marketing/3_quotations.py", title="見積書の作成", icon=":material/file_open:"),
            st.Page("pages/marketing/7_invoices.py", title="請求書の発行", icon=":material/file_open:"),
        ],
        "Accounting": [
            st.Page("pages/book_keeping/1_Journals.py", title="スマート仕訳", icon=":material/robot:"),
            st.Page("pages/book_keeping/2_Fixed_Asset_List.py", title="固定資産台帳", icon=":material/extension:"),
            st.Page("pages/book_keeping/3_Adjustment.py", title="決算整理仕訳", icon=":material/add_circle:"),
            st.Page("pages/book_keeping/4_Trial_Balance.py", title="合計残高試算表", icon=":material/add_circle:"),
            st.Page("pages/book_keeping/5_Statement.py", title="財務諸表", icon=":material/add_circle:"),
            st.Page("pages/book_keeping/6_Expense_Budget.py", title="予算の作成と管理(経費)", icon=":material/add_circle:"),
        ],
        "Emissions":[
            st.Page("pages/emissions/1_activity_list.py", title="排出源と係数の設定", icon=":material/solar_power:"),
            st.Page("pages/emissions/2_emission_by_activity.py", title="活動別排出量", icon=":material/wind_power:"),
            st.Page("pages/emissions/3_emission_by_project.py", title="プロジェクト別排出量", icon=":material/psychiatry:"),
            st.Page("pages/emissions/4_report.py", title="レポート出力", icon=":material/file_open:"),
        ],
        "Warranties":[
            st.Page("pages/warranties/1_conditions.py", title="保証条件設定", icon=":material/extension:"),
            st.Page("pages/warranties/2_products.py", title="保証製品一覧", icon=":material/extension:"),
        ],
    })
    pg.run()

elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')

# style
st.markdown("""
    <style>
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
        .stApp {
            background-image: url("%s");
            background-color:rgba(255,255,255,0.5);
            background-blend-mode:lighten;
            background-size: cover;
            background-repeat: no-repeat;
        }
        .stApp header {
            background: transparent
        }
    </style>
""" % st.session_state['background_image_url'], unsafe_allow_html=True)
