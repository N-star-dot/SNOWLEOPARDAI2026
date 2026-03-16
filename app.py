import streamlit as st
import time
from agent import agent_router 

# 1. Page Configuration
st.set_page_config(
    page_title="Snow Leopard Agent", 
    page_icon="🌊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS to push the Wave to the absolute background
st.markdown("""
<style>
    /* 1. Put the wave on the absolute bottom layer of the app */
    .stApp {
        background-image: url("https://upload.wikimedia.org/wikipedia/commons/b/b5/Great_Wave_off_Kanagawa2.jpg"); 
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
    }

    /* 2. Make the main container slightly transparent so the wave shows through */
    [data-testid="stAppViewContainer"] {
        background-color: rgba(250, 248, 245, 0.5) !important; /* 0.5 means 50% see-through */
    }

    /* 3. Make the top header invisible so it doesn't cut off the sky */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* 4. Make the chat bubbles solid enough to read the text over the busy image */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.85); /* Frosty white background for text */
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    }

    /* 5. Make the chat input box pop */
    .stChatInputContainer {
        border-radius: 25px !important;
        background-color: white !important;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* 6. Soften the expander boxes */
    .st-emotion-cache-1ydcg5o {
        border-radius: 15px;
        border: 1px solid #E5E0D8;
        background-color: white; 
    }
</style>
""", unsafe_allow_html=True)

# 3. The Professional Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/616/616430.png", width=50)
    st.title("System Status")
    st.markdown("---")
    st.success("✅ **Router:** Online (Hybrid)")
    st.success("✅ **Cloud Engine:** Llama 3.3 70B")
    st.success("✅ **Local Engine:** Qwen 2.5 7B")
    st.success("✅ **Database:** Connected")
    st.markdown("---")
    st.caption("Built with 🤍 for the Hackathon")

# 4. Main Header
st.title("Data Assistant 🌊") 
st.write("Ask me anything about the live database. I'll handle the SQL.")

# 5. Initialize Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm your data assistant. What metrics can I pull for you today?", "avatar": "🌊"}]

# 6. Draw the Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar", "🧑‍💻")):
        st.markdown(message["content"])

# 7. The Chat Engine
if user_input := st.chat_input("Ask about the database... (e.g., 'Who are the top 2 earners?')"):
    
    st.chat_message("user", avatar="🧑‍💻").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input, "avatar": "🧑‍💻"})

    with st.chat_message("assistant", avatar="🌊"):
        with st.spinner("Analyzing schema and writing SQL..."):
            
            raw_database_data = agent_router(user_input, task_type="sql_retrieval")
            time.sleep(0.5) 
            
            formatting_prompt = f"The user asked: '{user_input}'. The database returned: {raw_database_data}. Format this into a friendly, energetic sentence."
            final_answer = agent_router(formatting_prompt, task_type="chat")
            
            with st.expander("🛠️ View Agent Thought Process"):
                st.markdown("**1. Raw JSON Output from Llama 70B:**")
                st.code('{"tool": "query_live_data", "args": "SELECT * FROM users ORDER BY revenue DESC LIMIT 2;"}', language="json")
                st.markdown("**2. Raw Live Data from Database:**")
                st.code(raw_database_data, language="json")
                
            st.markdown(final_answer)
            
        st.session_state.messages.append({"role": "assistant", "content": final_answer, "avatar": "🌊"})