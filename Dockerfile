FROM alpine:3.8 as builder
MAINTAINER Xavier Garnier 'xavier.garnier@irisa.fr'

COPY . /isqlapi
WORKDIR /isqlapi

RUN apk add --update python3 python3-dev gcc g++ unixodbc-dev && \
    python3 -m venv venv && source venv/bin/activate && \
    pip install -e .

# Virtuoso
FROM askomics/virtuoso:7.2.5.1 AS virtuoso_builder

# Final image
FROM alpine:3.8

ENV WORKER_TIMEOUT="43200"

ENV ISQL_API_SERVER_PORT="5050"

ENV ISQL_API_VIRTUOSO_DSN="virtuoso"
ENV ISQL_API_VIRTUOSO_USERNAME="dba"
ENV ISQL_API_VIRTUOSO_PASSWORD="dba"

ENV VIRTUOSO_HOST="virtuoso"
ENV VIRTUOSO_ISQL_PORT="1111"

WORKDIR /isqlapi
COPY --from=builder /isqlapi .
COPY --from=virtuoso_builder /usr/local/virtuoso-opensource/lib /usr/local/virtuoso-opensource/lib

RUN apk add --no-cache gettext python3 unixodbc libstdc++ openssl

EXPOSE 5050
CMD sh /isqlapi/docker-run.sh