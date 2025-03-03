CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    theme VARCHAR(20) DEFAULT 'dark'
);

CREATE TABLE memes (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    category VARCHAR(50) NOT NULL
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    sender VARCHAR(50) NOT NULL,
    text TEXT NOT NULL
);
