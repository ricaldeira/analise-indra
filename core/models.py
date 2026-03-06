from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Projeto(models.Model):
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código")
    descricao = models.CharField(max_length=255, verbose_name="Descrição")
    mercado = models.CharField(max_length=100, verbose_name="Mercado")
    regiao = models.CharField(max_length=100, blank=True, verbose_name="Região")
    tipo_solucao = models.CharField(max_length=100, blank=True, verbose_name="Tipo de Solução")
    responsavel_comercial = models.CharField(max_length=100, blank=True, verbose_name="Responsável Comercial")

    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class ProcessamentoXLS(models.Model):
    """Armazena informações sobre cada processamento de arquivo XLS"""
    data_processamento = models.DateTimeField(auto_now_add=True, verbose_name="Data do Processamento")
    arquivo_nome = models.CharField(max_length=255, verbose_name="Nome do Arquivo")
    MESES_CHOICES = [
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
        (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
        (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')
    ]

    mes_fechado = models.IntegerField(choices=MESES_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(12)], verbose_name="Mês Fechado")
    ano = models.IntegerField(verbose_name="Ano")

    class Meta:
        verbose_name = "Processamento XLS"
        verbose_name_plural = "Processamentos XLS"
        ordering = ['-data_processamento']

    def __str__(self):
        return f"Processamento {self.arquivo_nome} - {self.mes_fechado}/{self.ano}"


class ConceitoMensal(models.Model):
    """Dados mensais para cada conceito de cada projeto"""

    CONCEITOS_CHOICES = [
        ('carteira_operativa', 'Carteira Operativa'),
        ('contratacion', 'Contratación'),
        ('ingresos', 'Ingresos'),
        ('coste', 'Coste'),
        ('margen', 'Margen'),
        ('margen_percentual', 'Margen(%)'),
        ('clientes', 'Clientes'),
        ('dpf', 'DPF'),
        ('alo', 'ALO'),
        ('existencias', 'Existencias'),
        ('mov_existencias', 'Mov. Existencias'),
        ('facturacion', 'Facturación'),
        ('cobros', 'Cobros'),
        ('costes_directos_corporativos', 'Costes directos corporativos'),
        ('costes_directos_auxiliares', 'Costes Directos Auxiliares'),
        ('costes_elab_ofertas', 'Costes Elab. De Ofertas'),
        ('disponibilidad', 'Disponibilidad'),
        ('actividades_id', 'Actividades I+D'),
        ('desviacion_tasa', 'Desviación Tasa'),
        ('margen_directo', 'Margen Directo'),
        ('margen_directo_percentual', 'Margen Directo (%)'),
    ]

    MESES_CHOICES = [
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
        (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
        (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')
    ]

    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='conceitos_mensais')
    processamento = models.ForeignKey(ProcessamentoXLS, on_delete=models.CASCADE, related_name='conceitos_mensais')
    conceito = models.CharField(max_length=50, choices=CONCEITOS_CHOICES, verbose_name="Conceito")
    mes = models.IntegerField(choices=MESES_CHOICES, verbose_name="Mês")

    # Valores realizados no mês
    valor_realizado = models.FloatField(default=0, verbose_name="Valor Realizado")

    # Valores planejados (POA) para o mês
    valor_planejado = models.FloatField(default=0, verbose_name="Valor Planejado (POA)")

    class Meta:
        verbose_name = "Conceito Mensal"
        verbose_name_plural = "Conceitos Mensais"
        unique_together = ['projeto', 'processamento', 'conceito', 'mes']
        ordering = ['projeto', 'mes', 'conceito']

    def __str__(self):
        return f"{self.projeto.codigo} - {self.get_conceito_display()} - {self.get_mes_display()}"

    @property
    def valor_realizado_ytd(self):
        """Calcula o valor YTD (Year To Date) realizado até o mês atual"""
        return ConceitoMensal.objects.filter(
            projeto=self.projeto,
            processamento=self.processamento,
            conceito=self.conceito,
            mes__lte=self.mes
        ).aggregate(total=models.Sum('valor_realizado'))['total'] or 0

    @property
    def valor_planejado_ytd(self):
        """Calcula o valor YTD (Year To Date) planejado até o mês atual"""
        return ConceitoMensal.objects.filter(
            projeto=self.projeto,
            processamento=self.processamento,
            conceito=self.conceito,
            mes__lte=self.mes
        ).aggregate(total=models.Sum('valor_planejado'))['total'] or 0
