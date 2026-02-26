from Symbol_agent.agent import Symbol_agent
from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool

#funçoes da API
from API_tools.tools_NCBI import (
    search_ncbi_human_gene,
    search_ncbi_human_gene_summary,
    search_ncbi_human_gene_description,
    search_ncbi_human_gene_ID
)

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

root_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
    name="NCBI_agent",
    instruction="Use the NCBI datasets tool to find data about human genes requested, use the symbol of the gene if provided, if not ask the symbol agent to fetch you the symbol. You may only answer questions about human genes, never other species",
    tools=[AgentTool(Symbol_agent), search_ncbi_human_gene, search_ncbi_human_gene_summary, search_ncbi_human_gene_description, search_ncbi_human_gene_ID],
)