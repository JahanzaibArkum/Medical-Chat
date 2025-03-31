from langchain.document_loaders import PyPDFLoader, DirectoryLoader  # Loads documents from PDFs and directories
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Splits text into smaller chunks for processing
from langchain.embeddings import HuggingFaceEmbeddings


# Function to extract text data from all PDF files in a specified directory
def load_pdf_file(data):
    # Initialize a DirectoryLoader to scan the directory for PDF files
    loader = DirectoryLoader(
        data,               # Path to the directory containing PDF files
        glob="*.pdf",       # Pattern to match only PDF files
        loader_cls=PyPDFLoader  # Specify PyPDFLoader as the file loader
    )

    # Load all matching PDF files and extract their contents as documents
    documents = loader.load()

    return documents  # Return the extracted documents

# Function to split documents into smaller chunks for processing
def text_split(extracted_data):
    
    
    # Initialize a RecursiveCharacterTextSplitter to split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # Maximum size of each chunk (in characters)
        chunk_overlap=20  # Overlap between chunks to maintain context
    )
    
    # Split the extracted documents into text chunks
    text_chunks = text_splitter.split_documents(extracted_data)

    return text_chunks  # Return the list of text chunks

# Function to download pre-trained embeddings from Hugging Face
def download_hugging_face_embeddings():
    """
    Downloads the 'all-MiniLM-L6-v2' sentence-transformer model from Hugging Face 
    and initializes it for generating text embeddings.

    Returns:
        embeddings: An instance of HuggingFaceEmbeddings to generate vector embeddings.
    """

    # Load the sentence transformer model from Hugging Face for embedding generation
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    return embeddings  # Return the initialized embeddings model

