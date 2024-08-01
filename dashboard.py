import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from st_pages import show_pages, Page, Section
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_icon="🧊",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title("Ai-Keiry")

with open('.streamlit/credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

print(config['credentials'])

# print(stauth.Hasher.hash_passwords(config['credentials']))

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized'],
    auto_hash=False
)

show_pages([Page("dashboard.py", "dashboard"),])
authenticator.login('main')

if st.session_state['authentication_status'] is True:
    authenticator.logout('logout', 'sidebar')
    show_pages([
        Page("dashboard.py", "dashboard"),
        Page("pages/book_keeping/1_Journals.py", "Book Keeping", icon=":books:"),
        Page("pages/book_keeping/2_Expense.py", "- 販管理費及び一般管理費"),
        Page("pages/book_keeping/3_Sales_and_Purchase.py", "- 売上と仕入れ"),
        Page("pages/book_keeping/4_Fixed_Asset_List.py", "- 固定資産台帳"),
        Page("pages/book_keeping/5_Adjustment.py", "- 決算整理仕訳"),
        Page("pages/book_keeping/6_Trial_Balance.py", "- 合計残高試算表"),
        Page("pages/book_keeping/7_Statement.py", "- 決算書"),
        Page("pages/book_keeping/8_Cash_Flow.py", "- キャッシュフロー計算書"),
        Page("pages/book_keeping/9_Business_Plan.py", "- 事業計画"),
        Section(name="Marketing", icon=":bird:"),
        Section(name="CO2 emissions", icon=":pig:"),
    ])

elif st.session_state['authentication_status'] is False:
    show_pages([Page("dashboard.py", "dashboard"),])
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    show_pages([Page("dashboard.py", "dashboard"),])
    st.warning('Please enter your username and password')

# style
st.markdown("""
    <style>
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)
