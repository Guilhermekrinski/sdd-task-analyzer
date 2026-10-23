# Especificação — TaskAnalyzer

## 1. Objetivo

O TaskAnalyzer é uma aplicação desenvolvida em Python para analisar tarefas e apresentar métricas relacionadas à produtividade e à conclusão das atividades.

## 2. Estrutura de uma tarefa

Cada tarefa deve conter os seguintes campos:

- `id`: identificador da tarefa.
- `titulo`: título ou descrição da tarefa.
- `prioridade`: prioridade atribuída à tarefa.
- `data_criacao`: data e hora de criação da tarefa.
- `data_conclusao`: data e hora de conclusão, quando aplicável.
- `status`: situação atual da tarefa.

## 3. Métricas esperadas

O sistema deverá calcular:

- Total de tarefas cadastradas.
- Total de tarefas concluídas.
- Total de tarefas pendentes.
- Tempo médio de conclusão em horas.
- Tempo médio de conclusão agrupado por prioridade.
- Taxa de atraso percentual.

Somente tarefas concluídas deverão ser consideradas no cálculo das métricas de conclusão.

## 4. Validações

O sistema deverá validar os dados recebidos e sua consistência lógica.

A data de conclusão não poderá ser anterior à data de criação. Entradas inválidas deverão gerar exceções específicas, acompanhadas de mensagens claras.

O sistema também deverá tratar entradas vazias e situações em que não existam tarefas concluídas, evitando divisão por zero e erros não tratados.

## 5. Regras de implementação

- Utilizar Python 3.11 ou superior.
- Utilizar anotações de tipo nas funções e métodos.
- Seguir os princípios de responsabilidade única e o padrão PEP 8.
- Documentar funções e métodos com docstrings no estilo Google.
- Utilizar tratamento de exceções específico.
- Não salvar dados em arquivos ou bancos de dados.
- Não adicionar funcionalidades ou regras de negócio que não estejam especificadas ou aprovadas.

## 6. Testes

O sistema deverá possuir testes automatizados com pytest para verificar os cálculos das métricas, as validações de entrada e os casos extremos.

Os testes deverão contemplar cenários de sucesso e de erro.

## 7. Ponto que precisa ser esclarecido

A taxa de atraso percentual está prevista entre as métricas, mas a estrutura de tarefa definida nesta especificação não apresenta um campo de prazo. Portanto, a regra para determinar quando uma tarefa está atrasada precisa ser esclarecida antes da implementação. Nenhum critério de atraso deverá ser presumido sem aprovação.

## 8. Regra adotada para a taxa de atraso

Para viabilizar o cálculo da taxa de atraso, será utilizado o campo adicional `data_prazo`, contendo a data e hora limite para conclusão da tarefa.

Uma tarefa será considerada atrasada quando estiver concluída e sua `data_conclusao` for posterior à `data_prazo`.

A taxa de atraso percentual será calculada dividindo o número de tarefas concluídas após o prazo pelo total de tarefas concluídas, multiplicando o resultado por 100.

Quando não houver tarefas concluídas, a taxa de atraso será 0.0.

Esta regra é uma decisão proposta para o projeto e deverá ser validada com o professor, caso o enunciado original estabeleça critérios diferentes.
