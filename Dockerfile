FROM python:3.11

WORKDIR /ag_case

COPY README.md .

COPY requirements.txt .

COPY .env .

RUN pip install -r requirements.txt
RUN pip install --upgrade pip
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY ./backend ./backend

CMD ["uvicorn", "backend.main:app", "--host", "agdb", "--port", "8000"]