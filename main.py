import streamlit as st
from langchain import PromptTemplate
from langchain_groq import ChatGroq


template = """
    Below is a draft text that may be poorly worded.
    Your goal is to:
    - Properly redact the draft text
    - Convert the draft text to a specified tone
    - Convert the draft text to a specified dialect


    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, \
        cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, \
        car park, trousers, windscreen


    Please start the redaction with a warm introduction. Add the introduction \
        if you need to.
    
    Below is the draft text, tone, and dialect:
    DRAFT: {draft}
    TONE: {tone}
    DIALECT: {dialect}

    YOUR {dialect} RESPONSE:
"""

#PromptTemplate variables definition
prompt = PromptTemplate(
    input_variables=["tone", "dialect", "draft"],
    template=template,
)


#LLM and key loading function
def load_LLM(groq_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = ChatGroq(temperature=.7, groq_api_key=groq_api_key)
    return llm


#Page title and header
st.set_page_config(page_title="Re-write your text")
st.header("Re-write your text")


#Intro: instructions
col1, col2 = st.columns(2)

with col1:
    st.markdown("Re-write your text in different styles.")

with col2:
    st.write("Contact with [AI Accelera](https://aiaccelera.com) to build your AI Projects")


#Input OpenAI API Key
st.markdown("## Enter Your GroqAI API Key")

def get_groq_api_key():
    input_text = st.text_input(label="GroqAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="groq_api_key_input", type="password")
    return input_text

groq_api_key = get_groq_api_key()


# Input
st.markdown("## Enter the text you want to re-write")

def get_draft():
    draft_text = st.text_area(label="Text", label_visibility='collapsed', placeholder="Your Text...", key="draft_input")
    return draft_text

draft_input = get_draft()

if len(draft_input.split(" ")) > 700:
    st.write("Please enter a shorter text. The maximum length is 700 words.")
    st.stop()

# Prompt template tunning options
col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your redaction to have?',
        ('Formal', 'Informal'))
    
with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British'))
    
    
# Output
st.markdown("### Your Re-written text:")

if draft_input:
    if not groq_api_key:
        st.warning('Please insert GroqAI API Key. \
            Instructions [here]()', 
            icon="⚠️")
        st.stop()

    llm = load_LLM(groq_api_key=groq_api_key)

    prompt_with_draft = prompt.format(
        tone=option_tone, 
        dialect=option_dialect, 
        draft=draft_input
    )

    improved_redaction = llm.invoke(prompt_with_draft)

    st.write(improved_redaction.content)
