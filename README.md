
1. Install dependencies with poetry or with pip
    - Install with pip
        ```shell
        python -m pip install poetry
        ```
    - Install with poetry
        ```shell
        python -m poetry install
        ```
2. You need .env file and should have these vars:
    - DB_USER={YOUR_DB_USER}
    - DB_PASSWORD={YOUR_DB_PASSWORD}
    - DB_HOST={YOUR_DB_HOST}
    - DB_PORT={YOUR_DB_PORT}
    - DB_NAME={YOUR_DB_NAME}
    - EMAIL_FROM={YOUR_EMAIL}
    - EMAIL_PASSWORD={YOUR_EMAIL_PASSWORD}
    - SECRET_MAIL={YOUR_HASH_CODE}
    
3. Run fastapi
    - Run with uvicorn
        ```shell
        python -m uvicorn backend.main:app --reload
        ```
3. To use the backend API url
    - For the interactive API
        http://127.0.0.1:8000/docs#/
    - For the json API
        http://127.0.0.1:8000/


