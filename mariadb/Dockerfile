FROM mariadb:10.7

ADD init.sql /docker-entrypoint-initdb.d

COPY my.cnf /etc/mysql/my.cnf

HEALTHCHECK CMD ["healthcheck.sh", "--su=mysql", "--connect", "--innodb_initialized"]