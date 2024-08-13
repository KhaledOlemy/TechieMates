-- Create database, user, configuring privileges.
SET GLOBAL validate_password.length = 4;
SET GLOBAL validate_password.policy=LOW;
CREATE DATABASE IF NOT EXISTS techiemate_dev_db;
CREATE USER IF NOT EXISTS 'techiemate_dev'@'localhost' IDENTIFIED BY 'techiemate_dev_pwd';
GRANT ALL PRIVILEGES ON `techiemate_dev_db`.* TO 'techiemate_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'techiemate_dev'@'localhost';
FLUSH PRIVILEGES;
