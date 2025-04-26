-- Esquema de la base de dades per a l'aplicació de gestió de tasques

CREATE TABLE IF NOT EXISTS tasques (
    id SERIAL PRIMARY KEY,
    titol TEXT NOT NULL,
    descripcio TEXT,
    data_venciment DATE,
    completat BOOLEAN DEFAULT false
);
