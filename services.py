from db import get_session, Project
from config import GITLAB_API_URL, PRIVATE_TOKEN
import logging

logger = logging.getLogger(__name__)

# Try to import the generated OpenAPI client
OPENAPI_AVAILABLE = False
try:
    from openapi_client.configuration import Configuration
    from openapi_client.api_client import ApiClient
    try:
        from openapi_client.api.projects_api import ProjectsApi
    except Exception:
        from openapi_client.api.default_api import DefaultApi as ProjectsApi
    OPENAPI_AVAILABLE = True
    logger.info("openapi_client available - fetch_projects will use it automatically.")
except Exception:
    OPENAPI_AVAILABLE = False
    logger.debug("openapi_client not available - will use requests fallback.", exc_info=True)

def fetch_projects_openapi(per_page=10, page=1):
    """Fetch projects using the generated OpenAPI client and save to DB."""
    cfg = Configuration(host=GITLAB_API_URL, api_key={"Private-Token": PRIVATE_TOKEN})
    with ApiClient(cfg) as client:
        api = ProjectsApi(client)

        if hasattr(api, "projects_get"):
            resp = api.projects_get(per_page=per_page, page=page)
        elif hasattr(api, "list_projects"):
            resp = api.list_projects(per_page=per_page, page=page)
        elif hasattr(api, "get_projects"):
            resp = api.get_projects(per_page=per_page, page=page)
        else:
            raise RuntimeError(
                "Generated Projects API doesn't expose a known list method. "
                "Inspect dir(api) to find the method name."
            )

        session = get_session()
        saved = 0
        try:
            for proj in resp or []:
                pid = None
                name = None
                desc = None

                if hasattr(proj, "id") or hasattr(proj, "name"):
                    pid = getattr(proj, "id", None)
                    name = getattr(proj, "name", None)
                    desc = getattr(proj, "description", None)

                if pid is None and isinstance(proj, dict):
                    pid = proj.get("id")
                    name = proj.get("name")
                    desc = proj.get("description")

                if pid is None and hasattr(proj, "to_dict"):
                    try:
                        d = proj.to_dict()
                        pid = d.get("id")
                        name = d.get("name")
                        desc = d.get("description")
                    except Exception:
                        pass

                if pid is None:
                    logger.debug("Skipping unrecognizable project item: %r", proj)
                    continue

                try:
                    pid_int = int(pid)
                except Exception:
                    logger.debug("Skipping project with non-int id: %r", pid)
                    continue

                existing = session.query(Project).filter(Project.id == pid_int).first()
                if not existing:
                    project = Project(id=pid_int, name=name or "unknown", description=desc)
                    session.add(project)
                    saved += 1

            session.commit()
            logger.info(f"Saved {saved} projects to database (via OpenAPI client).")
        finally:
            session.close()


def fetch_projects(per_page=10, page=1):
    if OPENAPI_AVAILABLE:
        try:
            return fetch_projects_openapi(per_page=per_page, page=page)
        except Exception as e:
            logger.warning(
                "OpenAPI client failed, falling back to requests implementation: %s", e, exc_info=True
            )

    import requests
    
    headers = {"Private-Token": PRIVATE_TOKEN}
    url = f"{GITLAB_API_URL}/projects?per_page={per_page}&page={page}"

    try:
        logger.info("Fetching projects from GitLab API (requests fallback)...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        projects = response.json()

        session = get_session()
        saved = 0
        try:
            for proj in projects:
                existing = session.query(Project).filter(Project.id == proj["id"]).first()
                if not existing:
                    project = Project(
                        id=proj["id"],
                        name=proj["name"],
                        description=proj.get("description"),
                    )
                    session.add(project)
                    saved += 1
            session.commit()
            logger.info(f"Saved {saved} projects to database.")
        finally:
            session.close()
    except Exception as e:
        logger.error(f"Error fetching projects: {e}", exc_info=True)

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
        logger.error(f"Error listing projects: {e}", exc_info=True)
    finally:
        session.close()
