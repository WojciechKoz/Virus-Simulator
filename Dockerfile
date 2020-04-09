FROM python:3
COPY ./src /usr/src/app
WORKDIR /usr/src/app
RUN pip install numpy matplotlib seaborn && apt install imagemagick 
CMD ["python", "main.py"]
