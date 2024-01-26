docker build -t read-service ./read-service 

docker run -d -p 5000:5000 read-service 

docker build -t write-service ./write-service 

docker run -d -p 5000:5001 write-service 

  

docker pull mysql 

docker run –-name mysql-service -e MYSQL_ROOT_PASSWORD=xxxx -d mysql 