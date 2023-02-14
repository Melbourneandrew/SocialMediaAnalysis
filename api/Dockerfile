FROM pytorch/pytorch:latest

#RUN apk update
#RUN apk add make automake gcc g++ subversion python3-dev
RUN apt-get update \
     && apt-get install -y \
        libgl1-mesa-glx \
        libx11-xcb1 \
     && apt-get clean all \
     && rm -r /var/lib/apt/lists/*

WORKDIR /app
COPY container_requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --default-timeout=900 -r requirements.txt

COPY . /app
EXPOSE 4001
CMD ["flask", "run", "--host", "0.0.0.0"]
