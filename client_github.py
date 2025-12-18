from requests import Response, get
from config import github_token


def fetch_users(url: str, page: int) -> Response:
    headers = {
            "Authorization": f"Bearer {github_token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    return get(f"{url}?page={page}", headers=headers)