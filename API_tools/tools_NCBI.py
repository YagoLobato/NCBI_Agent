import requests

print("✅ ADK components imported successfully.")
def extract_gene_summary(gene: dict) -> dict:
    gene = gene["reports"][0]["gene"]
    return {
        "gene_id": gene.get("gene_id"),
        "symbol": gene.get("symbol"),
        "description": (
            gene.get("summary")[0].get("description")
            if gene.get("summary") else None
        ),
        "tax_id": gene.get("tax_id"),
        "taxname": gene.get("taxname"),
        "type": gene.get("type"),
        "orientation": gene.get("orientation"),
        "accession_version": (
            gene.get("reference_standards")[0]
                .get("gene_range")
                .get("accession_version")
            if gene.get("reference_standards") else None
        ),
        "chromosomes": gene.get("chromosomes")
    }

def search_ncbi_human_gene(gene_symbol: str):
    """
    USE THIS TOOL ONLY IF NO OTHER TOOL IS SUITABLE
    Uses the provided gene symbol to find bulk information about a gene in the human genome
    """
    base_url = "https://api.ncbi.nlm.nih.gov/datasets/v2"
    url = f"{base_url}/gene/symbol/{gene_symbol}/taxon/human/dataset_report"
    print("Used general wrapper")
    return requests.get(url).json()


def search_ncbi_human_gene_summary(gene_symbol: str):
    """
    Uses the provided gene symbol to find a short summary containing different information about a gene in the human genome
    information included in this summary is:

    gene_id (numerical gene id)

    symbol (gene symbol, same as used in the query)

    description (short gene description text)

    tax_id (id of the taxon)

    taxname (scientific name of the taxon)

    type (gene type)

    orientation (gene orientation)

    accession_version (Acession code for the gene, enables searching for the DNA sequence of the gene in FASTA format)

    chromosomes (Gene location in chromosomes)

    """
    base_url = "https://api.ncbi.nlm.nih.gov/datasets/v2"
    url = f"{base_url}/gene/symbol/{gene_symbol}/taxon/human/dataset_report"
    print("Used summary wrapper")
    return extract_gene_summary(requests.get(url).json())

def search_ncbi_human_gene_description(gene_symbol: str):
    """Uses the provided gene symbol to find the description of a given gene in the human genome"""
    base_url = "https://api.ncbi.nlm.nih.gov/datasets/v2"
    url = f"{base_url}/gene/symbol/{gene_symbol}/taxon/human/dataset_report"
    print("Used description wrapper")
    data = requests.get(url).json()
    return(data["reports"][0]["gene"]["summary"][0]["description"])

def search_ncbi_human_gene_ID(gene_symbol: str):
    """Uses the provided gene symbol to find the numerical ID of a given gene in the human genome"""
    base_url = "https://api.ncbi.nlm.nih.gov/datasets/v2"
    url = f"{base_url}/gene/symbol/{gene_symbol}/taxon/human/dataset_report"
    print("Used ID wrapper")
    data = requests.get(url).json()
    return(data["reports"][0]["gene"]["gene_id"])