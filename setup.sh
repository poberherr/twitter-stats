#!/bin/bash

echo "Type the USER NAME for the DB user you want to create"
read user_name

echo "Type the USER PASSWORD for the DB user you want to create"
read user_password

sudo -u postgres psql -c "CREATE USER $user_name WITH PASSWORD '$user_password';"

echo "Type the DB NAME for the DB user you want to create"
read db_name
sudo -u postgres psql -c "CREATE DATABASE $db_name WITH ENCODING 'UTF8';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $db_name TO $user_name;"


# log back to normal user
exit
