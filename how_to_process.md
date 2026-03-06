Aba FC contém os dados que precisamos, que contém dados de projetos de TI, baseado em IFRS15.
Linha 36 - Título das colunas
Para cada projeto existem 13 linhas. Essas 13 linhas são assim nomeadas (Conceitos) e vou colocar uma observação para seu entendimento após ":":
    - Carteira Operativa: Saldo de contrato em R$. Após a contratação inicial esse saldo vai diminuindo conforme vai-se dando Ingressos ou Vendas, mês a mês no projeto.
    - Contratación: Valor do contrato assinado com cliente
    - Ingresos: Ou Ingressos ou revenue. É o esforço realizado no projeto que depois virará uma fatura (Facturación)
    - Coste: Custo do mês do projeto
    - Margen: Margem bruta, que é o Ingresso - Coste
    - Margen(%): Margem percentual, que é a Margem dividida pelo Ingresso.
    - Clientes: valor em R$ de que o cliente está devendo, ou seja, foi emitido fatura mas ainda não recebemos (cobro)
    - DPF: Quanto foi ingressado mas ainda não faturado. Todo ingresso teoricamente deve ter uma fatura em algum momento -futuro. Aqui é um ponto de atenção pois o gerente do projeto pode colocar mais ingresso para dar margem mas a -posteriori o cliente não reconhece e não autoriza o faturamento. Isso chama-se DPF fumaça.
    - ALO: Ao contrário do DPF isso é quando é faturado antes de ingressar. Mais raro de acontecer.
    - Existencias: São CAPEX, em R$ utilizado para ramp up de projeto ou quando passa por alguma dificultada
    - Mov. Existencias: São as movimentações de existências, para mais ou para menos. 
    - Facturación: Faturamento do mês
    - Cobros: Cobros realizados, ou seja, os recebimentos em dinheiro das faturas emitidas.

##Mapeamento de colunas:
B - Mercado - Pode ser Administraciones Públicas (AAPP) ou Sanidad (Saúde)
F - Código do projeto
G - Descrição do projeto
Q - Região do país
R - Tipo de solução - Agrupador para melhor análise de diferentes áreas dentro do mercado.
U - Responsável comercial ou KAM
AA - Conceitos. Aqui são os nomes de cada uma das 13 linhas de conceitos de cada projeto
AO:AZ - Este conjunto de colunas refere-se ao planejamento de cada projeto que a empresa faz no ano anterior, é como se espera que cada projeto irá performar em cada linha de conceito. Contratação, vendas, etc.
BB:BM - Este conjunto de colunas refere-se a como o projeto está performando no ano corrente. Se estamos em Março/2026 e já tivemos o fechamento do mês de janeiro e fevereiro, significa que as colunas referente à esses meses são imutáveis. O que mudará é o planejamento dos meses de março à dezembro.


##Outros conceitos
Cada projeto deve ter alguns números que é necessário incluir no modelo.
#Para mes isolado:
- contratacao_mes - o valor realizado de contratação em um determinado mês
- vendas_mes - o valor realizado de vendas / ingresso em um determinado mês
- margem_mes - o valor realizado de margem em um determinado mês
- contratacao_poa_mes - o valor que deveria ter sido realizado de contratação em um determinado mês, conforme o planejamento (POA)
- vendas__poa_mes - o valor que deveria ter sido realizado de ingresso em um determinado mês, conforme o planejamento (POA)
- margem__poa_mes - o valor que deveria ter sido realizado de margem em um determinado mês, conforme o planejamento (POA)


#Para acumulado YTD
- contratacao_ytd - o valor realizado de contratação acumulado desde janeiro até um determinado mês (devemos ter parâmetro para dizer qual mes é o fechado)
- vendas_mes - o valor realizado de ingresso acumulado desde janeiro até um determinado mês (devemos ter parâmetro para dizer qual mes é o fechado)
- margem_mes - o valor realizado de margem acumulado desde janeiro até um determinado mês (devemos ter parâmetro para dizer qual mes é o fechado)
- contratacao_poa_mes - o valor que deveria ter sido realizado de contratação acumulado desde janeiro até um determinado mês (devemos ter parâmetro para dizer qual mes é o fechado) em POA
- vendas__poa_mes - o valor que deveria ter sido realizado de ingresso acumulado desde janeiro até um determinado mês (devemos ter parâmetro para dizer qual mes é o fechado) em POA
- margem__poa_mes - o valor que deveria ter sido realizado de margem acumulado desde janeiro até um determinado mês (devemos ter parâmetro para dizer qual mes é o fechado) em POA

Nossos modelos devem ficar mapeados para que cada projeto tenha seus conceitos do mes, do mes planejado em POA, no acumulado e no acumulado planejado em POA.

