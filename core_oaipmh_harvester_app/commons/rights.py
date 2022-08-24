""" Rights
"""

# API Rights
API_CONTENT_TYPE = "api_oai_pmh"
API_ACCESS = "api_oai_pmh_access"

# OAI PMH Rights
OAI_PMH_CONTENT_TYPE = "oaipmh"
OAI_PMH_ACCESS = "oaipmh_access"


def get_description(right):
    """get_description

    Args:
        right:

    Returns:
    """
    return "Can " + right.replace("_", " ")
