FROM geerlingguy/docker-ubuntu2004-ansible:latest
RUN apt-get update -y && apt-get install -y aptitude build-essential python3-pip python3 python3-apt aptitude python-apt tree cron curl dumb-init
RUN pip3 install ansible ansible-runner ruamel.yaml
RUN mkdir -p /app
COPY requirements.yml /app/
RUN cd /app && ansible-galaxy install -r requirements.yml
COPY . /app
WORKDIR /app

RUN python3 run.py && ./bin/start.sh && python3 run.py
CMD python3 run.py