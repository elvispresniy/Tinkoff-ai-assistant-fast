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

def pipeline(query, chat_history):

    summarization = chat_history

    # Расширить запрос пользователя, добавив прошлые запросы
    query_extended = f"{chat_history[-400:]}{query}"
    print(f'\nextended query:\n\n{query_extended}')

    # Поски по эмбэддингу
    documents_raw = vectorstore.similarity_search(query_extended)
    documents = '\n\n'.join([document.page_content for document in documents_raw])

    # Сборка диалога-запроса
    conversation_args = {
        'documents': documents,
        'history': summarization,
        'input': query_extended
    }
    conversation_prompt = messagesc.templates['conversation_prompt'].format(**conversation_args)
    print(f'\nconversation_prompt:\n\n{conversation_prompt}')
    print(f'\nlength of conversation_prompt: {len(conversation_prompt)}')

    # Запрос к модели
    result = llm.predict(conversation_prompt)
    print(f'\nresult:\n\n{result}')

    # Сохранить новую историю диалога
    new_chat_history = f'''
    Клиент: {query}
    Бот-ассистент: {result}'''

    print(f'\nnew_chat_history:\n\n{new_chat_history}\n')

    return result, new_chat_history

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

