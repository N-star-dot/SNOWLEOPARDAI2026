import os
import requests
import json
import sqlite3
import base64
import pandas as pd
from datetime import datetime
import groq
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# --- TOOLS ---

def execute_snow_leopard_query(query):
    file_id = os.environ.get("SNOW_LEOPARD_FILE_ID")
    api_key = os.environ.get("SNOW_LEOPARD_API_KEY")
    
    if not file_id or not api_key:
        return "Error: Snow Leopard keys are not exported in the terminal."

    url = f"https://try.snowleopard.ai/api/v1/datafiles/{file_id}/chat/"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"message": query}
    
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=15)
        r.raise_for_status()
        return r.json().get("response", "No data found in the response.")
    except requests.exceptions.Timeout:
        return "Error: Snow Leopard API request timed out after 15 seconds."
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Snow Leopard Server: {e}"

def execute_vision_tool(image_b64, user_prompt="Describe this image in detail.", mime_type="image/jpeg"):
    """Sends a base64-encoded image to Groq's vision model for analysis."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_b64}",
                            },
                        },
                    ],
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.3,
            max_tokens=1024,
        )
        return chat_completion.choices[0].message.content
    except groq.RateLimitError:
        return "Error: Groq API rate limit exceeded. Please wait a moment and try again."
    except groq.APIConnectionError:
        return "Error: Failed to connect to Groq API. Please check your internet connection."
    except groq.GroqError as e:
        return f"Error: Groq Vision API error: {e}"
    except Exception as e:
        return f"Vision analysis error: {e}"

def execute_video_tool(video_bytes, user_prompt="Analyze this video and describe what you see."):
    """Extracts key frames from an MP4 video and analyzes them with the vision model."""
    import tempfile, subprocess, glob, os as _os
    import shutil
    frames_analyzed = []
    
    tmpdir = None
    try:
        tmpdir = tempfile.mkdtemp()
        video_path = _os.path.join(tmpdir, "input.mp4")
        with open(video_path, "wb") as f:
            f.write(video_bytes)
        
        # Extract 1 frame per second using ffmpeg
        frame_pattern = _os.path.join(tmpdir, "frame_%03d.jpg")
        try:
            subprocess.run(
                ["ffmpeg", "-i", video_path, "-vf", "fps=1", "-frames:v", "5", frame_pattern, "-y"],
                capture_output=True, timeout=20, check=True
            )
        except subprocess.TimeoutExpired:
            return "⚠️ Video processing timed out. The video might be too long or complex."
        except subprocess.CalledProcessError as e:
            return f"⚠️ Video processing failed (ffmpeg error): {e.stderr.decode('utf-8', errors='ignore')}"
        
        frame_files = sorted(glob.glob(_os.path.join(tmpdir, "frame_*.jpg")))
        
        if not frame_files:
            return "⚠️ Could not extract any readable frames from the video."
        
        for i, frame_path in enumerate(frame_files[:5]):
            with open(frame_path, "rb") as f:
                frame_b64 = base64.b64encode(f.read()).decode("utf-8")
            
            result = execute_vision_tool(
                frame_b64,
                f"This is frame {i+1} of a video. {user_prompt}",
                mime_type="image/jpeg"
            )
            frames_analyzed.append(f"**Frame {i+1}:** {result}")
        
        if frames_analyzed:
            header = f"🎬 **Video Analysis** ({len(frames_analyzed)} frames analyzed)\n\n"
            return header + "\n\n---\n\n".join(frames_analyzed)
        else:
            return "No frames could be analyzed successfully."
            
    except FileNotFoundError:
        return "⚠️ `ffmpeg` is not installed. Install it with `brew install ffmpeg` to enable video analysis."
    except Exception as e:
        return f"Video analysis processing error: {e}"
    finally:
        if tmpdir and _os.path.exists(tmpdir):
            shutil.rmtree(tmpdir, ignore_errors=True)

def execute_messaging_tool(content, recipient):
    """Simulated messaging — formats a professional report dispatch."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (
        f"✅ **Message Dispatched Successfully**\n\n"
        f"| Field | Details |\n"
        f"|---|---|\n"
        f"| **Recipient** | `{recipient}` |\n"
        f"| **Timestamp** | {timestamp} |\n"
        f"| **Status** | Delivered |\n\n"
        f"**Message Content:**\n> {content}"
    )

