FROM python:3.8

RUN pip3 install tweepy

RUN mkdir app
RUN git clone https://github.com/magnusnissel/cleantweets.git /app/cleantweets

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

WORKDIR /config
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/app/cleantweets/cleantweets.py"]
