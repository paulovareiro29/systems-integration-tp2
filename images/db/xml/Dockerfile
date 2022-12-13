FROM postgres:15.1

ENV POSTGRES_USER=is
ENV POSTGRES_PASSWORD=is
ENV POSTGRES_DB=is

COPY initial_schema.sql /docker-entrypoint-initdb.d/

EXPOSE 5432