# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "jupyter",
# META     "jupyter_kernel_name": "python3.11"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "ba9002d3-d37b-4928-b817-a4c94b5f5f1b",
# META       "default_lakehouse_name": "sysk_bronze_lh",
# META       "default_lakehouse_workspace_id": "d8c3bddb-d4a7-4056-9295-d33e7f331d87",
# META       "known_lakehouses": [
# META         {
# META           "id": "ba9002d3-d37b-4928-b817-a4c94b5f5f1b"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Stuff You Should Know Data Processing

# MARKDOWN ********************

# ## Notebook Setup

# CELL ********************

# Install libraries
%pip install azure-search-documents openai tiktoken

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# Import libraries
import requests
from datetime import datetime
import os
import notebookutils as nb
import xml.etree.ElementTree as ET
import re
import notebookutils
from datetime import datetime
from bs4 import BeautifulSoup
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import notebookutils
from openai import AzureOpenAI
import tiktoken
import time
import json
import sys

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ## Incrementally load data to bronze Fabric Lakehouse

# CELL ********************

def clean_date(date:str) -> str:
    dt = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z')
    return dt.date().isoformat()

def clean_description(description:str) -> str:
    try:
        soup = BeautifulSoup(description, 'html.parser')
        first_p_text = soup.find('p').get_text()

        return first_p_text

    except Exception as e:
        return description

def process_podcast_item(item) -> dict:
    
    load_date = str(datetime.now())
    title = item.find('title').text

    publish_date = item.find('pubDate').text
    publish_date = clean_date(publish_date)

    description = item.find('description').text
    description = clean_description(description)

    transcript_url = item.find('podcast:transcript[@type="text/plain"]', namespaces)
    transcript = requests.get(transcript_url.attrib["url"]).text

    episode_json = {
                    "guid":guid,
                    "title":title,
                    "publish_date":publish_date,
                    "description":description,
                    "transcript":transcript,
                    "datalake_load_date": load_date
                    }

    return episode_json

def save_json_file(data, path) -> None:
    j = json.dumps(data)
    with open(path, "w") as f:
        f.write(j)
        f.close()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# Incrementally processes the RSS feed for new json files

# Fabric raw_episode_json files
fabric_json_files = notebookutils.fs.ls('/lakehouse/default/Files/raw_episode_json')
fabric_json_guids = [file.name.split('.json')[0] for file in fabric_json_files]

# Define the RSS feed URL
rss_url = 'https://www.omnycontent.com/d/playlist/e73c998e-6e60-432f-8610-ae210140c5b1/A91018A4-EA4F-4130-BF55-AE270180C327/44710ECC-10BB-48D1-93C7-AE270180C33E/podcast.rss'
rss_response = requests.get(rss_url)
root = ET.fromstring(rss_response.content)

namespaces = {
    'podcast': 'https://podcastindex.org/namespace/1.0',
    'omny': 'https://omny.fm/rss-extensions'
}

# Each podcast is an item element
items = root.findall('.//item')

# Only process and save files that are new
iter = 0
total_len = len(items)
for item in items:
    iter += 1

    guid = item.find('omny:clipId', namespaces).text

    if guid in fabric_json_guids:
        print(f'Skipped {iter} / {total_len}', end='\r', flush=True)

    else:
        try:
            episode_data = process_podcast_item(item)
            transcript_file_path = f'/lakehouse/default/Files/raw_episode_json/{guid}.json'
            save_json_file(episode_data, transcript_file_path)
            print(f'Saved new {iter} / {total_len}', end='\r', flush=True)

        except Exception as e:
            print(f'Passing {iter} / {total_len} error: {e}')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ## Incrementally chunk and embed json data

# CELL ********************

# Set up Azure OpenAI Client
api_key = notebookutils.credentials.getSecret('syskakv','aoai')

aoai_client = AzureOpenAI(
    azure_endpoint='https://ai-foundry-hub-sysk.openai.azure.com/',
    api_key=api_key,
    api_version="2024-02-01"
)

# Generate embeddings function
def generate_embeddings(text:str) -> list:

    response = aoai_client.embeddings.create(
        model='text-embedding-ada-002',
        input=text
    )

    return response.data[0].embedding
    
