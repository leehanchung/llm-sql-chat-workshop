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

## Lab 1: Basic chat with data LLM App

The most quintessential llm application is a chat with text application. These type of application uses  a retrieval augmented generation (RAG) design pattern, where the application first retrieve the relevant texts from memory and then generate answers based on the retrieved text.

For our application, we will go through the following steps in the order of execution:

1. User uploads a PDF file.
2. App load and decode the PDF into plain text.
3. App chunks the text into smaller documents. This is because embedding models have limited input size.
4. App stores the embeddings into memory
5. User asks a question
6. App retrieves the relevant documents from memory and generate an answer based on the retrieved text.

The overall architecture is as follows:
![init](assets/arch_init.png)

Please implement the missing pieces in the [application](app/app.py)

### Lab 1: Solution

✅ [Solution](https://github.com/leehanchung/llm-sql-chat-workshop/tree/lab1/pdf-qa-app)

## Lab 2: Basic prompt engineering

Playing around our newly created application using the provided [sample PDF, Gap Q1 2023 Earnings Release](samples/1Q23-EPR-with-Tables-FINAL.pdf), we run into a hallucination problem from the following long  question to ask the model to summarize the key results:
> ```What's the results for the reporter quarter? Please describe in the following order using bullet points - revenue, gross margin, opex, op margin, net income, and EPS. INclude both gaap and non-gaap numbers. Please also include quarter over quarter changes.```

A whooping 36.6% operating margin for a retail business. That is 10x higher than Amazon's consolidated operating margins!!

![hallucination](assets/hallucination.png)

We again asked the model a simpler and more bounded question:
> ```What's the op margin for the current quarter```

![fact](assets/fact.png)

And it finds the answer.

Please resolve this hallucination problem with prompt engineering.

### Lab 2: Solution

✅ [Solution](https://github.com/leehanchung/ llm-sql-chat-workshop/tree/lab1/pdf-qa-app-final)

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
