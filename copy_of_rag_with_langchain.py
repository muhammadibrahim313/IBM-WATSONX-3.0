# -*- coding: utf-8 -*-
"""Copy of RAG_with_Langchain.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HSsvvkn2tMcQgdWC_W_MShk2kJFDgz5S

# Retrieval Augmented Generation (RAG) with Langchain
*Using IBM Granite Models*

## In this notebook
This notebook contains instructions for performing Retrieval Augumented Generation (RAG). RAG is an architectural pattern that can be used to augment the performance of language models by recalling factual information from a knowledge base, and adding that information to the model query. The most common approach in RAG is to create dense vector representations of the knowledge base in order to retrieve text chunks that are semantically similar to a given user query.

RAG use cases include:
- Customer service: Answering questions about a product or service using facts from the product documentation.
- Domain knowledge: Exploring a specialized domain (e.g., finance) using facts from papers or articles in the knowledge base.
- News chat: Chatting about current events by calling up relevant recent news articles.

In its simplest form, RAG requires 3 steps:

- Initial setup:
  - Index knowledge-base passages for efficient retrieval. In this recipe, we take embeddings of the passages using WatsonX, and store them in a vector database.
- Upon each user query:
  - Retrieve relevant passages from the database. In this recipe, we use an embedding of the query to retrieve semantically similar passages.
  - Generate a response by feeding retrieved passage into a large language model, along with the user query.

## Setting up the environment

Ensure you are running python 3.10 in a freshly-created virtual environment.
"""

import sys
assert sys.version_info >= (3, 10) and sys.version_info < (3, 12), f"Use Python 3.10 or 3.11 to run this notebook."

"""### Install dependencies

Granite Kitchen comes with a bundle of dependencies that are required for notebooks. See the list of packages in its [`setup.py`](https://github.com/ibm-granite-community/granite-kitchen/blob/main/setup.py).
"""

! pip install git+https://github.com/ibm-granite-community/utils \
    "langchain_community<0.3.0" \
    langchain-huggingface \
    langchain-milvus \
    replicate \
    wget

"""## Selecting System Components

### Choose your Embeddings Model

Specify the model to use for generating embedding vectors from text.

To use a model from a provider other than Huggingface, replace this code cell with one from [this Embeddings Model recipe](https://github.com/ibm-granite-community/utils/blob/main/recipes/Components/Langchain_Embeddings_Models.ipynb).
"""

from langchain_huggingface import HuggingFaceEmbeddings
embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

"""### Choose your Vector Database

Specify the database to use for storing and retrieving embedding vectors.

To connect to a vector database other than Milvus substitute this code cell with one from [this Vector Store recipe](https://github.com/ibm-granite-community/utils/blob/main/recipes/Components/Langchain_Vector_Stores.ipynb).
"""

from langchain_milvus import Milvus
import uuid

db_file = f"/tmp/milvus_{str(uuid.uuid4())[:8]}.db"
print(f"The vector database will be saved to {db_file}")

vector_db = Milvus(embedding_function=embeddings_model, connection_args={"uri": db_file}, auto_id=True)

"""### Choose your LLM
The LLM will be used for answering the question, given the retrieved text.

Select a Granite Code model from the [`ibm-granite`](https://replicate.com/ibm-granite) org on Replicate. Here we use the Replicate Langchain client to connect to the model.

To connect to a model on a provider other than Replicate, substitute this code cell with one from the [LLM component recipe](https://github.com/ibm-granite-community/granite-kitchen/blob/main/recipes/Components/Langchain_LLMs.ipynb).
"""

from langchain_community.llms import Replicate
from ibm_granite_community.notebook_utils import get_env_var, set_env_var

model = Replicate(
    model="ibm-granite/granite-3.0-8b-instruct",
    replicate_api_token=get_env_var('REPLICATE_API_TOKEN'),
)

"""## Building the Vector Database

In this example, we take the State of the Union speech text, split it into chunks, derive embedding vectors using the embedding model, and load it into the vector database for querying.

### Download the document

Here we use President Biden's State of the Union address from March 1, 2022.
"""

import os, wget

filename = 'state_of_the_union.txt'
url = 'https://raw.github.com/IBM/watson-machine-learning-samples/master/cloud/data/foundation_models/state_of_the_union.txt'

if not os.path.isfile(filename):
  wget.download(url, out=filename)

"""### Split the document into chunks

Split the document into text segments that can fit into the model's context window.
"""

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

loader = TextLoader(filename)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

"""### Populate the vector database

NOTE: Population of the vector database may take over a minute depending on your embedding model and service.
"""

vector_db.add_documents(texts)

"""## Querying the Vector Database

### Conduct a similarity search

Search the database for similar documents by proximity of the embedded vector in vector space.
"""

query = "What did the president say about Ketanji Brown Jackson"
docs = vector_db.similarity_search(query)
print(docs[0].page_content)

"""## Answering Questions

### Automate the RAG pipeline

Build a RAG chain with the model and the document retriever.
"""

from langchain.prompts import PromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Create a prompt template for question-answering with the retrieved context.
prompt_template = """<|start_of_role|>user<|end_of_role|>Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {input}<|end_of_text|>
<|start_of_role|>assistant<|end_of_role|>"""

# Assemble the retrieval-augmented generation chain.
qa_chain_prompt = PromptTemplate.from_template(prompt_template)
combine_docs_chain = create_stuff_documents_chain(model, qa_chain_prompt)
rag_chain = create_retrieval_chain(vector_db.as_retriever(), combine_docs_chain)

"""### Generate a retrieval-augmented response to a question

Use the RAG chain to process a question. The document chunks relevant to that question are retrieved and used as context.
"""

output = rag_chain.invoke({"input": "What did the president say about Ketanji Brown Jackson?"})

print(output['answer'])