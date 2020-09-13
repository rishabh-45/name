from . import SESSION, BASE
from sqlalchemy import Column, String, UnicodeText


class Channel(BASE):
    __tablename__ = "chats"
    keyword = Column(UnicodeText, primary_key=True, nullable=False)
    def __init__(self, keyword):
        self.keyword = keyword

Channel.__table__.create(checkfirst=True)


def get_chat():  # Check if any chat is saved or not
    try:
        return SESSION.query(Channel).all()
    finally:
        SESSION.close()


def save(keyword):
    adder = SESSION.query(Channel).get(keyword)
    if adder:
        adder.keyword = keyword
    else:
        adder = Channel(keyword)  # New chat
        SESSION.add(adder)  # Adding new chat
    SESSION.commit()
