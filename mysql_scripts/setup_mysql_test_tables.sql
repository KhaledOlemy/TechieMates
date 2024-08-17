USE tm_test_db;
-- Generate required tables
-- **************************************
CREATE TABLE roadmaps (
        id VARCHAR(60) NOT NULL, 
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
        title VARCHAR(256) NOT NULL, 
        short_description VARCHAR(4096) NOT NULL, 
        long_description VARCHAR(4096), 
        course_count INTEGER, 
        PRIMARY KEY (id), 
        UNIQUE (id)
);
CREATE TABLE users (
        id VARCHAR(60) NOT NULL, 
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
        first_name VARCHAR(256) NOT NULL, 
        last_name VARCHAR(256) NOT NULL, 
        password VARCHAR(256) NOT NULL, 
        email VARCHAR(256) NOT NULL, 
        phone VARCHAR(256), 
        roadmap_id VARCHAR(60), 
        partner_id VARCHAR(60), 
        PRIMARY KEY (id), 
        UNIQUE (id), 
        UNIQUE (email), 
        FOREIGN KEY(roadmap_id) REFERENCES roadmaps (id), 
        FOREIGN KEY(partner_id) REFERENCES users (id)
);
CREATE TABLE courses (
        id VARCHAR(60) NOT NULL, 
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
        title VARCHAR(256) NOT NULL, 
        short_description VARCHAR(4096) NOT NULL, 
        long_description VARCHAR(4096), 
        roadmap_id VARCHAR(60) NOT NULL, 
        order_in_roadmap INTEGER NOT NULL, 
        PRIMARY KEY (id), 
        CONSTRAINT course_roadmap_id_order_unique UNIQUE (order_in_roadmap, roadmap_id), 
        UNIQUE (id), 
        FOREIGN KEY(roadmap_id) REFERENCES roadmaps (id)
);
CREATE TABLE messages (
        id VARCHAR(60) NOT NULL, 
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
        from_user VARCHAR(60) NOT NULL, 
        to_user VARCHAR(60) NOT NULL, 
        text VARCHAR(4096) NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (id), 
        FOREIGN KEY(from_user) REFERENCES users (id), 
        FOREIGN KEY(to_user) REFERENCES users (id)
);
CREATE TABLE vendors (
        id VARCHAR(60) NOT NULL, 
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
        name VARCHAR(256) NOT NULL, 
        link VARCHAR(4096) NOT NULL, 
        cost INTEGER NOT NULL, 
        course_id VARCHAR(60) NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (id), 
        FOREIGN KEY(course_id) REFERENCES courses (id)
);
CREATE TABLE chapters (
        id VARCHAR(60) NOT NULL, 
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
        title VARCHAR(256) NOT NULL, 
        course_id VARCHAR(60) NOT NULL, 
        order_in_course INTEGER NOT NULL, 
        PRIMARY KEY (id), 
        CONSTRAINT chapter_course_id_order_unique UNIQUE (course_id, order_in_course), 
        UNIQUE (id), 
        FOREIGN KEY(course_id) REFERENCES courses (id)
);
CREATE TABLE progresses (
        id VARCHAR(60) NOT NULL, 
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
        user_id VARCHAR(60) NOT NULL, 
        roadmap_id VARCHAR(60) NOT NULL, 
        course_id VARCHAR(60) NOT NULL, 
        chapter_id VARCHAR(60) NOT NULL, 
        PRIMARY KEY (id), 
        CONSTRAINT progress_user_id_roadmap_id_unique UNIQUE (user_id, roadmap_id), 
        UNIQUE (id), 
        FOREIGN KEY(user_id) REFERENCES users (id), 
        FOREIGN KEY(roadmap_id) REFERENCES roadmaps (id), 
        FOREIGN KEY(course_id) REFERENCES courses (id), 
        FOREIGN KEY(chapter_id) REFERENCES chapters (id)
);
-- All tables created
-- -----------------------------------------------------------------------------------------
