"""
User Model
==========

用户数据模型定义。
这个文件展示了Pydantic数据模型的使用，以及枚举类型的应用。

重构演示点：
- 使用Pydantic进行数据验证
- 使用Enum定义用户角色
- 添加数据序列化/反序列化支持
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator


class UserRole(str, Enum):
    """用户角色枚举"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class User(BaseModel):
    """
    用户数据模型

    Attributes:
        id: 用户唯一标识
        username: 用户名
        email: 电子邮箱
        full_name: 全名
        role: 用户角色
        is_active: 是否激活
        created_at: 创建时间
        updated_at: 更新时间
    """

    id: Optional[int] = Field(None, description="用户ID")
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="电子邮箱")
    full_name: str = Field(..., min_length=1, max_length=100, description="全名")
    role: UserRole = Field(default=UserRole.USER, description="用户角色")
    is_active: bool = Field(default=True, description="是否激活")
    created_at: Optional[datetime] = Field(default_factory=datetime.now, description="创建时间")
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, description="更新时间")

    class Config:
        """模型配置"""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

    @validator('username')
    def username_must_be_alphanumeric(cls, v):
        """验证用户名只能包含字母、数字和下划线"""
        if not v.replace('_', '').isalnum():
            raise ValueError('用户名只能包含字母、数字和下划线')
        return v.lower()

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class UserCreate(BaseModel):
    """创建用户请求模型"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, description="密码（至少8位）")
    role: UserRole = Field(default=UserRole.USER)


class UserUpdate(BaseModel):
    """更新用户请求模型"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    """用户响应模型（不包含敏感信息）"""
    id: int
    username: str
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: Optional[str] = None
