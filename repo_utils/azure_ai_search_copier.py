from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

AZURE_SEARCH_ENDPOINT_SOURCE = ""
AZURE_SEARCH_KEY_SOURCE = ""
SOURCE_INDEX_NAME = ""
credential_source = AzureKeyCredential(AZURE_SEARCH_KEY_SOURCE)

AZURE_SEARCH_ENDPOINT_TARGET = ""
AZURE_SEARCH_KEY_TARGET = ""
TARGET_INDEX_NAME = ""
credential_target = AzureKeyCredential(AZURE_SEARCH_KEY_TARGET)

# Clients
index_client_source = SearchIndexClient(
    endpoint=AZURE_SEARCH_ENDPOINT_SOURCE, credential=credential_source
)
source_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT_SOURCE,
    index_name=SOURCE_INDEX_NAME,
    credential=credential_source,
)

index_client_target = SearchIndexClient(
    endpoint=AZURE_SEARCH_ENDPOINT_TARGET, credential=credential_target
)
target_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT_TARGET,
    index_name=TARGET_INDEX_NAME,
    credential=credential_target,
)

# Step 1: Copy index schema
if TARGET_INDEX_NAME not in [i.name for i in index_client_target.list_indexes()]:
    print(f"Creating target index: {TARGET_INDEX_NAME}")
    source_index = index_client_source.get_index(name=SOURCE_INDEX_NAME)
    source_index.name = TARGET_INDEX_NAME
    index_client_target.create_index(source_index)
else:
    print(f"Target index {TARGET_INDEX_NAME} already exists")

# Step 2: Copy documents with pagination
print("Fetching documents from source index...")

documents = []
results = source_client.search(search_text="*", top=1000, include_total_count=True)

while True:
    page_docs = [doc for doc in results]
    documents.extend(page_docs)

    print(f"Fetched {len(page_docs)} documents, total so far: {len(documents)}")

    if len(page_docs) == 0:
        break

    # Continue fetching the next page
    results = source_client.search(
        search_text="*", top=1000, skip=len(documents), include_total_count=True
    )


BATCH_SIZE = 1000
for i in range(0, len(documents), BATCH_SIZE):
    batch = documents[i : i + BATCH_SIZE]
    print(f"Uploading documents {i} to {i + len(batch) - 1}")
    try:
        target_client.upload_documents(documents=batch)
    except HttpResponseError as e:
        print(f"Failed batch at {i}: {e}")
