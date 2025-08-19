"""

import streamlit as st
import os
import sqlite3
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# --- Streamlit Title ---
st.title("Text-to-SQL Generator ")

# --- Device setup ---
device = torch.device("cpu")

# --- Load your model ---
checkpoint_path = "checkpoints/codet5_finetuned/checkpoint-2625"
tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)
model = AutoModelForSeq2SeqLM.from_pretrained(
    checkpoint_path,
    local_files_only=True,
    trust_remote_code=True
).to(device)

# --- Step 1: List all available DBs in the folder ---
db_folder = "data/test"  # folder containing your .sqlite files
db_files = []
for root, dirs, files in os.walk(db_folder):
    for file in files:
        if file.endswith(".sqlite"):
            full_path = os.path.join(root, file)
            db_files.append(full_path)

if not db_files:
    st.error("No databases found in folder!")
else:
    # Show only filenames in dropdown but keep mapping to full path
    db_choice = st.selectbox(
        "Select a database:",
        options=db_files,
         format_func=lambda x: os.path.splitext(os.path.basename(x))[0]
    )

    # --- Step 2: Connect to selected DB ---
    conn = sqlite3.connect(db_choice)
    cursor = conn.cursor()

    # --- Step 3: Display tables (names only) ---
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]

    st.subheader("Tables in selected database:")

    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        col_names = [c[1] for c in columns]  # just column names
        schema_str = f"{table} ({', '.join(col_names)})"
        st.text(schema_str)


    # --- Step 4: Input natural language question ---
    question = st.text_input("Enter your question:")

    if st.button("Generate SQL and Run Query"):
        if question:
            with st.spinner("Generating SQL..."):
                inputs = tokenizer(
                    question,
                    return_tensors="pt",
                    padding=True,
                    truncation=True,
                    max_length=128
                ).to(device)
                output_ids = model.generate(
                    **inputs,
                    max_length=128,
                    num_beams=4,
                    early_stopping=True
                )
                sql_query = tokenizer.decode(output_ids[0], skip_special_tokens=True)

            st.subheader("Generated SQL:")
            st.code(sql_query)

            # --- Step 5: Execute SQL ---
            try:
                df_result = pd.read_sql_query(sql_query, conn)
                st.subheader("Query Result:")
                st.dataframe(df_result)
            except Exception as e:
                st.error(f"Error executing SQL: {e}")

    conn.close()

"""

import streamlit as st
import os
import sqlite3
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# --- Page config ---
st.set_page_config(page_title="Text-to-SQL Generator", page_icon="📝", layout="wide")

# --- Custom CSS for styling ---
st.markdown(
    """
    <style>
    .stTextInput, .stTextArea { border-radius: 10px; }
    .stButton button { 
        background-color: #0066cc; 
        color: white; 
        border-radius: 6px; 
        padding: 8px 16px; 
        font-weight: bold;
    }
    .stCode { 
        background-color: #f8f9fa; 
        border-radius: 6px; 
        padding: 10px; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Title ---
st.title("📝 Text-to-SQL Generator")
st.write("Turn natural language questions into executable SQL queries.")

# --- Device setup ---
device = torch.device("cpu")

# --- Load model ---
checkpoint_path = "checkpoints/codet5_finetuned/checkpoint-2625"
tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)
model = AutoModelForSeq2SeqLM.from_pretrained(
    checkpoint_path,
    local_files_only=True,
    trust_remote_code=True
).to(device)

# --- Step 1: List DBs in sidebar ---
db_folder = "data/test"
db_files = []
for root, dirs, files in os.walk(db_folder):
    for file in files:
        if file.endswith(".sqlite"):
            full_path = os.path.join(root, file)
            db_files.append(full_path)

if not db_files:
    st.error("⚠️ No databases found in `data/test/` folder!")
else:
    db_choice = st.sidebar.selectbox(
        "📂 Select Database",
        options=db_files,
        format_func=lambda x: os.path.splitext(os.path.basename(x))[0]
    )

    # --- Step 2: Connect ---
    conn = sqlite3.connect(db_choice)
    cursor = conn.cursor()

    # --- Step 3: Show schema in expandable sections ---
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]

    st.sidebar.subheader("📑 Database Schema")
    for table in tables:
        with st.sidebar.expander(f"Table: {table}"):
            cursor.execute(f"PRAGMA table_info({table});")
            columns = cursor.fetchall()
            col_names = [c[1] for c in columns]
            st.write(", ".join(col_names))

    # --- Step 4: Input NL question ---
    st.subheader("💬 Ask a Question")
    question = st.text_input("Enter your question in natural language:")



    # --- Step 5: Generate + Run ---
    if st.button("🚀 Generate SQL and Run Query"):
        if question:
            with st.spinner("Generating SQL..."):
                inputs = tokenizer(
                    question,
                    return_tensors="pt",
                    padding=True,
                    truncation=True,
                    max_length=128
                ).to(device)
                output_ids = model.generate(
                    **inputs,
                    max_length=128,
                    num_beams=4,
                    early_stopping=True
                )
                sql_query = tokenizer.decode(output_ids[0], skip_special_tokens=True)

            # Show results in tabs
            tab1, tab2 = st.tabs(["📝 SQL Query", "📊 Query Result"])
            with tab1:
                st.code(sql_query, language="sql")
            with tab2:
                try:
                    df_result = pd.read_sql_query(sql_query, conn)
                    st.dataframe(df_result)
                except Exception as e:
                    st.error(f"❌ Error executing SQL: {e}")

    conn.close()
