# Notion Project Dashboard

**Version:** v0.2.1  
**Repository:** [notion-project-dashboard](https://github.com/philip-euste/notion-project-dashboard)

A full-stack project management dashboard that integrates **Notion, PostgreSQL, GitHub, and a React frontend** to centralize project information, track development activity, and synchronize project records across platforms.

Notion serves as the primary project management workspace, while PostgreSQL provides the database layer for the dashboard. The backend uses FastAPI to handle project operations, synchronization, and communication with external APIs.

The system supports project management through a web interface, Notion synchronization, and GitHub repository activity tracking. It also uses scheduled synchronization to keep project information updated without requiring manual refreshes.

---

## Version

**v0.2.1**

---

## Features

- Display projects stored in the PostgreSQL database.
- Retrieve project information synchronized from Notion.
- Create new projects through the dashboard.
- Update existing project properties.
- Archive projects through the dashboard.
- Synchronize project records from Notion to PostgreSQL.
- Support Notion pagination when retrieving project records.
- Map Notion database properties into application models.
- Track project status and priority.
- Track project potential and development progress.
- Store project descriptions and next possible actions.
- Track skills used and development environments.
- Store GitHub repository URLs.
- Retrieve GitHub repository information through the GitHub API.
- Track the latest GitHub push timestamp.
- Maintain GitHub synchronization timestamps.
- Schedule repository checks using individual check intervals.
- Prioritize repositories that have not been checked or have the oldest check timestamps.
- Limit GitHub synchronization to 40 repositories per run.
- Cache successful GitHub checks for six hours.
- Retry failed GitHub requests after 15 minutes.
- Handle GitHub API rate limits.
- Synchronize GitHub push timestamps back to Notion.
- Track whether GitHub timestamps have been successfully synchronized to Notion.
- Support scheduled and manually triggered synchronization through GitHub Actions.
- Receive Notion webhook events for changes made in the Notion workspace.
- Authenticate synchronization requests using a shared synchronization token.
- Provide REST API endpoints through FastAPI.
- Use SQLAlchemy for database operations.
- Manage database schema changes through Alembic migrations.
- Configure cross-origin requests for frontend and backend communication.

---

## Project Structure

```text
notion-project-dashboard/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── projects.py
│   │   │   ├── sync.py
│   │   │   └── webhooks.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── database/
│   │   │   ├── connection.py
│   │   │   └── models.py
│   │   ├── services/
│   │   │   ├── github_client.py
│   │   │   ├── notion_client.py
│   │   │   └── notion_sync.py
│   │   └── main.py
│   ├── migrations/
│   │   └── versions/
│   ├── requirements.txt
│   └── ...
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── ...
├── .github/
│   └── workflows/
│       └── ...
├── .gitignore
└── README.md
```

### File Responsibilities

| File / Directory | Responsibility |
|---|---|
| `backend/app/main.py` | FastAPI application initialization and router registration |
| `backend/app/api/projects.py` | Project CRUD endpoints |
| `backend/app/api/sync.py` | Notion and GitHub synchronization endpoints |
| `backend/app/api/webhooks.py` | Handles incoming Notion webhook events |
| `backend/app/core/config.py` | Application settings and environment configuration |
| `backend/app/database/connection.py` | SQLAlchemy database connection and session management |
| `backend/app/database/models.py` | Database models and project attributes |
| `backend/app/services/notion_client.py` | Notion API requests, page creation, updates, and archiving |
| `backend/app/services/notion_sync.py` | Retrieves and synchronizes Notion project records |
| `backend/app/services/github_client.py` | GitHub repository requests, caching, scheduling, and retry handling |
| `backend/migrations/` | Database schema migration configuration and history |
| `frontend/src/components/` | Reusable dashboard interface components |
| `frontend/src/services/api.js` | Frontend communication with the FastAPI backend |
| `frontend/src/App.jsx` | Main dashboard application |
| `frontend/src/main.jsx` | Frontend entry point |
| `.github/workflows/` | Scheduled and manually triggered synchronization workflows |

---

## Explanation

Notion Project Dashboard operates through several interconnected components:

1. **Project Management** — Display and manage project records through the React dashboard.
2. **Database Operations** — Store and retrieve project information using PostgreSQL.
3. **Notion Integration** — Retrieve project records and synchronize changes with the Notion workspace.
4. **GitHub Integration** — Retrieve repository activity and track the latest push timestamps.
5. **Synchronization** — Coordinate updates between Notion, PostgreSQL, and GitHub.
6. **Automation** — Use GitHub Actions to trigger scheduled synchronization.
7. **Deployment** — Host the FastAPI backend through Render and prepare the frontend for Cloudflare Pages deployment.

The general system pipeline is:

```text
             Notion Workspace
                    │
                    ▼
             Notion API
                    │
                    ▼
             FastAPI Backend
                    │
                    ▼
             PostgreSQL
                    │
                    ▼
             React Dashboard
```

GitHub synchronization operates separately:

```text
          GitHub Repositories
                    │
                    ▼
              GitHub API
                    │
                    ▼
             FastAPI Backend
                    │
                    ▼
               PostgreSQL
                    │
                    ▼
             Notion API
                    │
                    ▼
             Notion Workspace
```

---

## System Architecture

The application is divided into three primary layers.

### Frontend

The frontend is built using React and Vite.

It provides the user interface for viewing, creating, editing, and archiving projects.

The frontend communicates with the backend through HTTP requests using the configured API URL.

### Backend

The backend uses FastAPI to expose REST API endpoints.

It handles:

- Project creation and updates.
- Project retrieval and archiving.
- Database transactions.
- Notion API communication.
- GitHub API communication.
- Synchronization scheduling logic.
- Webhook event processing.
- Authentication of synchronization requests.

### Database

PostgreSQL is used as the application's persistent database.

The database is hosted through Neon and accessed using SQLAlchemy with Psycopg.

Alembic manages database schema changes through version-controlled migrations.

---

## Notion Integration

Notion acts as the primary project management workspace.

The integration retrieves project information from a Notion data source and maps its properties into the application's database model.

### Supported Properties

| Notion Property | Purpose |
|---|---|
| `Project name` | Project title |
| `Status` | Current project development status |
| `Skills Used` | Technologies and skills associated with the project |
| `Next Possible Action` | Suggested next development task |
| `Priority` | Project priority |
| `Potential` | Project potential classification |
| `Repository` | GitHub repository URL |
| `Locally Last Updated` | Date of the latest local project update |
| `GitHub Last Updated` | Latest GitHub push timestamp |
| `IDE` | Development environment used |

### Synchronization Direction

The integration uses two synchronization paths.

**Notion → PostgreSQL**

- Retrieve project records from Notion.
- Handle paginated responses.
- Convert Notion properties into application fields.
- Insert new records.
- Update existing records.
- Preserve relevant GitHub synchronization metadata when appropriate.

**PostgreSQL → Notion**

- Create Notion pages when new projects are created through the dashboard.
- Update Notion pages when project properties change.
- Archive corresponding Notion pages when projects are deleted through the dashboard.
- Write GitHub push timestamps into the `GitHub Last Updated` property.

Notion remains the primary workspace for project management, while PostgreSQL provides the dashboard's application data.

---

## GitHub Integration

The GitHub integration retrieves repository metadata through the GitHub REST API.

Its primary purpose is to track repository activity without checking every repository during every synchronization run.

### Repository Information

The integration retrieves:

- Repository information.
- Latest push timestamp (`pushed_at`).

The latest push timestamp is stored in PostgreSQL and synchronized to Notion through the `GitHub Last Updated` property.

### Scheduling and Caching

The GitHub synchronization service uses the following configuration:

| Setting | Value |
|---|---|
| Maximum repositories per run | 40 |
| Cache duration | 6 hours |
| Retry delay | 15 minutes |
| HTTP request timeout | 10 seconds |

Repositories are prioritized using their previous check timestamps.

The scheduling system:

1. Identifies projects with valid repository URLs.
2. Selects repositories whose next check time has arrived.
3. Prioritizes repositories that have never been checked.
4. Prioritizes older checks.
5. Processes up to 40 repositories per run.
6. Updates the next scheduled check time.
7. Defers unprocessed repositories to subsequent runs.

### Rate Limit Handling

The integration handles GitHub API rate limits, including HTTP 403 and 429 responses.

When a rate limit is encountered:

- The service identifies the retry delay when available.
- The current repository is deferred.
- Remaining repositories in the batch are deferred.
- The synchronization process stops making additional GitHub requests for that run.

This prevents unnecessary requests when the API temporarily restricts access.

### Notion Writeback

GitHub synchronization is tracked separately from Notion synchronization.

The database maintains:

| Field | Purpose |
|---|---|
| `github_pushed_at` | Latest repository push timestamp |
| `github_last_checked_at` | Last completed GitHub check |
| `github_next_check_at` | Next scheduled GitHub check |
| `github_notion_synced_at` | Last successful Notion writeback associated with the current GitHub timestamp |

When a repository's push timestamp changes, its Notion synchronization marker is reset.

The backend then updates the corresponding Notion page. Once successful, it records the synchronization timestamp to avoid unnecessary repeated writebacks.

---

## Synchronization System

The application uses multiple mechanisms to keep project information synchronized.

### Scheduled Synchronization

GitHub Actions triggers synchronization endpoints through scheduled workflows.

The workflows can also be executed manually through GitHub Actions.

### Notion Webhooks

Notion webhooks notify the backend when relevant workspace changes occur.

The backend processes the event and retrieves the necessary page information to synchronize the database.

Webhook requests are authenticated using an HMAC-SHA256 signature.

### Synchronization Authentication

Protected synchronization endpoints require an `X-Sync-Token` request header.

The backend validates the provided token against the configured synchronization secret.

This prevents unauthorized requests from triggering synchronization operations.

---

## Database Schema

The main database entity is the `Project` model.

It stores project information from Notion alongside GitHub synchronization metadata.

The database maintains information such as:

- Project identity.
- Notion page ID.
- Project name.
- Status.
- Priority.
- Potential.
- Skills used.
- Next possible action.
- Repository URL.
- Development environment.
- Local update date.
- GitHub push timestamp.
- GitHub check timestamps.
- Notion synchronization timestamp.

### Database Migrations

Alembic is used to manage database schema changes.

Create a migration:

```bash
alembic revision -m "migration description"
```

Apply migrations:

```bash
alembic upgrade head
```

Check the current database revision:

```bash
alembic current
```

Verify that the database schema matches the SQLAlchemy models:

```bash
alembic check
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/philip-euste/notion-project-dashboard.git

cd notion-project-dashboard
```

### Requirements

- Python 3.10 or newer.
- Node.js and npm.
- PostgreSQL-compatible database.
- Notion integration with access to the project data source.
- GitHub account and repository API access.

### Backend Installation

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Frontend Installation

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

---

## Configuration

The application uses environment variables to configure external services and database access.

### Backend Environment Variables

Create a `.env` file inside the backend directory.

```env
DATABASE_URL=

NOTION_API_KEY=

GITHUB_TOKEN=

SYNC_SECRET=
```

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `NOTION_API_KEY` | Notion internal integration secret |
| `GITHUB_TOKEN` | GitHub personal access token for authenticated API requests |
| `SYNC_SECRET` | Shared secret used to authenticate synchronization requests |

Do not commit environment files or expose API tokens in source code.

### Frontend Environment Variables

Configure the frontend API URL using a `.env` file inside the frontend directory.

```env
VITE_API_URL=http://127.0.0.1:8000
```

For production, replace the local backend URL with the deployed API endpoint.

---

## Usage

### Running the Backend

Navigate to the `backend/` directory and activate the virtual environment.

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### Running the Frontend

Navigate to the `frontend/` directory.

Start the Vite development server:

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

### API Endpoints

The backend exposes endpoints for project management, synchronization, and webhook processing.

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/projects/` | GET | Retrieve all projects |
| `/api/projects/{id}` | GET | Retrieve a specific project |
| `/api/projects/` | POST | Create a project |
| `/api/projects/{id}` | PATCH | Update a project |
| `/api/projects/{id}` | DELETE | Archive and remove a project from the dashboard |
| `/api/sync/notion` | POST | Trigger Notion synchronization |
| `/api/sync/github` | POST | Trigger GitHub synchronization |
| `/api/webhooks/notion` | POST | Receive Notion webhook events |

Protected synchronization endpoints require the `X-Sync-Token` header.

---

## Deployment

The application uses separate hosting services for its frontend, backend, and database.

| Component | Platform | Purpose |
|---|---|---|
| Frontend | Cloudflare Pages | React application hosting |
| Backend | Render | FastAPI application hosting |
| Database | Neon | PostgreSQL database hosting |
| Automation | GitHub Actions | Scheduled synchronization |
| Project Workspace | Notion | Primary project management workspace |
| Repository Hosting | GitHub | Source control and repository metadata |

### Backend Deployment

The FastAPI backend is deployed through Render.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Frontend Deployment

The frontend is intended to be deployed through Cloudflare Pages.

Build command:

```bash
npm run build
```

Build output directory:

```text
dist
```

The frontend must use the deployed backend URL through `VITE_API_URL`.

### Database Deployment

Neon hosts the PostgreSQL database.

The backend connects to the database through the configured `DATABASE_URL`.

Database migrations should be applied before deploying backend changes that depend on new columns or tables.

---

## Dependencies

### Backend

- Python 3.10+
- FastAPI
- Uvicorn
- SQLAlchemy
- Psycopg
- Alembic
- Pydantic Settings
- Python Dotenv
- HTTPX

### Frontend

- React
- Vite
- JavaScript
- CSS

### External Services

- Notion API
- GitHub REST API
- Neon PostgreSQL
- Render
- Cloudflare Pages
- GitHub Actions

---

## Design Philosophy

Notion Project Dashboard is designed around centralized project management and automated synchronization.

Instead of maintaining separate project records manually across different platforms, the application connects Notion, PostgreSQL, and GitHub through a shared backend.

The system separates project management data from repository activity.

**Project Management Data**

Contains project names, statuses, priorities, potential classifications, skills, development environments, and next possible actions.

**Repository Activity Data**

Contains GitHub repository information, push timestamps, and synchronization scheduling metadata.

**Synchronization State**

Tracks when records were checked, when they should be checked again, and whether changes have been successfully written back to Notion.

The objective is to provide a centralized dashboard while preserving Notion as the primary project workspace and reducing unnecessary API requests through scheduled synchronization and caching.

---

## Repository

GitHub: https://github.com/philip-euste/notion-project-dashboard

---

## License

See the `LICENSE` file for licensing information, if included.