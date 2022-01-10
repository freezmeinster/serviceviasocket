FROM python:3.7-slim

COPY server.py /server.py
RUN mkdir /root/share

ENTRYPOINT [ "python3","/server.py" ]
