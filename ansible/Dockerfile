FROM python:3.12-bookworm

RUN pip install ansible==9.1

RUN set -x && \
    \
    echo "==> Adding hosts for convenience..."  && \
    mkdir -p /etc/ansible /ansible && \
    echo "[local]" >> /etc/ansible/hosts && \
    echo "localhost" >> /etc/ansible/hosts && \
    \
    echo "==> Installing customize dependencies..." && \
    apt-get update && \
    apt-get install -y squashfs-tools xorriso isolinux \
    rsync

COPY roles /etc/ansible/roles
COPY group_vars /etc/ansible/group_vars

WORKDIR /ansible

CMD ["ansible-playbook", "playbook.yml"]