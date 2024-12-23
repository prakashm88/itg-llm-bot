import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from transformers import pipeline
import requests
from bs4 import BeautifulSoup

# Function to scrape the URLs
def scrape_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = ' '.join([p.get_text() for p in soup.find_all('p')])
    return text

# Function to generate embeddings using Sentence Transformers
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(text):
    return model.encode(text)

# FAISS Indexing
def create_faiss_index(embeddings):
    embeddings_np = np.array(embeddings).astype('float32')
    dimension = embeddings_np.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_np)
    return index

# Example URLs to scrape
urls = [
    "https://docs.oracle.com/en/java/javase/21/migrate/migrating-jdk-8-later-jdk-releases.html#GUID-C2BE0C3C-1EE4-4411-B112-9A360427D638",
    "https://goatswitch.ai/java-21-migration-guide-master-the-upgrade-from-java-8/",
    "https://github.com/spring-projects/spring-batch/wiki/Spring-Batch-5.0-Migration-Guide/",
    "https://github-wiki-see.page/m/micrometer-metrics/tracing/wiki/Spring-Cloud-Sleuth-3.1-Migration-Guide",
    "https://www.springcloud.io/post/2022-11/springboot3-upgrade-guide/#google_vignette&gsc.tab=0",
    "https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide"
]

# Scrape all URLs and create embeddings
all_texts = [scrape_url(url) for url in urls]
embeddings = [get_embeddings(text) for text in all_texts]
faiss_index = create_faiss_index(embeddings)

# Generative model for answering
generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')

def generate_answer(query, context):
    prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"
    response = generator(prompt, max_length=150, num_return_sequences=1)
    return response[0]['generated_text']

# Streamlit UI
st.title("Java & Spring Migration Q&A")

query = st.text_input("Ask a question about Java/Spring migration:")
if query:
    query_embedding = get_embeddings(query)
    query_embedding = np.array([query_embedding]).astype('float32')
    D, I = faiss_index.search(query_embedding, k=1)
    relevant_document = all_texts[I[0][0]]
    answer = generate_answer(query, relevant_document)
    st.write(f"Answer: {answer}")
