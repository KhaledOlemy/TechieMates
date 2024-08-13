-- Create database, user, configuring privileges.
SET GLOBAL validate_password.length = 4;
SET GLOBAL validate_password.policy=LOW;
CREATE DATABASE IF NOT EXISTS techiemate_test_db;
CREATE USER IF NOT EXISTS 'techiemate_test'@'localhost' IDENTIFIED BY 'techiemate_test_pwd';
GRANT ALL PRIVILEGES ON `techiemate_test_db`.* TO 'techiemate_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'techiemate_test'@'localhost';
FLUSH PRIVILEGES;
