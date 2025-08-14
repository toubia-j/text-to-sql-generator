# Text-to-SQL Generator

## Project Overview
This project builds a model that converts natural language questions into SQL queries, enabling non-technical users to query databases easily. The model is fine-tuned on the Spider dataset, a large, complex, cross-domain text-to-SQL dataset.

## Objective
- Enable users to ask questions in plain English.
- Automatically generate accurate SQL queries.
- Test queries on a sample database to validate results.

## Project Structure
- `data/` — Datasets (Spider or smaller test sets)
- `notebooks/` — Experimental notebooks for prototyping
- `src/` — Python modules and functions
- `Dockerfile` — Docker setup
- `requirements.txt` — Python dependencies
- `README.md` — Project documentation
- `.github/` — GitHub issues, workflows, and project boards

## Docker Setup

### Build Docker Image
```bash
docker build -t text-to-sql .
