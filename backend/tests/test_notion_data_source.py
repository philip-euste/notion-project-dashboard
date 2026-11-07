
import json

from app.services.notion_sync import fetch_notion_projects


def main() -> None:
    try:
        projects = fetch_notion_projects()

        print(f"Total projects retrieved: {len(projects)}")
        print(f"Projects with names: {sum(p['name'] is not None for p in projects)}")

        print("\nFIRST THREE MAPPED PROJECTS")
        print("-" * 40)

        for project in projects[:3]:
            print(json.dumps(
                project,
                indent=2,
                ensure_ascii=False,
                default=str,
            ))

    except Exception as error:
        print(f"Sync test failed: {type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
