FROM mariadb:10.4

ADD init.sql /docker-entrypoint-initdb.d


HEALTHCHECK CMD ["healthcheck.sh", "--su=mysql", "--connect", "--innodb_initialized"]