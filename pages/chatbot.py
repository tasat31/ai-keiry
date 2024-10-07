import streamlit as st
import pandas as pd
from ollama import Client

"""
### チャットボット(お試し)

最適な言語モデル(LLM)のご相談、提案を行います。
"""
client = Client(host='http://localhost:11434')

prompt = st.chat_input("ご質問をどうぞ")
if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    
    response = client.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': prompt,
        }],
    )

    with st.chat_message("assistant"):
        st.write(response['message']['content'])
