# Import libraries
import dateutil.parser
from urllib.request import Request, urlopen
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline


# Load models for text generation
tokenizer = AutoTokenizer.from_pretrained("MaRiOrOsSi/t5-base-finetuned-question-answering")
model = AutoModelForSeq2SeqLM.from_pretrained("MaRiOrOsSi/t5-base-finetuned-question-answering")
get_answer = pipeline("text2text-generation", model=model, tokenizer=tokenizer)


# Load model for summarizing
summarizer = pipeline("summarization", model="knkarthick/MEETING_SUMMARY")


def extract_text(url):
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


def extract_title(url):
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
    

def extract_deadline(text):
    """
    Function to extract deadline from text

    text: str
    return: datetime
    """
    # Define the question
    question = 'When is the deadline?'
    # Process text to answer the question
    deadline = get_answer(f'question: {question}  context: {text}', truncation=True, max_length=512)
    # Extract deadline from output
    deadline_text = deadline[0].get('generated_text')
    # Parse string to datetime object
    date = dateutil.parser.parse(deadline_text)
    # Convert datetime format
    date = date.strftime("%d-%m-%Y")
    # Return date in datetime format
    return date


def extract_summary(text):
    """
    Function to extract summary from text

    text: str
    return: str
    """
    # Process text to generate a summary
    summary_text = summarizer(text, truncation=True, max_length=512)
    # Extract summary from output
    summary = summary_text[0].get('summary_text')
    # Return summary in string format
    return summary

