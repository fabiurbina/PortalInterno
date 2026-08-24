# Portal Viesano

## Visão Geral

O Portal Viesano é um sistema interno desenvolvido como complemento e apoio ao sistema Omie, com o objetivo de ampliar a visualização, análise e acompanhamento dos processos operacionais da empresa.

O portal foi desenvolvido para transformar os dados disponíveis no Omie em informações mais claras, organizadas e direcionadas às necessidades operacionais e gerenciais da Viesano.

Entre suas principais funcionalidades estão o acompanhamento das etapas dos pedidos, relatórios de acompanhamento, relatórios gerais, dashboards, MRP, padronização das Ordens de Produção (OPs), padronização de fichas logísticas e extração rápida e resumida de informações.

O sistema também surgiu para suprir algumas limitações encontradas no acompanhamento visual e na extração de informações do Omie. Enquanto o Omie disponibiliza o acompanhamento dos processos principalmente através do Kanban, o Portal Viesano busca traduzir esses dados em uma visão mais objetiva, permitindo identificar de forma clara em qual etapa do processo cada pedido se encontra.

Além disso, o portal amplia as possibilidades de consulta e extração de dados, permitindo que informações operacionais sejam apresentadas de forma mais rápida, resumida e adequada às necessidades dos diferentes setores da empresa.


## Objetivo

O objetivo do Portal Viesano é centralizar e facilitar o acesso às informações operacionais da empresa, transformando os dados provenientes do Omie e de outras fontes em informações mais claras, rápidas e úteis para acompanhamento e tomada de decisão.

O portal busca proporcionar uma visão integrada dos processos, permitindo acompanhar pedidos, produção e demais etapas operacionais de forma objetiva, além de disponibilizar relatórios, dashboards e ferramentas de análise que apoiem as atividades dos diferentes setores.

Entre os principais objetivos estão:

- Melhorar a visualização e o acompanhamento dos pedidos em suas diferentes etapas;
- Facilitar a identificação da situação atual de cada pedido;
- Centralizar informações operacionais em um único ambiente;
- Agilizar a extração e consulta de relatórios;
- Disponibilizar informações resumidas para acompanhamento e tomada de decisão;
- Apoiar o planejamento das necessidades de materiais através do MRP;
- Padronizar informações utilizadas nas Ordens de Produção;
- Padronizar informações utilizadas nas fichas logísticas;
- Reduzir a necessidade de consultas e tratamentos manuais de dados;
- Ampliar as possibilidades de análise sobre os dados disponíveis no ambiente operacional.

## Escopo

O Portal Viesano contempla funcionalidades voltadas ao acompanhamento, análise e disponibilização de informações dos processos operacionais da empresa.

Atualmente, fazem parte do escopo do portal:

- **Acompanhamento de pedidos:** visualização da situação e da etapa em que cada pedido se encontra no processo operacional;
- **Relatórios operacionais:** consulta e extração de informações de forma rápida, organizada e resumida;
- **Dashboards:** apresentação visual de indicadores e informações relevantes para acompanhamento dos processos;
- **MRP:** apoio ao planejamento das necessidades de materiais e produção;
- **Ordens de Produção:** padronização e disponibilização das informações relacionadas às OPs;
- **Fichas logísticas:** padronização das informações utilizadas nos processos logísticos;
- **Acompanhamento da produção:** disponibilização de informações relacionadas às etapas e ao andamento dos processos produtivos;
- **Integração de dados:** utilização de informações provenientes do Omie e de outras fontes de dados utilizadas pela empresa;
- **Consultas operacionais:** acesso rápido a informações que anteriormente dependiam de consultas ou extrações manuais.

O escopo do portal é evolutivo e pode ser ampliado conforme novas necessidades operacionais e gerenciais sejam identificadas.


## Tecnologias

O Portal Viesano foi desenvolvido utilizando tecnologias voltadas para desenvolvimento web, processamento de dados, armazenamento e integração com sistemas externos.

### Backend

- **Python:** linguagem principal utilizada no desenvolvimento da aplicação e dos processos de tratamento de dados.
- **Django:** framework utilizado na construção do portal e gerenciamento das aplicações web.

### Banco de Dados

- **MySQL:** utilizado para armazenamento e consulta dos dados utilizados pelo portal.
- **Amazon RDS:** serviço utilizado para hospedagem do banco de dados em ambiente AWS.

### Frontend

- **HTML:** estrutura das páginas do portal.
- **CSS:** estilização e organização visual das interfaces.
- **JavaScript:** utilizado nas funcionalidades e interações necessárias nas páginas.

### Integrações e Dados

- **Omie:** sistema utilizado como uma das principais fontes de dados operacionais.
- **APIs:** utilizadas para comunicação e integração entre sistemas.
- **SQL:** utilizado para consultas, tratamento e organização dos dados.

### Infraestrutura

- **Amazon Web Services (AWS):** ambiente utilizado para hospedagem e infraestrutura da aplicação.
- **Amazon EC2:** ambiente utilizado para execução da aplicação.
- **Amazon RDS:** ambiente utilizado para hospedagem do banco de dados MySQL.


## Arquitetura

O Portal Viesano está estruturado em uma arquitetura baseada em aplicação web, na qual o Django atua como camada responsável pelo processamento das requisições, aplicação das regras de negócio e disponibilização das informações para os usuários.

De forma simplificada, o fluxo de dados pode ser representado da seguinte maneira:

```text
┌─────────────────────┐
│        OMIE         │
│  Sistema de origem  │
└──────────┬──────────┘
           │
           │ API / Dados
           ▼
┌─────────────────────┐
│ Processamento /     │
│ Integrações         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      MySQL / RDS    │
│   Banco de Dados    │
└──────────┬──────────┘
           │
           │ Consultas
           ▼
┌─────────────────────┐
│       Django        │
│   Portal Viesano    │
└──────────┬──────────┘
           │
           │ HTTP / HTTPS
           ▼
┌─────────────────────┐
│       Usuários      │
│ Internos / Operação │
└─────────────────────┘
```

## Estrutura e organização do projeto

A estrutura do Portal Viesano foi organizada de forma modular, separando as configurações do projeto, as funcionalidades da aplicação, as integrações externas, os arquivos de apresentação e a documentação.

A organização principal do projeto é apresentada abaixo:

```text
Portal Viesano/
│
├── portal/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── pedidos/
│   ├── views.py
│   ├── urls.py
│   ├── models.py
│   ├── mysql_service.py
│   ├── omie_service.py
│   ├── status_service.py
│   ├── preparar_dados.py
│   ├── email_service.py
│   ├── email_ses.py
│   ├── groq_service.py
│   │
│   ├── migrations/
│   │
│   ├── sql/
│   │   └── Posicao_estoque.sql
│   │
│   ├── static/
│   │   ├── css/
│   │   └── img/
│   │
│   ├── templates/
│   │   ├── páginas do portal
│   │   ├── emails/
│   │   └── relatorios/
│   │
│   └── templatetags/
│
├── integracoes/
│   └── omie.py
│
├── docs/
│   └── portal/
│       └── README.md
│
├── Manual/
│
├── manage.py
├── Portal.py
├── requirements.txt
└── .gitignore
```