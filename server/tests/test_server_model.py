from server.models import Server
from fabric import Connection
import pytest


@pytest.fixture
def server():
    return Server(
        **{
            "name": "test",
            "host": "localhost",
            "connect_username": "ubuntu",
            "connect_port": "22",
        }
    )


def test_server_connection(server):
    con = server.get_connection()
    assert isinstance(con, Connection)


@pytest.mark.parametrize(
    "function_name",
    [
        "get",
        "run",
        "close",
        "put",
        "sudo",
    ],
)
def test_server_connection_interface(
    server,
    function_name,
):
    con = server.get_connection()
    assert hasattr(con, function_name)
