from sqlalchemy.orm import Session
from app.models.user import User, pwd_context


def create_user(db: Session, username: str, password: str):
    """
    Создание пользователя
    :param db:
    :param username:
    :param password:
    :return:
    """
    hashed_password = pwd_context.hash(password)
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    """
    Аутентификация пользователя
    :param db:
    :param username:
    :param password:
    :return:
    """
    user = db.query(User).filter(User.username == username).first()
    if user and user.verify_password(password):
        return user
    return None
