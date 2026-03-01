-- payment_methods.sql
-- Sarah = user_id 1
INSERT INTO payment_methods (user_id, method_type, last_four, is_default)
VALUES
(1, 'credit_card', '4242', TRUE),
(1, 'paypal',      NULL,   FALSE),

-- Other users
(2, 'credit_card', '1111', TRUE),
(3, 'credit_card', '2222', TRUE);