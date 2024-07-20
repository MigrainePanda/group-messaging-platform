from application import engine
from sqlalchemy.orm import Session
from sqlalchemy import select

from application.models import User, ChatLog
def get_users() -> list:
    with Session(engine) as session, session.begin():
        try:
            users = session.execute(select(User).order_by(User.id)).scalars()
            users = [user.__dict__ for user in users]
            return users
        except:
            print("Unable to fetch users")
            return []

def get_user_by_id(user_id: int) -> User:
    with Session(engine) as session, session.begin():
        try:
            user = session.execute(select(User).filter_by(id=user_id)).scalar_one()
            user = user.__dict__
            return user
        except:
            print("Unable to find user")
            return None
    
def add_user(form: dict) -> bool:
    with Session(engine) as session, session.begin():
        try:
            user = User(
                username = form["username"],
                email = form["email"],
                password = form["password"],
                messages = []
            )
            session.add(user)
            session.commit()
            print("Successfully added user")
            return True
        except:
            print("Unable to add user")
            return False
        
def check_login(email: str, password: str) -> dict:
    with Session(engine) as session, session.begin():
        try:
            user = session.execute(select(User).filter_by(email=email)).scalar_one()
            if not user: 
                return {'error': 1}
            if user.password != password: 
                return {'error': 2}
            user = user.__dict__    
            return user
        except:
            print("Unable to search email/password")
            return {'error': -1}

def get_chat_rooms() -> dict:
    with Session(engine) as session, session.begin():
        try:
            chatlogs = session.execute(select(ChatLog).order_by(ChatLog.id)).scalars()
            chatlogs = [chatlog.__dict__ for chatlog in chatlogs]
            return chatlogs
        except:
            print("Unable to access chatlogs")
            return None

def create_chat_room(name: str) -> bool:
    with Session(engine) as session, session.begin():
        try:
            if len(name) >= 3:
                chatlog = ChatLog(
                            name = name,
                            messages = []
                        )
                session.add(chatlog)
                session.commit()
                return True
            else:
                return False
        except:
            print("Error trying to create chatroom")
            return False

def get_chat_by_id(room_id: int) -> dict:
    with Session(engine) as session, session.begin():
        try:
            chatlog = session.execute(select(ChatLog).filter_by(id=room_id)).scalar_one()
            print(chatlog.connected_users)
            chatlog = chatlog.__dict__
            return chatlog
        except:
            print(f"Unable to find chatlog with id {id}")
            return None

def add_user_connected(user_id:int , room_id:int) -> bool:
    with Session(engine) as session, session.begin():
        try:
            chatlog = session.execute(select(ChatLog).filter_by(id=room_id)).scalar_one()
            user = session.execute(select(User).filter_by(id=user_id)).scalar_one()
            user.current_chat = chatlog
            session.commit()
        except:
            print("Unable to add chat/user")
            return False
        
def rm_user_connected(user_id:int , room_id:int) -> bool:
    with Session(engine) as session, session.begin():
        try:
            user = session.execute(select(User).filter_by(id=user_id)).scalar_one()
            user.current_chat = None
            session.commit()
        except:
            print("Unable to remove chat/user")
            return False