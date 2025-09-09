from db import get_session, Project
from config import GITLAB_API_URL, PRIVATE_TOKEN
import logging

logger = logging.getLogger(__name__)

def fetch_projects(per_page=10, page=1):
    import requests
    from config import GITLAB_API_URL, PRIVATE_TOKEN

    headers = {"Private-Token": PRIVATE_TOKEN}
    url = f"{GITLAB_API_URL}/projects?per_page={per_page}&page={page}"

    try:
        logger.info("Fetching projects from GitLab API...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        projects = response.json()

        session = get_session()
        saved = 0
        for proj in projects:
            existing = session.query(Project).filter(Project.id == proj["id"]).first()
            if not existing:
                project = Project(
                    id=proj["id"],
                    name=proj["name"],
                    description=proj.get("description")
                )
                session.add(project)
                saved += 1
        session.commit()
        logger.info(f"Saved {saved} projects to database.")
    except Exception as e:
        logger.error(f"Error fetching projects: {e}")

def list_projects():
    """List all projects in the database."""
    session = get_session()
    try:
        projects = session.query(Project).all()
        if not projects:
            print("No projects found in database.")
            return
        for p in projects:
            print(f"[{p.id}] {p.name} - {p.description}")
    except Exception as e:
        logger.error(f"Error listing projects: {e}")
    finally:
        session.close()
