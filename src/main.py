from src.document_processor import DocumentProcessor
from src.vectorstore.faiss_store import FAISSStore
import os
from dotenv import load_dotenv
import streamlit as st
import openai
from src.pipeline import RAGChatbot
from src.memory.memory import MemoryStorage  # Importiere MemoryStorage

# Lädt .env-Datei nur, wenn nicht auf Streamlit Cloud
if (
    not st.secrets
):  # Falls keine Secrets in Streamlit vorhanden sind, dann lade die .env-Datei lokal
    load_dotenv()

# Wenn auf Streamlit Cloud, verwende die Secrets
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    REDIS_URL = st.secrets["REDIS_URL"]
except KeyError:
    # Wenn du lokal arbeitest und keine Secrets vorhanden sind, nimm die Umgebungsvariablen von .env
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    REDIS_URL = os.getenv("REDIS_URL")

# Erstelle Instanzen
index_dir = "temp"
if not os.path.exists(index_dir):
    os.makedirs(index_dir)
faiss_store = FAISSStore(index_file="temp/faiss_index.index")
client = openai

# Initialisiere den MemoryStorage (global)
memory_storage = MemoryStorage(redis_url=REDIS_URL)  # Beispiel: Redis URL

# Initialisiere den RAGChatbot mit FAISSStore, Client und MemoryStorage
chatbot = RAGChatbot(faiss_store, client, memory_storage)


# Dokumentverarbeitung
def process_document(uploaded_file):
    """
    Verarbeitet das Dokument unter Verwendung des DocumentProcessor.
    """
    document_processor = DocumentProcessor(
        openai_api_key=OPENAI_API_KEY, faiss_store=faiss_store, max_chunk_length=1000
    )
    return document_processor.process_document(uploaded_file)


# Benutzeranfragen verarbeiten
def process_user_query(user_query):
    """
    Verarbeitet die Benutzeranfrage und gibt eine Antwort basierend auf den gespeicherten Embeddings zurück.
    """
    # Verwendet die `process_user_input` Methode der `RAGChatbot`-Klasse
    return chatbot.process_user_input(user_query)
