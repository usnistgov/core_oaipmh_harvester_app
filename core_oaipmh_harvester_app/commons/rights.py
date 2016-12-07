# API Rights
api_content_type = "api_oai_pmh"
api_access = "api_oai_pmh_access"

# OAI PMH Rights
oai_pmh_content_type = "oaipmh"
oai_pmh_access = "oaipmh_access"


def get_description(right):
    return "Can " + right.replace("_", " ")
