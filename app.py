
"""
import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Force CPU
device = torch.device("cpu")

checkpoint_path = "checkpoints/codet5_finetuned/checkpoint-2625"

tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)
model = AutoModelForSeq2SeqLM.from_pretrained(
    checkpoint_path,
    local_files_only=True,
    trust_remote_code=True
).to(device)

st.title("Text-to-SQL Generator")

question = st.text_input("Enter your question:")

if st.button("Generate SQL"):
    if question:
        with st.spinner("Generating SQL..."):
            inputs = tokenizer(question, return_tensors="pt", padding=True, truncation=True, max_length=128).to(device)
            output_ids = model.generate(**inputs, max_length=128, num_beams=4, early_stopping=True)
            sql_query = tokenizer.decode(output_ids[0], skip_special_tokens=True)

        st.text_area("Generated SQL:", sql_query, height=200)

"""

import streamlit as st
import os
import sqlite3
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# --- Streamlit Title ---
st.title("Text-to-SQL Generator with Database Selection")

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
