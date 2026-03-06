from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Sum
from datetime import datetime
from .models import Projeto, ConceitoMensal, ProcessamentoXLS
import pandas as pd
import os
import logging

# Configure logger for this module
logger = logging.getLogger('core')

def upload_page(request):
    """Página de upload de arquivos XLS"""
    # Mês padrão: mês anterior ao atual
    hoje = datetime.now()
    mes_padrao = hoje.month - 1 if hoje.month > 1 else 12
    ano_padrao = hoje.year if hoje.month > 1 else hoje.year - 1

    context = {
        'mes_padrao': mes_padrao,
        'ano_padrao': ano_padrao,
        'meses': [
            (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
            (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
            (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')
        ]
    }
    return render(request, 'core/upload.html', context)

def dashboard(request):
    """Dashboard principal com as 3 abas"""
    # Obtém informações do último processamento
    ultimo_processamento = ProcessamentoXLS.objects.order_by('-data_processamento').first()

    aapp_data = get_dashboard_data('AAPP')
    sanidad_data = get_dashboard_data('Sanidad')
    consolidado_data = get_dashboard_data('Consolidado')

    context = {
        'aapp_data': aapp_data,
        'sanidad_data': sanidad_data,
        'consolidado_data': consolidado_data,
        'ultimo_processamento': ultimo_processamento,
    }
    return render(request, 'core/dashboard.html', context)

def api_dashboard_data(request, category):
    """API endpoint para dados do dashboard por categoria"""
    data = get_dashboard_data(category.upper())
    return JsonResponse(data)

@require_POST
@csrf_exempt
def process_upload(request):
    """Processa o upload do arquivo XLS"""
    logger.info("=== INÍCIO DO PROCESSAMENTO DE UPLOAD ===")

    try:
        if 'file' not in request.FILES:
            logger.error("Nenhum arquivo foi enviado na requisição")
            return JsonResponse({'success': False, 'error': 'Nenhum arquivo foi enviado.'})

        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name
        file_size = uploaded_file.size

        # Obtém o mês de fechamento selecionado
        mes_fechamento = int(request.POST.get('mes_fechamento', 2))  # Default Fevereiro

        logger.info(f"Arquivo recebido: {file_name} (tamanho: {file_size} bytes, mês fechamento: {mes_fechamento})")

        # Verifica se é um arquivo XLS/XLSX
        if not file_name.endswith(('.xls', '.xlsx')):
            logger.error(f"Tipo de arquivo não permitido: {file_name}")
            return JsonResponse({'success': False, 'error': 'Apenas arquivos XLS/XLSX são permitidos.'})

        logger.info("Tipo de arquivo validado com sucesso")

        # Salva o arquivo temporariamente
        from django.conf import settings
        file_path = os.path.join(settings.MEDIA_ROOT, 'temp_' + file_name)

        logger.info(f"Salvando arquivo temporariamente em: {file_path}")

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        logger.info(f"Arquivo salvo temporariamente. Tamanho final: {os.path.getsize(file_path)} bytes")

        # Processa o arquivo XLS
        logger.info("Iniciando processamento do arquivo XLS...")
        success, message = process_xls_file(file_path, mes_fechamento)

        # Remove o arquivo temporário
        if os.path.exists(file_path):
            os.unlink(file_path)
            logger.info("Arquivo temporário removido com sucesso")
        else:
            logger.warning("Arquivo temporário não encontrado para remoção")

        if success:
            logger.info(f"Processamento concluído com sucesso: {message}")
            messages.success(request, message)
            return JsonResponse({'success': True, 'message': message})
        else:
            logger.error(f"Processamento falhou: {message}")
            return JsonResponse({'success': False, 'error': message})

    except Exception as e:
        error_msg = f'Erro ao processar arquivo: {str(e)}'
        logger.exception(f"Erro inesperado no processamento de upload: {error_msg}")
        return JsonResponse({'success': False, 'error': error_msg})

def get_projetos_detalhes(category, ultimo_processamento):
    """Retorna dados detalhados dos projetos para a tabela"""
    logger.debug(f"Obtendo dados detalhados dos projetos para categoria: {category}")

    # Filtra projetos por categoria
    if category == 'AAPP':
        projetos = Projeto.objects.filter(mercado__icontains='Administraciones Públicas')
    elif category == 'Sanidad':
        projetos = Projeto.objects.filter(mercado__icontains='Sanidad')
    else:  # Consolidado
        projetos = Projeto.objects.all()

    projetos_data = []

    for projeto in projetos:
        # Calcula valores YTD para cada projeto
        contratacion_ytd = ConceitoMensal.objects.filter(
            projeto=projeto,
            processamento=ultimo_processamento,
            conceito='contratacion',
            mes__lte=ultimo_processamento.mes_fechado
        ).aggregate(total=Sum('valor_realizado'))['total'] or 0

        ingresos_ytd = ConceitoMensal.objects.filter(
            projeto=projeto,
            processamento=ultimo_processamento,
            conceito='ingresos',
            mes__lte=ultimo_processamento.mes_fechado
        ).aggregate(total=Sum('valor_realizado'))['total'] or 0

        margen_ytd = ConceitoMensal.objects.filter(
            projeto=projeto,
            processamento=ultimo_processamento,
            conceito='margen',
            mes__lte=ultimo_processamento.mes_fechado
        ).aggregate(total=Sum('valor_realizado'))['total'] or 0

        # Calcula margem percentual
        margen_percentual = (margen_ytd / ingresos_ytd * 100) if ingresos_ytd > 0 else 0

        # Formatar números com pontos como separadores
        def format_number(value):
            return f"{value:,.0f}".replace(",", ".")

        projetos_data.append({
            'codigo': projeto.codigo,
            'descricao': projeto.descricao,
            'mercado': projeto.mercado,
            'regiao': projeto.regiao or '',
            'tipo_solucao': projeto.tipo_solucao or '',
            'contratacion_ytd': contratacion_ytd,
            'ingresos_ytd': ingresos_ytd,
            'margen_ytd': margen_ytd,
            'margen_percentual': margen_percentual,
            'contratacion_ytd_formatted': format_number(contratacion_ytd),
            'ingresos_ytd_formatted': format_number(ingresos_ytd),
            'margen_ytd_formatted': format_number(margen_ytd),
        })

    # Ordena por margem percentual (decrescente) por padrão
    projetos_data.sort(key=lambda x: x['margen_percentual'], reverse=True)

    return projetos_data

def get_dashboard_data(category):
    """Retorna dados calculados do dashboard baseados nos dados processados"""
    logger.debug(f"Calculando dados do dashboard para categoria: {category}")

    try:
        # Obtém o último processamento
        ultimo_processamento = ProcessamentoXLS.objects.order_by('-data_processamento').first()
        logger.debug(f"Último processamento encontrado: {ultimo_processamento.id if ultimo_processamento else 'Nenhum'}")

        if not ultimo_processamento:
            # Retorna dados vazios se não há processamento
            return {
                'cards': [
                    {'title': 'Total Projetos', 'value': '0', 'change': '0%', 'change_type': 'neutral', 'icon': 'bi-folder'},
                    {'title': 'Receita Total', 'value': 'R$ 0', 'change': '0%', 'change_type': 'neutral', 'icon': 'bi-cash-stack'},
                    {'title': 'Margem Média', 'value': '0%', 'change': '0%', 'change_type': 'neutral', 'icon': 'bi-graph-up'},
                    {'title': 'Contratações', 'value': '0', 'change': '0%', 'change_type': 'neutral', 'icon': 'bi-clipboard-check'},
                    {'title': 'Projetos Ativos', 'value': '0', 'change': '0%', 'change_type': 'neutral', 'icon': 'bi-play-circle'},
                    {'title': 'ROI Médio', 'value': '0%', 'change': '0%', 'change_type': 'neutral', 'icon': 'bi-trophy'},
                ],
                'projetos': []
            }

        # Filtra projetos por categoria
        if category == 'AAPP':
            projetos = Projeto.objects.filter(mercado__icontains='Administraciones Públicas')
        elif category == 'Sanidad':
            projetos = Projeto.objects.filter(mercado__icontains='Sanidad')
        else:  # Consolidado
            projetos = Projeto.objects.all()

        # Calcula métricas
        total_projetos = projetos.count()

        # Receita Total (baseado em Ingresos realizados YTD)
        receita_total = 0
        margem_total = 0
        contratacoes_total = 0

        for projeto in projetos:
            # Ingresos realizados até o mês fechado
            ingresos_ytd = ConceitoMensal.objects.filter(
                projeto=projeto,
                processamento=ultimo_processamento,
                conceito='ingresos',
                mes__lte=ultimo_processamento.mes_fechado
            ).aggregate(total=Sum('valor_realizado'))['total'] or 0

            # Margem realizada até o mês fechado
            margen_ytd = ConceitoMensal.objects.filter(
                projeto=projeto,
                processamento=ultimo_processamento,
                conceito='margen',
                mes__lte=ultimo_processamento.mes_fechado
            ).aggregate(total=Sum('valor_realizado'))['total'] or 0

            # Contratações realizadas até o mês fechado
            contratacion_ytd = ConceitoMensal.objects.filter(
                projeto=projeto,
                processamento=ultimo_processamento,
                conceito='contratacion',
                mes__lte=ultimo_processamento.mes_fechado
            ).aggregate(total=Sum('valor_realizado'))['total'] or 0

            receita_total += ingresos_ytd
            margem_total += margen_ytd
            contratacoes_total += contratacion_ytd

        # Calcula margem média percentual
        margem_media_percentual = 0
        if receita_total > 0:
            margem_media_percentual = (margem_total / receita_total) * 100

        # Calcula projetos ativos (projetos com ingresos > 0 no último mês)
        projetos_ativos = 0
        for projeto in projetos:
            ingresos_ultimo_mes = ConceitoMensal.objects.filter(
                projeto=projeto,
                processamento=ultimo_processamento,
                conceito='ingresos',
                mes=ultimo_processamento.mes_fechado
            ).aggregate(total=Sum('valor_realizado'))['total'] or 0

            if ingresos_ultimo_mes > 0:
                projetos_ativos += 1

        # Calcula ROI médio (usando margem como proxy)
        roi_medio = margem_media_percentual

        # Formata valores
        def format_currency(value):
            if abs(value) >= 1000000:
                return f"R$ {value/1000000:.1f}M"
            elif abs(value) >= 1000:
                return f"R$ {value/1000:.0f}K"
            else:
                return f"R$ {value:.0f}"

        # Calcula variações (comparado com mês anterior - simplificado)
        # Aqui seria implementada lógica de comparação com processamento anterior
        def calculate_change(current, previous):
            if previous == 0:
                return current > 0 and "+100%" or "0%"
            change_pct = ((current - previous) / abs(previous)) * 100
            return f"{'+' if change_pct > 0 else ''}{change_pct:.0f}%"

        result = [
            {
                'title': 'Total Projetos',
                'value': str(total_projetos),
                'change': '+5%',  # Placeholder - seria calculado comparando com processamento anterior
                'change_type': 'positive',
                'icon': 'bi-folder'
            },
            {
                'title': 'Receita Total',
                'value': format_currency(receita_total),
                'change': '+8%',  # Placeholder
                'change_type': 'positive',
                'icon': 'bi-cash-stack'
            },
            {
                'title': 'Margem Média',
                'value': f'{margem_media_percentual:.1f}%',
                'change': f'{margem_media_percentual > 15 and "+" or "-"}{abs(margem_media_percentual - 15):.1f}%',
                'change_type': margem_media_percentual > 15 and 'positive' or 'negative',
                'icon': 'bi-graph-up'
            },
            {
                'title': 'Contratações',
                'value': format_currency(contratacoes_total),
                'change': '+12%',  # Placeholder
                'change_type': 'positive',
                'icon': 'bi-clipboard-check'
            },
            {
                'title': 'Projetos Ativos',
                'value': str(projetos_ativos),
                'change': '+7%',  # Placeholder
                'change_type': 'positive',
                'icon': 'bi-play-circle'
            },
            {
                'title': 'ROI Médio',
                'value': f'{roi_medio:.1f}%',
                'change': '+3%',  # Placeholder
                'change_type': 'positive',
                'icon': 'bi-trophy'
            },
        ]

        # Obtém dados detalhados dos projetos
        projetos_detalhes = get_projetos_detalhes(category, ultimo_processamento)

        logger.debug(f"Dados do dashboard calculados com sucesso para {category}: {len(result)} métricas, {len(projetos_detalhes)} projetos")
        return {
            'cards': result,
            'projetos': projetos_detalhes
        }

    except Exception as e:
        # Em caso de erro, retorna dados vazios
        logger.exception(f"Erro ao calcular dados do dashboard para categoria {category}: {e}")
        return {
            'cards': [
                {'title': 'Total Projetos', 'value': '0', 'change': '0%', 'change_type': 'neutral', 'icon': 'bi-folder'},
                {'title': 'Receita Total', 'value': 'R$ 0', 'change': '0%', 'change_type': 'neutral', 'icon': 'bi-cash-stack'},
                {'title': 'Margem Média', 'value': '0%', 'change': '0%', 'change_type': 'neutral', 'icon': 'bi-graph-up'},
                {'title': 'Contratações', 'value': '0', 'change': '0%', 'change_type': 'neutral', 'icon': 'bi-clipboard-check'},
                {'title': 'Projetos Ativos', 'value': '0', 'change': '0%', 'change_type': 'neutral', 'icon': 'bi-play-circle'},
                {'title': 'ROI Médio', 'value': '0%', 'change': '0%', 'change_type': 'neutral', 'icon': 'bi-trophy'},
            ],
            'projetos': []
        }

def process_xls_file(file_path, mes_fechamento=2):
    """Processa o arquivo XLS da aba FC e alimenta o banco de dados"""
    logger.info(f"=== INÍCIO DO PROCESSAMENTO XLS: {file_path} (mês fechamento: {mes_fechamento}) ===")

    try:
        # Lê apenas a aba FC
        logger.info("Lendo aba FC do arquivo Excel...")
        df = pd.read_excel(file_path, sheet_name='FC')
        logger.info(f"Arquivo lido com sucesso. Dimensões: {df.shape[0]} linhas x {df.shape[1]} colunas")

        # Mapeamento das colunas conforme documentação
        col_mapping = {
            'mercado': df.columns[1],      # Coluna B
            'codigo': df.columns[5],       # Coluna F
            'descricao': df.columns[6],    # Coluna G
            'regiao': df.columns[16],      # Coluna Q
            'tipo_solucao': df.columns[17], # Coluna R
            'responsavel': df.columns[20], # Coluna U
            'conceito': df.columns[26],    # Coluna AA
        }

        # Mapeamento dos meses (colunas de realização atual começam na coluna 53)
        meses_realizados = {
            1: df.columns[53],   # Janeiro
            2: df.columns[54],   # Fevereiro
            3: df.columns[55],   # Março
            4: df.columns[56],   # Abril
            5: df.columns[57],   # Maio
            6: df.columns[58],   # Junho
            7: df.columns[59],   # Julho
            8: df.columns[60],   # Agosto
            9: df.columns[61],   # Setembro
            10: df.columns[62],  # Outubro
            11: df.columns[63],  # Novembro
            12: df.columns[64],  # Dezembro
        }

        # Mapeamento dos meses planejados (POA) começam na coluna 40
        meses_poa = {
            1: df.columns[40],   # Janeiro POA
            2: df.columns[41],   # Fevereiro POA
            3: df.columns[42],   # Março POA
            4: df.columns[43],   # Abril POA
            5: df.columns[44],   # Maio POA
            6: df.columns[45],   # Junho POA
            7: df.columns[46],   # Julho POA
            8: df.columns[47],   # Agosto POA
            9: df.columns[48],   # Setembro POA
            10: df.columns[49],  # Outubro POA
            11: df.columns[50],  # Novembro POA
            12: df.columns[51],  # Dezembro POA
        }

        # Mapeamento dos conceitos
        conceito_mapping = {
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

        logger.info(f"Mapeamento de conceitos configurado: {len(conceito_mapping)} conceitos")

        # APAGA TODOS OS DADOS ANTERIORES (conforme solicitado)
        logger.info("Limpando dados anteriores...")
        processamento_count = ProcessamentoXLS.objects.count()
        projeto_count = Projeto.objects.count()
        conceito_count = ConceitoMensal.objects.count()

        ProcessamentoXLS.objects.all().delete()
        Projeto.objects.all().delete()

        logger.info(f"Dados anteriores removidos: {processamento_count} processamentos, {projeto_count} projetos, {conceito_count} conceitos")

        # Cria registro de processamento
        logger.info("Criando registro de processamento...")
        processamento = ProcessamentoXLS.objects.create(
            arquivo_nome=file_path.split('/')[-1],
            mes_fechado=mes_fechamento,
            ano=2026  # TODO: permitir seleção do ano também
        )
        logger.info(f"Registro de processamento criado: ID {processamento.id}, arquivo: {processamento.arquivo_nome}")

        # Processa apenas a partir da linha 35 (dados reais)
        logger.info("Iniciando processamento das linhas do arquivo (a partir da linha 35)...")
        projetos_processados = 0
        conceitos_processados = 0

        current_project = None
        project_data = {}
        linhas_processadas = 0

        # Rastrear projetos já processados neste processamento para evitar duplicatas
        projetos_processados_neste_arquivo = set()

        for idx, row in df.iterrows():
            if idx < 35:  # Pula cabeçalhos
                continue

            linhas_processadas += 1

            # Log progresso a cada 100 linhas
            if linhas_processadas % 100 == 0:
                logger.info(f"Processadas {linhas_processadas} linhas...")

            try:
                # Extrai dados básicos
                codigo = str(row[col_mapping['codigo']]).strip() if pd.notna(row[col_mapping['codigo']]) else None
                conceito_raw = str(row[col_mapping['conceito']]).strip() if pd.notna(row[col_mapping['conceito']]) else None

                # Se temos um código de projeto válido, é o início de um novo projeto
                if codigo and codigo != 'nan' and conceito_raw == 'Carteira Operativa':
                    # Verificar se este projeto já foi processado neste arquivo
                    if codigo in projetos_processados_neste_arquivo:
                        logger.warning(f"Projeto {codigo} já foi processado neste arquivo (linha {idx + 1}). Pulando próximas 12 linhas para evitar duplicatas.")
                        # Pular as próximas 12 linhas (total 13 incluindo esta)
                        linhas_para_pular = 12
                        continue

                    # Salva o projeto anterior se existir
                    if current_project and project_data:
                        logger.info(f"Salvando projeto: {current_project['codigo']} - {len(project_data)} conceitos")
                        _salvar_projeto_com_conceitos(current_project, project_data, processamento)
                        projetos_processados += 1
                        projetos_processados_neste_arquivo.add(current_project['codigo'])

                    # Inicia novo projeto
                    current_project = {
                        'codigo': codigo,
                        'descricao': str(row[col_mapping['descricao']]).strip() if pd.notna(row[col_mapping['descricao']]) else '',
                        'mercado': str(row[col_mapping['mercado']]).strip() if pd.notna(row[col_mapping['mercado']]) else '',
                        'regiao': str(row[col_mapping['regiao']]).strip() if pd.notna(row[col_mapping['regiao']]) else '',
                        'tipo_solucao': str(row[col_mapping['tipo_solucao']]).strip() if pd.notna(row[col_mapping['tipo_solucao']]) else '',
                        'responsavel_comercial': str(row[col_mapping['responsavel']]).strip() if pd.notna(row[col_mapping['responsavel']]) else '',
                    }
                    project_data = {}
                    logger.debug(f"Novo projeto iniciado: {codigo}")

                # Se temos um conceito válido, processa os dados mensais
                if conceito_raw and conceito_raw in conceito_mapping:
                    conceito_key = conceito_mapping[conceito_raw]

                    # Extrai dados mensais realizados
                    dados_mensais = {}
                    for mes, col_realizado in meses_realizados.items():
                        valor_realizado = row[col_realizado] if pd.notna(row[col_realizado]) else 0
                        dados_mensais[mes] = {
                            'realizado': float(valor_realizado) if isinstance(valor_realizado, (int, float)) else 0,
                            'planejado': 0  # Será preenchido abaixo
                        }

                    # Extrai dados mensais planejados (POA)
                    for mes, col_poa in meses_poa.items():
                        valor_poa = row[col_poa] if pd.notna(row[col_poa]) else 0
                        if mes in dados_mensais:
                            dados_mensais[mes]['planejado'] = float(valor_poa) if isinstance(valor_poa, (int, float)) else 0

                    project_data[conceito_key] = dados_mensais

            except Exception as e:
                logger.error(f"Erro ao processar linha {idx + 1}: {str(e)}")
                return False, f"Erro ao processar linha {idx + 1}: {str(e)}"

        # Salva o último projeto
        if current_project and project_data:
            logger.info(f"Salvando último projeto: {current_project['codigo']} - {len(project_data)} conceitos")
            _salvar_projeto_com_conceitos(current_project, project_data, processamento)
            projetos_processados += 1

        # Conta total de conceitos processados
        conceitos_processados = ConceitoMensal.objects.filter(processamento=processamento).count()

        logger.info("=== PROCESSAMENTO XLS CONCLUÍDO COM SUCESSO ===")
        logger.info(f"Total de linhas processadas: {linhas_processadas}")
        logger.info(f"Projetos processados: {projetos_processados}")
        logger.info(f"Projetos únicos encontrados: {len(projetos_processados_neste_arquivo)}")
        logger.info(f"Conceitos mensais criados: {conceitos_processados}")

        if len(projetos_processados_neste_arquivo) != projetos_processados:
            projetos_pulados = projetos_processados - len(projetos_processados_neste_arquivo)
            logger.warning(f"Projetos com duplicatas pulados: {projetos_pulados}")

        success_msg = f"Arquivo processado com sucesso! {projetos_processados} projetos e {conceitos_processados} registros de conceitos processados."
        logger.info(success_msg)

        return True, success_msg

    except Exception as e:
        error_msg = f"Erro ao processar arquivo XLS: {str(e)}"
        logger.exception(f"Erro crítico no processamento XLS: {error_msg}")
        return False, error_msg


def _salvar_projeto_com_conceitos(project_info, project_data, processamento):
    """Salva um projeto e seus conceitos mensais no banco de dados"""
    logger.debug(f"Salvando projeto {project_info['codigo']} com {len(project_data)} conceitos")

    # Cria ou atualiza o projeto
    projeto, created = Projeto.objects.get_or_create(
        codigo=project_info['codigo'],
        defaults={
            'descricao': project_info['descricao'],
            'mercado': project_info['mercado'],
            'regiao': project_info['regiao'],
            'tipo_solucao': project_info['tipo_solucao'],
            'responsavel_comercial': project_info['responsavel_comercial'],
        }
    )

    # Se o projeto já existia, atualiza os dados
    if not created:
        projeto.descricao = project_info['descricao']
        projeto.mercado = project_info['mercado']
        projeto.regiao = project_info['regiao']
        projeto.tipo_solucao = project_info['tipo_solucao']
        projeto.responsavel_comercial = project_info['responsavel_comercial']
        projeto.save()
        logger.debug(f"Projeto {project_info['codigo']} atualizado")
    else:
        logger.debug(f"Projeto {project_info['codigo']} criado")

    # Cria os registros de conceitos mensais
    conceitos_criados = 0
    for conceito_key, dados_mensais in project_data.items():
        for mes, valores in dados_mensais.items():
            ConceitoMensal.objects.create(
                projeto=projeto,
                processamento=processamento,
                conceito=conceito_key,
                mes=mes,
                valor_realizado=valores['realizado'],
                valor_planejado=valores['planejado']
            )
            conceitos_criados += 1

    logger.debug(f"Criados {conceitos_criados} registros de conceitos mensais para projeto {project_info['codigo']}")
