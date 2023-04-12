import sys
import os
import uvicorn

from backend.endpoints.app import create_app

sys.path.append(os.getcwd())
app = create_app()


if __name__ == "__main__":
    if app:
        uvicorn.run("main:app", host="agdb", port=8000, reload=True)

