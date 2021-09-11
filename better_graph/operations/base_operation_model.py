from typing import List, Any, Literal

from pydantic import BaseModel


class BaseOperationModel(BaseModel):
    """
    method: Literal['query', 'mutation']
    input_model: Any
    output_model: Any
    permissions: List[str]  # Permissions must be a callable that return a List of PRIVILEGES_ID from DB
    resolver: Any
    """
