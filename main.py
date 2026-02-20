from langchain_groq import ChatGroq
import streamlit as st 
from dotenv import load_dotenv
import os 

st.set_page_config(page_title="Chat Bot ",page_icon=":mortar_board",layout="centered")


def build_model(model_name:str):
   
    model = ChatGroq(
        model=model_name,
        max_tokens=400,
        api_key = st.secrets["GROQ_API_KEY"]
    )
    return model

def chat(user_input,model_name):
    model=build_model(model_name)
    response= model.invoke(user_input)
    return response.content

# while True:
#     user_input= input("You :")
#     if user_input.strip().lower() in ["exit","quit"]:
#         break
#     chat(user_input)

st.title("AI Chat Bot ")
st.caption("AI based chat Bot Ask anything")

with st.sidebar:
   st.subheader("Functions to handle ")
   model_name = st.selectbox(label="select Model",options=["llama-3.1-8b-instant","llama-3.3-70b-versatile","openai/gpt-oss-120b","groq/compound-mini"])
   if st.button("clear chat"):
      st.session_state.messages=[]
      st.rerun()
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


      
      
user_query =st.chat_input("Ask anything ")
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("assistant"):
       with st.spinner("Thinking"):
           try:
               response = chat(user_query, model_name)
           except Exception as ex:
               st.markdown("Error while answering",str(ex))
               response = "Sorry, I couldn't process your request."  # fallback
           st.markdown(response)
           st.session_state.messages.append({"role": "assistant", "content": response})
       
