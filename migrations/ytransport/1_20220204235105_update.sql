-- upgrade --
CREATE UNIQUE INDEX "uid_player_usernam_c6ed95" ON "player" ("username");
-- downgrade --
DROP INDEX "idx_player_usernam_c6ed95";
