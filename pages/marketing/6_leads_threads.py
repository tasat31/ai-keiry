import datetime
import streamlit as st
from streamlit import session_state as ss
from streamlit_modal import Modal
from app.types.lead_thread import LeadThread
from services.leads import lead_id_name_options
from services.lead_threads import find, save

def select_lead():
    ss.leads_threads = []

def post_message(chat: dict):
    message = st.chat_message("assistant")
    message.write("Posted at %s by %s \n\n %s" % (chat["posted_at"], chat["posted_by"], chat["comment"] ))

if 'leads_threads' not in ss:
    ss.leads_threads = []

"""
### 見込み客スレッド
"""

lead_selected = st.selectbox(
    label="見込み客名",
    options=lead_id_name_options(),
    key="select-lead",
    index=None,
    placeholder="選択して下さい",
    format_func=lambda x: x["name"],
    on_change=select_lead
)

if lead_selected:
    lead_threads = find(lead_id=lead_selected["id"])
    if lead_threads is not None:
        ss.leads_threads = lead_threads.array_comments

prompt = st.chat_input("メモを書く")
if prompt:
    ss.leads_threads.append({
        "comment": prompt,
        "posted_by": st.session_state['name'],
        "posted_at": datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
    })

    if (lead_selected is not None):
        save(LeadThread(
            lead_id=lead_selected["id"],
            array_comments=ss.leads_threads,
            array_attachments=[]
        ))

with st.container(height=480):
    for chat in ss.leads_threads:
        post_message(chat)

# style
st.markdown("""
    <style>
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)
