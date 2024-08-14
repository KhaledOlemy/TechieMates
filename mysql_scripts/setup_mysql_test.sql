-- Create database, user, configuring privileges.
SET GLOBAL validate_password.length = 4;
SET GLOBAL validate_password.policy=LOW;
CREATE DATABASE IF NOT EXISTS tm_test_db;
CREATE USER IF NOT EXISTS 'tm_test'@'localhost' IDENTIFIED BY 'tm_test_pwd';
GRANT ALL PRIVILEGES ON `tm_test_db`.* TO 'tm_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'tm_test'@'localhost';
FLUSH PRIVILEGES;
