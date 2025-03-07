from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.db import get_db
from app.models.item import Item, ItemCreate, ItemResponse
from app.models.item_dao import ItemDAO
from app.models.user_dao import UserDAO

router = APIRouter()

@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, user_id: int, db: Session = Depends(get_db)):
    """创建新物品"""
    # 验证用户是否存在
    user = UserDAO.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return ItemDAO.create_user_item(db=db, item=item, user_id=user_id)

@router.get("/", response_model=List[ItemResponse])
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取物品列表"""
    items = ItemDAO.get_items(db, skip=skip, limit=limit)
    return items

@router.get("/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    """根据ID获取特定物品"""
    db_item = ItemDAO.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物品不存在"
        )
    return db_item

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item_data: ItemCreate, db: Session = Depends(get_db)):
    """更新物品信息"""
    db_item = ItemDAO.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物品不存在"
        )
    return ItemDAO.update_item(db=db, item_id=item_id, item_data=item_data)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """删除物品"""
    db_item = ItemDAO.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物品不存在"
        )
    ItemDAO.delete_item(db=db, item_id=item_id)
    return None 