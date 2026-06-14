"""
User Service Tests
==================

用户服务单元测试
这个文件展示了pytest测试的编写方式。

重构演示点：
- 测试用例可以更系统化
- 可以使用fixture减少重复代码
- 测试覆盖率可以提高
"""

import pytest
from datetime import datetime

from src.models.user import User, UserCreate, UserUpdate, UserRole
from src.services.user_service import UserService
from src.utils.validators import validate_email, validate_password, validate_username


@pytest.fixture
def user_service():
    """创建用户服务实例"""
    return UserService()


@pytest.fixture
def sample_user_data():
    """创建示例用户数据"""
    return UserCreate(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        password="TestPass123",
        role=UserRole.USER
    )


@pytest.fixture
def sample_admin_data():
    """创建示例管理员数据"""
    return UserCreate(
        username="admin",
        email="admin@example.com",
        full_name="Admin User",
        password="AdminPass123",
        role=UserRole.ADMIN
    )


class TestUserService:
    """用户服务测试类"""

    def test_create_user_success(self, user_service, sample_user_data):
        """测试成功创建用户"""
        user = user_service.create_user(sample_user_data)

        assert user is not None
        assert user.id == 1
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.role == UserRole.USER.value
        assert user.is_active is True

    def test_create_user_duplicate_username(self, user_service, sample_user_data):
        """测试创建重复用户名的用户"""
        user_service.create_user(sample_user_data)

        duplicate_data = UserCreate(
            username="testuser",  # 重复的用户名
            email="another@example.com",
            full_name="Another User",
            password="TestPass123",
            role=UserRole.USER
        )

        with pytest.raises(ValueError) as excinfo:
            user_service.create_user(duplicate_data)

        assert "用户名已存在" in str(excinfo.value)

    def test_create_user_duplicate_email(self, user_service, sample_user_data):
        """测试创建重复邮箱的用户"""
        user_service.create_user(sample_user_data)

        duplicate_data = UserCreate(
            username="anotheruser",
            email="test@example.com",  # 重复的邮箱
            full_name="Another User",
            password="TestPass123",
            role=UserRole.USER
        )

        with pytest.raises(ValueError) as excinfo:
            user_service.create_user(duplicate_data)

        assert "邮箱已存在" in str(excinfo.value)

    def test_get_user(self, user_service, sample_user_data):
        """测试获取用户"""
        created_user = user_service.create_user(sample_user_data)
        retrieved_user = user_service.get_user(created_user.id)

        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id

    def test_get_user_not_found(self, user_service):
        """测试获取不存在的用户"""
        user = user_service.get_user(999)
        assert user is None

    def test_get_user_by_username(self, user_service, sample_user_data):
        """测试根据用户名获取用户"""
        user_service.create_user(sample_user_data)
        user = user_service.get_user_by_username("testuser")

        assert user is not None
        assert user.username == "testuser"

    def test_update_user(self, user_service, sample_user_data):
        """测试更新用户信息"""
        user = user_service.create_user(sample_user_data)

        update_data = UserUpdate(full_name="Updated Name")
        updated_user = user_service.update_user(user.id, update_data)

        assert updated_user is not None
        assert updated_user.full_name == "Updated Name"

    def test_delete_user(self, user_service, sample_user_data):
        """测试删除用户"""
        user = user_service.create_user(sample_user_data)
        result = user_service.delete_user(user.id)

        assert result is True
        assert user_service.get_user(user.id) is None

    def test_delete_user_not_found(self, user_service):
        """测试删除不存在的用户"""
        result = user_service.delete_user(999)
        assert result is False

    def test_list_users(self, user_service, sample_user_data, sample_admin_data):
        """测试获取用户列表"""
        user_service.create_user(sample_user_data)
        user_service.create_user(sample_admin_data)

        users = user_service.list_users()
        assert len(users) == 2

    def test_list_users_active_only(self, user_service, sample_user_data):
        """测试只获取激活用户"""
        user = user_service.create_user(sample_user_data)
        user_service.deactivate_user(user.id)

        active_users = user_service.list_users(active_only=True)
        assert len(active_users) == 0

    def test_deactivate_user(self, user_service, sample_user_data):
        """测试停用用户"""
        user = user_service.create_user(sample_user_data)
        result = user_service.deactivate_user(user.id)

        assert result is True
        user = user_service.get_user(user.id)
        assert user.is_active is False

    def test_activate_user(self, user_service, sample_user_data):
        """测试激活用户"""
        user = user_service.create_user(sample_user_data)
        user_service.deactivate_user(user.id)

        result = user_service.activate_user(user.id)
        assert result is True

        user = user_service.get_user(user.id)
        assert user.is_active is True

    def test_get_user_stats(self, user_service, sample_user_data, sample_admin_data):
        """测试获取用户统计"""
        user_service.create_user(sample_user_data)
        user_service.create_user(sample_admin_data)

        stats = user_service.get_user_stats()

        assert stats["total_users"] == 2
        assert stats["active_users"] == 2
        assert stats["by_role"]["user"] == 1
        assert stats["by_role"]["admin"] == 1

    def test_search_users(self, user_service, sample_user_data):
        """测试搜索用户"""
        user_service.create_user(sample_user_data)

        results = user_service.search_users("test")
        assert len(results) == 1

    def test_search_users_no_results(self, user_service, sample_user_data):
        """测试搜索无结果"""
        user_service.create_user(sample_user_data)

        results = user_service.search_users("nonexistent")
        assert len(results) == 0


