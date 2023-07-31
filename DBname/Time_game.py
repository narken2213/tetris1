import datetime

import sqlalchemy

from DBname.DBsession import SqlAlchemyBase


class timeGame(SqlAlchemyBase):
    __tablename__ = 'time_game'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    create_data = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    timeingame = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    level = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    def __repr__(self):
        return f'<timeGame> {self.id} | {self.create_data} | {self.score} | {self.timeingame} | {self.level}'