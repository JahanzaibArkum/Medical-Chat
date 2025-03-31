from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os


load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY


extracted_data=load_pdf_file(data='data/')
text_chunks=text_split(extracted_data)
embeddings = download_hugging_face_embeddings()


pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medicalbot"




# Embed each text chunk and upsert the embeddings into the specified Pinecone index
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,  # The list of text chunks to be embedded
    index_name=index_name,  # The name of the Pinecone index where embeddings will be stored
    embedding=embeddings,   # The embedding function/model used to generate vector representations
)