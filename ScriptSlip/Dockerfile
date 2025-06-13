FROM debian:bullseye

ENV DEBIAN_FRONTEND=noninteractive

# Install required packages including ssh-keygen
RUN apt-get update && apt-get install -y \
    postfix \
    python3 \
    rsyslog \
    mailutils \
    procmail \
    cron \
    netcat \
    sudo \
    gcc \
    sharutils \
    mpack \
    wget \
    openssh-client \
    && apt-get clean

# Configure Postfix (local only)
RUN echo "mindbreak.local" > /etc/mailname && \
    postconf -e "myhostname = mindbreak.local" && \
    postconf -e "mydestination = mindbreak.local, localhost" && \
    postconf -e "inet_interfaces = localhost" && \
    postconf -e "inet_protocols = ipv4" && \
    postconf -e "mailbox_command ="

# Create user and mail setup
RUN useradd -m worker && \
    mkdir -p /var/mail && touch /var/mail/worker && \
    chown worker:mail /var/mail/worker && chmod 660 /var/mail/worker && \
    echo "sys.admin: worker" >> /etc/aliases && newaliases

#Create admin
RUN useradd -m admin

# Setup challenge directory and files
RUN mkdir -p /srv && \
    \
    # Script vulnérable (sans eval)
    echo '#!/bin/bash\nCONFIG="/srv/keygen.conf"\nLIB=$(grep "^algo" "$CONFIG" | cut -d":" -f2- | xargs)\nssh-keygen -t $LIB' > /srv/generate_key.sh && \
    \
    # Rabbit-hole scripts
    echo '#!/bin/bash\nCONF="/srv/clean.conf"\nPATTERN=$(grep "^pattern" "$CONF" | cut -d":" -f2 | xargs)\nrm -rf /tmp/*$PATTERN*' > /srv/cleanup.sh && \
    echo '#!/bin/bash\nCONF="/srv/logger.conf"\nLOGFILE=$(grep "^logfile" "$CONF" | cut -d":" -f2 | xargs)\necho "$(date) - ping google.com" >> $LOGFILE\nping -c 1 8.8.8.8 >> $LOGFILE 2>&1' > /srv/logger.sh && \
    \
	echo '#!/usr/bin/env bash\nset -euo pipefail\nCONFIG="/srv/backup_logs.conf"\nDEST_DIR=$(grep "^DEST_DIR=" "$CONFIG" | cut -d"=" -f2)\nSOURCE_DIR=$(grep "^SOURCE_DIR=" "$CONFIG" | cut -d"=" -f2)\nDATE=$(date +%F_%H-%M)\ntar czf "${DEST_DIR}/logs_${DATE}.tgz" "$SOURCE_DIR" >/dev/null 2>&1\nlogger "[backup_logs] archived ${SOURCE_DIR} -> ${DEST_DIR}/logs_${DATE}.tgz"' > /srv/backup_logs.sh && \
	echo 'DEST_DIR=/var/archives\nSOURCE_DIR=/var/log' > /srv/backup_logs.conf && \
	\
	echo '#!/usr/bin/env bash\nset -euo pipefail\nCONFIG="/srv/rotate_archives.conf"\nARCHIVE_DIR=$(grep "^ARCHIVE_DIR=" "$CONFIG" | cut -d"=" -f2)\nKEEP_DAYS=$(grep "^KEEP_DAYS=" "$CONFIG" | cut -d"=" -f2)\nfind "$ARCHIVE_DIR" -type f -name "logs_*.tgz" -mtime +"$KEEP_DAYS" -exec rm -f {} \\;\nlogger "[rotate_archives] pruned archives older than ${KEEP_DAYS} days in ${ARCHIVE_DIR}"' > /srv/rotate_archives.sh && \
	echo 'ARCHIVE_DIR=/var/archives\nKEEP_DAYS=7' > /srv/rotate_archives.conf && \
	\

    # Configuration files
    echo 'algo : rsa' > /srv/keygen.conf && \
    echo 'pattern : temp' > /srv/clean.conf && \
    echo 'logfile : /var/log/stats.log' > /srv/logger.conf && \
    \
    # Permissions
    chmod +x /srv/*.sh && \
    chmod 664 /srv/*.conf && \
    chown worker:root /srv/*.conf
# Create flag
RUN echo "MB{fwd_m3_y0ur_$h}" >> /home/worker/flag.txt && \
	echo "MB{k3yg3ni3_sOrt_d3_s4_l4mp3}" >> /home/admin/flag.txt &&\
	chown admin:admin /home/admin/flag.txt && \
	chmod 600 /home/admin/flag.txt
	
# Setup crontab entries
RUN echo "* * * * * admin /srv/generate_key.sh" >> /etc/crontab && \
    echo "* * * * * admin /srv/cleanup.sh" >> /etc/crontab && \
    echo "* * * * * admin /srv/logger.sh" >> /etc/crontab

# IDS & mail monitor
COPY smtp_proxy_ids.py /smtp_proxy_ids.py
COPY mail_monitor.sh /mail_monitor.sh
RUN chmod +x /mail_monitor.sh

# Visibility
RUN chmod +r /srv/*.sh /etc/crontab

EXPOSE 2525

CMD service postfix start && \
    service cron start && \
    /mail_monitor.sh & \
    python3 /smtp_proxy_ids.py
