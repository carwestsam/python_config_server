FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY ./src /app
COPY ./sample_config /config
ENV CONFIG_URI file:///config
