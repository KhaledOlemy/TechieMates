-- Create database, user, configuring privileges.
SET GLOBAL validate_password.length = 4;
SET GLOBAL validate_password.policy=LOW;
CREATE DATABASE IF NOT EXISTS techiemate_test_db;
CREATE USER IF NOT EXISTS 'techiemate_test'@'localhost' IDENTIFIED BY 'techiemate_test_pwd';
GRANT ALL PRIVILEGES ON `techiemate_test_db`.* TO 'techiemate_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'techiemate_test'@'localhost';
FLUSH PRIVILEGES;
USE techiemate_test_db;
-- Generate required tables
-- ************************************** `roadmaps`
CREATE TABLE `roadmap`
(
 `id`			varchar(100) NOT NULL ,
 `created_at`        	datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
 `updated_at`        	datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
 `title`             	text NOT NULL ,
 `short_description` 	text NOT NULL ,
 `long_description`  	text NULL ,

PRIMARY KEY (`id`)
);
-- ************************************** `users`
CREATE TABLE `user`
(
 `id`			varchar(100) NOT NULL ,
 `created_at`      	datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
 `updated_at`      	datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
 `first_name`	   	text NOT NULL ,
 `last_name`       	text NOT NULL ,
 `password`        	text NOT NULL ,
 `email`           	text NOT NULL ,
 `phone`           	text NULL ,
 `active_roadmap`  	varchar(100) NULL ,
 `partner_id`      	varchar(100) NULL ,

 PRIMARY KEY (`id`)
);
ALTER TABLE user
ADD CONSTRAINT active_roadmap_roadmaps_fk
FOREIGN KEY (active_roadmap) REFERENCES roadmap(id);
ALTER TABLE user
ADD CONSTRAINT partner_id_users_fk
FOREIGN KEY (partner_id) REFERENCES user(id);
-- ************************************** `messages`
CREATE TABLE `message`
(
 `id`           	varchar(100) NOT NULL ,
 `created_at`   	datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
 `updated_at`   	datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
 `from_user`    	varchar(100) NOT NULL ,
 `to_user`		varchar(100) NOT NULL ,
 `text`			text NOT NULL ,

 PRIMARY KEY (`id`)
);
ALTER TABLE message
ADD CONSTRAINT from_user_users_fk
FOREIGN KEY (from_user) REFERENCES user(id);
ALTER TABLE message
ADD CONSTRAINT to_user_users_fk
FOREIGN KEY (to_user) REFERENCES user(id);
-- ************************************** `courses`
CREATE TABLE `course`
(
 `id`                varchar(100) NOT NULL ,
 `created_at`        datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
 `updated_at`        datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
 `title`             text NOT NULL ,
 `short_description` text NOT NULL ,
 `long_description`  text NULL ,
 `roadmap_id`        varchar(100) NOT NULL ,
 `order_in_roadmap`  int NOT NULL ,

 PRIMARY KEY (`id`)
);
ALTER TABLE course
ADD CONSTRAINT roadmap_id_roadmaps_fk
FOREIGN KEY (roadmap_id) REFERENCES roadmap(id);
-- ************************************** `vendors`
CREATE TABLE `vendor`
(
 `id`         varchar(100) NOT NULL ,
 `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
 `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
 `name`       text NOT NULL ,
 `link`       text NOT NULL ,
 `cost`       int NOT NULL ,
 `course_id`  varchar(100) NOT NULL ,

 PRIMARY KEY (`id`)
);
ALTER TABLE vendor
ADD CONSTRAINT course_id_courses_fk
FOREIGN KEY (course_id) REFERENCES course(id);
-- All tables created
-- -----------------------------------------------------------------------------------------
