CREATE TABLE IF NOT EXISTS tags (
    tag_type VARCHAR(128) NOT NULL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS tag_data (
    tag_type VARCHAR(128) REFERENCES tags(tag_type) ON DELETE CASCADE,
    title VARCHAR(128) DEFAULT NULL,
    info VARCHAR(512) NOT NULL
);