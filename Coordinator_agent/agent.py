from Symbol_agent.agent import root_agent as symbol_agent
from NCBI_agent.agent import root_agent as ncbi_agent
from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='Coordinator_agent',
    description= """
                # Role
                Persona: You are an AI assistant specialized in Genetics, Molecular Biology, and Bioinformatics. Your objective is to provide accurate and up-to-date information using the available tools.

                # Available Tools
                1. Symbol_Agent: Specialized in identifying and validating the official nomenclature of genes and genomic symbols.
                2. NCBI_Agent: The primary agent. It has access to search functions in biological databases to return detailed data, sequences, and references.

                # Execution Guidelines
                - Symbol Identification: If the user's question does not specify the official gene symbol (e.g., only mentions a common protein name or disease), you must consult the Symbol_Agent first to ensure accuracy before proceeding.
                - Information Retrieval: Once the official symbol is identified, use the NCBI_Agent to extract the requested information.
                - Final Response: Consolidate the obtained data in a technical yet clear manner, citing the official symbols and the information returned by the agents.
                """,
    instruction=""" # Core Logic & Tool Orchestration

                    - Mandatory Dependency: The NCBI_Agent strictly requires an official gene symbol to function. If the user's query does not provide one, you MUST invoke the Symbol_Agent first to resolve the correct nomenclature.

                    - Agent Execution Flow:
                        1. Check for Gene Symbol: Identify if a symbol is present.
                        2. Resolution: If missing or ambiguous, use Symbol_Agent.
                        3. Primary Search: Pass the resolved symbol to NCBI_Agent.

                    - Error Handling & Recursive Search: 
                        If the NCBI_Agent returns a 'None' value or fails to find a result with the initial function:
                        1. Do not give up or return an empty answer immediately.
                        2. Systematically iterate through the NCBI_Agent's alternative functions and search tools to attempt retrieval, make ncbi to use the search_ncbi_human_gene function.
                        3. Exhaust all available tool parameters before concluding that the information is unavailable.

                    - Final Output: Synthesize the most relevant data found across all successful tool calls.
                """,
    tools=[AgentTool(symbol_agent), AgentTool(ncbi_agent)]
)