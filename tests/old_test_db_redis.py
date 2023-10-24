import pytest

from health_access.utils import redis_client


@pytest.mark.django_db
def test_redis_connection():
    assert redis_client.ping(), "Failed to connect to Redis"
