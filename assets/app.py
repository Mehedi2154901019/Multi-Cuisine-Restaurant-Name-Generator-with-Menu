import streamlit as st
from secret_key import key
import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain,LLMChain

##llm setup
os.environ['GROQ_API_KEY']=key
llm=ChatGroq(temperature=0.6,model='openai/gpt-oss-120b') 

#function to invoke request and return response
def get_names_items(cuisine):

    prompt_template_name=PromptTemplate(
        input_variables=['cuisine'],
        template="I want to open a restaurant for {cuisine} food. Suggest me a just a single name, nothing else."
        )
    name_chain=LLMChain(llm=llm,prompt=prompt_template_name,output_key="restaurant_name")

    prompt_template_items=PromptTemplate(
        input_variables=['restaurant_name'],
        template="Suggest me some menu items for {restaurant_name}. Return it as a comma separated list."
        )
    food_chain=LLMChain(llm=llm,prompt=prompt_template_items,output_key="menu_items")

  
    
    final_chain=SequentialChain(
        chains=[name_chain,food_chain],
        input_variables=["cuisine"],
        output_variables=['restaurant_name','menu_items']
    )
    response=final_chain({'cuisine':cuisine})

    return response



#Streamlit app code to show response

st.title("🍽 Multi-Cuisine Restaurant Name Generator with Menu Items")

cuisine=st.sidebar.selectbox("Pick a Cuisine",("Bangladeshi","Mexican","Pakistani","Italian","Turkish","Malaysian","Chinese","French","Japanese","Arabian","Thai","Russian","Lebanese","Egyptian","Indian","Greek","Vietnamese","Korean","Moroccan","Brazilian","Persian","Caribbean","German","American"))


if cuisine:
    
    response= get_names_items(cuisine)
    st.header(response['restaurant_name'].strip())
    menu_items=response['menu_items'].strip().split(",")
    st.write("**Menu Items**")
    for item in menu_items:
        st.write("-", item)
