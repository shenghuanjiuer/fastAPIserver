# core/exceptions.py

class BizException(Exception):
    """业务异常基类"""
    def __init__(self, code: int, message: str, status_code: int = 400):
        self.code = code          # 业务码
        self.message = message    # 错误消息
        self.status_code = status_code  # HTTP状态码


class NotFoundException(BizException):
    """资源不存在"""
    def __init__(self, message: str = "资源不存在"):
        super().__init__(code=1001, message=message, status_code=404)


class AuthException(BizException):
    """认证失败"""
    def __init__(self, message: str = "认证失败"):
        super().__init__(code=1002, message=message, status_code=401)


class ForbiddenException(BizException):
    """权限不足"""
    def __init__(self, message: str = "权限不足"):
        super().__init__(code=1003, message=message, status_code=403)