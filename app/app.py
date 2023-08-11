import sys
import warnings

import chainlit as cl
from dotenv import load_dotenv
from duckdb_engine import DuckDBEngineWarning
from langchain.chat_models import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain

from database import DATABASE


sys.path.append('..')
warnings.filterwarnings("ignore", category=DuckDBEngineWarning)
load_dotenv()


@cl.on_chat_start
async def init():

    llm = ChatOpenAI(
        model_name='gpt-4-32k-0613',
        temperature=0,
        streaming=True
    )
    chain = SQLDatabaseChain.from_llm(
        llm=llm,    
        db=DATABASE,
        verbose=True
    )

    # Let the user know that the system is ready
    msg = cl.Message("Chat with SQL Database initiailized. You can now ask questions!")
    await msg.update()

    # Set the user session to Chain and use the initialized chain.
    cl.user_session.set("chain", chain)


@cl.on_message
async def main(message):
    # Get the chain for the session
    chain = cl.user_session.get("chain")  # type: SQLDatabaseChain

    answer_prefix_tokens=["Answer:"]
    
    # Streaming answers
    cb = cl.LangchainCallbackHandler(
        stream_final_answer=True,
        answer_prefix_tokens=answer_prefix_tokens,
    )

    # SQLDatabaseChain is only sync, so need to use make_async to turn it into async.
    response = await cl.make_async(chain.run)(
        message,
        callbacks=[cb],
    )

    await cl.Message(content=response).send()
