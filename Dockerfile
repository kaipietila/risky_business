FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /rb
WORKDIR /rb
COPY requirements.txt /rb/
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download de_core_news_sm
COPY . /rb/