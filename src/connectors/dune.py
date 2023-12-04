import logging

from dune_client.query import QueryBase
from exceptions.exceptions import FailedQueryError, EmptyQueryResultError


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

    try:
        result = client.run_query(query)
    except Exception as e:
        logging.error(e)
        raise FailedQueryError()

    if not result.state.is_complete():
        logging.error(f'Cant complete the query. {result.query_id}')
        raise EmptyQueryResultError()

    return result.result.rows
