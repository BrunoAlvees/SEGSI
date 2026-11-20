# Evidências do M2 (Bruno, opção 2: RADIUS federado)

Capturas de ecrã organizadas para o relatório. Os originais continuam em `Pictures\Screenshots`.

| Pasta | Conteúdo | Passo do enunciado |
|---|---|---|
| `01-ambiente/linux/` | Instalação do Ubuntu Server 22.04 (IP fixo 192.168.56.20, OpenSSH) | Ambiente de teste |
| `01-ambiente/dc/` | Instalação do Windows Server 2019, nome SEGSI-DC, IP 192.168.56.10, Windows Update | Passo 1 |
| `99-problemas-resolvidos/` | Erros encontrados e corrigidos (rede, DNS, arranque, modo NEM) | Opcional: secção de dificuldades |

## Próximas pastas

- `02-dc-promocao/` : promoção a Domain Controller (passo 2)
- `03-freeradius-ad/` : FreeRADIUS ligado ao AD (passo 3)
- `04-gpo-auditoria/` : GPOs de auditoria (passo 4)
- `05-hardening/` : Kerberos sem cifras fracas, LDAP sign and seal, teste do Linux (passo 5)
- `06-utilizadores/` : Isaac e Moses no AD, Sara e Abraham no FreeRADIUS, login no Linux (passo 6)
- `07-matriz-acessos/` : quem entra e quem não entra no Windows e no Linux (passo 7)

## Regra de nomes

`NN-o-que-mostra.png`, por ordem cronológica dentro de cada pasta (ex.: `03-hostname-segsi-dc.png`).
