import streamlit as st
from langchain.prompts import PromptTemplate
from ctransformers.langchain import CTransformers

# function to get response from model
def getresponse(input_text,no_words):
    # Load Model from bin file
    llm = CTransformers(model='models/llama-2-7b.ggmlv3.q6_K.bin',
                        model_type='llama',
                        config={'max_new_tokens':256,
                                'temperature':0.01})
    
    # Prompt template
    template = f"""
                Act as an experienced writer. 
                Pay attention to pacing, suspense, and character growth to create a narrative that will keep readers turning the pages and leave a lasting impression.
                Make sure to maintain a consistent tone and writing style that aligns with the rest of the book.
                Make sure the characters are consistent and the interactions between characters maintain a interesting but consistent dynamic.
                Make sure and the plot is cohesive and engaging. 
                End with a cliff hanger that makes a reader want to continue to read.
                Write the next chapter of a book given the previous chapter of the book below.
                ```
                {input_text} 
                ```
                Use the plotline for the next chapter given below to write the next chapter
                ```
                {plotline}
                ```
                Write the chapter in less than {no_words}
                """
    
    # use prompt template
    prompt = PromptTemplate(input_variables = ["input_text","plotline","no_words"],
                            template = template)
    
    # Response
    response = llm(prompt.format(input_text=input_text, plotline = plotline, no_words=no_words))
    print(response)

    return response


# page config
st.set_page_config(page_title="AI Ghost writer",
                   page_icon=':books:',
                   layout='centered',
                   initial_sidebar_state='expanded')

password = st.sidebar.text_input("Password to use the app")

st.header("AI Ghost Writer")

# input from user
input_text=st.text_area("Enter the current chapter of the book", height=5)
plotline=st.text_area("Enter a brief summary of the plotline for the next chapter you want me to write", height=5)
no_words = st.text_input('Maximum number of words for the chapter you want me to write')

submit = st.button("Generate")

if password != st.secrets['APP_PASSWORD']:
    st.warning('Check password', icon="⚠️")
elif submit and password == st.secrets['APP_PASSWORD']: 
    next_chapter_response = getresponse(input_text,plotline,no_words)
    st.header('Next Chapter')
    st.write(next_chapter_response)

