FROM mariadb:10.4

ADD crawlerdb.sql /docker-entrypoint-initdb.d/ddl.sql


