from DBname import DBsession
from DBname.Time_game import timeGame
from DBname.Stand_game import StandGame

def add_time_game(score, level, data):
    time_game = timeGame()
    time_game.score = score
    time_game.level = level
    time_game.timeingame = data
    db_sess = DBsession.create_session()
    db_sess.add(time_game)
    db_sess.commit()
    db_sess.close()


def add_stand_game(score, level):
    stand_game = StandGame()
    stand_game.score = score
    stand_game.level = level
    db_sess = DBsession.create_session()
    db_sess.add(stand_game)
    db_sess.commit()
    db_sess.close()