"""
XLS Processing Module - Refactored Architecture

This module provides a robust, testable XLS processing system with:
- Separation of concerns
- Data validation
- Transactional batch operations
- Error recovery
- Consistent processing across all projects
"""

from .xls_processor import XLSProcessor
from .project_parser import ProjectParser
from .concept_parser import ConceptParser
from .data_validator import DataValidator, ValidationResult
from .batch_saver import BatchSaver, ProcessingResult

__all__ = [
    'XLSProcessor',
    'ProjectParser',
    'ConceptParser',
    'DataValidator',
    'ValidationResult',
    'BatchSaver',
    'ProcessingResult',
]