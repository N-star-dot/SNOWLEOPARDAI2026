import os
import requests
import json
from groq import Groq

# --- 1. INITIALIZATION ---
# Make sure you run `export GROQ_API_KEY='your_key'` in the VS Code terminal before running this!
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# --- 2. THE TOOLS (The Actions) ---
def execute_snow_leopard_query(sql_query):
    print(f"\n🚀 [SYSTEM: Executing Snow Leopard API] -> {sql_query}")
    # In reality, this makes the live HTTP request to Snow Leopard.
    # For now, we return fake JSON live data to test the pipeline.
    return '[{"user": "Alice", "revenue": 5000}, {"user": "Bob", "revenue": 4200}]'

# --- 3. THE PARSER (The Bridge) ---
def parse_and_execute(llm_response):
    print(f"🧠 [Groq Raw Output]:\n{llm_response}\n")
    
    try:
        # We parse the JSON directly. No more brittle regex parsing!
        decision = json.loads(llm_response)
        tool_name = decision.get("tool")
        arguments = decision.get("args")
        
        print(f"⚙️  [PARSER TRIGGERED] -> Routing to Python function: {tool_name}")
        
        if tool_name == "query_live_data":
            # Physically run the Python function with the SQL the LLM generated
            raw_data = execute_snow_leopard_query(arguments)
            return raw_data
        else:
            return f"Error: Tool '{tool_name}' does not exist."
            
    except json.JSONDecodeError:
        return "[Parser Error] The LLM did not output valid JSON."

# --- 4. THE BRAINS (Local vs Cloud) ---
def ask_local_m4(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {"model": "qwen2.5:7b", "prompt": prompt, "stream": False}
    try:
        response = requests.post(url, json=payload)
        return response.json()["response"]
    except Exception as e:
        return "Error: Is Ollama running in your Mac terminal?"

def ask_cloud(prompt):
    # The system prompt strictly demands a JSON object
    strict_system_prompt = """You are a robotic database routing script. 
    You have access to ONE tool: 'query_live_data'.
    You MUST output a valid JSON object with EXACTLY two keys: "tool" and "args".
    
    EXAMPLE OUTPUT:
    {"tool": "query_live_data", "args": "SELECT * FROM users ORDER BY revenue DESC LIMIT 5;"}
    """

    chat_completion = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": strict_system_prompt},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile", 
        temperature=0.0, # Zero creativity allowed
        response_format={"type": "json_object"} # FORCES the model to only output JSON
    )
    return chat_completion.choices[0].message.content

# --- 5. THE ROUTER (The Orchestrator) ---
def agent_router(user_input, task_type="chat"):
    if task_type == "sql_retrieval":
        print("☁️ Routing to Cloud (Llama 70B) to figure out the database schema...")
        llm_decision = ask_cloud(user_input)
        
        # Pass the LLM's JSON straight into the parser to execute the tool
        live_data = parse_and_execute(llm_decision)
        return live_data
        
    else:
        print("💻 Routing to Local M4 (Qwen 7B) for fast conversational formatting...")
        return ask_local_m4(user_input)

# --- 6. RUNNING THE LOOP ---
if __name__ == "__main__":
    print("\n--- Testing Full Agent Loop ---")
    
    # We ask a complex database question
    user_question = "I need to find the top 5 users by revenue."
    
    # 1. Groq figures out the SQL, outputs JSON, and the parser executes the tool
    retrieved_database_json = agent_router(user_question, task_type="sql_retrieval")
    print(f"📦 [Database Returned]: {retrieved_database_json}\n")
    
    # 2. We send the ugly JSON back to the local M4 model to format it nicely!
    formatting_prompt = f"The user asked: '{user_question}'. The database returned this raw JSON: {retrieved_database_json}. Format this into a friendly, energetic sentence."
    final_answer = agent_router(formatting_prompt, task_type="chat")
    
    print(f"\n✨ FINAL AGENT RESPONSE TO USER:\n{final_answer}\n")