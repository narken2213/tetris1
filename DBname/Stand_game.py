import datetime

import sqlalchemy

from DBname.DBsession import SqlAlchemyBase


class StandGame(SqlAlchemyBase):
    __tablename__ = 'stand_game'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    create_data = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    level = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    def __repr__(self):
        return f'<timeGame> {self.id} | {self.create_data} | {self.score} | {self.level}'