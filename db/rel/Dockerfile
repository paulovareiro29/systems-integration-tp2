FROM postgres:15.1

ENV POSTGRES_USER=is
ENV POSTGRES_PASSWORD=is
ENV POSTGRES_DB=is

RUN apt update \
    && apt install wget -y \
    && apt install postgresql-15-postgis-3 -y \
    && apt install postgis -y

COPY initial_schema.sql /docker-entrypoint-initdb.d/

EXPOSE 5432