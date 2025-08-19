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
- 
## Datasets
For details on the datasets used in this project (including download links and preprocessing instructions), see the [Datasets README](data/README.md).

## Docker Setup

### Build Docker Image
```bash
docker build -t text-to-sql .
```
### Run the container
```bash
docker run -it --rm \
    -p 8501:8501 \
    -v ${PWD}:/app \
    text-to-sql \
    streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```
### 3. Open the Streamlit App
Once the container is running, open your web browser and go to:
```bash
http://localhost:8501
```


