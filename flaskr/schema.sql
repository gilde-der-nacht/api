DROP TABLE IF EXISTS container;

CREATE TABLE container (
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
--     what does DEFAULT do?
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP,
    public TEXT,
    private TEXT,
    not_valid BOOLEAN
);