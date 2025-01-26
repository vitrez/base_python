# 1) docker build -t ping-pong .
# 2) docker run -it -d -p 8000:8000 ping-pong


FROM python:3.12-bookworm

ENV APP=/opt/app
RUN mkdir ${APP}
WORKDIR ${APP}
COPY requirements.txt app.py ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT ["python", "./app.py"]