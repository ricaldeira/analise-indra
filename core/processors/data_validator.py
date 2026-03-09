"""
Data validation for XLS processing
"""

import logging
from typing import Dict, Any
from .models import ProjectData, ValidationResult

logger = logging.getLogger(__name__)


class DataValidator:
    """Valida dados antes do processamento"""

    def validate_project_data(self, project_data: ProjectData) -> ValidationResult:
        """Valida se dados do projeto estão consistentes"""
        errors = []
        warnings = []

        # Verificar código do projeto
        if not project_data.project_code or not project_data.project_code.strip():
            errors.append("Código do projeto vazio ou inválido")
            return ValidationResult(valid=False, errors=errors, warnings=warnings)

        # Verificar se tem pelo menos um conceito
        if not project_data.concepts:
            errors.append(f"Projeto {project_data.project_code} sem conceitos definidos")
        elif len(project_data.concepts) < 1:  # Pelo menos um conceito
            warnings.append(f"Projeto {project_data.project_code} tem poucos conceitos ({len(project_data.concepts)})")

        # Verificar se tem pelo menos um conceito financeiro básico
        financial_concepts = ['ingresos', 'margen', 'contratacion', 'coste']
        has_financial = any(concept in project_data.concepts for concept in financial_concepts)
        if not has_financial:
            warnings.append(f"Projeto {project_data.project_code} sem conceitos financeiros básicos")

        # Verificar conceitos obrigatórios (menos rigoroso)
        recommended_concepts = ['ingresos', 'margen', 'contratacion']
        missing_concepts = []
        for concept in recommended_concepts:
            if concept not in project_data.concepts:
                missing_concepts.append(concept)

        if missing_concepts:
            warnings.append(f"Conceitos recomendados ausentes: {', '.join(missing_concepts)}")

        # Validar valores numéricos
        for concept_name, monthly_data in project_data.concepts.items():
            for month, values in monthly_data.items():
                # Validar valores realizados
                if not self._is_valid_number(values.realizado):
                    errors.append(f"Valor realizado inválido para {concept_name} mês {month}: {values.realizado}")

                # Validar valores planejados
                if not self._is_valid_number(values.planejado):
                    errors.append(f"Valor planejado inválido para {concept_name} mês {month}: {values.planejado}")

                # Verificar valores negativos inesperados
                if values.realizado < 0 and concept_name in ['ingresos', 'margen']:
                    warnings.append(f"Valor negativo para {concept_name} mês {month}: {values.realizado}")

        # Validar metadados
        if not project_data.metadata.descricao:
            warnings.append(f"Descrição vazia para projeto {project_data.project_code}")

        if not project_data.metadata.mercado:
            warnings.append(f"Mercado vazio para projeto {project_data.project_code}")

        # Verificar consistência entre meses
        months_per_concept = {}
        for concept_name, monthly_data in project_data.concepts.items():
            months_per_concept[concept_name] = set(monthly_data.keys())

        if len(set(frozenset(months) for months in months_per_concept.values())) > 1:
            warnings.append("Conceitos têm meses diferentes - possível inconsistência de dados")

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def validate_raw_row(self, row: Dict[str, Any]) -> ValidationResult:
        """Valida uma linha bruta da planilha"""
        errors = []
        warnings = []

        # Verificar se tem código do projeto
        project_code = None
        for col_name in ['codigo', 'project_code', 'projeto']:
            if col_name in row and row[col_name] and str(row[col_name]).strip() != 'nan':
                project_code = str(row[col_name]).strip()
                break

        if not project_code:
            errors.append("Linha sem código de projeto válido")
            return ValidationResult(valid=False, errors=errors, warnings=warnings)

        # Verificar se tem conceito
        concept = None
        if 'conceito' in row and row['conceito']:
            concept = str(row['conceito']).strip()

        if not concept:
            warnings.append(f"Linha do projeto {project_code} sem conceito definido")

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def _is_valid_number(self, value) -> bool:
        """Verifica se valor é um número válido"""
        if value is None:
            return False

        try:
            # Aceita valores numéricos e strings que podem ser convertidas
            if isinstance(value, (int, float)):
                return not (isinstance(value, float) and (value != value))  # NaN check
            elif isinstance(value, str):
                # Tenta converter string numérica
                cleaned = value.strip().replace(',', '.')
                float(cleaned)
                return True
            return False
        except (ValueError, TypeError):
            return False