При настройке бд добавить
"""
sudo dnf install postgresql-server-devel
"""

Установить в бд pgvector.
"""
cd /tmp
git clone --branch v0.4.4 https://github.com/pgvector/pgvector.git
cd pgvector
make
make install # may need sudo
"""

Инициализировать расширение суперюзером.
"""
CREATE EXTENSION vector;
"""
