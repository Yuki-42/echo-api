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

CREATE TABLE public.files (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),  /* Id is also the filename */
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    created_by uuid NOT NULL
);

CREATE TABLE public.guilds (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    owner_id uuid NOT NULL,
    name TEXT NOT NULL,
    icon uuid
);

CREATE TABLE public.channels(
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    guild_id uuid NOT NULL,
    name TEXT NOT NULL,
    type INT NOT NULL,
    parent uuid
);

CREATE TABLE public.messages(
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    user_id uuid NOT NULL,
    channel_id uuid NOT NULL,
    body TEXT NOT NULL,
    embeds jsonb[] NOT NULL DEFAULT [],  /* See https://www.postgresql.org/docs/current/datatype-json.html for justification for using jsonb instead of json */
    attachments uuid[] NOT NULL DEFAULT []
);

CREATE TABLE public.roles(
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    guild_id uuid NOT NULL,
    name TEXT NOT NULL,
    colour VARCHAR(6) NOT NULL DEFAULT '000000',
    separate_display BOOLEAN NOT NULL DEFAULT FALSE,
    permissions INT NOT NULL DEFAULT 0
);

CREATE TABLE public.user_roles(
    user_id uuid NOT NULL,
    role_id uuid NOT NULL
);

CREATE TABLE public.guild_members(
    user_id uuid NOT NULL,
    guild_id uuid NOT NULL
);

CREATE TABLE public.channel_members(
    user_id uuid NOT NULL,
    channel_id uuid NOT NULL,
    permissions INT NOT NULL DEFAULT 0
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

/* Create checks */
ALTER TABLE public.channels
    ADD CONSTRAINT channel_type_check CHECK (type >= 0 AND type <= 2);


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

/* Create relations */


/* Apply permissions */
REVOKE ALL ON ALL TABLES IN SCHEMA secured FROM public;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA secured TO disbroad;
GRANT USAGE ON SCHEMA secured TO disbroad;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO disbroad;
GRANT USAGE ON SCHEMA public TO disbroad;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO public;
GRANT USAGE ON SCHEMA public TO public;



