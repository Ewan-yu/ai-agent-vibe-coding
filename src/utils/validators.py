"""
Validators Module
=================

验证工具函数模块。
这个文件展示了输入验证和数据清洗的实现。

重构演示点：
- 函数可以进一步模块化
- 错误处理可以统一
- 可以添加更多验证规则
"""

import re
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """
    验证邮箱格式是否正确

    Args:
        email: 待验证的邮箱地址

    Returns:
        (是否有效, 错误信息或成功信息)

    Examples:
        >>> validate_email("user@example.com")
        (True, "邮箱格式正确")
        >>> validate_email("invalid-email")
        (False, "邮箱格式不正确")
    """
    if not email:
        return False, "邮箱不能为空"

    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_pattern, email):
        return True, "邮箱格式正确"
    else:
        return False, "邮箱格式不正确"


def validate_password(password: str) -> Tuple[bool, str]:
    """
    验证密码强度

    规则：
    - 至少8位
    - 包含至少一个大写字母
    - 包含至少一个小写字母
    - 包含至少一个数字

    Args:
        password: 待验证的密码

    Returns:
        (是否有效, 错误信息或成功信息)

    Examples:
        >>> validate_password("MyPass123")
        (True, "密码强度合格")
        >>> validate_password("weak")
        (False, "密码长度不足8位")
    """
    if not password:
        return False, "密码不能为空"

    if len(password) < 8:
        return False, "密码长度不足8位"

    if not re.search(r'[A-Z]', password):
        return False, "密码必须包含至少一个大写字母"

    if not re.search(r'[a-z]', password):
        return False, "密码必须包含至少一个小写字母"

    if not re.search(r'[0-9]', password):
        return False, "密码必须包含至少一个数字"

    return True, "密码强度合格"


def validate_username(username: str) -> Tuple[bool, str]:
    """
    验证用户名格式

    规则：
    - 只能包含字母、数字、下划线
    - 长度3-50位

    Args:
        username: 待验证的用户名

    Returns:
        (是否有效, 错误信息或成功信息)
    """
    if not username:
        return False, "用户名不能为空"

    if len(username) < 3:
        return False, "用户名长度不足3位"

    if len(username) > 50:
        return False, "用户名长度超过50位"

    username_pattern = r'^[a-zA-Z0-9_]+$'
    if not re.match(username_pattern, username):
        return False, "用户名只能包含字母、数字和下划线"

    return True, "用户名格式正确"


def sanitize_string(input_str: str) -> str:
    """
    清洗字符串，移除危险字符

    Args:
        input_str: 输入字符串

    Returns:
        清洗后的字符串
    """
    if not input_str:
        return ""

    # 移除潜在的XSS攻击字符
    dangerous_patterns = ['<script', '</script', 'javascript:', 'onerror=']
    result = input_str
    for pattern in dangerous_patterns:
        result = result.replace(pattern, '')

    return result.strip()
