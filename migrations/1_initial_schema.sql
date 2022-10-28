SET SCHEMA 'public';

-- FUNCTION: edit_updated_at()

-- DROP FUNCTION IF EXISTS edit_updated_at();

CREATE OR REPLACE FUNCTION edit_updated_at()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
BEGIN
	NEW.updated_at = timezone('utc', now());
	RETURN NEW;
END;
$BODY$;

ALTER FUNCTION edit_updated_at()
    OWNER TO dokusei;


-- Type: tank_types

-- DROP TYPE IF EXISTS tank_types;

DO $$ BEGIN
	CREATE TYPE tank_types AS ENUM (
		'Light tank', 'Medium tank', 'Heavy tank', 'Super-heavy tank', 'Cruiser tank', 'Infrantry tank', 'Main battle tank', 'Tank destroyer', 'Assault gun', 'Self-propelled gun', 'Self-propelled howitzer'
	);
	EXCEPTION
		WHEN duplicate_object THEN null;
END $$;

ALTER TYPE tank_types
    OWNER TO dokusei;


-- Table: tank

-- DROP TABLE IF EXISTS tank;

CREATE TABLE IF NOT EXISTS tank
(
    name VARCHAR(100) NOT NULL,
    manufactured boolean NOT NULL DEFAULT TRUE,
    type tank_types NOT NULL,
    country VARCHAR(50) NOT NULL,
    created_at timestamp without time zone NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at timestamp without time zone NOT NULL DEFAULT timezone('utc'::text, now()),
    CONSTRAINT tank_pkey PRIMARY KEY (name)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS tank
    OWNER to dokusei;


-- Trigger: update_tank_updated_at

-- DROP TRIGGER IF EXISTS update_tank_updated_at ON tank;

CREATE OR REPLACE TRIGGER update_tank_updated_at
    BEFORE UPDATE 
    ON tank
    FOR EACH ROW
    EXECUTE FUNCTION edit_updated_at();


-- Table: tank_image

-- DROP TABLE IF EXISTS tank_image;

CREATE TABLE IF NOT EXISTS tank_image
(
    id SERIAL,
    tank_name VARCHAR(100) NOT NULL,
    image_link TEXT NOT NULL,
    created_at timestamp without time zone NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at timestamp without time zone NOT NULL DEFAULT timezone('utc'::text, now()),
    CONSTRAINT tank_image_pkey PRIMARY KEY (id),
    CONSTRAINT tank_image_tank_image_unique UNIQUE (image_link),
    CONSTRAINT tank_image_tank_name_fk FOREIGN KEY (tank_name)
        REFERENCES tank (name) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS tank_image
    OWNER to dokusei;


-- Index: tank_image_tank_name_index

-- DROP INDEX IF EXISTS tank_image_tank_name_index;

CREATE INDEX IF NOT EXISTS tank_image_tank_name_index
    ON tank_image USING btree
    (tank_name ASC NULLS LAST)
    TABLESPACE pg_default;

-- Trigger: update_tank_updated_at

-- DROP TRIGGER IF EXISTS update_tank_updated_at ON tank;

CREATE OR REPLACE TRIGGER update_tank_image_updated_at
    BEFORE UPDATE
    ON tank_image
    FOR EACH ROW
    EXECUTE FUNCTION edit_updated_at();
