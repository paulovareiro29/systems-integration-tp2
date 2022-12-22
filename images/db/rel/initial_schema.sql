CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS POSTGIS;
CREATE EXTENSION IF NOT EXISTS POSTGIS_TOPOLOGY;

CREATE TABLE public.areas (
	id				uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name			VARCHAR(250) UNIQUE NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.types (
	id				uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name			VARCHAR(250) UNIQUE NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);


CREATE TABLE public.hosts (
	id				uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name			VARCHAR(250) NOT NULL,
	verified		VARCHAR(250) NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.airbnbs (
	id				uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name			VARCHAR(250) NOT NULL,
	price			INT,
	host_id			uuid NOT NULL,
	type_id			uuid,
	area_id			uuid,
	neighbourhood	VARCHAR(250),
	street			VARCHAR(250),
	geom			GEOMETRY,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

ALTER TABLE airbnbs
    ADD CONSTRAINT airbnbs_hosts_id_fk
        FOREIGN KEY (host_id) REFERENCES hosts
            ON DELETE CASCADE;

ALTER TABLE airbnbs
    ADD CONSTRAINT airbnbs_type_id_fk
        FOREIGN KEY (type_id) REFERENCES types
            ON DELETE SET NULL;

ALTER TABLE airbnbs
    ADD CONSTRAINT airbnbs_areas_id_fk
        FOREIGN KEY (area_id) REFERENCES areas
            ON DELETE SET NULL;

