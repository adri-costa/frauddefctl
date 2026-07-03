# frauddefctl

Terminal administrativo para **Google Cloud Fraud Defense / reCAPTCHA Enterprise**.

O objetivo é centralizar tarefas rotineiras de Application Security:

- gestão de chaves de site reCAPTCHA / Fraud Defense;
- gestão de API Keys da GCP usadas pela integração;
- inventário e governança;
- métricas e indicador SAFE x RISK;
- identificação de chaves obsoletas;
- busca por nome, ID, URL, domínio e IP;
- troubleshooting de integração;
- troubleshooting por Assessment ID via logs;
- annotations;
- relatórios CSV, JSON e Markdown;
- modo interativo estilo ATM e modo pipeline.

> Nome definido: `frauddefctl`, para evitar confusão com time de fraude e manter foco em Fraud Defense control.

---

## Status

Este é o **esqueleto inicial navegável** do projeto.

Já inclui:

- CLI com `typer`;
- menu interativo com `rich`;
- config YAML com múltiplos projetos;
- parser de múltiplos valores;
- classificação SAFE/RISK com threshold padrão `0.5`;
- exportador CSV/JSON/Markdown;
- relatório SAFE x RISK a partir de CSV;
- stubs dos adapters Google Cloud;
- testes unitários básicos.

Ainda não inclui chamadas reais para GCP. Elas entram na próxima fase pelos adapters:

- `RecaptchaAdapter`;
- `ApiKeysAdapter`;
- `CloudLoggingAdapter`;
- `BigQueryAdapter`.

---

## Instalação local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Com integrações Google Cloud, usar:

```bash
pip install -e '.[gcp]'
```

---

## Autenticação prevista

Humano local:

```bash
gcloud auth application-default login
```

Pipeline:

- service account;
- Workload Identity;
- service account impersonation.

A ferramenta deve usar ADC para manter o mesmo código no modo humano e pipeline.

---

## Configuração

Arquivo exemplo:

```bash
config/config.example.yaml
```

Validar config:

```bash
frauddefctl config validate --config config/config.example.yaml
```

---

## Menu interativo

```bash
frauddefctl --interactive
```

Padrão de navegação em todo submenu:

```text
[0] Voltar
[99] Menu principal
[q] Sair
```

---

## Parser de múltiplos valores

Aceita:

- vírgula;
- ponto e vírgula;
- tab;
- espaço;
- quebra de linha;
- arquivo `.txt`.

Exemplo:

```bash
frauddefctl utils parse-values --values "id1,id2; id3	id4"
```

---

## Classificação SAFE x RISK

Regra padrão:

```text
SAFE    = score >= 0.5
RISK    = score <  0.5
UNKNOWN = score ausente
```

Exemplo:

```bash
frauddefctl risk classify --score 0.5
frauddefctl risk classify --score 0.49
```

---

## Relatório SAFE x RISK

Exemplo de input:

```bash
examples/assessment_sample.csv
```

Executar:

```bash
frauddefctl report safe-risk \
  --input examples/assessment_sample.csv \
  --threshold 0.5 \
  --formats csv,json,markdown
```

Saídas:

```text
reports/metrics/safe_risk_summary_YYYYMMDD_HHMMSS.csv
reports/metrics/safe_risk_summary_YYYYMMDD_HHMMSS.json
reports/metrics/safe_risk_summary_YYYYMMDD_HHMMSS.md
```

---

## Módulos planejados

```text
[1] Ambiente e autenticação
[2] Chaves de site reCAPTCHA / Fraud Defense
[3] Chaves de API Google Cloud
[4] Inventário e governança
[5] Métricas e uso
[6] Troubleshooting de integração
[7] Troubleshooting de Assessment ID
[8] Annotations
[9] Relatórios e evidências
[10] Drift Detection
```

---

## Guardrails obrigatórios

- SDK/API-first.
- `gcloud` como fallback operacional.
- ADC como padrão de autenticação.
- Dry-run obrigatório em operações destrutivas.
- Remoção em produção exige `force` e justificativa.
- Mascaramento de dados sensíveis por padrão.
- Auditoria própria em JSONL.
- Service accounts separadas para read-only e admin.
- Assessment ID retroativo depende de logs da aplicação, Cloud Logging ou BigQuery.

---

## Próximas fases

### MVP 1 — Fundação read-only

- Implementar listagem real de reCAPTCHA keys.
- Implementar listagem real de API keys.
- Exportar inventário consolidado.
- Implementar busca por nome, ID, domínio, URL e IP.

### MVP 2 — Governança e métricas

- Implementar `GetMetrics`.
- Calcular SAFE x RISK por chave.
- Identificar chaves obsoletas.
- Detectar API keys sem restrição.
- Detectar labels fora do padrão.

### MVP 3 — Operações administrativas

- Criar/editar/remover site keys.
- Criar/editar/rotacionar API keys.
- Gerenciar IP overrides.
- Drift detection.

### MVP 4 — Troubleshooting avançado

- Validar integração com token real.
- Investigar Assessment IDs via Cloud Logging/BigQuery.
- Annotation individual e em lote.
- Pacote Google Support.
