import json
import uuid
import requests
import streamlit as st

# Set up page configuration
st.set_page_config(
    page_title="Evoflow",
    layout="wide",
    page_icon="🌊",
)

# Generate or load existing session ID
if "id" not in st.session_state:
    st.session_state.id = str(uuid.uuid4()).lower()


# Title of the app
st.title("Evoflow")

# Sidebar with options
st.sidebar.title("Options")

# LLM selection with markdown
st.sidebar.header("Select LLM")
llms = ["Llama3-70b", "GPT-4o", "Other"]
selected_llm = st.sidebar.selectbox("Choose a Language Model", llms)
st.sidebar.markdown(f"**Selected LLM**: {selected_llm}")

# Tools selection
st.sidebar.header("Select Tools")
tools = ["Calculator", "File Tools", "Web Search"]
selected_tools = st.sidebar.multiselect("Choose Tools", tools)
st.sidebar.markdown(f"**Selected Tools**: {', '.join(selected_tools)}")

# Evo Team members selection
st.sidebar.header("Select Evo Team Members")
team_members = ["Data Analyst", "Research Assistant", "Investment Assistant"]
selected_members = st.sidebar.multiselect("Choose Team Members", team_members)
st.sidebar.markdown(f"**Selected Members**: {', '.join(selected_members)}")

# Knowledge base URL input
st.sidebar.header("Knowledge Base URL")
kb_url = st.sidebar.text_input("Enter Knowledge Base URL", "https://example.com")
st.sidebar.markdown(f"[Knowledge Base URL]({kb_url})")

# PDF upload for knowledge base
st.sidebar.header("Knowledge Base PDF")
uploaded_pdf = st.sidebar.file_uploader("Upload a PDF", type="pdf")

# Display uploaded PDF information
if uploaded_pdf is not None:
    st.sidebar.markdown(f"**Uploaded PDF**: {uploaded_pdf.name}")
else:
    st.sidebar.markdown("**No PDF uploaded**")

# Main chat-like interface (simplified for demo purposes).
# API URL for the new service
API_URL = "https://ositamiles-ai-agent.hf.space/api/v1/prediction/becaf24b-517a-4ebe-b4b8-0c33fa23cf1b"

# Function to query the new API
def query(payload):
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Initialize session state for messages if not already set
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("What is up?"):
    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    # Placeholder for AI response
    with st.spinner(text='Querying the AI agent...'):
        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            payload = {
                "question": prompt,
                "overrideConfig": {
                    "sessionId": st.session_state.id
                }
            }

            # Generate response from the new API
            response = query(payload)

            # Sample JSON output
            json_output = json.dumps(response)
            # Parse the JSON string
            data = json.loads(json_output)
            # Get the value of the "text" field
            text = data.get("text")

            # Display the AI response
            message_placeholder.markdown(text)
            # Append AI message to session state
            st.session_state.messages.append({"role": "assistant", "content": text})
