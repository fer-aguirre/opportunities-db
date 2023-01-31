import streamlit as st
import requests
import pandas as pd
import dateutil.parser
from urllib.request import urlopen
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Load models for text generation
tokenizer = AutoTokenizer.from_pretrained("MaRiOrOsSi/t5-base-finetuned-question-answering")
model = AutoModelForSeq2SeqLM.from_pretrained("MaRiOrOsSi/t5-base-finetuned-question-answering")

# Load model for summarizing
summarizer = pipeline("summarization", model="knkarthick/MEETING_SUMMARY")

url = st.text_input('Enter the URL')

if url:
    # Make requests to the specified urls
    response = requests.get(url, verify=False)

    # Return content of the response
    html = response.text

    # Function to remove tags
    def remove_tags(html):
        # parse html content
        soup = BeautifulSoup(html, "html.parser")
        for data in soup(['style', 'script']):
            # Remove tags
            data.decompose()
        # return data by retrieving the tag content
        return ' '.join(soup.stripped_strings)


    # Print the extracted data
    url_text = remove_tags(html)

    # Apply BeautifulSoup module
    soup = BeautifulSoup(urlopen(url))

    # Extract title
    title = soup.title.get_text()

    # Create instance for text2text-generation task
    get_answer = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

    # Define question to answer
    question = 'When is the deadline?'

    # Apply question answering function to text
    deadline = get_answer(f'question: {question}  context: {url_text}', truncation=True, max_length=512)

    deadline_text = deadline[0].get('generated_text')
    # Parse string to datetime object
    date = dateutil.parser.parse(deadline_text)
    # Convert datetime format
    date = date.strftime("%d-%m-%Y")

    summary = summarizer(url_text, truncation=True, max_length=512)

    summary_text = summary[0].get('summary_text')


    # Create a list with data
    data = [title, date, summary_text, url]
    # Create a dataframe object
    df = pd.DataFrame(columns=['title', 'deadline', 'summary', 'url'], data=[data])
    
    def make_clickable(url):
        # target _blank to open new window
        return f'<a target="_blank" href="{url}">{url}</a>'

    # link is the column with hyperlinks
    df['url'] = df['url'].apply(make_clickable)

    df = df.to_html(escape=False)

    st.write(df, unsafe_allow_html=True)
    # st.dataframe(df)