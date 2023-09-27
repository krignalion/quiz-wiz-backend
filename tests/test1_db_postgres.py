import pytest
from health_access.utils import get_postgres_connection

@pytest.mark.django_db
def test_postgres_connection():
    connection = get_postgres_connection()
    assert connection is not None