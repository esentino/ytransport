-- upgrade --
CREATE TABLE IF NOT EXISTS "town" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "latitude" DOUBLE PRECISION NOT NULL,
    "longitude" DOUBLE PRECISION NOT NULL
);
CREATE TABLE IF NOT EXISTS "player" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL,
    "money" INT NOT NULL  DEFAULT 50000,
    "town_id" INT NOT NULL REFERENCES "town" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "transport" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "load" INT NOT NULL,
    "delivered_load" INT NOT NULL,
    "money" INT NOT NULL,
    "begin_id" INT NOT NULL REFERENCES "town" ("id") ON DELETE CASCADE,
    "destination_id" INT NOT NULL REFERENCES "town" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "truck" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "price" INT NOT NULL,
    "speed" INT NOT NULL,
    "max_load" INT NOT NULL
);
CREATE TABLE IF NOT EXISTS "playertruck" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "load" INT NOT NULL,
    "start_transport" TIMESTAMPTZ,
    "player_id" INT NOT NULL REFERENCES "player" ("id") ON DELETE CASCADE,
    "transport_id" INT REFERENCES "transport" ("id") ON DELETE CASCADE,
    "truck_id" INT NOT NULL REFERENCES "truck" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
