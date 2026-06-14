"""
User Service
============

用户管理服务模块。
这个文件包含用户管理的业务逻辑。

重构演示点：
1. 长函数需要拆分
2. 重复代码需要抽取
3. 错误处理不一致
4. 缺少类型注解
5. 硬编码的魔法数字

这个文件故意设计了一些需要重构的代码，用于演示Claude Code的重构能力。
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from ..models.user import User, UserCreate, UserUpdate, UserRole


class UserService:
    """
    用户管理服务

    提供用户的增删改查功能
    """

    def __init__(self):
        """初始化服务，模拟数据库存储"""
        self._users: Dict[int, User] = {}
        self._next_id: int = 1

    def create_user(self, user_data: UserCreate) -> User:
        """
        创建新用户

        Args:
            user_data: 用户创建数据

        Returns:
            创建的用户对象

        Raises:
            ValueError: 用户名或邮箱已存在
        """
        # 检查用户名是否已存在
        for user in self._users.values():
            if user.username == user_data.username:
                raise ValueError("用户名已存在")
            if user.email == user_data.email:
                raise ValueError("邮箱已存在")

        # 创建新用户
        new_user = User(
            id=self._next_id,
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            role=user_data.role,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        self._users[self._next_id] = new_user
        self._next_id += 1

        return new_user

    def get_user(self, user_id: int) -> Optional[User]:
        """
        根据ID获取用户

        Args:
            user_id: 用户ID

        Returns:
            用户对象，不存在则返回None
        """
        return self._users.get(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        根据用户名获取用户

        Args:
            username: 用户名

        Returns:
            用户对象，不存在则返回None
        """
        # TODO: 这里可以用更高效的方式实现
        for user in self._users.values():
            if user.username == username:
                return user
        return None

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """
        更新用户信息

        Args:
            user_id: 用户ID
            user_data: 更新数据

        Returns:
            更新后的用户对象，不存在则返回None
        """
        user = self._users.get(user_id)
        if not user:
            return None

        # 更新字段
        if user_data.username is not None:
            user.username = user_data.username
        if user_data.email is not None:
            user.email = user_data.email
        if user_data.full_name is not None:
            user.full_name = user_data.full_name
        if user_data.role is not None:
            user.role = user_data.role
        if user_data.is_active is not None:
            user.is_active = user_data.is_active

        user.updated_at = datetime.now()
        return user

    def delete_user(self, user_id: int) -> bool:
        """
        删除用户

        Args:
            user_id: 用户ID

        Returns:
            是否删除成功
        """
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

    def list_users(self, active_only: bool = False) -> List[User]:
        """
        获取用户列表

        Args:
            active_only: 是否只返回激活的用户

        Returns:
            用户列表
        """
        users = list(self._users.values())

        if active_only:
            users = [u for u in users if u.is_active]

        return users

    def get_users_by_role(self, role: UserRole) -> List[User]:
        """
        根据角色获取用户列表

        Args:
            role: 用户角色

        Returns:
            符合条件的用户列表
        """
        # TODO: 这个函数可以和list_users合并
        result = []
        for user in self._users.values():
            if user.role == role.value:
                result.append(user)
        return result

    def deactivate_user(self, user_id: int) -> bool:
        """
        停用用户

        Args:
            user_id: 用户ID

        Returns:
            是否操作成功
        """
        user = self._users.get(user_id)
        if not user:
            return False

        user.is_active = False
        user.updated_at = datetime.now()
        return True

    def activate_user(self, user_id: int) -> bool:
        """
        激活用户

        Args:
            user_id: 用户ID

        Returns:
            是否操作成功
        """
        user = self._users.get(user_id)
        if not user:
            return False

        user.is_active = True
        user.updated_at = datetime.now()
        return True

    def get_user_stats(self) -> Dict[str, Any]:
        """
        获取用户统计信息

        Returns:
            包含各种统计数据的字典
        """
        total = len(self._users)
        active = sum(1 for u in self._users.values() if u.is_active)
        inactive = total - active

        # 按角色统计
        role_stats = {}
        for role in UserRole:
            role_stats[role.value] = sum(
                1 for u in self._users.values()
                if u.role == role.value
            )

        return {
            "total_users": total,
            "active_users": active,
            "inactive_users": inactive,
            "by_role": role_stats
        }

    def search_users(self, keyword: str) -> List[User]:
        """
        搜索用户

        Args:
            keyword: 搜索关键词

        Returns:
            匹配的用户列表
        """
        # TODO: 搜索功能可以更强大
        results = []
        keyword_lower = keyword.lower()

        for user in self._users.values():
            if (keyword_lower in user.username.lower() or
                keyword_lower in user.email.lower() or
                keyword_lower in user.full_name.lower()):
                results.append(user)

        return results
