FROM python:3.9.10-slim-buster
COPY ./code/ /usr/local/src/myscripts
WORKDIR /usr/local/src/myscripts
RUN apt-get update
RUN apt-get install ffmpeg -y
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["streamlit", "run", "ui.py", "--server.port", "80"]