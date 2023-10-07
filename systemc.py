from config import PINECONE_API_KEY, OPENAI_API_KEY
import messagesc

from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings

import pinecone

# LLM
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

# Embeddings initialization
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Vectorstore initialization
pinecone.init(      
	api_key=PINECONE_API_KEY,
	environment='asia-southeast1-gcp-free'      
)      
index = pinecone.Index('tinkoffai')

vectorstore = Pinecone.from_existing_index("tinkoffai", embedding=embeddings)

def new_pipeline(query, chat_history):

    # Similarity search
    docs_raw = vectorstore.similarity_search(query)
    docs = '\n'.join([doc.page_content for doc in docs_raw])

    # Structure a conversation query
    query_args = {
        'documents': docs,
        'history': chat_history,
        'input': query
    }
    query_prompt = messagesc.templates['conversation_prompt'].format(**query_args)
    print(f'query_prompt:\n{query_prompt}\n\n')

    # Inference the model
    result = llm.predict(query_prompt)

    chat_history_new = f'''
    {chat_history[-600:]}
    Ассистент: {result[:40]}...
    Клиент: {query}'''

    return result, chat_history_new

