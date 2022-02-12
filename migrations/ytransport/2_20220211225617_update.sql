-- upgrade --
INSERT INTO town (name,latitude, longitude) VALUES ('Alfa town', 1, 1);
INSERT INTO town (name,latitude, longitude) VALUES ('Beta town', 50, 20);
INSERT INTO town (name,latitude, longitude) VALUES ('Gamma town', 20, 50);
INSERT INTO town (name,latitude, longitude) VALUES ('Delta town', 50, 50);
-- downgrade --
DELETE FROM town WHERE ID in (1, 2, 3, 4);
ALTER SEQUENCE town_id_seq RESTART WITH 1;
