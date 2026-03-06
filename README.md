# Análise Indra

Sistema web profissional para análise de projetos desenvolvido com Django, apresentando uma interface moderna e responsiva para upload e visualização de dados de projetos.

## 🚀 Características

- **Upload de Arquivos XLS/XLSX**: Interface intuitiva para upload e processamento de arquivos Excel
- **Dashboard Analítico**: Visualização de dados com 3 abas principais (AAPP, Sanidad, Consolidado)
- **Design Profissional**: Interface moderna com Bootstrap 5 e animações suaves
- **Banco de Dados Relacional**: Modelos estruturados para projetos e conceitos
- **Processamento Inteligente**: Engine para processamento automático de dados XLS
- **Interface Responsiva**: Funciona perfeitamente em desktop e dispositivos móveis

## 📋 Funcionalidades

### 📤 Upload de Arquivos
- Upload seguro de arquivos XLS/XLSX
- Validação automática do formato e estrutura dos dados
- Feedback visual durante o processamento
- Tratamento de erros e mensagens informativas

### 📊 Dashboard
- **3 Abas Principais**:
  - **AAPP**: Indicadores específicos para projetos AAPP
  - **Sanidad**: Métricas de saúde e projetos relacionados
  - **Consolidado**: Visão geral consolidada de todos os projetos

- **6 Cards por Aba**:
  - Total de Projetos
  - Receita Total
  - Margem Média
  - Contratações
  - Projetos Ativos
  - ROI Médio

### 🗄️ Modelos de Dados

#### Projeto
```python
- codigo: CharField (Código único do projeto)
- descricao: CharField (Descrição detalhada)
- mercado: CharField (Segmento de mercado)
```

#### Conceitos
```python
- projeto: ForeignKey (Relacionamento com Projeto)
- contratacao: FloatField (Valor de contratação)
- venda: FloatField (Valor de venda)
- margem: FloatField (Valor da margem)
- margem_percentual: FloatField (Margem percentual)
```

## 📊 Sistema de Logging

O sistema inclui logging abrangente para monitoramento e depuração:

### **Logs Disponíveis:**
- **Arquivo**: `logs/processamento.log` - Log detalhado de todas as operações
- **Console**: Logs em tempo real no terminal durante execução
- **Níveis**: INFO, DEBUG, ERROR, WARNING

### **O que é Logado:**
- ✅ **Upload de arquivos**: Tamanho, validação, salvamento temporário
- ✅ **Processamento XLS**: Leitura, mapeamento, limpeza de dados
- ✅ **Criação de registros**: Projetos e conceitos salvos
- ✅ **Progresso**: Contadores de linhas processadas (a cada 100 linhas)
- ✅ **Erros**: Detalhes completos de falhas e exceções
- ✅ **Dashboard**: Cálculos de métricas e consultas

### **Como Visualizar Logs:**
```bash
# Script interativo
./visualizar_logs.sh

# Comando direto
tail -f logs/processamento.log  # Tempo real
tail -50 logs/processamento.log # Últimas 50 linhas
grep "ERROR" logs/processamento.log # Apenas erros
```

### **Exemplo de Log:**
```
INFO 2026-03-05 17:19:53 Arquivo recebido: arquivo.xlsx (12MB)
INFO 2026-03-05 17:20:00 Arquivo lido: 7380 linhas x 136 colunas
INFO 2026-03-05 17:20:01 Salvando projeto: PRJ001 - 13 conceitos
INFO 2026-03-05 17:20:47 Processadas 1100 linhas...
ERROR 2026-03-05 17:21:13 Constraint UNIQUE failed...
```

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 6.0
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Processamento XLS**: Pandas, OpenPyXL
- **Ícones**: Bootstrap Icons

## 📦 Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- pip
- Virtualenv (recomendado)

### Instalação

