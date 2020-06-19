FROM python:latest
ADD . /todo
WORKDIR /todo
RUN pip install flask pymongo bigchaindb-driver 
