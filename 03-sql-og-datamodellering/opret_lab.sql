-- Laboratoriedatabase til dag 3.
-- Opret databasen:  sqlite3 lab.db < opret_lab.sql
-- Start forfra:     rm lab.db  og kør kommandoen igen.

PRAGMA foreign_keys = ON;

CREATE TABLE instrument (
    id    INTEGER PRIMARY KEY,
    navn  TEXT NOT NULL UNIQUE,
    type  TEXT NOT NULL
);

CREATE TABLE forsoeg (
    id         INTEGER PRIMARY KEY,
    titel      TEXT NOT NULL,
    startdato  TEXT NOT NULL,   -- ISO-format: ÅÅÅÅ-MM-DD
    ansvarlig  TEXT NOT NULL
);

CREATE TABLE maaling (
    id             INTEGER PRIMARY KEY,
    forsoeg_id     INTEGER NOT NULL REFERENCES forsoeg(id),
    instrument_id  INTEGER NOT NULL REFERENCES instrument(id),
    tidspunkt      TEXT NOT NULL,   -- ISO-format: ÅÅÅÅ-MM-DD TT:MM
    temperatur     REAL,            -- °C, NULL hvis ikke målt
    tryk           REAL             -- hPa, NULL hvis ikke målt
);

INSERT INTO instrument (id, navn, type) VALUES
    (1, 'T-100', 'termometer'),
    (2, 'B-20',  'barometer'),
    (3, 'M-5',   'multisensor'),
    (4, 'S-1',   'spektrometer');

INSERT INTO forsoeg (id, titel, startdato, ansvarlig) VALUES
    (1, 'Kalibrering',     '2026-09-01', 'Sofie'),
    (2, 'Temperaturserie', '2026-09-08', 'Sofie'),
    (3, 'Trykfald',        '2026-09-15', 'Mads'),
    (4, 'Pilotforsøg',     '2026-10-01', 'Ida');

INSERT INTO maaling (forsoeg_id, instrument_id, tidspunkt, temperatur, tryk) VALUES
    (1, 1, '2026-09-01 09:00', 20.1, NULL),
    (1, 2, '2026-09-01 09:00', NULL, 1013.2),
    (1, 3, '2026-09-01 09:05', 20.3, 1013.0),
    (1, 3, '2026-09-01 09:10', 20.2, 1013.1),
    (2, 3, '2026-09-08 10:00', 18.5, 1009.4),
    (2, 3, '2026-09-08 11:00', 21.0, 1009.1),
    (2, 3, '2026-09-08 12:00', 23.7, 1008.8),
    (2, 3, '2026-09-08 13:00', 26.2, 1008.5),
    (2, 1, '2026-09-08 13:00', 26.0, NULL),
    (2, 3, '2026-09-08 14:00', 28.9, 1008.3),
    (2, 1, '2026-09-08 14:00', 29.1, NULL),
    (3, 2, '2026-09-15 08:00', NULL, 1020.5),
    (3, 2, '2026-09-15 09:00', NULL, 1015.2),
    (3, 3, '2026-09-15 09:00', 19.4, 1015.0),
    (3, 2, '2026-09-15 10:00', NULL, 1004.8),
    (3, 3, '2026-09-15 10:00', 19.6, 1004.9),
    (3, 2, '2026-09-15 11:00', NULL, 997.3),
    (3, 3, '2026-09-15 11:00', 19.9, 997.0);
