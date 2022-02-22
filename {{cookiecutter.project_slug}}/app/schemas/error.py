"""Pydantic schemas."""
from typing import Optional
from pydantic import BaseModel, Field


class Error(BaseModel):
    """Error model."""
    status_code: int
    code: Optional[int] = None
    message: str = Field(..., description='Error message')


class ErrorResponse(BaseModel):
    """Error response model."""
    status: str = 'failure'
    error: Error

    class Config:
        """Example schema."""
        schema_extra = {
            'example': {
                'status': 'failure',
                'error': {
                    'status_code': 'HTTP status code',
                    'code': None,
                    'message': 'error message'
                }
            }
        }
