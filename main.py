import argparse
import logging
from services import fetch_projects, list_projects 
from db import get_session, Project

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Attempt to import generated OpenAPI client
OPENAPI_AVAILABLE = False
try:
    from openapi_client.configuration import Configuration
    from openapi_client.api_client import ApiClient
    from openapi_client.api.projects_api import ProjectsApi
    OPENAPI_AVAILABLE = True
    logger.info("openapi_client available — you can use --use-openapi with fetch.")
except Exception:
    OPENAPI_AVAILABLE = False

def add_project(id, name, description=None):
    """Add a new project manually into the database."""
    session = get_session()
    try:
        project = Project(id=id, name=name, description=description)
        session.add(project)
        session.commit()
        logger.info(f"Added project [{id}] {name}")
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to add project: {e}")
    finally:
        session.close()

def update_project(id, description):
    """Update the description of a project."""
    session = get_session()
    try:
        project = session.query(Project).filter(Project.id == id).first()
        if project:
            project.description = description
            session.commit()
            logger.info(f"Updated project [{id}] {project.name} with new description.")
        else:
            logger.warning(f"No project found with ID {id}")
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to update project: {e}")
    finally:
        session.close()

def delete_project(id):
    """Delete a project by ID."""
    session = get_session()
    try:
        project = session.query(Project).filter(Project.id == id).first()
        if project:
            session.delete(project)
            session.commit()
            logger.info(f"Deleted project [{id}] {project.name}")
        else:
            logger.warning(f"No project found with ID {id}")
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to delete project: {e}")
    finally:
        session.close()

def fetch_projects_openapi(per_page=10, page=1):
    """Fetch projects using the generated OpenAPI client and save to DB."""
    if not OPENAPI_AVAILABLE:
        logger.warning("OpenAPI client not available; falling back to requests-based fetch.")
        return fetch_projects(per_page=per_page, page=page)

    cfg = Configuration(host="https://gitlab.boon.com.au/api/v4", api_key={"Private-Token": "personalcn_fGc1stmBzycXEzP2s"})
    with ApiClient(cfg) as client:
        api = ProjectsApi(client)

        if hasattr(api, "projects_get"):
            resp = api.projects_get(per_page=per_page, page=page)
        elif hasattr(api, "list_projects"):
            resp = api.list_projects(per_page=per_page, page=page)
        else:
            raise RuntimeError("Generated Projects API doesn't expose a known list method. Inspect dir(api).")

        session = get_session()
        saved = 0
        for item in resp or []:
            pid = None
            name = None
            desc = None
            try:
                if hasattr(item, "id"):
                    pid = getattr(item, "id")
                elif hasattr(item, "to_dict"):
                    pid = item.to_dict().get("id")
                else:
                    pid = item.get("id") if isinstance(item, dict) else None

                if hasattr(item, "name"):
                    name = getattr(item, "name")
                elif hasattr(item, "to_dict"):
                    name = item.to_dict().get("name")
                else:
                    name = item.get("name") if isinstance(item, dict) else None

                if hasattr(item, "description"):
                    desc = getattr(item, "description")
                elif hasattr(item, "to_dict"):
                    desc = item.to_dict().get("description")
                else:
                    desc = item.get("description") if isinstance(item, dict) else None
            except Exception:
                logger.debug("Couldn't extract fields from an item; skipping.", exc_info=True)
                continue

            if pid is None:
                continue

            existing = session.query(Project).filter(Project.id == pid).first()
            if not existing:
                project = Project(id=int(pid), name=name or "unknown", description=desc)
                session.add(project)
                saved += 1

        session.commit()
        session.close()
        logger.info(f"Saved {saved} projects to database (via OpenAPI client).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitLab CLI")
    subparsers = parser.add_subparsers(dest="command")

    fetch_parser = subparsers.add_parser("fetch", help="Fetch projects from GitLab API")
    fetch_parser.add_argument("--per-page", type=int, default=10)
    fetch_parser.add_argument("--page", type=int, default=1)
    fetch_parser.add_argument("--use-openapi", action="store_true", help="Use generated OpenAPI client if available")

    subparsers.add_parser("list", help="List projects in database")
    
    add_parser = subparsers.add_parser("add", help="Add a project manually")
    add_parser.add_argument("id", type=int)
    add_parser.add_argument("name", type=str)
    add_parser.add_argument("--description", type=str, default=None)

    # Update project
    update_parser = subparsers.add_parser("update", help="Update project description")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("description", type=str)

    # Delete project
    delete_parser = subparsers.add_parser("delete", help="Delete a project by ID")
    delete_parser.add_argument("id", type=int)

    args = parser.parse_args()

    if args.command == "fetch":
        # minimal change here: call OpenAPI variant only if flag present
        if getattr(args, "use_openapi", False):
            fetch_projects_openapi(per_page=args.per_page, page=args.page)
        else:
            fetch_projects(per_page=args.per_page, page=args.page)
    elif args.command == "list":
        list_projects()
    elif args.command == "add":
        add_project(args.id, args.name, args.description)
    elif args.command == "update":
        update_project(args.id, args.description)
    elif args.command == "delete":
        delete_project(args.id)
    else:
        parser.print_help()
