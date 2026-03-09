"""
Main XLS Processor - Coordinates all processing steps
"""

import logging
import pandas as pd
from typing import Dict
from .project_parser import ProjectParser
from .concept_parser import ConceptParser
from .data_validator import DataValidator
from .batch_saver import BatchSaver
from .models import ProjectData, ProcessingResult, ProcessingError
from ..models import ProcessamentoXLS

logger = logging.getLogger(__name__)


class XLSProcessor:
    """Processador XLS com arquitetura limpa e testável"""

    def __init__(self, file_path: str, mes_fechamento: int):
        self.file_path = file_path
        self.mes_fechamento = mes_fechamento

        # Componentes injetados
        self.project_parser = ProjectParser()
        self.concept_parser = ConceptParser()
        self.validator = DataValidator()
        self.batch_saver = BatchSaver()

        # Mapeamento de colunas padrão
        self.col_mapping = {
            'mercado': 'B',      # Coluna B
            'codigo': 'F',       # Coluna F
            'descricao': 'G',    # Coluna G
            'regiao': 'Q',       # Coluna Q
            'tipo_solucao': 'R', # Coluna R
            'responsavel': 'U',  # Coluna U
            'conceito': 'AA',    # Coluna AA
            'is_pipeline': 'K',  # Coluna K
            'is_active': 'P',    # Coluna P
        }

        # Converte letras de coluna para índices numéricos
        self.col_mapping_numeric = self._convert_column_mapping()

    def process(self) -> ProcessingResult:
        """Método principal - fluxo limpo e previsível"""
        try:
            logger.info(f"=== INÍCIO DO PROCESSAMENTO XLS: {self.file_path} (mês fechamento: {self.mes_fechamento}) ===")

            # 1. Carregar e validar dados brutos
            raw_data = self._load_data()
            logger.info(f"Dados carregados: {raw_data.shape[0]} linhas x {raw_data.shape[1]} colunas")

            # 2. Agrupar por projeto
            project_groups = self.project_parser.group_by_projects(raw_data, self.col_mapping_numeric)
            logger.info(f"Projetos encontrados: {len(project_groups)}")

            # 3. Validar grupos de projetos
            validation_issues = self.project_parser.validate_project_groups(project_groups)
            if validation_issues:
                logger.warning(f"Problemas encontrados em {len(validation_issues)} projetos:")
                for project_code, issue in list(validation_issues.items())[:5]:  # Mostra primeiros 5
                    logger.warning(f"  {project_code}: {issue}")

            # 4. Criar registro de processamento
            processamento = self._create_processamento_record()
            logger.info(f"Processamento criado: ID {processamento.id}")

            # 5. Processar cada projeto independentemente
            processed_projects = []
            validation_errors = []

            for project_code, project_rows in project_groups.items():
                try:
                    logger.debug(f"Processando projeto: {project_code}")
                    project_data = self.concept_parser.process_project(project_code, project_rows)

                    # Validar dados do projeto
                    validation_result = self.validator.validate_project_data(project_data)
                    if not validation_result.valid:
                        logger.error(f"Projeto {project_code} inválido: {', '.join(validation_result.errors[:3])}")
                        validation_errors.extend(validation_result.errors)
                        continue

                    if validation_result.warnings:
                        logger.warning(f"Projeto {project_code} warnings: {', '.join(validation_result.warnings[:2])}")

                    processed_projects.append(project_data)

                except Exception as e:
                    error_msg = f"Erro processando projeto {project_code}: {e}"
                    logger.error(error_msg)
                    validation_errors.append(error_msg)
                    continue

            logger.info(f"Projetos validados e prontos para salvar: {len(processed_projects)}")

            # 6. Salvar em lote com rollback
            result = self.batch_saver.save_all(processed_projects, processamento)

            # Adiciona erros de validação ao resultado
            result.errors.extend(validation_errors)
            result.failed += len(validation_errors)

            logger.info("=== PROCESSAMENTO XLS CONCLUÍDO ===")
            return result

        except Exception as e:
            logger.error(f"Erro crítico no processamento: {e}")
            raise ProcessingError(f"Falha no processamento: {e}")

    def _load_data(self) -> pd.DataFrame:
        """Carrega dados da planilha XLS"""
        try:
            df = pd.read_excel(self.file_path, sheet_name='FC', header=None)

            # Remove linhas completamente vazias
            df = df.dropna(how='all')

            # Validação básica
            if df.empty:
                raise ProcessingError("Planilha vazia ou sem dados")

            if df.shape[0] < 35:  # Mínimo esperado
                raise ProcessingError(f"Planilha muito pequena: {df.shape[0]} linhas")

            return df

        except Exception as e:
            raise ProcessingError(f"Erro carregando planilha: {e}")

    def _create_processamento_record(self) -> ProcessamentoXLS:
        """Cria registro de processamento"""
        from datetime import datetime

        # Remove processamento anterior se existir com mesmo arquivo
        ProcessamentoXLS.objects.filter(
            arquivo_nome__endswith=self.file_path.split('/')[-1]
        ).delete()

        processamento = ProcessamentoXLS.objects.create(
            arquivo_nome=self.file_path.split('/')[-1],
            mes_fechado=self.mes_fechamento,
            ano=2026  # TODO: permitir configuração
        )

        return processamento

    def _convert_column_mapping(self) -> Dict[str, int]:
        """Converte mapeamento de letras para índices numéricos"""
        # Ex: 'B' -> 1, 'F' -> 5, 'AA' -> 26, etc.
        result = {}
        for logical_name, excel_col in self.col_mapping.items():
            # Converte letra Excel para índice (A=0, B=1, etc.)
            if len(excel_col) == 1:
                col_index = ord(excel_col.upper()) - ord('A')
            else:
                # Para colunas como AA, AB, etc.
                col_index = 26 * (ord(excel_col[0].upper()) - ord('A') + 1) + (ord(excel_col[1].upper()) - ord('A'))

            result[logical_name] = col_index

        return result