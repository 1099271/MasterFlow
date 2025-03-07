from sqlalchemy.orm import Session
from app.models.item import Item, ItemCreate

class ItemDAO:
    @staticmethod
    def get_item(db: Session, item_id: int):
        """根据ID获取物品"""
        return db.query(Item).filter(Item.id == item_id).first()
    
    @staticmethod
    def get_items(db: Session, skip: int = 0, limit: int = 100):
        """获取物品列表"""
        return db.query(Item).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_user_items(db: Session, user_id: int, skip: int = 0, limit: int = 100):
        """获取指定用户的物品"""
        return db.query(Item).filter(Item.owner_id == user_id).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_user_item(db: Session, item: ItemCreate, user_id: int):
        """创建用户的物品"""
        db_item = Item(**item.dict(), owner_id=user_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    @staticmethod
    def update_item(db: Session, item_id: int, item_data: ItemCreate):
        """更新物品"""
        db_item = ItemDAO.get_item(db, item_id)
        if db_item:
            # 更新物品字段
            for key, value in item_data.dict().items():
                setattr(db_item, key, value)
            
            db.commit()
            db.refresh(db_item)
        return db_item
    
    @staticmethod
    def delete_item(db: Session, item_id: int):
        """删除物品"""
        db_item = ItemDAO.get_item(db, item_id)
        if db_item:
            db.delete(db_item)
            db.commit()
        return True 