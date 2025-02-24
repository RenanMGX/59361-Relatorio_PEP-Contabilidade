# Relatório de PEP - Extração de Dados SAP

Este repositório contém um script Python para extrair dados do SAP e gerar relatórios consolidando informações do processo PEP.

## Visão Geral
O script principal (`main.py`) executa as seguintes etapas:
- Carrega parâmetros a partir de um arquivo JSON (`args.json`).
- Realiza a extração de dados para diferentes divisões, conforme especificado.
- Gera um arquivo Excel com os relatórios e compacta os arquivos em um ZIP.
- Registra mensagens informativas durante o processo utilizando o módulo `informativo`.

## Requisitos
- Python 3.8 ou superior.
- Dependências internas e módulos do SAP devidamente configurados.
- Sistema operacional com suporte ao locale `pt_BR.UTF-8`.

## Instalação
1. Clone o repositório para o diretório desejado.
2. Instale as dependências necessárias de acordo com os módulos utilizados no projeto.
3. Configure o arquivo `args.json` com os parâmetros:
   - `divisao`: Lista de divisões a serem processadas.
   - `date`: Data inicial no formato ISO.
   - `acumulado`: Boolean, definindo se a extração será acumulada.
   - `final_date`: Data final (opcional).

## Uso
Execute o script principal:
