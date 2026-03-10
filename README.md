# Análise Indra

Sistema web profissional para análise de projetos desenvolvido com Django, apresentando uma interface moderna e responsiva para upload e visualização de dados de projetos.

## 🚀 Características

- **Upload de Arquivos XLS/XLSX**: Interface intuitiva para upload e processamento de arquivos Excel
- **Dashboard Analítico Vue.js**: Visualização de dados moderna com 3 abas principais (AAPP, Sanidad, Consolidado)
- **Componentes Reativos**: Interface construída com Vue.js 3 + Pinia para experiência fluida
- **Filtros e Ordenação**: Sistema avançado de filtros por margem e mercado com ordenação dinâmica
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
- **Frontend**: Vue.js 3 + Pinia, Bootstrap 5, HTML5, CSS3, JavaScript
- **Build Tool**: Vite (desenvolvimento), Webpack (produção)
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

3. **Instale as dependências Python**:
   ```bash
   pip install django pandas openpyxl
   ```

4. **Instale as dependências Node.js**:
   ```bash
   npm install
   ```

5. **Execute as migrações**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Inicie o servidor**:
   ```bash
   # Opção 1: Apenas backend (Django)
   python manage.py runserver

   # Opção 2: Desenvolvimento completo (Django + Vue.js)
   npm run django:dev
   ```

7. **Acesse a aplicação**:
   - Página inicial (Upload): http://localhost:8000/
   - Dashboard: http://localhost:8000/dashboard/

## 📁 Estrutura do Projeto

```
analise-indra/
├── frontend/              # Código fonte Vue.js
│   └── src/
│       ├── components/    # Componentes Vue reutilizáveis
│       │   ├── MetricCard.vue      # Cards métricos
│       │   ├── DashboardTabs.vue   # Sistema de abas
│       │   └── ProjectTable.vue    # Tabela com filtros
│       ├── stores/        # Stores Pinia (gerenciamento de estado)
│       │   ├── dashboard.js        # Estado do dashboard
│       │   └── projectTable.js     # Estado da tabela
│       ├── DashboardApp.vue       # App principal Vue.js
│       ├── main.js        # Configuração Vue + Pinia
│       └── dashboard.js   # Ponto de entrada do dashboard
├── analise_indra/         # Configurações do projeto Django
│   ├── settings.py        # Configurações principais
│   ├── urls.py           # URLs do projeto
│   └── wsgi.py           # Configuração WSGI
├── core/                  # App principal Django
│   ├── migrations/       # Migrações do banco
│   ├── templates/core/   # Templates HTML
│   │   ├── base.html     # Template base
│   │   ├── upload.html   # Página de upload
│   │   └── dashboard.html # Dashboard
│   ├── models.py         # Modelos de dados
│   ├── views.py          # Views e lógica
│   └── urls.py           # URLs do app
├── static/               # Arquivos estáticos Django
│   ├── css/
│   │   └── style.css     # Estilos personalizados
│   ├── js/
│   │   └── main.js       # JavaScript personalizado
│   └── img/              # Imagens (se necessário)
├── media/                # Arquivos de mídia (uploads)
├── db.sqlite3           # Banco de dados SQLite
├── package.json         # Configuração Node.js
├── vite.config.js       # Configuração Vite
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

### Workflow de Desenvolvimento

#### Desenvolvimento Local
1. **Clone e configure o ambiente** (veja seção de instalação)
2. **Desenvolvimento Frontend**: `npm run dev` para hot reload do Vue.js
3. **Desenvolvimento Backend**: `python manage.py runserver` para Django
4. **Desenvolvimento Completo**: `npm run django:dev` para ambos simultaneamente

#### Modificando Componentes Vue.js
- Arquivos em `frontend/src/` são automaticamente compilados
- Use `npm run build:watch` para desenvolvimento contínuo
- Componentes são servidos via Django templates

#### Adicionando Novos Componentes
1. Crie o componente em `frontend/src/components/`
2. Importe no componente pai apropriado
3. Registre no `components` do componente pai
4. Execute `npm run build` para gerar arquivos estáticos

### Comandos Úteis

#### Django (Backend)
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

#### Vue.js (Frontend)
```bash
# Instalar dependências
npm install

# Desenvolvimento (com hot reload)
npm run dev

# Build para produção
npm run build

# Build e watch (para desenvolvimento com Django)
npm run build:watch

# Desenvolvimento completo (Django + Vue.js)
npm run django:dev

# Lint do código
npm run lint
```

## 🎯 Arquitetura Frontend

### Vue.js + Pinia
O frontend foi migrado para **Vue.js 3** com **Pinia** para gerenciamento de estado reativo:

- **Componentes Reutilizáveis**: `MetricCard`, `DashboardTabs`, `ProjectTable`
- **Estado Centralizado**: Stores Pinia para dashboard e tabela
- **Reatividade Automática**: Atualização automática da UI baseada em estado
- **Composition API**: Código mais organizado e reutilizável

### Funcionalidades Vue.js Implementadas
- ✅ **Cards Métricos Reativos**: Atualização automática por categoria
- ✅ **Sistema de Abas**: Navegação fluida entre AAPP, Sanidad, Consolidado
- ✅ **Tabela Interativa**: Filtros por margem e mercado, ordenação por coluna
- ✅ **Cálculos Dinâmicos**: Totais atualizados automaticamente com filtros
- ✅ **Estado Persistente**: Gerenciamento centralizado com Pinia

### Próximos Passos

1. **Implementar API REST**: Para integração com outros sistemas
2. **Adicionar Gráficos**: Charts.js para visualizações avançadas
3. **Autenticação**: Sistema de login e permissões
4. **Testes Unitários**: Cobertura completa para componentes Vue
5. **TypeScript**: Migração gradual para melhor type safety
6. **PWA**: Funcionalidades offline e notificações push
7. **Exportação**: Geração de relatórios em PDF/Excel
8. **Notificações**: Sistema de alertas e notificações

## 📝 Notas de Desenvolvimento

- ✅ **Migração Vue.js Completa**: Frontend migrado para Vue.js 3 + Pinia
- ✅ **Componentes Reutilizáveis**: Arquitetura modular e testável
- ✅ **Estado Reativo**: Gerenciamento moderno com Pinia
- ✅ **Filtros e Ordenação**: Funcionalidades avançadas implementadas
- O processamento XLS está implementado mas pode ser expandido
- A validação de dados pode ser aprimorada conforme necessidades específicas
- Considerar implementação de cache para melhor performance
- Arquivos estáticos precisam de configuração adequada em produção (Nginx/Apache)

## 📄 Licença

Este projeto é propriedade da Análise Indra. Todos os direitos reservados.

## 🔧 Troubleshooting

### Problemas Comuns

#### Vue.js não carrega no dashboard
```bash
# Execute o build do frontend
npm run build

# Colete arquivos estáticos
python manage.py collectstatic --noinput

# Reinicie o servidor Django
python manage.py runserver
```

#### Arquivos estáticos não são servidos em desenvolvimento
- Verifique se `DEBUG = True` no `settings.py`
- Execute `python manage.py collectstatic` após builds
- Para produção, configure um servidor web (Nginx/Apache) para servir arquivos estáticos

#### Erro de dependências Node.js
```bash
# Limpe node_modules e reinstale
rm -rf node_modules package-lock.json
npm install
```

#### Hot reload não funciona
```bash
# Execute em terminais separados
npm run build:watch    # Terminal 1
python manage.py runserver  # Terminal 2
```

## 👥 Contato

Para dúvidas ou sugestões, entre em contato com a equipe de desenvolvimento.