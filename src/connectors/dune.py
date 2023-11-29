import logging

from dune_client.query import QueryBase


def dune_request(
    query_id: int,
    query_name: str,
    params: list,
    client: object
) -> list:
    # params is the list of dune_client.QueryParameter

    query = QueryBase(
        name=query_name,
        query_id=query_id,
        params=params
    )
    result = client.run_query(query)
    if not result.state.is_complete():
        logging.ERROR(f'Cant complete the query. {result.query_id}')
        return []
    return result.result.rows
