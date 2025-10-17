FROM python:3.11-bullseye

WORKDIR /app

COPY requirements.txt .

RUN apt-get update -y && apt-get install -y texlive-latex-extra

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app"

CMD [ "tail -f /dev/null" ]