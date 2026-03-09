"""
Data models for XLS processing
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class MonthlyValues:
    """Valores mensais para um conceito"""
    realizado: float
    planejado: float


@dataclass
class ConceptData:
    """Dados de um conceito específico"""
    name: str
    monthly_data: Dict[int, MonthlyValues]  # mes -> valores


@dataclass
class ProjectMetadata:
    """Metadados do projeto"""
    descricao: str = ""
    mercado: str = ""
    regiao: str = ""
    tipo_solucao: str = ""
    responsavel_comercial: str = ""
    is_pipeline: bool = False
    is_active: bool = True


@dataclass
class ProjectData:
    """Dados completos de um projeto"""
    project_code: str
    concepts: Dict[str, Dict[int, MonthlyValues]]  # conceito -> {mes -> valores}
    metadata: ProjectMetadata

    def get_concept_months(self, concept: str) -> Dict[int, MonthlyValues]:
        """Retorna dados mensais de um conceito"""
        return self.concepts.get(concept, {})

    def has_concept(self, concept: str) -> bool:
        """Verifica se projeto tem um conceito"""
        return concept in self.concepts


@dataclass
class ValidationResult:
    """Resultado de validação"""
    valid: bool
    errors: List[str]
    warnings: List[str] = None

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


@dataclass
class ProcessingResult:
    """Resultado do processamento"""
    successful: int
    failed: int
    errors: List[str]
    processed_projects: List[str] = None
    skipped_projects: List[str] = None

    def __post_init__(self):
        if self.processed_projects is None:
            self.processed_projects = []
        if self.skipped_projects is None:
            self.skipped_projects = []

    @property
    def total_projects(self) -> int:
        """Total de projetos processados"""
        return self.successful + self.failed


class ProcessingError(Exception):
    """Erro customizado com contexto"""

    def __init__(self, message: str, project_code: str = None, row_data: Dict = None):
        super().__init__(message)
        self.project_code = project_code
        self.row_data = row_data