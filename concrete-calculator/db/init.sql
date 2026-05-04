CREATE TABLE IF NOT EXISTS diameters (
    name VARCHAR(10),
    diameter_mm INTEGER
);

INSERT INTO diameters (name, diameter_mm) VALUES
('HA8', 8),
('HA10', 10),
('HA12', 12),
('HA14', 14),
('HA16', 16),
('HA20', 20),
('HA25', 25),
('HA32', 32),
('HA40', 40)
ON CONFLICT DO NOTHING;