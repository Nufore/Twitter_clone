"""created medias table

Revision ID: e5b017e95f50
Revises: c3106a0f3417
Create Date: 2024-03-22 00:21:36.110545

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e5b017e95f50"
down_revision: Union[str, None] = "c3106a0f3417"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("medias", "tweet_id", existing_type=sa.INTEGER(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("medias", "tweet_id", existing_type=sa.INTEGER(), nullable=False)
    # ### end Alembic commands ###
