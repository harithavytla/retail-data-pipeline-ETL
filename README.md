This is a sample project on building a data pipeline from a MySQL Database which acts a transactional database to PostgreSQL Database which acts as a Data warehouse.
MySQL Database 'retail' stores the transactional and non transactional tables of a sample ecommerce website.
PostgreSQL Database 'retail_dw' is set up as a DWH which can be used for Analytics and Reporting purpose.
Below are the usecases which I have considered while building the pipeline :
  1) Analyzing the product table 
  2) Analyzing order counts based on order status 
  3) Analyzing the revenue generated and revenue pending on daily basis
Refer to the attached design document for details.  

# Getting Started
### SetUp docker 
Install docker. I have used a VM on GCP instance.
### Data
Clone data from https://github.com/dgadiraju/retail_db

```git clone https://github.com/dgadiraju/retail_db/create_db.sql```

### Setup MySQL(Source) and PostgreSQL(Target)
Pull mysql image 

```docker pull mysql```

Pull postgreSQL image 

```docker pull postgres```
   
Create a network between the source and target

```docker network create -d bridge data-pipeline-nw```

### Source DB

Execute below commands to create a container, enter the container, create Source DB, retail_user and excute create_tables script to create all the required tables

```
docker run --name mysql_retail -d -e MYSQL_ROOT_PASSWORD='' here -v retail_db:/retail_db --network data-pipeline-nw -p 3306:3306 mysql 
docker exec -it mysql_retail mysql -u root -p
CREATE DATABASE retail;
CREATE USER retail_user IDENTIFIED BY '';
FLUSH PRIVILEGES;
USE retail;
SOURCE /retail_db/create_db.sql;
````

### Target DB 

Execute below commands to create a container, enter the container, create Target DB, retail_user and grant all privileges to retail_user

```
sudo docker run --name pg_retail_dw  -e POSTGRES_PASSWORD='' -d -v /retail_db:/retail_dw -p 5432:5432 postgres
docker exec -it pg_retail_dw psql -U postgres -W
CREATE DATABASE retail_db;
CREATE USER retail_user WITH ENCRYPTED PASSWORD '';
GRANT ALL PRIVILEGES ON DATABASE retail_dw TO retail_user;
```

Code for this project has been developed in Python using PyCharm IDE. 