def generate_chunks_from_text(text: str, max_tokens: int = 2000, overlap: int = 200) -> list[str]:
    # Load the tokenizer for your embedding model (this uses cl100k_base for most OpenAI models)
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)

    chunks = []
    start = 0
    while start < len(tokens):
        end = start + max_tokens
        chunk_tokens = tokens[start:end]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)
        start += max_tokens - overlap  # slide window with overlap

    return chunks

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

fabric_raw_json_files = notebookutils.fs.ls('/lakehouse/default/Files/raw_episode_json')

fabric_json_processed_files = notebookutils.fs.ls('/lakehouse/default/Files/processed_episode_json')
fabric_processed_json_guids = [file.name.split('_')[0] for file in fabric_json_processed_files]

total_len = len(fabric_raw_json_files)

documents = []
iter = 0
for file in fabric_raw_json_files:
    iter += 1

    guid = file.name.split('.json')[0]

    if guid in fabric_processed_json_guids:
         print(f'Skipped {iter} / {total_len}', end='\r', flush=True)

    else:
        start_time = time.time()

        with open(file.path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        episode_title = json_data['title']
        publish_date = json_data['publish_date']
        description = json_data['description']
        transcript = json_data['transcript']

        transcript = json_data['transcript']
        chunks = generate_chunks_from_text(transcript)

        i = 0
        for chunk in chunks:
            chunk_id = f'{i:03d}'
            chunk_embedding = generate_embeddings(chunk)

            document = {
                "id": f'{guid}_{chunk_id}',
                "title": episode_title,
                "publish_date": publish_date,
                "description": description,
                "transcript": chunk,
                "embedding": chunk_embedding
            }

            documents.append(document)
            file_save_path = f'/lakehouse/default/Files/processed_episode_json/{guid}_{chunk_id}.json'
            save_json_file(document, file_save_path)

            i += 1

        duration = time.time() - start_time
        print(f'Saved new {iter} / {total_len} | Time: {duration:.2f}s')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ## Incrementally upload chunked json to Azure AI Search service

# CELL ********************

# Set up Azure AI Search Client
api_key = notebookutils.credentials.getSecret('syskakv','ai-search')

endpoint = 'https://ai-search-syskai.search.windows.net'
index_name = 'sysk_episode_transcripts'

search_client = SearchClient(endpoint=endpoint,
                      index_name=index_name,
                      credential=AzureKeyCredential(api_key))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

def get_payload_size(docs) -> int:
    """Estimate payload size in bytes."""
    return sys.getsizeof(json.dumps({"value": docs}))

def batch_documents(documents, max_payload_bytes=16 * 1024 * 1024, max_docs_per_batch=1000) -> None:
    """Yield batches that respect Azure AI Search limits."""
    batch = []
    current_size = 0

    for doc in documents:
        doc_json = json.dumps(doc)
        doc_size = sys.getsizeof(doc_json)

        if (current_size + doc_size > max_payload_bytes) or (len(batch) >= max_docs_per_batch):
            yield batch
            batch = []
            current_size = 0

        batch.append(doc)
        current_size += doc_size

    if batch:
        yield batch

def check_document_in_azure_ai_search(document_id:str) -> str:
    try:
        doc = search_client.get_document(key=document_id)
        return True
    except Exception as e:
        return False

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# Incrementally load documents to Azure AI Search
fabric_json_processed_files = notebookutils.fs.ls('/lakehouse/default/Files/processed_episode_json')

documents = []
total_len = len(fabric_json_processed_files)
iter = 1
for file in fabric_json_processed_files:
    file_name = file.name.split('.')[0]

    if(check_document_in_azure_ai_search(file_name)):
        pass

    # Upload Document not found in Azure AI Search
    else:

        try:
            with open(file.path, 'r') as f:
                data = json.load(f)
            
            documents.append(data)

            print(f'Parsed document: {iter}/{total_len}', end='\r', flush=True)

        except:
            print('Document could not be parsed')

    iter += 1


for i, batch in enumerate(batch_documents(documents)):
    result = search_client.upload_documents(documents=batch)
    print(f"Batch {i+1} uploaded - Success Count {len([r.succeeded for r in result])} / {len(documents)}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }
