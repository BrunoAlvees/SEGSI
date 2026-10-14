# SEGSI

Materiais e trabalhos da UC **Segurança de Sistemas e de Informação** (Mestrado em Engenharia Informática, ISEP, 2026/27).

Grupo: Bruno, Leonor, Liane

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `docs/` | Regras de funcionamento/avaliação e enunciado do M1 |
| `docs/teoricas/` | Slides das aulas teóricas (Topic 1–9) |
| `docs/tp/` | Aulas TP (Business Continuity, Disaster Recovery, Security Plan, Risk Management) |
| `docs/exercicios/` | Guias PL01–PL11, PDFs de apoio e capturas dos exercícios |
| `capturas-SEGSI/` | Capturas do trabalho M1 (`cap1`–`cap6`) |

> **Imagem do BitLocker:** o ficheiro `imgWinBitlocker (1)` (~66 MB) não está no repositório.
> Descarregar do Moodle e colocar em `docs/exercicios/` — já está no `.gitignore`.

## Avaliação

- Final = 30% M1 + 30% M2 + 40% M3 (sem exame final)
- Cada momento = 70% documento + 30% discussão individual

## M1 – Análise de tráfego

Cada elemento analisa **2 capturas** diferentes (3 elementos → 6 capturas). Para cada captura:

a. Intervenientes
b. Protocolo principal
c. Operações realizadas (quem inicia, quem responde, dados trocados)
d. Problemas de segurança e mitigação
e. [opcional] Outras considerações

| Captura | Protocolo | Responsável |
|---|---|---|
| cap1 | LDAP | Bruno |
| cap2 | POP3 | Leonor |
| cap3 | FTP | Liane |
| cap4 | Telnet | Liane |
| cap5 | RADIUS | Leonor |
| cap6 | UDP 1434 (SQL Slammer) | Bruno |

### Exercícios individuais atribuídos

| Elemento | Guião | Exercício |
|---|---|---|
| Bruno | PL01 | 4 |
| Leonor | PL03 | 1 |
| Liane | PL04 | 2 |

Cada elemento deve guardar as notas e evidências do seu exercício para o anexo individual do relatório M1.

Entrega:

- Máximo de 20 páginas por aluno, sem contar anexos e referências.
- Cada aluno anexa individualmente um exercício dos guias PL.
- Prazo de entrega: **23 de outubro de 2026** (confirmar a hora limite no Moodle).
- Submetido no Moodle por um só elemento do grupo.
- Nome do ficheiro: `SIGLA-PROF_NUM1_NUM2_NUM3.PDF`
