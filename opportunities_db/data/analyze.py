# Import libraries
import dateutil.parser
import pandas as pd
import numpy as np
from urllib.request import Request, urlopen
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
# Import modules
import opportunities_db.data.load as load

# Load data
data_processed = load.data_processed

# Load models for text generation
tokenizer = AutoTokenizer.from_pretrained("MaRiOrOsSi/t5-base-finetuned-question-answering")
model = AutoModelForSeq2SeqLM.from_pretrained("MaRiOrOsSi/t5-base-finetuned-question-answering")
get_answer = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

# Load model for summarizing
summarizer = pipeline("summarization", model="knkarthick/MEETING_SUMMARY")


def extract_text(url: str):
    """
    Function to parse text from url

    url: str
    return: str
    """
    # Disable warning
    disable_warnings(InsecureRequestWarning)
    # Make a request to the specified url
    response = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    # Return content of the response
    html = urlopen(response).read()
    # Parse html content
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
    # Return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)


def extract_title(url: str):
    """
    Function to extract title from url

    url: str
    return: str
    """
    # Make a request to the specified urls
    response = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    # Return content of the response
    html = urlopen(response).read()
    # Parse html content
    soup = BeautifulSoup(html, "html.parser")
    # Extract title
    title = soup.title.get_text()
    # Return title in string format
    return title
    

def extract_deadline(text: str):
    """
    Function to extract deadline from text

    text: str
    return: datetime
    """
    # Define the question
    question = 'When is the deadline for a proposal submission?'
    # Process text to answer the question
    deadline = get_answer(f'question: {question}  context: {text}', truncation=True, max_length=512)
    # Extract deadline from output
    deadline_text = deadline[0].get('generated_text')
    try:
        # Parse string to datetime object
        date = dateutil.parser.parse(deadline_text)
        # Convert datetime format
        date = date.strftime("%d-%m-%Y")
    except Exception:
        date = np.nan
    # Return date in datetime format
    return date


def extract_summary(text: str):
    """
    Function to extract summary from text

    text: str
    return: str
    """
    # Process text to generate a summary
    summary_text = summarizer(text, truncation=True, max_length=512)
    return summary_text[0].get('summary_text')


def read_csv(filename: str):
    """
    Function to read a CSV file and return a dataframe
    """
    return pd.read_csv(filename)

def flatten_list(l: list):
    """
    Function to flatten a list of lists

    l: list
    return: list
    """
    return [item for sublist in l for item in sublist]


def compare_data(df1, df2):
    """
    Function to compare two dataframes and return new rows

    df1: dataframe
    df2: dataframe
    return: list
    """
    df1 = df1['url'].to_frame()
    diff = (pd.concat([df1, df2]).drop_duplicates(keep=False))
    return flatten_list(diff.values.tolist())


def create_dataframe(titles: list, deadlines: list, summaries: list, urls: list):
    """
    Function to create a dataframe from lists

    titles: list
    deadlines: list
    summaries: list
    urls: list

    return: dataframe
    """
    # Create a dataframe object from multiple lists
    return pd.DataFrame(list(zip(titles, deadlines, summaries, urls)), columns=['title', 'deadline', 'summary', 'url'])

