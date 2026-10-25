# CONTEXT_RULES — TaskAnalyzer

## 1. Linguagem e ambiente

- Utilizar Python 3.11 ou superior.
- Utilizar pytest para executar os testes automatizados.
- Não adicionar bibliotecas externas sem necessidade ou autorização.

## 2. Padrões de código

- Utilizar type hints em todas as funções e métodos.
- Seguir as convenções PEP 8.
- Utilizar docstrings no estilo Google.
- Aplicar o princípio da responsabilidade única (SRP).
- Utilizar nomes descritivos para variáveis, funções, classes e métodos.

## 3. Validação e tratamento de erros

- Utilizar exceções específicas para entradas inválidas.
- A exceção de validação definida para o projeto será `TaskValidationError`.
- Apresentar mensagens de erro claras.
- Validar a consistência das datas das tarefas.
- Evitar divisão por zero e resultados incorretos em casos extremos.
- Não ignorar erros silenciosamente.

## 4. Restrições do projeto

- Não persistir dados em arquivos ou bancos de dados.
- Não adicionar funcionalidades que não estejam previstas na especificação ou aprovadas.
- Não inventar regras de negócio quando houver ambiguidades.
- Não alterar assinaturas públicas de funções sem autorização.
- Não modificar os cenários de teste fornecidos pelo professor.
- Não alterar a estrutura de pastas exigida pelo trabalho.

## 5. Testes

- Criar e executar testes automatizados com pytest.
- Cobrir cenários de sucesso, erros de validação e casos extremos.
- Corrigir falhas identificadas pelos testes antes de considerar a implementação concluída.
- Não afirmar que os testes passaram sem executar os testes e verificar o resultado.

## 6. Processo de desenvolvimento

- Desenvolver em etapas pequenas e verificáveis.
- Utilizar Git para registrar as alterações.
- Criar commits com mensagens claras e descritivas.
- Revisar o código e os resultados dos testes antes de concluir cada etapa.
- Solicitar revisão humana antes de considerar uma versão finalizada.

## 7. Ambiguidades

Quando a especificação não definir uma regra necessária, interromper a implementação dessa regra e solicitar esclarecimento. Não presumir critérios de negócio, especialmente para o cálculo da taxa de atraso percentual, enquanto não houver uma definição aprovada.