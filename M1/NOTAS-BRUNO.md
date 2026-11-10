# SEGSI — Assignment 1: Traffic Analysis

Mestrado em Engenharia Informática — Segurança de Sistemas e de Informação (ISEP)

Grupo de 3 elementos. Análise de capturas Wireshark + um exercício individual dos guias PL.

## Regras do enunciado (resumo)
- Cada membro analisa **2 capturas**; nenhuma captura é analisada por mais do que um membro (3 membros = 6 capturas).
- Para cada captura identificar: (a) intervenientes; (b) protocolo principal; (c) operações do protocolo (quem inicia/responde, características, dados); (d) problemas de segurança e mitigações; (e) [opcional] outras considerações.
- Máx. **20 páginas por aluno** (sem anexos nem referências).
- Cada aluno anexa **individualmente 1 exercício** dos guias PL atribuído.
- Submissão: 1 aluno, PDF no Moodle. Nome: `SIGLAPROF_nº1_nº2_nº3.PDF`.

## Divisão das capturas

| Captura | Protocolo | Intervenientes | Responsável |
|---|---|---|---|
| cap1.pcapng | LDAP (simple bind) | 192.168.170.130 → .132 (AD `segsi_domain.local`) | **Bruno** ✅ |
| cap2.cap | POP3 | 192.168.2.100 → 64.246.26.20 | _em aberto_ |
| cap3.cap | FTP | 192.168.2.101 → .100 | _em aberto_ |
| cap4.cap | Telnet | 192.168.251.1 → .11 | _em aberto_ |
| cap5.pcap | RADIUS | pfSense .135 → .131 | _em aberto_ |
| cap6.pcap | SQL Slammer (UDP/1434) | 218.232.95.60 → 192.168.1.4 | **Bruno** ✅ |

> A Liane e a Leonor escolhem 2 cada uma das capturas em aberto (temas diferentes recomendado).

## Exercícios individuais (guias PL)

| Aluno | Exercício |
|---|---|
| Bruno | **PL01 — Ex. 4** (NTLM LDAP) |
| Liane | **PL04 — Ex. 2** |
| Leonor | **PL03 — Ex. 1** |

## Estrutura do repositório
```
SEGSI/
├── capturas-SEGSI/            # as 6 capturas do trabalho
├── analises/            # análise de cada captura, por aluno
│   ├── bruno/           # cap1, cap6
│   ├── liane/
│   └── leonor/
├── exercicios/          # exercício individual de cada aluno
│   ├── bruno/           # PL01 Ex4 + NTLM_LDAP.pcapng
│   ├── liane/
│   └── leonor/
├── relatorio/           # relatório final (montagem para PDF)
└── recursos/            # imagens, screenshots, notas partilhadas
```
