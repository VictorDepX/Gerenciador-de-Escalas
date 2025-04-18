# Calendário de Escalas - Protótipo

## Descrição

Este é um protótipo de um sistema de gerenciamento de escalas de funcionários, desenvolvido para permitir a organização de escalas de forma simples e visualmente agradável. O projeto é uma aplicação web interativa com suporte a temas claros e escuros, e está sendo desenvolvido com diversas tecnologias modernas para garantir flexibilidade e usabilidade.

### Funcionalidades principais:

- **Calendário Interativo**: Visualização do calendário do mês com diferenciação entre dias úteis, fins de semana e feriados.
- **Gerenciamento de Escalas**: Atribuição de funcionários a datas específicas de forma intuitiva.
- **Troca de Tema**: Alternância entre temas claro e escuro para uma melhor experiência de usuário.
- **Responsividade**: O sistema é responsivo, ajustando-se automaticamente a diferentes tamanhos de tela, incluindo dispositivos móveis.
- **Geração de Relatórios**: Geração de relatórios em PDF para exportação das escalas, utilizando o **ReportLab**.

## Tecnologias Utilizadas

Este projeto utiliza uma série de tecnologias e bibliotecas modernas para fornecer uma interface limpa e eficiente. As principais tecnologias incluem:

- **HTML5**: Estrutura básica da página.
- **CSS3**: Estilo e design da página, com foco em um layout minimalista e colorido.
- **JavaScript**: Lógica de interatividade e manipulação do calendário.
- **Python**: Linguagem de backend para gerenciamento de dados e geração de relatórios.
- **Flask**: Framework web em Python para criação de rotas e APIs.
- **Bootstrap**: Biblioteca front-end para design responsivo e componentes prontos para uso.
- **ReportLab**: Biblioteca Python para geração de relatórios PDF a partir dos dados de escalas.
- **Fontes**: Utilização da fonte **Arial** para garantir uma aparência limpa e legível.

## Objetivo do Projeto

Este projeto tem como objetivo criar uma solução simples e eficiente para o gerenciamento de escalas de funcionários. Com o uso de tecnologias modernas, o sistema oferece uma interface intuitiva para organização das escalas, incluindo um calendário interativo e recursos para gerar relatórios.

Este protótipo está em fase de desenvolvimento e planeja expandir suas funcionalidades, como:

- **Persistência de Dados**: Implementação de armazenamento de dados em banco de dados.
- **Autenticação e Controle de Acesso**: Inclusão de funcionalidade de login e gestão de permissões de usuário.
- **Melhorias na Visualização**: Inclusão de opções para diferentes visualizações de calendário (semanal, mensal, etc.).
- **Exportação Avançada**: Geração de relatórios em diferentes formatos (PDF, CSV).

## Como Executar

### Pré-requisitos

Para rodar o projeto localmente, você precisa ter os seguintes requisitos instalados:

- **Python 3.x**
- **Flask**: Para criar o backend.
- **ReportLab**: Para geração de relatórios PDF.
- **Bootstrap**: Para o layout responsivo.
- **Bibliotecas adicionais**: Consulte o arquivo `requirements.txt` para instalar as dependências.

### Instalação

1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/calendario-de-escalas.git
```

2. Navegue até o diretório do projeto:

```bash
cd calendario-de-escalas
```

3. Crie um ambiente virtual Python e instale as dependências:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows, use venv\Scripts\activate
pip install -r requirements.txt
```

4. Execute o servidor Flask:

```bash
python app.py
```

5. Abra o navegador e acesse:

 http://127.0.0.1:5000

O sistema estará disponível no endereço especificado.



