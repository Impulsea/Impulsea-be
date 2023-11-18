from dune_client.types import QueryParameter
from dune_client.client import DuneClient

from connectors.dune import dune_request
from config import DUNE_API_KEY


def get_wallet_score(address: str):

    QUERY_ID = 3211159
    QUERY_NAME = 'Arbitrum_Impulsea_XP'

    params = [QueryParameter.text_type(name="address1", value=address)]
    cli = DuneClient(api_key=DUNE_API_KEY)

    res = dune_request(
        query_id=QUERY_ID,
        query_name=QUERY_NAME,
        params=params,
        client=cli
    )

    address = res[0].get("address", 0)
    program_engagement = res[0].get("program_engagement", 0)
    protocol_activity = res[0].get("protocol_activity", 0)
    competitors_activity = res[0].get("competitors_activity", 0)
    sybil_likelihood = res[0].get("sybil_likelihood", 0)

    total_xp = 10 * (program_engagement + protocol_activity + competitors_activity + sybil_likelihood)

    return {
        "Address": address,
        "Program Engegement":  program_engagement,
        "Protocol Activity": protocol_activity,
        "Competitors Activity": competitors_activity,
        "Sybil Likelihood": sybil_likelihood,
        "Total XP": total_xp
    }
