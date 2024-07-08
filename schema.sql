/*
Defines the schema for the database. Execute this script to set up the database.
*/

/* Create the disbroad user */
CREATE USER disbroad WITH ENCRYPTED PASSWORD 'disbroad';

/* Create the disbroad database */
CREATE DATABASE disbroad WITH OWNER disbroad;

/* Connect to the disbroad database */
\c disbroad;

/* Enable UUID extension */
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

/* Create the schema, Note that public is automatically created */
CREATE SCHEMA secured;

CREATE TABLE public.users (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    email TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL
);

CREATE TABLE public.guilds (
    
);

CREATE TABLE public.channels(

);

CREATE TABLE public.messages(

);

CREATE TABLE secured.passwords (
    user_id uuid PRIMARY KEY REFERENCES public.users(id),
    password VARCHAR(130) NOT NULL,
    last_updated TIMESTAMP NOT NULL DEFAULT current_timestamp
);

CREATE TABLE secured.two_factor (
    user_id uuid PRIMARY KEY REFERENCES public.users(id),
    secret TEXT NOT NULL,
    backup_codes VARCHAR(8)[8] NOT NULL,
    last_updated TIMESTAMP NOT NULL DEFAULT current_timestamp
);

/* Create Rules */
CREATE OR REPLACE RULE update_last_updated AS
    ON UPDATE TO secured.passwords
    DO INSTEAD
    UPDATE secured.passwords
    SET last_updated = current_timestamp
    WHERE user_id = NEW.user_id;

CREATE OR REPLACE RULE update_last_updated_two_factor AS
    ON UPDATE TO secured.two_factor
    DO INSTEAD
    UPDATE secured.two_factor
    SET last_updated = current_timestamp
    WHERE user_id = NEW.user_id;


/* Apply permissions */
REVOKE ALL ON ALL TABLES IN SCHEMA secured FROM public;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA secured TO disbroad;
GRANT USAGE ON SCHEMA secured TO disbroad;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO disbroad;
GRANT USAGE ON SCHEMA public TO disbroad;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO public;
GRANT USAGE ON SCHEMA public TO public;



