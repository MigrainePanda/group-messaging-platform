from application import engine
from sqlalchemy.orm import Session
from sqlalchemy import select

from application.models import User, ChatLog, Message
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
            )
            session.add(user)
            session.commit()
            print("Successfully added user")
            return True
        except:
            print("Unable to add user")
            return False
        
def save_msg(form: dict) -> bool:
    with Session(engine) as session, session.begin():
        try:
            user = session.execute(select(User).filter_by(id=form['user_id'])).scalar_one()
            chatlog = session.execute(select(ChatLog).filter_by(id=form['chatlog_id'])).scalar_one()
            message = Message(
                body = form['body'],
                user = user,
                chatlog = chatlog
            )
            session.add(message)
            session.commit()
            print("Successfully saved message")
            return True
        except Exception as err:
            print("Unable to save message:", err)
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
            # connected_users = session.execute(select(User).filter(User.current_chat != None).order_by(User.current_chat_id))
            # print(connected_users.all()) 

            # print(connected_users)
            return chatlogs
        except:
            print("Unable to get chatlogs")
            return None

def get_connected_users() -> dict:
    with Session(engine) as session, session.begin():
        try:
            connected_users = session.execute(select(User.current_chat_id, User.id).filter(User.current_chat != None).order_by(User.current_chat_id))
            ax = {}
            for user in connected_users.all():
                a = user._mapping
                print("user: ", a)
                b = a["current_chat_id"]
                if (b in ax):
                    ax[b] += 1
                else:
                    ax[b] = 1
            return ax
        except:
            print("Unable to retrieve connected users count")
            return None

def create_chat_room(name: str) -> bool:
    with Session(engine) as session, session.begin():
        try:
            if len(name) >= 3:
                chatlog = ChatLog(
                    name = name,
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
            #print(chatlog.current_users)
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