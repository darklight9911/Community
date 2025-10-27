from ..extensions import redis_client

VOTE_KEY_TEMPLATE = "{item_type}:votes"


def _key(item_type: str) -> str:
    return VOTE_KEY_TEMPLATE.format(item_type=item_type)


def update_vote_count(item_type: str, item_id: int, value: int) -> int:
    if redis_client is None:
        return 0
    # Use hash per item type: HINCRBY post:votes <id> <delta>
    new_val = redis_client.hincrby(_key(item_type), str(item_id), int(value))
    return int(new_val)


def get_vote_count(item_type: str, item_id: int) -> int:
    if redis_client is None:
        return 0
    val = redis_client.hget(_key(item_type), str(item_id))
    return int(val) if val is not None else 0
