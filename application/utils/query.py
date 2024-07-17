from application import engine
from sqlalchemy.orm import Session
from sqlalchemy import select

from application.models import User

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
            user = session.execute(select(User).filter_by(id=user_id)).scalar()
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
            user = session.execute(select(User).filter_by(email=email)).scalar()
            if not user: 
                return {'error': 1}
            if user.password != password: 
                return {'error': 2}
            user = user.__dict__
            return user
        except:
            print("Unable to search email/password")
            return {'error': -1}
