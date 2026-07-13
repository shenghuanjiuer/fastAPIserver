from fastapi import Query

class Pagination:
    """分页参数依赖类"""
    
    def __init__(
        self,
        page: int = Query(1, ge=1, description="页码，从1开始"),
        size: int = Query(10, ge=1, le=100, description="每页数量，最大100")
    ):
        self.page = page
        self.size = size
    
    @property
    def offset(self) -> int:
        """计算偏移量"""
        return (self.page - 1) * self.size
    
    @property
    def limit(self) -> int:
        """限制数量，等同于 size"""
        return self.size