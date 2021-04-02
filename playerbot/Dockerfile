FROM python:3.8
RUN pip3 install --upgrade absl-py discord.py requests

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

RUN git clone https://github.com/gerrowadat/shite.git /shite

WORKDIR /config
ENTRYPOINT [ "/entrypoint.sh" ]
CMD ["python3"]
