import requests
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.item import create_random_item
from app.tests.utils.utils import get_server_api


def test_create_item(superuser_token_headers: dict, db: Session) -> None:
    server_api = get_server_api()
    data = {"title": "Foo", "description": "Fighters"}
    response = requests.post(
        f"{server_api}{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


def test_read_item(superuser_token_headers: dict, db: Session) -> None:
    item = create_random_item(db)
    server_api = get_server_api()
    response = requests.get(
        f"{server_api}{settings.API_V1_STR}/items/{item.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == item.title
    assert content["description"] == item.description
    assert content["id"] == item.id
    assert content["owner_id"] == item.owner_id
