-- addresses.sql
-- Sarah = user_id 1
INSERT INTO addresses (user_id, street, city, state, zip_code, country, is_default)
VALUES
(1, '123 Lake Shore Dr', 'Chicago', 'IL', '60601', 'USA', TRUE),
(1, '500 W Madison St',  'Chicago', 'IL', '60661', 'USA', FALSE),

-- Other users
(2, '10 Market St',      'San Francisco', 'CA', '94105', 'USA', TRUE),
(3, '200 Broadway',      'New York',      'NY', '10007', 'USA', TRUE);