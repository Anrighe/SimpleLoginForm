CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users
(
  	username TEXT NOT NULL UNIQUE PRIMARY KEY,
  	password TEXT NOT NULL
);

/* Creates a new user */
/* INSERT INTO users (username, password) VALUES ('admin', crypt('admin', gen_salt('bf'))); */

/* Modifies a user password */
/* UPDATE users SET password = crypt('admin', gen_salt('bf'))) WHERE username = 'admin'; */

/* Looks up for the 'admin' username */
/* SELECT *
   FROM users
   WHERE username = 'admin' AND password = crypt('admin', password); */
   