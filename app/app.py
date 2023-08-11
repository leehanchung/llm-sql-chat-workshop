import sys
import warnings

import chainlit as cl
from dotenv import load_dotenv
from duckdb_engine import DuckDBEngineWarning
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType

from database import DATABASE


sys.path.append('..')
warnings.filterwarnings("ignore", category=DuckDBEngineWarning)
load_dotenv()


@cl.on_chat_start
async def init():

    llm = OpenAI(
        model="text-davinci-003",
        temperature=0,
        streaming=True
    )
    toolkit = SQLDatabaseToolkit(db=DATABASE, llm=llm)
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

    # Let the user know that the system is ready
    msg = cl.Message("Chat with SQL Database initiailized. You can now ask questions!")
    await msg.update()

    # Set the user session to Chain and use the initialized chain.
    cl.user_session.set("agent", agent)


@cl.on_message
async def main(message):
    # Get the chain for the session
    agent = cl.user_session.get("agent")  # type: AgentExecutor
   
    # Streaming answers
    cb = cl.LangchainCallbackHandler(
        stream_final_answer=True,
    )

    # SQLDatabaseChain is only sync, so need to use make_async to turn it into async.
    response = await cl.make_async(agent.run)(
        message,
        callbacks=[cb],
    )

    await cl.Message(content=response).send()
