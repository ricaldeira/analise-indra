"""
Project parser - Groups XLS rows by project code
"""

import logging
from typing import Dict, List, Optional
from collections import defaultdict
import pandas as pd

logger = logging.getLogger(__name__)


class ProjectParser:
    """Agrupa linhas por código de projeto"""

    def group_by_projects(self, df: pd.DataFrame, col_mapping: Dict[str, str]) -> Dict[str, List[Dict]]:
        """
        Agrupa todas as linhas por código de projeto

        Args:
            df: DataFrame pandas com dados da planilha
            col_mapping: Mapeamento de colunas

        Returns:
            Dict com código do projeto -> lista de linhas
        """
        logger.info("Agrupando linhas por código de projeto...")

        projects = defaultdict(list)

        for idx, row in df.iterrows():
            try:
                project_code = self._extract_project_code(row, col_mapping)
                if project_code:
                    row_dict = self._row_to_dict(row, col_mapping)
                    projects[project_code].append(row_dict)
                else:
                    logger.debug(f"Linha {idx + 1} sem código de projeto válido")
            except Exception as e:
                logger.warning(f"Erro processando linha {idx + 1}: {e}")
                continue

        # Filtrar projetos vazios
        valid_projects = {code: rows for code, rows in projects.items() if rows}
        logger.info(f"Encontrados {len(valid_projects)} projetos válidos")

        return dict(valid_projects)

    def _extract_project_code(self, row: pd.Series, col_mapping: Dict[str, int]) -> Optional[str]:
        """Extrai código do projeto de forma robusta"""
        # Tenta múltiplas colunas possíveis
        possible_columns = ['codigo', 'project_code', 'projeto']

        for col_name in possible_columns:
            col_index = col_mapping.get(col_name)
            if col_index is not None and col_index < len(row) and pd.notna(row[col_index]):
                code = str(row[col_index]).strip()
                if code and code.lower() not in ['nan', 'none', '']:
                    return code

        return None

    def _row_to_dict(self, row: pd.Series, col_mapping: Dict[str, int]) -> Dict:
        """Converte linha pandas para dicionário"""
        row_dict = {}

        # Mapeamento reverso: indice_coluna -> nome_logico
        reverse_mapping = {v: k for k, v in col_mapping.items()}

        for col_index, value in row.items():
            col_logical = reverse_mapping.get(col_index, f'col_{col_index}')
            if pd.notna(value):
                row_dict[col_logical] = value
            else:
                row_dict[col_logical] = None

        return row_dict

    def validate_project_groups(self, project_groups: Dict[str, List[Dict]]) -> Dict[str, str]:
        """
        Valida grupos de projetos e retorna problemas encontrados.
        Filtra projetos que não são projetos reais (totais, subtotais, etc.)
        """
        issues = {}
        valid_projects = {}

        for project_code, rows in project_groups.items():
            # Filtrar projetos que não são códigos de projeto reais
            if self._is_invalid_project_code(project_code):
                continue  # Ignorar silenciosamente

            if len(rows) < 2:  # Pelo menos 2 linhas (Carteira + 1 conceito)
                issues[project_code] = f"Apenas {len(rows)} linhas - poucos dados"
                continue

            # Verificar se tem linha de "Carteira Operativa" (marcador de projeto)
            has_carteira = any(
                row.get('conceito') == 'Carteira Operativa'
                for row in rows
            )
            if not has_carteira:
                issues[project_code] = "Sem linha 'Carteira Operativa'"
                continue

            # Verificar se tem pelo menos um conceito financeiro
            financial_concepts = ['ingresos', 'margen', 'contratacion', 'coste']
            has_financial_data = any(
                any(row.get('conceito') == concept for concept in ['Ingresos', 'Margen', 'Contratación', 'Coste'])
                for row in rows
            )
            if not has_financial_data:
                issues[project_code] = "Sem dados financeiros"
                continue

            # Projeto válido
            valid_projects[project_code] = rows

        # Substituir project_groups pelos projetos válidos
        project_groups.clear()
        project_groups.update(valid_projects)

        return issues

    def _is_invalid_project_code(self, project_code: str) -> bool:
        """
        Verifica se o código não representa um projeto real
        """
        if not project_code or project_code.lower() in ['nan', 'none', '']:
            return True

        # Projetos que são apenas números (provavelmente totais ou códigos inválidos)
        if project_code.replace('.', '').replace('-', '').isdigit():
            return True

        # Códigos muito curtos ou muito longos
        if len(project_code) < 3 or len(project_code) > 20:
            return True

        # Códigos que parecem meses
        months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        if project_code.lower() in months:
            return True

        return False