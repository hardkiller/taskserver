CREATE DATABASE taskserver;

CREATE USER 'vegan' IDENTIFIED BY 'your-very-secure-password';

GRANT ALL ON taskserver.* TO 'vegan'@'%';