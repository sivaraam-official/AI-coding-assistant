import streamlit as st
from openai import OpenAI
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Local AI Coding Assistant",
    page_icon="💻",
    layout="wide"
)

# --- INITIALIZE API CLIENT ---
# Points to LM Studio's default local server address
LM_STUDIO_URL = "http://localhost:1234/v1"
MODEL_NAME = "qwen3-8b"  # Ensure this matches the identifier in LM Studio

client = OpenAI(
    base_url=LM_STUDIO_URL,
    api_key="sk-lm-XlKi2wqv:Y7mhkZr2NlOeMEM9P3lZ"  # LM Studio does not require a real key, but a placeholder is needed
)

# --- STATE MANAGEMENT ---
if "messages" not in st.session_state:
    # System prompt guides the LLM to behave like a senior software engineer
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "You are an expert senior AI programming assistant. Provide clean, efficient, and well-commented code. Explain your logic clearly."
        }
    ]

# --- HELPER FUNCTIONS ---
def get_ai_response(prompt_history):
    """Sends the conversation history to LM Studio and streams the response."""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=prompt_history,
            temperature=0.7,
            stream=True
        )
        return response
    except Exception as e:
        st.error(f"Error connecting to LM Studio: {e}")
        st.info("Please verify that LM Studio is running, the local server is started on port 1234, and your model is loaded.")
        return None

def trigger_quick_action(action_prompt, code_context=""):
    """Appends a pre-defined prompt to the chat history and triggers processing."""
    full_prompt = f"{action_prompt}\n\n```python\n{code_context}\n```" if code_context else action_prompt
    st.session_state.messages.append({"role": "user", "content": full_prompt})
    st.rerun()

# --- SIDEBAR INTERFACE ---
with st.sidebar:
    st.title("⚙️ Controls & Features")
    st.markdown("Use these quick actions to analyze or generate code rapidly.")
    
    # 1. File Upload Feature
    st.subheader("📁 Upload Code File")
    uploaded_file = st.file_uploader("Upload a text or code file (.py, .js, .txt, .ts, .java, etc.)", type=[
    "py", "js", "ts", "java", "c", "cpp", "cs",
    "go", "rs", "php", "kt", "swift",
    "html", "css", "sql", "sh", "ps1",
    "txt", "md"
])
    
    uploaded_code = ""
    if uploaded_file is not None:
        try:
            uploaded_code = uploaded_file.read().decode("utf-8")
            st.success(f"Loaded: {uploaded_file.name}")
            st.code(uploaded_code[:300] + ("..." if len(uploaded_code) > 300 else ""), line_numbers=True)
        except Exception as e:
            st.error(f"Could not read file: {e}")

    st.markdown("---")
    
    # 2. Quick Action Buttons
    st.subheader("⚡ Quick Actions")
    
    if st.button("🔍 Explain Code", use_container_width=True):
        if uploaded_code:
            trigger_quick_action("Please provide a detailed line-by-line explanation of this code.", uploaded_code)
        else:
            st.warning("Please upload a file first to use this feature.")
            
    if st.button("🐛 Find Bugs", use_container_width=True):
        if uploaded_code:
            trigger_quick_action("Review this code for bugs, logic flaws, or security vulnerabilities, and provide fixes.", uploaded_code)
        else:
            st.warning("Please upload a file first to use this feature.")
            
    if st.button("🚀 Optimize Code", use_container_width=True):
        if uploaded_code:
            trigger_quick_action("Suggest optimizations to make this code faster, more readable, and more memory-efficient.", uploaded_code)
        else:
            st.warning("Please upload a file first to use this feature.")

    st.markdown("---")
    
# --- MAIN CHAT INTERFACE ---
st.title("💻 AI Coding Assistant")
st.caption(f"Connected to LM Studio Endpoint: `{LM_STUDIO_URL}` | Model: `{MODEL_NAME}`")

# Display previous conversation messages (skipping the system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Handle Chat Input
if user_input := st.chat_input("Ask a coding question or describe the program you want to build..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Save user message to state
    st.session_state.messages.append({"role": "user", "content": user_input})

# Generate AI response if the last message is from the user
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Get streaming output from local server
        stream = get_ai_response(st.session_state.messages)
        
        if stream:
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            # Save assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})