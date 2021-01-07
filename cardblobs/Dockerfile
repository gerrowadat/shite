FROM python:3.8
RUN apt-get update
RUN mkdir /app
WORKDIR /app
RUN git clone https://github.com/gerrowadat/shite.git /app/shite
RUN ln -s /app/shite/tides/irishtides.py /app/shite/cardblobs/irishtides.py
RUN pip install -r /app/shite/cardblobs/requirements.txt
EXPOSE 54332
ENTRYPOINT [ "python" ]
CMD [ "/app/shite/cardblobs/app.py" ]
