FROM python:3
WORKDIR /usr/src/app
RUN pip install numpy matplotlib seaborn && apt-get install imagemagick
COPY ./src /usr/src/app
CMD ["python", "main.py", "/tmp/output/"]
