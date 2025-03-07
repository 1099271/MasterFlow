from sqlalchemy.orm import Session
from app.models.user import User, UserCreate

class UserDAO:
    @staticmethod
    def get_user(db: Session, user_id: int):
        """根据ID获取用户"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        """根据邮箱获取用户"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100):
        """获取用户列表"""
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        """创建新用户"""
        from app.utils.security import get_password_hash
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password,
            is_active=user.is_active
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserCreate):
        """更新用户信息"""
        db_user = UserDAO.get_user(db, user_id)
        if db_user:
            # 更新字段
            db_user.email = user_data.email
            db_user.username = user_data.username
            db_user.is_active = user_data.is_active
            
            # 如果提供了新密码，则更新密码
            if user_data.password:
                from app.utils.security import get_password_hash
                db_user.hashed_password = get_password_hash(user_data.password)
            
            db.commit()
            db.refresh(db_user)
        return db_user
    
    @staticmethod
    def delete_user(db: Session, user_id: int):
        """删除用户"""
        db_user = UserDAO.get_user(db, user_id)
        if db_user:
            db.delete(db_user)
            db.commit()
        return True 