import sys, os

candidates = [
    os.path.join(os.getcwd(), "gitlab_openapi_client"),
    os.path.join(os.getcwd(), "gitlab_openapi_client", "openapi_client"),
    os.path.join(os.getcwd(), "openapi_client"),
]

added = False
for cand in candidates:
    if os.path.isdir(cand):
        print("Adding to sys.path:", cand)
        sys.path.insert(0, cand)
        added = True
        break
if not added:
    print("No generated client folder found in candidates, continuing with default sys.path")

try:
    from openapi_client.configuration import Configuration
    from openapi_client.api_client import ApiClient
    
    try:
        from openapi_client.api.projects_api import ProjectsApi
    except Exception:
        import importlib
        ProjectsApi = importlib.import_module("openapi_client.api.projects_api").ProjectsApi

    cfg = Configuration(host="https://gitlab.boon.com.au/api/v4", api_key={"Private-Token":"personalcn_fGc1stmBzycXEzP2s"})
    with ApiClient(cfg) as client:
        api = ProjectsApi(client)
        print("Available methods:", [m for m in dir(api) if not m.startswith("_")])
        resp = api.projects_get(per_page=5, page=1)
        print("Response type:", type(resp), "len:", len(resp))
        for p in resp:
            try:
                print(f"{p.id} {p.name}")
            except Exception:
                print(p)
except Exception as e:
    print("OpenAPI import / call failed:", type(e).__name__, e)
