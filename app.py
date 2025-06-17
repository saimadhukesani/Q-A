import streamlit as st
from  langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.llms import Ollama
import os


from dotenv import load_dotenv
load_dotenv()

#Langsmith
os.environ["LangChain_API_Key"]=os.getenv("LangChain_API_Key")
os.environ["Langchain_Tracing_`v2`"]="True"
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")

##promtp template
prompt=ChatPromptTemplate.from_messages(
  [
    ("system","you are an helpful assistent.Please response to the user querries"),
    ("user","Question:{question}")
  ]
)

def generate_responce(question,engine,temperature,max_tocken):
  llm=Ollama(model=engine)
  output_parser=StrOutputParser()
  chain=prompt|llm|output_parser
  answer=chain.invoke({"question":question})
  return answer
## Select the OpenAI model
engine=st.sidebar.selectbox("Select Ollama model", ["mistral","llama3:latest", "deepseek-r1"])

## Adjust response parameter
temperature=st.sidebar.slider ("Temperature", min_value=0.0,max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

 ## MAin interface for user input
st.write("Goe ahead and ask any question")
user_input=st.text_input("You:")

if user_input :
  response=generate_responce(user_input, engine, temperature, max_tokens)
  st.write(response)
else:
  st.write("Please provide the user input")