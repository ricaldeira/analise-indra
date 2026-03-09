"""
Batch saver - Saves project data in transactions
"""

import logging
from typing import List, Dict
from django.db import transaction
from .models import ProjectData, ProcessingResult, ProcessingError
from ..models import Projeto, ConceitoMensal, ProcessamentoXLS

logger = logging.getLogger(__name__)


class BatchSaver:
    """Salvamento em lote com transações"""

    def save_all(self, projects_data: List[ProjectData], processamento: ProcessamentoXLS) -> ProcessingResult:
        """Salva todos os projetos em uma transação"""
        logger.info(f"Iniciando salvamento de {len(projects_data)} projetos")

        saved_projects = []
        errors = []

        # Processa projetos em lotes menores para evitar timeout
        batch_size = 10
        for i in range(0, len(projects_data), batch_size):
            batch = projects_data[i:i + batch_size]
            batch_result = self._save_batch(batch, processamento)
            saved_projects.extend(batch_result['saved'])
            errors.extend(batch_result['errors'])

        # Atualiza agregados após salvar tudo
        try:
            self._update_project_aggregates(processamento)
        except Exception as e:
            logger.error(f"Erro atualizando agregados: {e}")
            errors.append(f"Erro atualizando agregados: {e}")

        result = ProcessingResult(
            successful=len(saved_projects),
            failed=len(errors),
            errors=errors,
            processed_projects=saved_projects
        )

        logger.info(f"Processamento concluído: {result.successful} sucesso, {result.failed} falhas")

        # Log projetos processados com sucesso
        if result.successful > 0:
            logger.info(f"Projetos processados: {', '.join(saved_projects[:5])}{'...' if len(saved_projects) > 5 else ''}")

        # Log erros
        if errors:
            logger.warning(f"Erros encontrados: {len(errors)}")
            for error in errors[:3]:  # Mostra apenas primeiros 3 erros
                logger.warning(f"  {error}")

        return result

    def _save_batch(self, projects_batch: List[ProjectData], processamento: ProcessamentoXLS) -> Dict:
        """Salva projetos individualmente para isolamento de erros"""
        saved = []
        errors = []

        for project_data in projects_batch:
            try:
                # Cada projeto em sua própria transação
                with transaction.atomic():
                    self._save_single_project(project_data, processamento)
                    saved.append(project_data.project_code)
            except Exception as e:
                error_msg = f"Erro salvando {project_data.project_code}: {e}"
                logger.error(error_msg)
                errors.append(error_msg)

        return {'saved': saved, 'errors': errors}

    def _save_single_project(self, project_data: ProjectData, processamento: ProcessamentoXLS) -> None:
        """Salva dados de um projeto específico"""
        # Cria ou atualiza projeto
        projeto, created = Projeto.objects.get_or_create(
            codigo=project_data.project_code,
            defaults={
                'descricao': project_data.metadata.descricao,
                'mercado': project_data.metadata.mercado,
                'regiao': project_data.metadata.regiao,
                'tipo_solucao': project_data.metadata.tipo_solucao,
                'responsavel_comercial': project_data.metadata.responsavel_comercial,
                'is_pipeline': project_data.metadata.is_pipeline,
                'is_active': project_data.metadata.is_active,
            }
        )

        if not created:
            # Atualiza dados se projeto já existia
            projeto.descricao = project_data.metadata.descricao
            projeto.mercado = project_data.metadata.mercado
            projeto.regiao = project_data.metadata.regiao
            projeto.tipo_solucao = project_data.metadata.tipo_solucao
            projeto.responsavel_comercial = project_data.metadata.responsavel_comercial
            projeto.is_pipeline = project_data.metadata.is_pipeline
            projeto.is_active = project_data.metadata.is_active
            projeto.save()

        # Salva conceitos mensais
        conceitos_criados = 0
        for concept_key, monthly_data in project_data.concepts.items():
            for mes, values in monthly_data.items():
                ConceitoMensal.objects.update_or_create(
                    projeto=projeto,
                    processamento=processamento,
                    conceito=concept_key,
                    mes=mes,
                    defaults={
                        'valor_realizado': values.realizado,
                        'valor_planejado': values.planejado
                    }
                )
                conceitos_criados += 1

        logger.debug(f"Projeto {project_data.project_code}: {conceitos_criados} registros salvos")

    def _update_project_aggregates(self, processamento: ProcessamentoXLS) -> None:
        """Atualiza agregados dos projetos após processamento"""
        from ..views import update_projeto_aggregates
        update_projeto_aggregates(processamento)