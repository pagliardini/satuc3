"""Actualizar modelo con relacion a marca

Revision ID: e8391851b7fd
Revises: 93d738242157
Create Date: 2025-05-16 21:46:01.621284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8391851b7fd'
down_revision = '93d738242157'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stock_ubicacion', schema=None) as batch_op:
        batch_op.add_column(sa.Column('producto_id', sa.Integer(), nullable=False))
        batch_op.alter_column('codigo',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.drop_constraint('uq_area_codigo', type_='unique')
        # Cambiar esta línea para proporcionar un nombre a la restricción
        batch_op.create_foreign_key('fk_stock_producto', 'productos', ['producto_id'], ['id'])
        batch_op.drop_column('producto_nombre')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stock_ubicacion', schema=None) as batch_op:
        batch_op.add_column(sa.Column('producto_nombre', sa.VARCHAR(length=200), nullable=False))
        # También actualizar esta línea para que coincida
        batch_op.drop_constraint('fk_stock_producto', type_='foreignkey')
        batch_op.create_unique_constraint('uq_area_codigo', ['area_id', 'codigo'])
        batch_op.alter_column('codigo',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.drop_column('producto_id')
    # ### end Alembic commands ###
