FROM python:3.9

WORKDIR /app 

COPY . /app 

RUN pip install flask flask_sqlalchemy pymysql

EXPOSE 5002

CMD ["python", "read_service.py"] 