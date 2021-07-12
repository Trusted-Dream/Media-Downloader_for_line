FROM python:3.9.1
ADD . /opt/app
WORKDIR /opt/app
RUN apt-get update && apt-get install -y \
wget xz-utils

RUN apt-get install -y ffmpeg \
&& apt clean \
&& rm -rf /var/lib/apt/lists/*

RUN pip install .
ENTRYPOINT ["python", "app.py"]
