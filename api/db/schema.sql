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

CREATE TABLE public.users
(
    id          uuid PRIMARY KEY   DEFAULT uuid_generate_v4(),
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    email       TEXT      NOT NULL UNIQUE,
    username    TEXT      NOT NULL,
    icon        uuid,
    bio         TEXT,
    status      jsonb     NOT NULL DEFAULT '{}', /* Json Object. See docs/database.md#status */ /* TODO: Actually do this small documentation */
    last_online TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_online   BOOLEAN   NOT NULL DEFAULT FALSE,
    is_banned   BOOLEAN   NOT NULL DEFAULT FALSE,
    is_verified BOOLEAN   NOT NULL DEFAULT FALSE
);

CREATE TABLE public.files
(
    id         uuid PRIMARY KEY   DEFAULT uuid_generate_v4(), /* Id is also the filename */
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by uuid      NOT NULL
);

CREATE TABLE public.guilds
(
    id         uuid PRIMARY KEY   DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    owner_id   uuid      NOT NULL,
    name       TEXT      NOT NULL,
    icon       uuid
);

CREATE TABLE public.channels
(
    id         uuid PRIMARY KEY   DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    guild_id   uuid      NOT NULL,
    name       TEXT      NOT NULL,
    type       INT       NOT NULL,
    parent     uuid
);

CREATE TABLE public.messages
(
    id         uuid PRIMARY KEY   DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id    uuid      NOT NULL,
    channel_id uuid      NOT NULL,
    body       TEXT      NOT NULL,
    embeds     jsonb     NOT NULL DEFAULT '{}' /* See https://www.postgresql.org/docs/current/datatype-json.html for justification for using jsonb instead of json */
);

CREATE TABLE public.message_attachments
(
    message_id uuid NOT NULL,
    file_id    uuid NOT NULL
);

CREATE TABLE public.roles
(
    id               uuid PRIMARY KEY    DEFAULT uuid_generate_v4(),
    created_at       TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    guild_id         uuid       NOT NULL,
    name             TEXT       NOT NULL,
    colour           VARCHAR(6) NOT NULL DEFAULT '000000',
    separate_display BOOLEAN    NOT NULL DEFAULT FALSE,
    permissions      INT        NOT NULL DEFAULT 0
);

CREATE TABLE public.user_roles
(
    user_id uuid NOT NULL,
    role_id uuid NOT NULL
);

CREATE TABLE public.guild_members
(
    user_id         uuid NOT NULL,
    guild_id        uuid NOT NULL,
    nickname        TEXT,
    profile_picture uuid NOT NULL /* Set the default profile picture to be the user's profile picture */
);

CREATE TABLE public.channel_members
(
    user_id     uuid NOT NULL,
    channel_id  uuid NOT NULL,
    permissions INT  NOT NULL DEFAULT 0
);

CREATE TABLE public.invites
(
    id          uuid PRIMARY KEY   DEFAULT uuid_generate_v4(),
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    guild_id    uuid      NOT NULL,
    channel_id  uuid      NOT NULL,
    created_by  uuid      NOT NULL,
    uses        INT       NOT NULL DEFAULT 1,
    expires_at  TIMESTAMP,
    target_user uuid,
    code        TEXT
);

CREATE TABLE secured.devices
(
    id          uuid PRIMARY KEY   DEFAULT uuid_generate_v4(),
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name        TEXT      NOT NULL,
    ip          TEXT      NOT NULL,
    mac         TEXT      NOT NULL,
    lang        TEXT      NOT NULL,
    os          TEXT      NOT NULL,
    screen_size TEXT      NOT NULL,
    country     TEXT      NOT NULL
);

