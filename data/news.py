import datetime
import sqlalchemy
from sqlalchemy import orm
import hashlib

from .db_session import SqlAlchemyBase


class Course(SqlAlchemyBase):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    included_users = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    invite_code = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    categories = orm.relation("Category", secondary="association", backref="news")

    def create_link(self, id, date):
        start = f"{id}{date}"
        hash_object = hashlib.sha1(start.encode())
        self.invite_code = hash_object.hexdigest()



