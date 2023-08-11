# since the sqlchain prompts will have their own optimization,
# we don't want the results of this prompt to change the input, just route it


MULTI_SQL_ROUTER_TEMPLATE = """
Given a raw text input to a language model select the model prompt best suited for
the input. You will be given the names of the available prompts and a description of
what the prompt is best suited for.

<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like:
```json
{{{{
    "destination": string \\ name of the prompt to use or "DEFAULT"
    "next_inputs": string \\ the original input
}}}}
```

REMEMBER: "destination" MUST be one of the candidate prompt names specified below OR
it can be "DEFAULT" if the input is not well suited for any of the candidate prompts.
REMEMBER: "next_inputs" can just be the original input

<< CANDIDATE PROMPTS >>
{destinations}

<< INPUT >>
{{input}}

<< OUTPUT >>
"""