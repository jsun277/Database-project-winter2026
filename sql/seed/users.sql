-- users.sql
INSERT INTO users (email, password_hash, first_name, last_name)
VALUES
('sarah@example.com', '$2b$12$dummyhashsarah', 'Sarah', 'Connor'),
('mike@example.com',  '$2b$12$dummyhashmike',  'Mike',  'Lee'),
('ava@example.com',   '$2b$12$dummyhashava',   'Ava',   'Patel');