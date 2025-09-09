## Overview
This is a simple command-line tool to interact with the GitLab API.  
It allows you to perform CRUD operations on GitLab projects using a local database.

## Project Structure
gitlab_cli/
│
├── main.py # Entry point for CLI commands
├── services.py # Functions to interact with GitLab API & database
├── database.py # Database models and session management
├── config.py # GitLab API configuration (URL and token)
├── requirements.txt # Python dependencies
└── gitlab.db # SQLite database file (auto-generated)

## Requirements
- Python 3.9+  
- Virtual environment

Install dependencies:
```bash
pip install -r requirements.txt

## Configuration
Set your GitLab API details in config.py:
![config.py](image-1.png)

## Usage
Activate virtual environment:
```bash
source .venv/bin/activate

1. Fetch projects from GitLab API (Create)
```bash
python main.py fetch --per-page 5 --page 1

2. List projects (Read)
```bash
python main.py list

3. Add a project manually (Create)
```bash
python main.py add 999 "demo-project" --description "Demo project"

4. Update a project description (Update)
```bash
python main.py update 999 "Updated description"

5. Delete a project (Delete)
```bash
python main.py delete 999

