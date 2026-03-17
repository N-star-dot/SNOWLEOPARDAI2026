import streamlit as st
import pandas as pd
import sqlite3
import json
import agent # Imports the logic from agent.py

# --- 1. UI SETUP & THEME ---
st.set_page_config(page_title="The Wave AI", page_icon="🌊", layout="wide")

# The Great Wave Background & Styling
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
/* Make chat bubbles readable over the dark wave */
[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.90);
    border-radius: 10px;
    padding: 10px;
    box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
st.title("🌊 The Wave: Hybrid Neural Agent")

# --- 2. SESSION STATE (Memory) ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dataset_columns" not in st.session_state:
    st.session_state.dataset_columns = "IMDb default columns"
# NEW: Initialize the Neural Toggle memory
if "active_mode" not in st.session_state:
    st.session_state.active_mode = "Cloud (Snow Leopard - IMDb)"

# --- 3. THE LIBRARIAN & NEURAL TOGGLE (Sidebar) ---
with st.sidebar:
    # THE MASTER SWITCH (Neural Toggle)
    st.header("🧠 Neural Mode")
    st.session_state.active_mode = st.radio(
        "Direct the Agent's Focus:",
        ["Cloud (Snow Leopard - IMDb)", "Local (Uploaded CSV - SQLite)"],
        index=0 if "Cloud" in st.session_state.active_mode else 1
    )
    
    st.divider()
    
    # THE LIBRARIAN
    st.header("📂 The Librarian")
    st.markdown("Upload a massive dataset. We process it in chunks and trim excess columns to save memory.")
    
    data_type = st.selectbox("Data Format", ("CSV (Spreadsheet)", "JSON"))
    uploaded_file = st.file_uploader("Drop dataset here", type=["csv", "json"])
    
    if uploaded_file is not None:
        try:
            conn = sqlite3.connect('hackathon_database.db')
            MAX_COLUMNS = 500 # The safety limit for SQLite
            
            if data_type == "CSV (Spreadsheet)":
                chunk_size = 10000
                first_chunk = True
                
                progress_text = st.empty()
                progress_text.text("Processing big data in chunks...")
                
                for chunk in pd.read_csv(uploaded_file, chunksize=chunk_size):
                    if len(chunk.columns) > MAX_COLUMNS:
                        chunk = chunk.iloc[:, :MAX_COLUMNS]
                        
                    if first_chunk:
                        chunk.to_sql('user_data', conn, if_exists='replace', index=False)
                        st.session_state.dataset_columns = ", ".join(chunk.columns.tolist())
                        
                        if len(chunk.columns) == MAX_COLUMNS:
                            st.warning(f"⚠️ Dataset too wide! Trimmed to {MAX_COLUMNS} columns to prevent database crash.")
                            
                        first_chunk = False
                    else:
                        chunk.to_sql('user_data', conn, if_exists='append', index=False)
                
                progress_text.empty() 
                
            else:
                df = pd.read_json(uploaded_file)
                if len(df.columns) > MAX_COLUMNS:
                    df = df.iloc[:, :MAX_COLUMNS]
                    st.warning(f"⚠️ Dataset too wide! Trimmed to {MAX_COLUMNS} columns.")
                    
                df.to_sql('user_data', conn, if_exists='replace', index=False)
                st.session_state.dataset_columns = ", ".join(df.columns.tolist())
            
            st.success("✅ Massive Database Generated!")
            
            with st.expander("Preview Extracted Data"):
                preview_df = pd.read_sql_query("SELECT * FROM user_data LIMIT 5", conn)
                st.dataframe(preview_df)
                
        except Exception as e:
            st.error(f"Upload failed: {e}")

# --- 5. THE ANALYST (Interactive Visualization) ---
st.header("📊 The Analyst: Live Dashboard")

try:
    conn = sqlite3.connect('hackathon_database.db')
    
    check_df = pd.read_sql_query("SELECT 1 FROM user_data LIMIT 1", conn)
    
    if not check_df.empty:
        with st.expander("Open Data Visualization Tools", expanded=True):
            
            columns_df = pd.read_sql_query("PRAGMA table_info(user_data)", conn)
            all_columns = columns_df['name'].tolist()
            
            sample_df = pd.read_sql_query("SELECT * FROM user_data LIMIT 100", conn)
            numeric_columns = sample_df.select_dtypes(include=['number']).columns.tolist()

            col1, col2, col3 = st.columns(3)
            with col1:
                chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot"])
            with col2:
                x_axis = st.selectbox("X-Axis (Categories)", all_columns)
            with col3:
                y_axis = st.selectbox("Y-Axis (Numbers)", numeric_columns)
                
            if st.button("Generate Visualization"):
                st.subheader(f"{y_axis} vs. {x_axis}")
                
                query = f"SELECT `{x_axis}`, `{y_axis}` FROM user_data LIMIT 1000"
                chart_data = pd.read_sql_query(query, conn).set_index(x_axis)
                
                if chart_type == "Bar Chart":
                    st.bar_chart(chart_data)
                elif chart_type == "Line Chart":
                    st.line_chart(chart_data)
                elif chart_type == "Scatter Plot":
                    scatter_df = pd.read_sql_query(query, conn)
                    st.scatter_chart(scatter_df, x=x_axis, y=y_axis)
                    
except Exception as e:
    st.info("Upload a dataset in the sidebar to unlock the visualization dashboard!")
    
st.divider()

# --- 4. THE CHAT INTERFACE ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me to analyze the data, identify an image, or send a report..."):
    
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
            
            # THE UI UPGRADE: Extracting the "Thought" and hiding it!
            try:
                # Find the JSON bracket boundaries just like we did in the parser
                start_idx = raw_decision.find('{')
                end_idx = raw_decision.rfind('}')
                clean_json = raw_decision[start_idx:end_idx+1]
                
                decision_dict = json.loads(clean_json)
                agent_thought = decision_dict.get("thought", "Processing...")
                tool_used = decision_dict.get("tool", "Unknown Tool")
                
                # Hide the thought inside a sleek dropdown bracket
                with st.expander(f"🧠 Agent Thinking... (Routed to: {tool_used})"):
                    st.write(f"**Internal Thought:** {agent_thought}")
                    st.text("Raw JSON Execution:")
                    st.code(clean_json, language="json")
            except:
                # Backup plan if the JSON is completely weird
                with st.expander("⚙️ View Agent Routing Logic"):
                    st.code(raw_decision, language="json")
            
            # Display the final, polished answer outside the bracket!
            st.markdown(final_answer)
            
    st.session_state.messages.append({"role": "assistant", "content": final_answer})