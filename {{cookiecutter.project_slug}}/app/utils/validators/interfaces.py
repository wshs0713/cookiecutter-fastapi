"""Validator interface."""
from typing import Any
from abc import ABCMeta, abstractmethod
from fastapi import status, HTTPException


class BaseValidator:
    """Base validator class."""
    __metaclass__ = ABCMeta
    target: Any
    is_valid: bool

    def __init__(self, target):
        self.target = target
        self.is_valid = False

    def run_valid(self):
        """Validate."""
        if self.is_valid:
            pass
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'The data is invalid for {type(self).__name__}.'
            )

    @abstractmethod
    def valid(self) -> None:
        """Validate."""
        return self.run_valid()
