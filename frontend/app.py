import streamlit as st
import requests
import json
from typing import Optional
import time
import base64

# Configure page
st.set_page_config(
    page_title="PDF RAG Chatbot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
def load_custom_css():
    # Get theme from session state or default to Light
    theme = st.session_state.get('theme', 'Light')
    
    if theme == "Dark":
        st.markdown("""
        <style>
        /* Dark theme styling */
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        
        .main-header {
            background: linear-gradient(135deg, #2c3e50 0%, #4a235a 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            color: white;
            text-align: center;
        }
        
        .card {
            background: #1e293b;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: transform 0.3s ease;
            color: #fafafa;
        }
        
        .user-message {
            background-color: #1e3a8a;
            border-left: 4px solid #3b82f6;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
            animation: slideInLeft 0.3s ease-out;
            color: #fafafa;
        }
        
        .assistant-message {
            background-color: #374151;
            border-left: 4px solid #10b981;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
            animation: slideInRight 0.3s ease-out;
            color: #fafafa;
        }
        
        /* Progress bar styling for dark theme */
        .stProgress > div > div > div {
            background-color: #10b981;
        }
        
        /* Button styling for dark theme */
        .stButton>button {
            background-color: #4f46e5;
            color: white;
            border: 1px solid #6366f1;
        }
        
        .stButton>button:hover {
            background-color: #4338ca;
            border: 1px solid #818cf8;
        }
        
        /* File uploader styling for dark theme */
        .uploadedFile {
            background-color: #1e293b;
            border: 2px dashed #60a5fa;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            color: #fafafa;
        }
        
        /* Document card styling for dark theme */
        .document-card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        /* Light theme styling (default) */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            color: white;
            text-align: center;
        }
        
        .main-header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            animation: fadeIn 1s ease-in;
        }
        
        .main-header p {
            font-size: 1.2rem;
            opacity: 0.9;
            animation: slideUp 1s ease-out;
        }
        
        /* Chat message styling */
        .user-message {
            background-color: #e3f2fd;
            border-left: 4px solid #2196f3;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
            animation: slideInLeft 0.3s ease-out;
        }
        
        .assistant-message {
            background-color: #f5f5f5;
            border-left: 4px solid #4caf50;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
            animation: slideInRight 0.3s ease-out;
        }
        
        /* Button styling */
        .stButton>button {
            border-radius: 10px;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* File uploader styling */
        .uploadedFile {
            background-color: #f0f8ff;
            border: 2px dashed #2196f3;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* Progress bar styling */
        .stProgress > div > div > div {
            background-color: #4caf50;
        }
        
        /* Card styling */
        .card {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }
        
        /* Document card styling */
        .document-card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        /* Status indicators */
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-online {
            background-color: #4caf50;
        }
        
        .status-offline {
            background-color: #f44336;
        }
        
        .status-processing {
            background-color: #ff9800;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.4; }
            100% { opacity: 1; }
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes slideInLeft {
            from { transform: translateX(-20px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes slideInRight {
            from { transform: translateX(20px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        /* Typing indicator */
        .typing-indicator {
            display: flex;
            align-items: center;
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            background-color: #9E9E9E;
            border-radius: 50%;
            margin: 0 2px;
            animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-dot:nth-child(1) { animation-delay: 0s; }
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-5px); }
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .main-header h1 {
                font-size: 2rem;
            }
            
            .main-header p {
                font-size: 1rem;
            }
        }
        </style>
        """, unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000/api"

def upload_pdf_to_api(uploaded_file) -> Optional[dict]:
    """Upload PDF file to the backend API"""
    try:
        files = {"files": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        response = requests.post(f"{API_BASE_URL}/upload", files=files)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Upload failed: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend API. Make sure the server is running.")
        return None
    except Exception as e:
        st.error(f"Upload error: {str(e)}")
        return None

def ask_question_to_api(question: str, top_k: int = 5) -> Optional[dict]:
    """Send question to the backend API"""
    try:
        params = {"query": question}
        response = requests.post(f"{API_BASE_URL}/query", params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Query failed: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend API. Make sure the server is running.")
        return None
    except Exception as e:
        st.error(f"Query error: {str(e)}")
        return None

def stream_ask_question(question: str, top_k: int = 5):
    """Stream question to the backend API"""
    try:
        params = {"query": question}
        with requests.post(f"{API_BASE_URL}/query-stream", params=params, stream=True) as r:
            if r.status_code == 200:
                for chunk in r.iter_content(None, decode_unicode=True):
                    yield chunk
            else:
                st.error(f"Query failed: {r.status_code} - {r.text}")
                yield "Sorry, I couldn't process your question. Please try again."
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend API. Make sure the server is running.")
        yield "Cannot connect to backend API. Please make sure the server is running."
    except Exception as e:
        st.error(f"Query error: {str(e)}")
        yield "Sorry, I couldn't process your question. Please try again."

def check_api_health() -> bool:
    """Check if the backend API is running"""
    try:
        response = requests.get(f"{API_BASE_URL.replace('/api', '')}/docs", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_system_status():
    """Get detailed system status from backend"""
    try:
        response = requests.get(f"{API_BASE_URL}/status", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def typing_indicator():
    """Display a typing indicator"""
    return st.markdown("""
    <div class="typing-indicator">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    </div>
    """, unsafe_allow_html=True)

def display_message(role, content, sources=None):
    """Display a chat message with enhanced styling"""
    if role == "user":
        st.markdown(f'<div class="user-message"><strong>You:</strong> {content}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message"><strong>🤖 Assistant:</strong> {content}', unsafe_allow_html=True)
        if sources:
            with st.expander("📚 View Sources", expanded=False):
                st.write(f"Answer based on {len(sources)} document chunks:")
                for i, source in enumerate(sources, 1):
                    # If source is a dict with text, display it
                    if isinstance(source, dict) and "text" in source:
                        with st.container(border=True):
                            st.write(f"**Source Chunk {i}**")
                            st.info(source.get("text", "No text available."))
                    else:
                        # Fallback for string sources
                        st.markdown(f"{i}. {source}")
        st.markdown("</div>", unsafe_allow_html=True)

def main():
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state variables
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = {}
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat input - must be at the top level, not inside any containers
    user_input = st.chat_input("Ask a question about your documents...")
    
    # Modern header with animations
    st.markdown("""
    <div class="main-header">
        <h1>📚 PDF RAG Chatbot</h1>
        <p>Transform your PDF documents into an interactive knowledge base with AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API health
    api_connected = check_api_health()
    system_status = get_system_status() if api_connected else None
    
    # Initialize top_k with a default value
    top_k = 5
    
    # Create responsive layout
    # Main content area with responsive columns
    main_col, sidebar_col = st.columns([3, 1])
    
    with main_col:
        # Main content area
        st.header("💬 Chat with your Documents")
        
        # Add chat management buttons
        col1, col2 = st.columns([8, 2])
        with col2:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
            # Welcome message
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "Hello! I'm your PDF RAG Chatbot. Upload some PDF documents and ask me questions about them!"
            })
        
        # Display chat messages with enhanced styling in a scrollable container
        chat_container = st.container()
        with chat_container:
            # Create a scrollable area for chat messages
            st.markdown("""
            <div style="height: 500px; overflow-y: auto; border: 1px solid #e0e0e0; border-radius: 10px; padding: 1rem;">
            """, unsafe_allow_html=True)
            
            for message in st.session_state.messages:
                display_message(message["role"], message["content"], message.get("sources"))
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Add a sample questions section
        with st.expander("💡 Sample Questions", expanded=False):
            sample_queries = [
                "What is this document about?",
                "Summarize the main points",
                "What are the key findings?",
                "List the important dates mentioned",
                "Who are the main people discussed?"
            ]
            
            # Responsive grid for sample questions
            cols = st.columns(2)
            for i, query in enumerate(sample_queries):
                with cols[i % 2]:
                    if st.button(f"💬 {query}", key=f"main_sample_{i}", use_container_width=True):
                        st.session_state.sample_query = query
                        st.rerun()
        
        # Handle sample queries
        if 'sample_query' in st.session_state:
            user_input = st.session_state.sample_query
            del st.session_state.sample_query
    
    # Handle chat input (must be at the top level)
    if user_input:
        # Get the current top_k value from session state or default
        top_k = st.session_state.get('top_k', 5)
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message with animation
        display_message("user", user_input)
        
        # Get AI response with streaming
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            
            # Use st.write_stream to display the response dynamically
            response = ""
            for chunk in stream_ask_question(user_input, top_k):
                response += chunk
                response_placeholder.markdown(f'<div class="assistant-message"><strong>🤖 Assistant:</strong> {response}</div>', unsafe_allow_html=True)
            
            # Add the full response to history
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Sidebar
    with sidebar_col:
        st.header("⚙️ Configuration")
        
        # API Status with visual indicator and details
        if api_connected:
            st.markdown('<span class="status-indicator status-online"></span> API Connected', unsafe_allow_html=True)
            if system_status:
                with st.expander("📊 System Details", expanded=False):
                    st.json(system_status)
        else:
            st.markdown('<span class="status-indicator status-offline"></span> API Disconnected', unsafe_allow_html=True)
            st.warning("Please start the backend server to enable full functionality")
        
        # Document Management
        st.markdown("---")
        st.header("📄 Document Management")
        
        # File uploader with enhanced styling
        uploaded_files = st.file_uploader(
            "Upload PDF Documents",
            type=["pdf"],
            accept_multiple_files=True,
            help="Upload one or more PDF files to build your knowledge base"
        )
        
        if uploaded_files:
            # File preview section
            st.markdown(f"<div class='uploadedFile'>📁 {len(uploaded_files)} file(s) selected</div>", unsafe_allow_html=True)
            
            # Show file details
            for uploaded_file in uploaded_files:
                with st.expander(f"📄 {uploaded_file.name}"):
                    file_details = {
                        "Filename": uploaded_file.name,
                        "File size": f"{len(uploaded_file.getvalue()) / 1024:.2f} KB",
                        "File type": uploaded_file.type
                    }
                    st.json(file_details)
            
            if st.button("🚀 Process Documents", type="primary", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                file_progress = st.empty()
                
                total_files = len(uploaded_files)
                total_chunks = 0
                processed_files = []
                failed_files = []
                
                for i, uploaded_file in enumerate(uploaded_files):
                    status_text.markdown(f"**Processing {uploaded_file.name}...**")
                    progress_bar.progress((i + 1) / total_files)
                    file_progress.markdown(f"File {i+1} of {total_files}")
                    
                    result = upload_pdf_to_api(uploaded_file)
                    if result:
                        chunks = result.get('chunks', 0)
                        total_chunks += chunks
                        processed_files.append(uploaded_file.name)
                        # Store info after successful upload
                        st.session_state.processed_files[uploaded_file.name] = {
                            "chunks": chunks,
                            "status": "✅ Processed"
                        }
                        st.success(f"✅ {uploaded_file.name}: {chunks} chunks")
                    else:
                        failed_files.append(uploaded_file.name)
                        st.error(f"❌ Failed to process {uploaded_file.name}")
                
                status_text.markdown("**Processing complete!**")
                file_progress.empty()
                time.sleep(1)
                status_text.empty()
                progress_bar.empty()
                
                # Summary card
                st.markdown(f"""
                <div class="card">
                    <h4>📊 Processing Summary</h4>
                    <p>✅ Successfully processed: {len(processed_files)} files</p>
                    <p>📦 Total chunks created: {total_chunks}</p>
                    {'<p>❌ Failed files: ' + str(len(failed_files)) + '</p>' if failed_files else ''}
                </div>
                """, unsafe_allow_html=True)
                
                if failed_files:
                    st.warning(f"⚠️ Failed to process {len(failed_files)} documents: {', '.join(failed_files)}")

        # Document Dashboard
        st.markdown("---")
        st.header("🗂️ Knowledge Base")
        if not st.session_state.processed_files:
            st.info("Upload PDF documents to start building your knowledge base.")
        else:
            for filename, details in st.session_state.processed_files.items():
                with st.container(border=True):
                    st.subheader(f"📄 {filename}")
                    st.write(f"**Status:** {details['status']}")
                    st.write(f"**Chunks:** {details['chunks']}")
        
        # Query Configuration
        st.markdown("---")
        st.header("🔍 Query Settings")
        top_k = st.slider(
            "Number of relevant chunks",
            min_value=1,
            max_value=10,
            value=st.session_state.get('top_k', 5),
            help="How many document chunks to retrieve for context"
        )
        # Store the value in session state so it can be accessed from main area
        st.session_state['top_k'] = top_k
        
        # Theme selector
        st.markdown("---")
        st.header("🎨 Theme")
        theme = st.selectbox("Select Theme", ["Light", "Dark"], 
                            index=0 if st.session_state.get('theme', 'Light') == 'Light' else 1)
        st.session_state['theme'] = theme
        
        # Enhanced System Info
        st.markdown("---")
        st.header("📊 System Info")
        
        # System status with enhanced visuals
        st.markdown("### 🔄 Status")
        if api_connected:
            st.markdown('<span class="status-indicator status-online"></span> Frontend Active', unsafe_allow_html=True)
            st.markdown('<span class="status-indicator status-online"></span> Backend Connected', unsafe_allow_html=True)
            if system_status and system_status.get("vector_store", {}).get("document_count", 0) > 0:
                st.markdown('<span class="status-indicator status-online"></span> Documents Indexed', unsafe_allow_html=True)
                doc_count = system_status["vector_store"]["document_count"]
                st.info(f"📚 {doc_count} document chunks indexed")
            else:
                st.markdown('<span class="status-indicator status-processing"></span> No Documents Indexed', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-indicator status-offline"></span> Frontend Active', unsafe_allow_html=True)
            st.markdown('<span class="status-indicator status-offline"></span> Backend Disconnected', unsafe_allow_html=True)
            
        st.info(f"🔍 Retrieving {top_k} chunks per query")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("📖 API Documentation", use_container_width=True):
            st.markdown("[Open API Documentation](http://127.0.0.1:8000/docs)")
        
        # Usage tips
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Upload multiple PDFs to build a comprehensive knowledge base
        - Ask specific questions for better results
        - Use the source viewer to see which documents were used
        - Adjust the number of chunks for different response styles
        """)
        
        # Sample queries
        st.markdown("### 🎯 Sample Queries")
        sample_queries = [
            "What is this document about?",
            "Summarize the main points",
            "What are the key findings?",
            "List the important dates mentioned",
            "Who are the main people discussed?"
        ]
        
        for query in sample_queries:
            if st.button(f"💬 {query}", key=f"sample_{query[:10]}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": query})
                st.rerun()

if __name__ == "__main__":
    main()