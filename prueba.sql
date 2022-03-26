-- Crear una tabla
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);
CREATE TABLE sqlite_sequence(name,seq);
CREATE UNIQUE INDEX username ON users (username);

-- Query para ver datos internos
SELECT * FROM users;

-- Insertar datos
INSERT INTO users (username, hash) VALUES ("jhoneder1993", "1234");