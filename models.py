from database import Base
import sqlalchemy as sa
import datetime
class RedragonZoneRecords(Base):

    __tablename__ = "redragonzone"

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    orignal_url = sa.Column(sa.String(1000))
    name = sa.Column(sa.String(255))
    price = sa.Column(sa.String(10))
    # sale_price = sa.Column(sa.Integer)

    created_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    updated_at = sa.Column(sa.DateTime, onupdate=datetime.datetime.utcnow)
    deleted_at = sa.Column(sa.DateTime)