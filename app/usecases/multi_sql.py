from langchain.chains.router.base import RouterChain, MultiRouteChain
from typing import Any, Dict, List, Mapping, Optional
from langchain.chains.llm import LLMChain
from langchain.chains import ConversationChain
from langchain.base_language import BaseLanguageModel
from langchain.prompts.prompt import PromptTemplate
from langchain.chains.router.base import MultiRouteChain, RouterChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from typing_extensions import Self
from langchain.utilities import SQLDatabase

from .sql import SQLDatabase, SQLDatabaseChain
from .multi_sql_prompts import MULTI_SQL_ROUTER_TEMPLATE



class MultiSQLChain(MultiRouteChain):
    """A multi-route chain that uses an LLM router chain to choose amongst SQL chains."""

    router_chain: RouterChain
    """Chain for deciding a destination chain and the input to it."""
    destination_chains: Mapping[str, SQLDatabaseChain]
    """Map of name to candidate chains that inputs can be routed to."""
    default_chain: LLMChain
    """Default chain to use when router doesn't map input to one of the destinations."""

    @property
    def output_keys(self) -> List[str]:
        return ["text"]

    @classmethod
    def from_prompts(
        cls,
        llm: BaseLanguageModel,
        db: SQLDatabase,
        prompt_infos: List[Dict[str, str]],
        default_chain: Optional[LLMChain] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> Self:
        """Convenience constructor for instantiating from destination prompts."""
        destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
        destinations_str = "\n".join(destinations)
        router_template = MULTI_SQL_ROUTER_TEMPLATE.format(
            destinations=destinations_str
        )
        router_prompt = PromptTemplate(
            template=router_template,
            input_variables=["input"],
            output_parser=RouterOutputParser(next_inputs_inner_key="query"),
        )
        router_chain = LLMRouterChain.from_llm(llm, router_prompt)
        destination_chains = {}
        for p_info in prompt_infos:
            name = p_info["name"]
            prompt_template = p_info["prompt_template"]
            prompt = PromptTemplate(template=prompt_template,
                                    input_variables=["input", "table_info", ],
                                    )
            chain = SQLDatabaseChain.from_llm(llm, db, prompt=prompt,
                                              output_key="text",
                                              verbose=verbose,
                                              )
            destination_chains[name] = chain
        _default_chain = default_chain or ConversationChain(llm=llm, output_key="text")
        return cls(
            router_chain=router_chain,
            destination_chains=destination_chains,
            default_chain=_default_chain,
            **kwargs,
        )
