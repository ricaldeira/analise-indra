"""
Concept parser - Processes concepts for a specific project
"""

import logging
from typing import Dict, List
from .models import ProjectData, ProjectMetadata, MonthlyValues

logger = logging.getLogger(__name__)


class ConceptParser:
    """Processa conceitos para um projeto específico"""

    # Mapeamento de conceitos da planilha para chaves do sistema
    CONCEITO_MAPPING = {
        'Carteira Operativa': 'carteira_operativa',
        'Contratación': 'contratacion',
        'Ingresos': 'ingresos',
        'Coste': 'coste',
        'Margen': 'margen',
        'Margen(%)': 'margen_percentual',
        'Clientes': 'clientes',
        'DPF': 'dpf',
        'ALO': 'alo',
        'Existencias': 'existencias',
        'Mov. Existencias': 'mov_existencias',
        'Facturación': 'facturacion',
        'Cobros': 'cobros',
        'Costes directos corporativos': 'costes_directos_corporativos',
        'Costes Directos Auxiliares': 'costes_directos_auxiliares',
        'Costes Elab. De Ofertas': 'costes_elab_ofertas',
        'Disponibilidad': 'disponibilidad',
        'Actividades I+D': 'actividades_id',
        'Desviación Tasa': 'desviacion_tasa',
        'Margen Directo': 'margen_directo',
        'Margen Directo (%)': 'margen_directo_percentual',
    }

    # Meses do ano
    MESES = list(range(1, 13))

    # Colunas de valores realizados (53-64)
    MESES_REALIZADOS = {mes: 52 + mes for mes in MESES}

    # Colunas de valores POA/planejados (40-51)
    MESES_POA = {mes: 39 + mes for mes in MESES}

    def process_project(self, project_code: str, rows: List[Dict]) -> ProjectData:
        """Processa todos os conceitos de um projeto"""
        logger.debug(f"Processando projeto {project_code} com {len(rows)} linhas")

        concepts_data = {}
        metadata = self._extract_metadata(rows)

        for row in rows:
            concept_name = self._extract_concept(row)
            if concept_name:
                concept_key = self._map_concept(concept_name)
                if concept_key:
                    # Processa valores mensais para este conceito
                    monthly_data = self._extract_monthly_values(row)
                    if monthly_data:
                        concepts_data[concept_key] = monthly_data

        return ProjectData(
            project_code=project_code,
            concepts=concepts_data,
            metadata=metadata
        )

    def _extract_concept(self, row: Dict) -> str:
        """Extrai nome do conceito da linha"""
        return row.get('conceito', '').strip() if row.get('conceito') else ''

    def _map_concept(self, concept_name: str) -> str:
        """Mapeia nome do conceito para chave do sistema"""
        return self.CONCEITO_MAPPING.get(concept_name, concept_name.lower().replace(' ', '_'))

    def _extract_monthly_values(self, row: Dict) -> Dict[int, MonthlyValues]:
        """Extrai valores mensais (realizados e POA) da linha"""
        monthly_data = {}

        for mes in self.MESES:
            # Valor realizado
            col_realizado = f'col_{self.MESES_REALIZADOS[mes]}'
            valor_realizado = self._extract_numeric_value(row, col_realizado)

            # Valor POA/planejado
            col_poa = f'col_{self.MESES_POA[mes]}'
            valor_planejado = self._extract_numeric_value(row, col_poa)

            monthly_data[mes] = MonthlyValues(
                realizado=valor_realizado,
                planejado=valor_planejado
            )

        return monthly_data

    def _extract_numeric_value(self, row: Dict, column_key: str) -> float:
        """Extrai e converte valor numérico de forma robusta"""
        value = row.get(column_key)

        if value is None:
            return 0.0

        try:
            # Trata strings numéricas
            if isinstance(value, str):
                # Remove espaços e converte vírgulas para pontos
                cleaned = value.strip().replace(',', '.')
                if not cleaned or cleaned.lower() in ['nan', 'none', '']:
                    return 0.0

                # Ignorar nomes de meses em espanhol
                month_names = [
                    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
                ]
                if cleaned.lower() in month_names:
                    return 0.0

                return float(cleaned)
            # Trata números diretamente
            elif isinstance(value, (int, float)):
                return float(value)
            else:
                return 0.0
        except (ValueError, TypeError):
            logger.warning(f"Valor inválido '{value}' na coluna {column_key}, usando 0.0")
            return 0.0

    def _extract_metadata(self, rows: List[Dict]) -> ProjectMetadata:
        """Extrai metadados do projeto da primeira linha válida"""
        for row in rows:
            if row.get('conceito') == 'Carteira Operativa':
                return ProjectMetadata(
                    descricao=self._clean_text(row.get('descripcion', row.get('descricao', ''))),
                    mercado=self._clean_text(row.get('mercado', 'Não informado')),
                    regiao=self._clean_text(row.get('regiao', '')),
                    tipo_solucao=self._clean_text(row.get('tipo_solucao', '')),
                    responsavel_comercial=self._clean_text(row.get('responsavel', '')),
                    is_pipeline=self._parse_boolean(row.get('is_pipeline')),
                    is_active=self._parse_boolean(row.get('is_active', True))
                )

        # Fallback se não encontrou linha de Carteira Operativa
        return ProjectMetadata(
            descricao=self._clean_text(rows[0].get('descripcion', rows[0].get('descripcion', ''))) if rows else '',
            mercado=self._clean_text(rows[0].get('mercado', 'Não informado')) if rows else 'Não informado',
            is_active=True
        )

    def _clean_text(self, value) -> str:
        """Limpa texto removendo valores inválidos"""
        if not value or str(value).lower() in ['nan', 'none', '']:
            return ''
        return str(value).strip()

    def _parse_boolean(self, value) -> bool:
        """Converte valor para booleano de forma robusta"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            # Valores que significam False
            false_values = ['no', 'false', 'falso', 'inactivo', 'cancelado', 'finalizado', '']
            return str(value).lower() not in false_values
        if isinstance(value, (int, float)):
            return bool(value)
        return False