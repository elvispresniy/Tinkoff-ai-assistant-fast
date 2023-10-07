FROM python:3.11.4

WORKDIR /app

COPY . /app

RUN pip install requests langchain tiktoken flask openai pinecone-client

EXPOSE 8080

ENV NAME World

CMD ["python", "appc.py"]
