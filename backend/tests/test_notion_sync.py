
from app.database.connection import SessionLocal
from app.services.notion_sync import sync_notion_projects


def main() -> None:
    db = SessionLocal()

    try:
        result = sync_notion_projects(db)

        print("NOTION SYNCHRONIZATION COMPLETE")
        print("-" * 40)
        print(f"Total projects: {result['total']}")
        print(f"Created: {result['created']}")
        print(f"Updated: {result['updated']}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