1. **Clone o repositório** (ou crie a estrutura conforme descrito)
2. **Crie e ative o ambiente virtual**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install django pandas openpyxl
   ```

4. **Execute as migrações**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Inicie o servidor**:
   ```bash
   python manage.py runserver
   ```

6. **Acesse a aplicação**:
   - Página inicial (Upload): http://localhost:8000/
   - Dashboard: http://localhost:8000/dashboard/

## 📁 Estrutura do Projeto

```
analise-indra/
├── analise_indra/          # Configurações do projeto Django
│   ├── settings.py        # Configurações principais
│   ├── urls.py           # URLs do projeto
│   └── wsgi.py           # Configuração WSGI
├── core/                  # App principal
│   ├── migrations/       # Migrações do banco
│   ├── templates/core/   # Templates HTML
│   │   ├── base.html     # Template base
│   │   ├── upload.html   # Página de upload
│   │   └── dashboard.html # Dashboard
│   ├── models.py         # Modelos de dados
│   ├── views.py          # Views e lógica
│   └── urls.py           # URLs do app
├── static/               # Arquivos estáticos
│   ├── css/
│   │   └── style.css     # Estilos personalizados
│   ├── js/
│   │   └── main.js       # JavaScript personalizado
│   └── img/              # Imagens (se necessário)
├── media/                # Arquivos de mídia (uploads)
├── db.sqlite3           # Banco de dados SQLite
├── manage.py            # Script de gerenciamento Django
└── README.md            # Esta documentação
```

## 📊 Formato do Arquivo XLS

O arquivo XLS deve conter as seguintes colunas obrigatórias:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `codigo` | String | Código único do projeto |
| `descricao` | String | Descrição do projeto |
| `mercado` | String | Segmento de mercado |
| `contratacao` | Float | Valor de contratação |
| `venda` | Float | Valor de venda |
| `margem` | Float | Valor da margem |
| `margem_percentual` | Float | Margem percentual (%) |

### Exemplo de Arquivo XLS:
```
codigo,descricao,mercado,contratacao,venda,margem,margem_percentual
PRJ001,Projeto AAPP Alpha,AAPP,100000,120000,20000,16.67
PRJ002,Projeto Sanidad Beta,Sanidad,80000,95000,15000,15.79
```

## 🎨 Design e UX

### Tema Visual
- **Cores Principais**: Gradiente azul-roxo (#667eea → #764ba2)
- **Tipografia**: Inter (sans-serif moderna)
- **Estilo**: Minimalista com elementos glassmorphism
- **Animações**: Transições suaves e hover effects

### Componentes
- **Cards**: Design moderno com sombras e hover effects
- **Botões**: Gradientes e animações de elevação
- **Navegação**: Navbar responsiva com ícones
- **Formulários**: Campos com validação visual

### Responsividade
- **Mobile-First**: Design otimizado para dispositivos móveis
- **Breakpoints**: Bootstrap 5 (sm, md, lg, xl)
- **Grid System**: Flexível e adaptável

## 🔧 Desenvolvimento

### Comandos Úteis

```bash
# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic

# Executar testes
python manage.py test

# Verificar migrações
python manage.py showmigrations
```

### Próximos Passos

1. **Implementar API REST**: Para integração com outros sistemas
2. **Adicionar Gráficos**: Charts.js para visualizações avançadas
3. **Autenticação**: Sistema de login e permissões
4. **Filtros Avançados**: Pesquisa e filtros no dashboard
5. **Exportação**: Geração de relatórios em PDF/Excel
6. **Notificações**: Sistema de alertas e notificações

## 📝 Notas de Desenvolvimento

- O dashboard atualmente mostra dados mockados
- O processamento XLS está implementado mas pode ser expandido
- A validação de dados pode ser aprimorada conforme necessidades específicas
- Considerar implementação de cache para melhor performance

## 📄 Licença

Este projeto é propriedade da Análise Indra. Todos os direitos reservados.

## 👥 Contato

Para dúvidas ou sugestões, entre em contato com a equipe de desenvolvimento.