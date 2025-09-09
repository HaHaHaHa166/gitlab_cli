import argparse
import logging
from services import fetch_projects, list_projects
from db import get_session, Project

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitLab CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Fetch projects
    fetch_parser = subparsers.add_parser("fetch", help="Fetch projects from GitLab API")
    fetch_parser.add_argument("--per-page", type=int, default=10)
    fetch_parser.add_argument("--page", type=int, default=1)

    # List projects
    subparsers.add_parser("list", help="List projects in database")

    # Add project
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
