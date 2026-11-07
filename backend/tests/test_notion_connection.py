import httpx

from app.core.config import settings


NOTION_VERSION = "2026-03-11"
NOTION_BASE_URL = "https://api.notion.com/v1"


def main() -> None:
    if not settings.notion_api_key or not settings.notion_database_id:
        print("Missing NOTION_API_KEY or NOTION_DATABASE_ID in .env")
        return

    headers = {
        "Authorization": f"Bearer {settings.notion_api_key}",
        "Notion-Version": NOTION_VERSION,
    }

    url = f"{NOTION_BASE_URL}/databases/{settings.notion_database_id}"

    try:
        response = httpx.get(
            url,
            headers=headers,
            timeout=20.0,
        )
        response.raise_for_status()

        database = response.json()

        print("Notion connection successful.")
        print(f"Database ID: {database.get('id')}")

        data_sources = database.get("data_sources", [])

        print(f"Data sources found: {len(data_sources)}")

        for source in data_sources:
            print(f"- {source.get('name')}: {source.get('id')}")

    except httpx.HTTPStatusError as error:
        print(f"Notion API error: HTTP {error.response.status_code}")
        print(error.response.text)

    except httpx.RequestError as error:
        print(f"Connection error: {error}")


if __name__ == "__main__":
    main()