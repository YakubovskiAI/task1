CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    birthday TIMESTAMP NOT NULL,
    name VARCHAR(50) NOT NULL,
    room INT NOT NULL,
    sex VARCHAR NOT NULL,
    CONSTRAINT fk_room FOREIGN KEY(room) REFERENCES rooms(id)
);