import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from services.kittings import fiscal_term_settings

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

    pg = st.navigation({
        "Home": [
            st.Page("pages/dashboard.py", title="dashboard", icon=":material/home:"),
            st.Page("pages/settings.py", title="設定", icon=":material/settings:")
        ],
        "Marketing":[
            st.Page("pages/marketing/1_leads.py", title="見込み客", icon=":material/add_circle:"),
            st.Page("pages/marketing/2_senarios.py", title="シナリオの作成と実行", icon=":material/add_circle:"),
            st.Page("pages/marketing/3_quotations.py", title="見積書の作成", icon=":material/add_circle:"),
            st.Page("pages/marketing/4_projects.py", title="プロジェクト一覧", icon=":material/add_circle:"),
            st.Page("pages/marketing/5_business_plan.py", title="事業計画", icon=":material/add_circle:"),
        ],
        "Accounting": [
            st.Page("pages/book_keeping/1_Journals.py", title="仕訳と元帳", icon=":material/add_circle:"),
            st.Page("pages/book_keeping/4_Fixed_Asset_List.py", title="固定資産台帳", icon=":material/add_circle:"),
            st.Page("pages/book_keeping/5_Adjustment.py", title="決算整理仕訳", icon=":material/add_circle:"),
            st.Page("pages/book_keeping/6_Trial_Balance.py", title="合計残高試算表", icon=":material/add_circle:"),
            st.Page("pages/book_keeping/7_Statement.py", title="財務諸表", icon=":material/add_circle:"),
        ],
        "Emissions":[
            st.Page("pages/emissions/1_activity_list.py", title="排出源と係数の設定", icon=":material/add_circle:"),
            st.Page("pages/emissions/2_emission_by_activity.py", title="活動別排出量", icon=":material/add_circle:"),
            st.Page("pages/emissions/3_emission_by_project.py", title="プロジェクト別排出量", icon=":material/add_circle:"),
            st.Page("pages/emissions/4_report.py", title="レポート出力", icon=":material/add_circle:"),
        ],
        "Warranties":[
            st.Page("pages/warranties/1_conditions.py", title="保証条件設定", icon=":material/add_circle:"),
            st.Page("pages/warranties/2_products.py", title="保証製品一覧", icon=":material/add_circle:"),
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
    </style>
""", unsafe_allow_html=True)
