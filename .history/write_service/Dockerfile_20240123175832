FROM python:3.9

WORKDIR /app 

COPY . /app 

RUN pip install flask flask_sqlalchemy pymysql

EXPOSE 5001

CMD ["python", "write_service.py"] 