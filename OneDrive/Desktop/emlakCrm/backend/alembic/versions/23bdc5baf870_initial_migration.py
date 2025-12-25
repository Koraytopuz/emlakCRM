"""Initial migration

Revision ID: 23bdc5baf870
Revises: 
Create Date: 2025-12-21 14:46:55.861727

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import geoalchemy2

# revision identifiers, used by Alembic.
revision = '23bdc5baf870'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # PostGIS sistem tablolarını silmeye çalışmayın - bunlar extension'a ait
    # Bizim tablolarımız main.py'de Base.metadata.create_all() ile oluşturuluyor
    # Bu migration sadece Alembic versiyonunu işaretlemek için
    pass


def downgrade() -> None:
    # PostGIS sistem tablolarını geri oluşturmayın
    pass
