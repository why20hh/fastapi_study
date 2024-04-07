import datetime
from sqlalchemy.orm import Session
from models.user_models import User, UserCreate, UserUpdate
import bcrypt


def authenticate_user(username: str, password: str, db: Session):
    user = get_user(db, username)
    print(user.user_name, user.user_password)
    if not user:
        return False  # 用户不存在
    if not bcrypt.checkpw(password.encode('utf-8'), user.user_password.encode('utf-8')):
        return False  # 密码不匹配
    return True  # 用户名和密码均匹配


def get_user(db: Session, get_user_name: str):
    return db.query(User).filter(User.user_name == get_user_name).first()


def create_user(db: Session, user_data: UserCreate):
    existing_user = get_user(db, user_data.name)
    if existing_user:
        return {"message": "User already exists with this username"}
    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
    user = User(user_name=user_data.name, user_email=user_data.email, user_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, user_data: UserUpdate):
    # 检查用户名是否已存在，排除当前用户
    existing_user = db.query(User).filter(User.user_name == user_data.name, User.id != user.id).first()
    if existing_user:
        return "Another user already exists with this username"

    # 检查电子邮件是否已存在，排除当前用户
    existing_email = db.query(User).filter(User.user_email == user_data.email, User.id != user.id).first()
    if existing_email:
        return "Another user already exists with this email"

    # 确保用户名不会被修改
    user_data.name = user.user_name  # 将输入的用户名设置为当前用户的用户名

    # 只在密码字段非空时更新密码
    if user_data.password:
        hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
        user.user_password = hashed_password

    # 更新用户邮箱和用户名
    user.user_email = user_data.email

    # 更新最后修改时间
    user.last_modified_time = datetime.datetime.now()

    db.commit()
    db.refresh(user)  # 刷新数据库中的用户对象
    return user


def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()
