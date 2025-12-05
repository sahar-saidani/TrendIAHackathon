CREATE TABLE accounts (
    account_id VARCHAR PRIMARY KEY,
    username VARCHAR,
    created_at DATE,
    followers INT,
    following INT,
    posts_per_day FLOAT,
    credibility VARCHAR
);

CREATE TABLE narratives (
    narrative_id VARCHAR PRIMARY KEY,
    token_id VARCHAR,
    topic VARCHAR,
    start_time TIMESTAMP,
    end_time TIMESTAMP
);

CREATE TABLE post_narrative_link (
    post_id VARCHAR,
    narrative_id VARCHAR,
    PRIMARY KEY (post_id, narrative_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
    FOREIGN KEY (narrative_id) REFERENCES narratives(narrative_id) ON DELETE CASCADE
);
