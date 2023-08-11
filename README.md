# Workshop 2: Chat with SQL Database App using OpenAI, Langchain, and Chainlit

This repository contains a workshop for learning LLM Application Development using Langchain, OpenAI, and Chainlit. The workshop goes over the process of developing an LLM application that provides a chat interface to a SQL database. The prerequisite to the workshop is basic working knowledge of Git, Linux, and Python. The workshop is organized as follows.

| Lab | Learning Objective | Problem | Solution |
| --- | ------------------ | ------- | :------: |
| 1   | Basic chat with data LLM App  | 🐒 [PDF Q&A Application](https://github.com/leehanchung/llm-sql-chat-workshop/tree/main) | ✅ [Solution](https://github.com/leehanchung/llm-sql-chat-workshop/tree/part1) |
| 2   | Basic prompt engineering      | 🐒 [Improving Q&A Factuality](https://github.com/leehanchung/llm-sql-chat-workshop/tree/part2) | ✅ [Solution](https://github.com/leehanchung/llm-sql-chat-workshop/tree/part3) |

To run the fully functional application, please checkout [Lab 2 Solution](https://github.com/leehanchung/llm-sql-chat-workshop/tree/lab3) branch and follow the [instruction to run the application](#run-the-application)

The app provides an chat interface that asks user to upload a PDF document and then allow users to ask questions against the PDF document. It uses OpenAI's API for the chat and embedding models, Langchain for the framework, and Chainlit as the fullstack interface.

For the purpose of the workshop, we are using the [Crunchbase Data Daily CSV Export](https://data.crunchbase.com/docs/daily-csv-export) as the example database. The database contains 17 tables.

The completed application looks as follows:
![SQL Q&A App](assets/app.png)

## 🧰 Stack

- [Python](https://www.python.org/downloads/release/python-3100/)
- [Langchain](https://python.langchain.com/docs/get_started/introduction.html)
- [Chainlit](https://docs.chainlit.io/overview)
- [OpenAI](https://openai.com/)
- [DuckDB](https://duckdb.org/)


## Data Source

The source of the same data for the workshop is [Crunchbase Data Daily CSV Export](https://data.crunchbase.com/docs/daily-csv-export). It is an export of a database of 17 tables


## 👉 Getting Started

We use [Python Poetry](https://python-poetry.org/) for managing virtual environments and we recommend using [pyenv](https://github.com/pyenv/pyenv) to manage Python versions. Alternatively, you can use [Mamba](https://mamba.readthedocs.io/en/latest/) for Python version management.

Install and start the Poetry shell as follows.

```bash
poetry install
poetry shell
```

Please create an `.env` file from `.env.sample` once the application is installed. Edit the `.env` file with your OpenAI org and OpenAI key.

```bash
cp .env.sample .env
```

### Run the Application

#### Setup our local database

We will first download the CSV tar balls from Crunchbase's website, unzip them, and ingest them into a local DuckDB file.

```bash
./source/download-sample.sh
python data/ingest_csv.py
```

#### Run the application
```bash
chainlit run app/app.py -w
```

## Lab 1: Gathering and Debugging Chat with SQL LLM App

One way that people can utilize LLM to better improve their workflows is to use LLM to chat with SQL Database for some SQL query automations. These type of applications uses LLM to translate natural language query into SQL and run the SQL query against a database. The results is then summarized by the LLM.

** NOTE: Since we are running queries directly against SQL Database, there's a significant SQL Injection Risk **

We have created a template repository so you can play around and see how the chat with SQL Database works and how it become fragile. The goal 

Please implement extract the right files from `langchain` and `langchain_experiments` so we can tune our prompts.

### Lab 1: Solution

✅ [Solution](https://github.com/leehanchung/llm-sql-chat-workshop/tree/part1)

## Lab 2: Add Prompt Chaining

Playing around our newly created application using the provided data, we are constantly running into problems parsing the LLM outputs. One of the reason is that if we directly use `SQLDatabaseChain`, it will attempt to invoke SQL Database every single time. This is not necessary!!

Please resolve this issue with prompt chaining.

### Lab 2: Solution

✅ [Solution](https://github.com/leehanchung/llm-sql-chat-workshop/tree/part2)

## LICENSE

This repository is open source under GPLv3 and please cite it as:
```bibtex
@misc{PDF_QA_App_Workshop,
  author = {Lee, Hanchung},
  title = {Workshop 2: Chat with SQL Database App using OpenAI, Langchain, and Chainlit},
  url = {https://github.com/leehanchung/llm-sql-chat-workshop},
  year = {2023},
  month = {8},
  howpublished = {Github Repo},
}
```