CREATE TABLE secured.tokens
(
    user_id   uuid PRIMARY KEY NOT NULL,
    device_id uuid             NOT NULL,
    token     TEXT             NOT NULL,
    last_used TIMESTAMP        NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE secured.passwords
(
    user_id      uuid PRIMARY KEY,
    password     VARCHAR(130) NOT NULL,
    last_updated TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE secured.two_factor
(
    user_id      uuid PRIMARY KEY REFERENCES public.users (id),
    secret       TEXT          NOT NULL,
    backup_codes VARCHAR(8)[8] NOT NULL,
    last_updated TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

/* Create checks */
ALTER TABLE public.channels
    ADD CONSTRAINT channel_type_check CHECK (type >= 0 AND type <= 2);

/* Create functions */
CREATE OR REPLACE FUNCTION set_default_profile_picture()
    RETURNS TRIGGER AS
$$
BEGIN
    new.profile_picture = (SELECT icon FROM public.users WHERE id = new.user_id);
    RETURN new;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION hash_bigint(text) RETURNS bigint AS
$$
SELECT ('x' || SUBSTR(MD5($1), 1, 16))::BIT(64)::BIGINT;
$$ LANGUAGE sql;

/* Create triggers */
CREATE TRIGGER set_default_profile_picture
    BEFORE INSERT
    ON public.guild_members
EXECUTE FUNCTION set_default_profile_picture();

/* Create Rules */
CREATE OR REPLACE RULE update_last_updated AS
    ON UPDATE TO secured.passwords
    DO INSTEAD
    UPDATE secured.passwords
    SET last_updated = CURRENT_TIMESTAMP
    WHERE user_id = new.user_id;

CREATE OR REPLACE RULE update_last_updated_two_factor AS
    ON UPDATE TO secured.two_factor
    DO INSTEAD
    UPDATE secured.two_factor
    SET last_updated = CURRENT_TIMESTAMP
    WHERE user_id = new.user_id;

/* Create relations */
ALTER TABLE public.files
    ADD CONSTRAINT files_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users (id);

ALTER TABLE public.guilds
    ADD CONSTRAINT guilds_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users (id);
ALTER TABLE public.guilds
    ADD CONSTRAINT guilds_icon_fkey FOREIGN KEY (icon) REFERENCES public.files (id);

ALTER TABLE public.channels
    ADD CONSTRAINT channels_guild_id_fkey FOREIGN KEY (guild_id) REFERENCES public.guilds (id);
ALTER TABLE public.channels
    ADD CONSTRAINT channels_parent_fkey FOREIGN KEY (parent) REFERENCES public.channels (id);

ALTER TABLE public.messages
    ADD CONSTRAINT messages_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users (id);
ALTER TABLE public.messages
    ADD CONSTRAINT messages_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channels (id);

ALTER TABLE public.message_attachments
    ADD CONSTRAINT message_attachments_message_id_fkey FOREIGN KEY (message_id) REFERENCES public.messages (id);
ALTER TABLE public.message_attachments
    ADD CONSTRAINT message_attachments_file_id_fkey FOREIGN KEY (file_id) REFERENCES public.files (id);

ALTER TABLE public.roles
    ADD CONSTRAINT roles_guild_id_fkey FOREIGN KEY (guild_id) REFERENCES public.guilds (id);

ALTER TABLE public.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users (id);
ALTER TABLE public.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles (id);

ALTER TABLE public.guild_members
    ADD CONSTRAINT guild_members_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users (id);
ALTER TABLE public.guild_members
    ADD CONSTRAINT guild_members_guild_id_fkey FOREIGN KEY (guild_id) REFERENCES public.guilds (id);
ALTER TABLE public.guild_members
    ADD CONSTRAINT guild_members_profile_picture_fkey FOREIGN KEY (profile_picture) REFERENCES public.files (id);

ALTER TABLE public.channel_members
    ADD CONSTRAINT channel_members_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users (id);
ALTER TABLE public.channel_members
    ADD CONSTRAINT channel_members_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channels (id);

ALTER TABLE public.invites
    ADD CONSTRAINT invites_guild_id_fkey FOREIGN KEY (guild_id) REFERENCES public.guilds (id);
ALTER TABLE public.invites
    ADD CONSTRAINT invites_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channels (id);
ALTER TABLE public.invites
    ADD CONSTRAINT invites_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users (id);
ALTER TABLE public.invites
    ADD CONSTRAINT invites_target_user_fkey FOREIGN KEY (target_user) REFERENCES public.users (id);

ALTER TABLE secured.tokens
    ADD CONSTRAINT tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users (id);
ALTER TABLE secured.tokens
    ADD CONSTRAINT tokens_device_id_fkey FOREIGN KEY (device_id) REFERENCES secured.devices (id);

ALTER TABLE secured.passwords
    ADD CONSTRAINT passwords_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users (id);

ALTER TABLE secured.two_factor
    ADD CONSTRAINT two_factor_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users (id);

/* Apply permissions */
REVOKE ALL ON ALL TABLES IN SCHEMA secured FROM PUBLIC;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA secured TO disbroad;
GRANT USAGE ON SCHEMA secured TO disbroad;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO disbroad;
GRANT USAGE ON SCHEMA public TO disbroad;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO PUBLIC;
GRANT USAGE ON SCHEMA public TO PUBLIC;



