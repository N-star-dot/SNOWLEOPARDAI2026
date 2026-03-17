import streamlit as st
import pandas as pd
import sqlite3
import json
import agent 

# --- 1. UI SETUP & THEME ---
st.set_page_config(page_title="Acumen AI", page_icon="🌊", layout="wide")

# The Great Wave Background & "Glassmorphism" Styling
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://upload.wikimedia.org/wikipedia/commons/b/b5/Great_Wave_off_Kanagawa2.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
/* Comfy Glassmorphism Chat Bubbles */
[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(10px); /* The frosted glass effect */
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0px 8px 16px rgba(0,0,0,0.1);
    border: 1px solid rgba(255, 255, 255, 0.5);
}
/* Minimalist Sidebar styling */
[data-testid="stSidebar"] {
    background-color: rgba(240, 242, 246, 0.95);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
st.title("🌊 Acumen: Hybrid Neural Agent")

# --- 2. MEMORY & STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dataset_columns" not in st.session_state:
    st.session_state.dataset_columns = "IMDb default columns"
if "active_mode" not in st.session_state:
    st.session_state.active_mode = "Cloud (Snow Leopard - IMDb)"

# --- 3. MINIMALIST SIDEBAR (Tabs Setup) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>⚙️ Control Panel</h2>", unsafe_allow_html=True)
    st.write("") # Spacer
    
    # The Tabs to hide complexity
    tab_core, tab_data, tab_tools = st.tabs(["🧠 Core", "📂 Data", "🔌 Tools"])

    # TAB 1: NEURAL ROUTING
    with tab_core:
        st.subheader("Neural Focus")
        st.session_state.active_mode = st.radio(
            "Select Agent Environment:",
            ["Cloud (Snow Leopard - IMDb)", "Local (Uploaded CSV - SQLite)"],
            index=0 if "Cloud" in st.session_state.active_mode else 1,
            label_visibility="collapsed"
        )
        st.caption("Determines which database the agent queries first.")

    # TAB 2: THE LIBRARIAN (Data Ingestion)
    with tab_data:
        st.subheader("Data Ingestion")
        data_type = st.selectbox("Format", ("CSV (Spreadsheet)", "JSON"), label_visibility="collapsed")
        uploaded_file = st.file_uploader("Drop dataset here", type=["csv", "json"])
        
        if uploaded_file is not None:
            try:
                conn = sqlite3.connect('hackathon_database.db')
                MAX_COLUMNS = 500
                
                if data_type == "CSV (Spreadsheet)":
                    chunk_size = 10000
                    first_chunk = True
                    progress_text = st.empty()
                    progress_text.text("Processing chunks...")
                    
                    for chunk in pd.read_csv(uploaded_file, chunksize=chunk_size):
                        if len(chunk.columns) > MAX_COLUMNS:
                            chunk = chunk.iloc[:, :MAX_COLUMNS]
                        if first_chunk:
                            chunk.to_sql('user_data', conn, if_exists='replace', index=False)
                            st.session_state.dataset_columns = ", ".join(chunk.columns.tolist())
                            if len(chunk.columns) == MAX_COLUMNS:
                                st.warning(f"Trimmed to {MAX_COLUMNS} columns.")
                            first_chunk = False
                        else:
                            chunk.to_sql('user_data', conn, if_exists='append', index=False)
                    progress_text.empty() 
                else:
                    df = pd.read_json(uploaded_file)
                    if len(df.columns) > MAX_COLUMNS:
                        df = df.iloc[:, :MAX_COLUMNS]
                    df.to_sql('user_data', conn, if_exists='replace', index=False)
                    st.session_state.dataset_columns = ", ".join(df.columns.tolist())
                
                st.success("Database Active!")
                with st.expander("Preview Local Data"):
                    preview_df = pd.read_sql_query("SELECT * FROM user_data LIMIT 5", conn)
                    st.dataframe(preview_df)
            except Exception as e:
                st.error(f"Upload failed: {e}")
                
        st.divider()
        
        # PREP FOR TEAMMATE: Vision Tool Uploader
        st.subheader("Vision Processor")
        st.file_uploader("Upload Image for Analysis", type=["png", "jpg", "jpeg"])
        st.caption("Powered by YOLO/Gemini Vision")

    # TAB 3: INTEGRATIONS
    with tab_tools:
        st.subheader("Communications")
        st.text_input("Target Phone / Email", placeholder="+1 (555) 000-0000")
        st.caption("Used by the Agent to send automated reports.")

# --- 4. THE ANALYST DASHBOARD ---
try:
    conn = sqlite3.connect('hackathon_database.db')
    check_df = pd.read_sql_query("SELECT 1 FROM user_data LIMIT 1", conn)
    
    if not check_df.empty:
        with st.expander("📊 Open Analyst Dashboard"):
            columns_df = pd.read_sql_query("PRAGMA table_info(user_data)", conn)
            all_columns = columns_df['name'].tolist()
            sample_df = pd.read_sql_query("SELECT * FROM user_data LIMIT 100", conn)
            numeric_columns = sample_df.select_dtypes(include=['number']).columns.tolist()

            col1, col2, col3 = st.columns(3)
            with col1: chart_type = st.selectbox("Chart", ["Bar Chart", "Line Chart", "Scatter Plot"])
            with col2: x_axis = st.selectbox("X-Axis", all_columns)
            with col3: y_axis = st.selectbox("Y-Axis", numeric_columns)
                
            if st.button("Generate Visualization", use_container_width=True):
                query = f"SELECT `{x_axis}`, `{y_axis}` FROM user_data LIMIT 1000"
                chart_data = pd.read_sql_query(query, conn).set_index(x_axis)
                
                if chart_type == "Bar Chart": st.bar_chart(chart_data)
                elif chart_type == "Line Chart": st.line_chart(chart_data)
                elif chart_type == "Scatter Plot": 
                    scatter_df = pd.read_sql_query(query, conn)
                    st.scatter_chart(scatter_df, x=x_axis, y=y_axis)
except Exception:
    pass

st.write("") # Clean spacing

# --- 5. THE CHAT INTERFACE ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me to analyze data, identify an image, or send a report..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Routing query to Groq & Data Sources..."):
            raw_decision, final_answer = agent.ask_agent(
                prompt, 
                st.session_state.messages, 
                st.session_state.dataset_columns,
                st.session_state.active_mode
            )
            
            try:
                start_idx = raw_decision.find('{')
                end_idx = raw_decision.rfind('}')
                clean_json = raw_decision[start_idx:end_idx+1]
                decision_dict = json.loads(clean_json)
                
                agent_thought = decision_dict.get("thought", "Processing...")
                tool_used = decision_dict.get("tool", "Unknown Tool")
                
                with st.expander(f"🧠 Agent Thinking... (Routed to: {tool_used})"):
                    st.write(f"**Internal Thought:** {agent_thought}")
                    st.text("Raw JSON Execution:")
                    st.code(clean_json, language="json")
            except:
                with st.expander("⚙️ View Agent Routing Logic"):
                    st.code(raw_decision, language="json")
            
            st.markdown(final_answer)
            
    st.session_state.messages.append({"role": "assistant", "content": final_answer})