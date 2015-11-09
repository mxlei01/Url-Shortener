FROM ubuntu:14.04
MAINTAINER SequenceIQ

#===========================Start Fix PAM======================================
#Setup build environment for libpam
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get -y build-dep pam

#Rebuild and istall libpam with --disable-audit option
RUN export CONFIGURE_OPTS=--disable-audit && cd /root && apt-get -b source pam && dpkg -i libpam-doc*.deb libpam-modules*.deb libpam-runtime*.deb libpam0g*.deb
#===========================End Fix PAM========================================

#===========================Start Update Ubuntu================================
RUN apt-get -y update 
RUN apt-get -y upgrade 
RUN apt-get -y install apt-utils 
RUN apt-get -y update 
RUN apt-get -y upgrade
RUN apt-get -y install build-essential
RUN apt-get -y install python-dev
RUN apt-get -y install libpq-dev
#===========================End Update Ubuntu==================================

#===========================Start Install Postgres===============================
# Add the PostgreSQL PGP key to verify their Debian packages.
# It should be the same key as https://www.postgresql.org/media/keys/ACCC4CF8.asc
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8

# Add PostgreSQL's repository. It contains the most recent stable release
#     of PostgreSQL, ``9.4``.
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list

# Install ``python-software-properties``, ``software-properties-common`` and PostgreSQL 9.4
#  There are some warnings (in red) that show up during the build. You can hide
#  them by prefixing each apt-get statement with DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python-software-properties software-properties-common postgresql-9.4 postgresql-client-9.4 postgresql-contrib-9.4

# Note: The official Debian and Ubuntu images automatically ``apt-get clean``
# after each ``apt-get``

# Run the rest of the commands as the ``postgres`` user created by the ``postgres-9.4`` package when it was ``apt-get installed``
USER postgres

# Create a PostgreSQL role named ``docker`` with ``docker`` as the password and
# then create a database `url_db` owned by the ``docker`` role.
# Note: here we use ``&&\`` to run commands one after the other - the ``\``
#       allows the RUN command to span multiple lines.
RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
    createdb -O docker url_db

# Create a table named url
RUN   /etc/init.d/postgresql start &&\
    psql url_db --command " CREATE TABLE url\
	(\
	shortened_url varchar (255) NOT NULL,\
	original_url varchar(255) NOT NULL,\
	PRIMARY KEY (shortened_url)\
	)"

# Create a table named url_info
RUN /etc/init.d/postgresql start &&\
    psql url_db --command "CREATE TABLE url_info\
	(\
	shortened_url varchar (255),\
	count_visited int,\
	date timestamp,\
	domain varchar (255),\
	FOREIGN KEY (shortened_url) REFERENCES url(shortened_url)\
	ON DELETE CASCADE)"

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.4/main/pg_hba.conf

# And add ``listen_addresses`` to ``/etc/postgresql/9.4/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.4/main/postgresql.conf

# Expose the PostgreSQL port
EXPOSE 5432

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]
#===========================Start Install Postgres===============================

#=====Create a folder, and copy our application into the application folder====
USER root
RUN mkdir /application
COPY Tornado-Application /application/Tornado-Application
#=====Create a folder, and copy our application into the application folder====

#===========================Installing Supervisord=============================
RUN apt-get install -y supervisor
#===========================Installing Supervisord=============================

#===========================Installing Python Requirements=====================
RUN apt-get install -y python-pip
RUN pip install -r /application/Tornado-Application/requirements.txt
#===========================Installing Python Requirements=====================

#===========================Run Supervisord====================================
COPY Supervisord/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN mkdir /var/supervisord
CMD /usr/bin/supervisord
#===========================Run Supervisord====================================