# Executes real SQL generated by Groq
def execute_local_sqlite_query(sql_query):
    conn = None
    try:
        conn = sqlite3.connect('hackathon_database.db', timeout=10)
        
        if "SELECT" not in sql_query.upper() and "PRAGMA" not in sql_query.upper():
            return "Error: Only SELECT queries or PRAGMA commands are permitted for local data analysis."
            
        df = pd.read_sql_query(sql_query, conn)
        
        if df.empty:
            return "Query executed successfully, but returned 0 rows. The data might not match your conditions."
        
        # Stop massive tables from blowing up Groq's token limit
        if len(df) > 50:
            df = df.head(50)
            
        return f"Raw Database Results:\n{df.to_markdown()}"
    except (sqlite3.OperationalError, pd.io.sql.DatabaseError) as e:
        return f"SQL Syntax or Database Error (The AI may have hallucinated a column): {e}"
    except Exception as e:
        return f"Unexpected Error executing SQL: {e}"
    finally:
        if conn:
            conn.close()

# --- SQL HEALING LOOP ---
def execute_sql_with_healing(sql_query, available_columns="Unknown"):
    """
    Wraps SQL execution with a self-healing retry loop.
    If the query fails, feeds the error back to Llama 3.3 to rewrite it.
    Max 2 retry attempts before failing gracefully.
    """
    MAX_RETRIES = 2
    current_query = sql_query

    for attempt in range(MAX_RETRIES + 1):
        result = execute_local_sqlite_query(current_query)

        # Check if the result is an error that can be healed
        is_error = isinstance(result, str) and any(
            result.startswith(prefix) for prefix in [
                "SQL Syntax",
                "Error:",
                "Unexpected Error",
            ]
        )

        if not is_error:
            return result  # Success — pass through

        # If we've exhausted retries, fail gracefully
        if attempt >= MAX_RETRIES:
            return (
                "I attempted to query your data but encountered a persistent error "
                "after multiple attempts. This may be due to a mismatch between the "
                "question and the available data columns. "
                f"Available columns are: {available_columns}. "
                "Please try rephrasing your question."
            )

        # --- Hidden healing loop: ask Llama 3.3 to fix the query ---
        healing_prompt = (
            f"You are a SQL repair assistant. The following SQLite query failed:\n\n"
            f"```sql\n{current_query}\n```\n\n"
            f"The error was:\n{result}\n\n"
            f"The table is named 'user_data' and has these columns: {available_columns}.\n\n"
            f"Rewrite the query to fix the error. Output ONLY the corrected SQL query, "
            f"no explanation, no markdown fences."
        )

        try:
            repair_response = client.chat.completions.create(
                messages=[{"role": "user", "content": healing_prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.0,
            )
            repaired_query = repair_response.choices[0].message.content.strip()
            # Strip markdown fences if the model wraps them anyway
            if repaired_query.startswith("```"):
                repaired_query = repaired_query.strip("`").strip()
                if repaired_query.lower().startswith("sql"):
                    repaired_query = repaired_query[3:].strip()
            current_query = repaired_query
        except Exception:
            # If the healing call itself fails, return the original error
            return result


# --- THE PARSER ---
def parse_and_execute(llm_response, image_b64=None, video_bytes=None, available_columns="Unknown"):
    try:
        # Robust JSON extraction: find outermost braces to handle markdown wrappers
        _start = llm_response.find('{')
        _end = llm_response.rfind('}')
        if _start != -1 and _end > _start:
            clean_json_string = llm_response[_start:_end + 1]
        else:
            clean_json_string = llm_response
            
        decision = json.loads(clean_json_string)
        tool = decision.get("tool") or decision.get("name")
        args = decision.get("args") or decision.get("parameters", {})
        
        if tool == "query_live_data":
            return tool, execute_snow_leopard_query(args.get("query", ""))
        elif tool == "query_local_data":
            return tool, execute_sql_with_healing(args.get("sql_query", args.get("query", "")), available_columns)
        elif tool == "analyze_image":
            if image_b64:
                prompt = args.get("prompt", "Describe this image in detail and extract any data or text visible.")
                return tool, execute_vision_tool(image_b64, prompt)
            else:
                return tool, "Error: No image is currently uploaded. Please upload an image in the 📂 Data tab first."
        elif tool == "analyze_video":
            if video_bytes:
                prompt = args.get("prompt", "Analyze this video and describe what you see.")
                return tool, execute_video_tool(video_bytes, prompt)
            else:
                return tool, "Error: No video is currently uploaded. Please upload a video in the 📂 Data tab first."
        elif tool == "send_message":
            return tool, execute_messaging_tool(args.get("msg", args.get("content", "")), args.get("to", args.get("recipient", "Unknown")))
        elif tool == "direct_response":
            return tool, args.get("text", "I'm not sure how to respond to that.")
        else:
            return "error", f"Error: The Brain tried to use an unknown tool: {tool}"
            
    except json.JSONDecodeError:
        return "error", f"Error: Brain did not output valid JSON. Raw output: {llm_response}"

# --- COMMAND CENTER ---
def ask_agent(user_input, chat_history=None, available_columns="Unknown", active_mode="Cloud", temperature=0.1, contact_target=None, has_image=False, has_video=False, video_bytes=None):
    """
    Returns (raw_decision, tool_name, tool_result, needs_synthesis).
    The caller should use stream_synthesis() if needs_synthesis is True.
    """
    
    mode_instruction = ""
    if "Cloud" in active_mode:
        mode_instruction = "You are currently in CLOUD mode. Use 'query_live_data' for remote queries."
    else:
        mode_instruction = f"You are currently in LOCAL mode. The SQLite table is named 'user_data' and contains content from uploaded files (CSV, PDF, PPTX slides, or DOCX documents). The columns are: {available_columns}."

    contact_instruction = ""
    if contact_target:
        contact_instruction = f"\nThe user has configured a contact target: {contact_target}. If they ask to send/text/email a summary or report, use the 'send_message' tool with this recipient."

    image_instruction = ""
    if has_image:
        image_instruction = "\nThe user has uploaded an image for analysis. If they ask about an image, picture, photo, or chart, use the 'analyze_image' tool."

    video_instruction = ""
    if has_video:
        video_instruction = "\nThe user has uploaded a video for analysis. If they ask about a video, clip, or footage, use the 'analyze_video' tool."

    system_prompt = f"""You are an elite AI Data Analyst. 
    {mode_instruction}
    {contact_instruction}
    {image_instruction}
    {video_instruction}
    
    You have 6 tools available:
    1. 'query_live_data' - args: {{"query": "search text"}}
    2. 'query_local_data' - args: {{"sql_query": "A VALID SQLITE SELECT QUERY. e.g. SELECT * FROM user_data WHERE..."}}
    3. 'analyze_image' - args: {{"prompt": "What to analyze in the image"}}
    4. 'analyze_video' - args: {{"prompt": "What to analyze in the video"}}
    5. 'send_message' - args: {{"msg": "text content", "to": "recipient phone/email"}}
    6. 'direct_response' - args: {{"text": "Your reply."}}
    
    DYNAMIC ROLE ADAPTATION:
    Analyze the user's intent and the retrieved data to adopt the most helpful persona:
    - ACADEMIC/LECTURE DATA: Act as a 'Patient Tutor'. Explain concepts simply, solve problems step-by-step, and offer to test the user's knowledge.
    - BUSINESS/FINANCIAL DATA: Act as a 'Strategic Consultant'. Identify trends, suggest optimizations, and provide clear actionable strategies for profit or efficiency.
    - GENERAL DATA: Act as an elite 'Data Analyst'. Provide high-level insights and clear visualizations.

    CRITICAL INSTRUCTIONS:
    - If the user asks about content from a PDF, Slide, or Document, you MUST use 'query_local_data' to retrieve it.
    - If you don't know what's in the document yet, start by querying: SELECT * FROM user_data LIMIT 20
    - For specific questions, use: SELECT * FROM user_data WHERE text_content LIKE '%keyword%'
    - If the user asks for local data, you MUST write a valid SQL query for the 'query_local_data' tool. 
    
    OUTPUT FORMAT:
    You MUST output ONLY a valid JSON object.
    {{
        "thought": "A clear, human-readable, and non-technical explanation of what you are doing right now (e.g. 'I am searching the lecture notes for a definition of gravity'). NO CODE OR SQL HERE.",
        "tool": "the_tool_name",
        "args": {{"key": "value"}}
    }}"""

    messages_payload = [{"role": "system", "content": system_prompt}]
    
    if chat_history:
        for msg in chat_history[-6:]:
            messages_payload.append({"role": msg["role"], "content": str(msg["content"])})
            
    messages_payload.append({"role": "user", "content": user_input})

    try:
        # Phase 1: Routing decision (not streamed — we need the full JSON)
        chat_completion = client.chat.completions.create(
            messages=messages_payload,
            model="llama-3.3-70b-versatile",
            temperature=temperature,
        )
        
        raw_decision = chat_completion.choices[0].message.content
        tool_name, tool_result = parse_and_execute(raw_decision, video_bytes=video_bytes, available_columns=available_columns)
        
        needs_synthesis = tool_name in ["query_live_data", "query_local_data"] and isinstance(tool_result, str) and "Error" not in tool_result
        return raw_decision, tool_name, tool_result, needs_synthesis
        
    except groq.RateLimitError:
        return '{"error": "API Failure", "tool": "error"}', "error", "Groq AI generation rate limit reached. Please wait a moment.", False
    except groq.APIConnectionError:
        return '{"error": "API Failure", "tool": "error"}', "error", "Network connection to Groq API failed.", False
    except groq.GroqError as e:
        return '{"error": "API Failure", "tool": "error"}', "error", f"Groq API Error: {e}", False
    except Exception as e:
        return '{"error": "Unexpected Engine Failure", "tool": "error"}', "error", f"Core execution error: {e}", False


def stream_synthesis(user_input, tool_result, temperature=0.1):
    """
    Generator that yields tokens for the synthesis response.
    Used by the UI for typewriter streaming.
    """
    synthesis_prompt = f"""The user originally asked: "{user_input}".
    You ran a database query and got this raw data back:
    
    {tool_result}
    
    Please read this data and answer the user's question directly. 
    ADAPT YOUR PERSONA based on the data:
    - If this is LECTURE/ACADEMIC data, act as a TEACHER. Explain concepts, show step-by-step solutions, and be encouraging.
    - If this is BUSINESS/FINANCIAL data, act as a STRATEGIC CONSULTANT. Identify 'Why' things are happening and suggest 'What to do next' to improve profit or efficiency.
    - Otherwise, be a high-level DATA ANALYST.
    
    Do NOT just repeat the raw table. Summarize the findings, highlight trends, and provide meaningful, ACTIONABLE analysis."""
    
    try:
        stream = client.chat.completions.create(
            messages=[{"role": "system", "content": synthesis_prompt}],
            model="llama-3.3-70b-versatile",
            temperature=min(temperature + 0.3, 1.0),
            stream=True,
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
                
    except groq.RateLimitError:
        yield "\n\n⚠️ Analysis rate limit reached. Please hold on a moment before asking another question."
    except groq.APIConnectionError:
        yield "\n\n⚠️ Network connection interrupted while streaming analysis."
    except groq.GroqError as e:
        yield f"\n\n⚠️ Groq API Error during synthesis: {e}"
    except Exception as e:
        yield f"\n\n⚠️ Unexpected error during stream synthesis: {e}"


# --- PROACTIVE EDA BRIEFING ---
def stream_proactive_briefing(eda_summary):
    """
    Generator that streams a proactive welcome briefing after a dataset upload.
    Takes a pre-computed EDA summary and asks Llama 3.3 to generate a warm
    welcome with 3 specific suggested questions.
    """
    briefing_prompt = (
        f"You are an elite AI Data Analyst named Acumen. A user just uploaded a new dataset. "
        f"Here is the automated Exploratory Data Analysis summary:\n\n"
        f"{eda_summary}\n\n"
        f"Generate a warm, concise welcome briefing (3-5 sentences max) that:\n"
        f"1. Acknowledges the dataset and highlights 1-2 interesting observations from the EDA.\n"
        f"2. Suggests EXACTLY 3 specific, actionable questions the user can ask about THIS data. "
        f"Format them as a numbered list. Make the questions specific to the actual column names and data characteristics.\n\n"
        f"Keep the tone professional but approachable. Use markdown formatting."
    )

    try:
        stream = client.chat.completions.create(
            messages=[{"role": "user", "content": briefing_prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.4,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    except groq.RateLimitError:
        yield "\n\n⚠️ Rate limit reached while generating briefing. You can still ask questions about your data!"
    except groq.APIConnectionError:
        yield "\n\n⚠️ Network connection interrupted. Your data is loaded — go ahead and ask a question!"
    except Exception as e:
        yield f"\n\n⚠️ Could not generate briefing: {e}. Your data is ready for analysis!"