class TestValidators:
    """验证器测试类"""

    def test_validate_email_valid(self):
        """测试有效邮箱验证"""
        is_valid, message = validate_email("user@example.com")
        assert is_valid is True

    def test_validate_email_invalid(self):
        """测试无效邮箱验证"""
        is_valid, message = validate_email("invalid-email")
        assert is_valid is False

    def test_validate_email_empty(self):
        """测试空邮箱验证"""
        is_valid, message = validate_email("")
        assert is_valid is False

    def test_validate_password_valid(self):
        """测试有效密码验证"""
        is_valid, message = validate_password("MyPass123")
        assert is_valid is True

    def test_validate_password_too_short(self):
        """测试密码太短"""
        is_valid, message = validate_password("Short1")
        assert is_valid is False

    def test_validate_password_no_uppercase(self):
        """测试密码没有大写字母"""
        is_valid, message = validate_password("nopass123")
        assert is_valid is False

    def test_validate_password_no_lowercase(self):
        """测试密码没有小写字母"""
        is_valid, message = validate_password("NOPASS123")
        assert is_valid is False

    def test_validate_password_no_digit(self):
        """测试密码没有数字"""
        is_valid, message = validate_password("NoDigitPass")
        assert is_valid is False

    def test_validate_username_valid(self):
        """测试有效用户名验证"""
        is_valid, message = validate_username("testuser")
        assert is_valid is True

    def test_validate_username_too_short(self):
        """测试用户名太短"""
        is_valid, message = validate_username("ab")
        assert is_valid is False

    def test_validate_username_invalid_chars(self):
        """测试用户名包含非法字符"""
        is_valid, message = validate_username("test user")
        assert is_valid is False


class TestUserModel:
    """用户模型测试类"""

    def test_user_creation(self):
        """测试用户模型创建"""
        user = User(
            username="testuser",
            email="test@example.com",
            full_name="Test User"
        )

        assert user.username == "testuser"
        assert user.email == "test@example.com"

    def test_user_to_dict(self):
        """测试用户模型转字典"""
        user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            full_name="Test User"
        )

        user_dict = user.to_dict()
        assert isinstance(user_dict, dict)
        assert user_dict["id"] == 1
        assert user_dict["username"] == "testuser"

    def test_user_role_enum(self):
        """测试用户角色枚举"""
        assert UserRole.ADMIN.value == "admin"
        assert UserRole.USER.value == "user"
        assert UserRole.GUEST.value == "guest"
