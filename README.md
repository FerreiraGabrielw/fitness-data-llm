# fitness-data-api-llm
Hevy API + Nutrition Data + LLM
Teste
--

# 📌 Roadmap E2E — *fitness-data-platform*

> **Objetivo:** Construir uma plataforma de dados ponta a ponta para análise de treino e dieta, com ingestão histórica via CSV, ingestão incremental via API, banco relacional, análises, automação e relatórios com LLM na AWS.

---

## 🔹 FASE 0 — Preparação (agora)

### ✅ Congelar o dataset tratado

---

## 🔹 FASE 1 — Modelagem de Dados (engenharia)

### 🎯 Objetivo

Transformar um CSV achatado em um **modelo relacional escalável**, compatível com API futura.

### 1.1 Definir entidades principais

* Workout
* Exercise
* Set
* Cardio (ou exercício com tempo/distância)
* Calendar (dimensão de tempo)

### 1.2 Definir granularidade de cada tabela

* Qual tabela é por treino?
* Qual é por exercício?
* Qual é por série?

### 1.3 Definir chaves

* Primary Keys
* Foreign Keys
* Natural vs Surrogate Keys

### 1.4 Criar diagrama lógico (ERD)

* Mesmo que simples (draw.io / dbdiagram)
* Esse diagrama vira **documentação central**

---

## 🔹 FASE 2 — Banco de Dados (AWS)

### 🎯 Objetivo

Criar um banco PostgreSQL produtivo e barato.

### 2.1 Criar RDS PostgreSQL (Free Tier)

* Região: us-east-1
* db.t3.micro
* Storage mínimo
* Security Group restrito

### 2.2 Criar schema no banco

* Criar tabelas conforme modelagem
* Criar índices essenciais
* Garantir integridade referencial

📌 **Checkpoint:** banco pronto e acessível

---

## 🔹 FASE 3 — Pipeline de Ingestão (ETL)

### 🎯 Objetivo

Automatizar ingestão do CSV e preparar para API futura.

### 3.1 Ingestão histórica (CSV)

* Python
* pandas → SQLAlchemy
* Inserção em ordem correta (dimensões → fatos)

### 3.2 Validações no pipeline

* Tipagem
* Null checks
* Constraints (FK)

### 3.3 Separar camadas

* Raw → Cleaned → Enriched (conceitualmente)
* Banco guarda **cleaned**

📌 **Checkpoint:** dados carregados no banco sem erro

---

## 🔹 FASE 4 — Enriquecimento Analítico

### 🎯 Objetivo

Criar métricas que NÃO existem no dado bruto.

### 4.1 Criar tabelas derivadas ou views

* 1RM
* Volume (tonnage)
* Séries efetivas
* Progressão por exercício

### 4.2 Integrar dados de dieta

* Tabela dieta diária
* Relacionar por data
* Relacionar com treino

### 4.3 Integrar aderência

* Aderência treino
* Aderência dieta

📌 **Checkpoint:** banco analítico pronto

---

## 🔹 FASE 5 — Análises e Visualizações

### 🎯 Objetivo

Gerar insights claros e reproduzíveis.

### 5.1 Queries SQL analíticas

* Progressão por exercício
* Volume semanal
* Relação treino × dieta
* Aderência × resultado

### 5.2 Dashboards (opcional)

* Python (Plotly)
* ou Streamlit
* ou notebook estruturado

📌 **Checkpoint:** análises claras e replicáveis

---

## 🔹 FASE 6 — Automação (Orquestração)

### 🎯 Objetivo

Rodar tudo automaticamente.

### 6.1 Criar jobs

* Ingestão diária (API no futuro)
* Atualização de métricas semanais

### 6.2 Ferramentas

* AWS Lambda **ou**
* Cron + EC2 pequena **ou**
* Prefect / Airflow (se quiser elevar o nível)

📌 **Checkpoint:** pipeline automático

---

## 🔹 FASE 7 — LLM & Relatórios Inteligentes

### 🎯 Objetivo

Gerar relatórios semanais interpretativos.

### 7.1 Coletar métricas da semana

* SQL → dataframe
* Agregações chave

### 7.2 Prompt engineering

* Contexto de treino
* Contexto de dieta
* Comparação com semanas anteriores

### 7.3 Output

* Relatório em texto
* Salvo em S3
* (Opcional) enviado por e-mail

📌 **Checkpoint:** relatório automático gerado por IA

---

## 🔹 FASE 8 — Documentação & Portfólio

### 🎯 Objetivo

Transformar isso em **case profissional**.

### 8.1 README final

* Arquitetura
* Stack
* Decisões técnicas
* Prints de gráficos

### 8.2 Diagrama de arquitetura AWS

* S3
* RDS
* Lambda
* LLM

