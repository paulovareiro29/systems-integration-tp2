CREATE TABLE public.imported_documents (
	id              serial PRIMARY KEY,
	file_name       VARCHAR(250) NOT NULL,
	xml             XML NOT NULL,
	migrated		BOOLEAN DEFAULT false NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	deleted_on		TIMESTAMP DEFAULT NULL
);

CREATE UNIQUE INDEX imported_filename ON imported_documents (file_name) WHERE deleted_on IS NULL;

CREATE TABLE public.converted_documents (
    id              serial PRIMARY KEY,
    src             VARCHAR(250) NOT NULL,
    file_size       BIGINT NOT NULL,
    dst             VARCHAR(250) UNIQUE NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	deleted_on		TIMESTAMP DEFAULT NULL
);

CREATE UNIQUE INDEX converted_src ON converted_documents (src) WHERE deleted_on IS NULL;
