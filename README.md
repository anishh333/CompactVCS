# CompactVCS

CompactVCS is a simple version control system backed by Supabase, with a Streamlit UI to manage repositories, files, commits, and branches.

## Prerequisites

- Python 3.10+
- A Supabase project with tables: `repository`, `file`, `commit`, `commitfile`, `branch`
- Supabase URL and Service Role API key

## Setup

1. Create a virtual environment and install deps:
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: . .venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with:
```env
supabase_url=YOUR_SUPABASE_URL
supabase_key=YOUR_SUPABASE_SERVICE_ROLE_KEY
```

3. Ensure the following tables exist (minimal columns):
   - `repository(repo_id serial pk, name text)`
   - `file(file_id serial pk, repo_id int, filename text, content text)`
   - `commit(commit_id serial pk, repo_id int, message text, timestamp timestamptz default now())`
   - `commitfile(id serial pk, commit_id int, file_id int, version_number int, content text)`
   - `branch(branch_id serial pk, repo_id int, name text, head_commit_id int null)`

4. Run the app:
```bash
streamlit run streamlit_app.py
```

## Structure

- `src/dao/*`: Low-level DB access via Supabase
- `src/services/*`: Business logic orchestration
- `streamlit_app.py`: Streamlit UI, uses the services

## Notes

- Configuration is loaded from `.env` via `src/config.py:get_supabase()`.
- The UI supports: creating repos, adding/updating files, creating commits, viewing commit history, rollback to a commit, creating and merging branches (updates head).