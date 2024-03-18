from openai import OpenAI
import streamlit as st

# function to get response from model
def getresponse(input_text,plotline,extra_notes,no_words):
    client = OpenAI()
    
    # Prompt template
    template = f"""
                Act as an experienced writer. 
                Pay attention to pacing, suspense, and character growth to create a narrative that will keep readers turning the pages and leave a lasting impression.
                Make sure to maintain a consistent tone and writing style that aligns with the rest of the book.
                Make sure the characters are consistent and the interactions between characters maintain a interesting but consistent dynamic.
                Make sure and the plot is cohesive and engaging. 
                End with a cliff hanger that makes a reader want to continue to read.
                Write the next chapter of a book given the previous chapters of the book below. Use the plotline as well as the extra notes on the characters and scene.
                ```
                {input_text} 
                ```
                Use the plotline given below to write the next chapter.
                ```
                {plotline}
                ```
                Extra notes to set the scene and information about the characters that you should use to write the chapter.
                ```
                {extra_notes}
                ```
                Write the chapter in less than {no_words}
                """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": template},
            {"role": "user", "content": "Can you generate the next chapter of the book using the style and characters of the book given so far and the plotline of the next chapter?"}
        ]
    )
    print(response)

    return response

# page config
st.set_page_config(page_title="AI Ghost writer",
                   page_icon=':books:',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("AI Ghost Writer")

# input from user
input_text=st.text_area("Enter the current chapter of the book", height = 15)
plotline=st.text_area("Enter a brief summary of the plotline for the next chapter you want me to write", height=5)
extra_notes = st.text_area("Extra notes to set the scene and information about the characters that I should use to write the chapter", height=5)
no_words = st.text_input('Maximum number of words for the chapter you want me to write')

submit = st.button("Generate")

if submit:
    with st.status('👩🏾‍🍳 Whipping up your next chapter...', expanded=True) as status:
        next_chapter_response = getresponse(input_text,plotline,extra_notes,no_words)
        st.header('Next Chapter')
        st.write(next_chapter_response.choices[0].message.content)
        # how much is openai costing me?
        st.write('Prompt tokens = ',next_chapter_response.usage.prompt_tokens,' which should be about ',round(next_chapter_response.usage.prompt_tokens/1000000*50,6),'cents ($0.50 per million tokens)')
        st.write('Completion tokens = ',next_chapter_response.usage.completion_tokens,' which should be about ',round(next_chapter_response.usage.completion_tokens/1000000*150,6),'cents ($1.50 per million tokens)')
        st.write('Total approximate cost for this chapter = ',round(next_chapter_response.usage.prompt_tokens/1000000*50+next_chapter_response.usage.completion_tokens/1000000*150,6),' US cents')
