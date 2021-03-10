FROM python:3.8
RUN apt-get -y update
RUN apt-get install -y python3-pip build-essential libglib2.0-dev libyaml-dev
RUN pip3 install --upgrade plantgateway 

RUN ln -s /config/plantgw.yaml /root/.plantgw.yaml
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

WORKDIR /config
ENTRYPOINT [ "/entrypoint.sh" ]
CMD ["plantgateway"]
