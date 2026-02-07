from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import Optional

from app.models.user import User
from app.schemas.auth import UserRegister, Token
from app.core.security import hash_password, verify_password, create_access_token


class AuthService:
    
    async def register(self, db: AsyncSession, data: UserRegister) -> User:
        # تحقق من التكرار
        result = await db.execute(
            select(User).where(
                or_(User.email == data.email, User.username == data.username)
            )
        )
        if result.scalar_one_or_none():
            raise ValueError("المستخدم موجود")
        
        user = User(
            email=data.email,
            username=data.username,
            hashed_password=hash_password(data.password)
        )
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user
    
    async def authenticate(self, db: AsyncSession, username: str, password: str) -> Optional[User]:
        result = await db.execute(
            select(User).where(
                or_(User.username == username, User.email == username)
            )
        )
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    def create_token(self, user: User) -> Token:
        token = create_access_token(
            subject=user.id,
            extra={"username": user.username, "role": user.role.value}
        )
        return Token(access_token=token)


auth_service = AuthService()
