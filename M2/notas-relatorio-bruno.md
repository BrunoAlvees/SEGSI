# Notas para o relatório do M2 (Bruno, opção 2)

Ideias apontadas durante o trabalho. Não é texto para colar: é para escrever pelas minhas palavras e saber defender na oral.

## Ligação M1 → M2 (observação de 2026-11-20)

| No M1 analisei (atacante) | No M2 construí (administrador) |
|---|---|
| cap1: LDAP simple bind ao AD sem cifra, password visível | Linux (FreeRADIUS/winbind) liga-se ao mesmo tipo de servidor (AD) |
| PL01 ex. 4: desafio NTLM capturado e password crackada com Hashcat | `ntlm_auth` usa NTLM (MSCHAPv2) entre FreeRADIUS e DC |
| cap5: pedidos RADIUS entre NAS e servidor | PAM do Linux envia Access-Request ao FreeRADIUS |

- O hardening do passo 5 responde aos ataques do M1:
  - LDAP sign and seal: o tráfego da cap1 passa a ir assinado e cifrado.
  - Bloquear RC4/DES no Kerberos: dificulta a quebra offline (como fiz com o Hashcat).
- **Evidência a recolher:** captura de tráfego (Wireshark no PC ou `tcpdump` no Linux) **antes e depois** do hardening, para mostrar o conteúdo visível antes e cifrado depois.

## Outras notas

- Passwords iguais para Isaac e Moses: aceitável só em laboratório; numa organização real, "User must change password at next logon".
- Password do RADIUS no PAP: escondida só com MD5(secret + autenticador), por isso o secret tem de ser forte (gerado com `openssl rand -hex 16`).
- Utilizadores locais do FreeRADIUS guardados com hash SHA-512 com salt (`Crypt-Password`), não em texto.
- **Políticas de password desiguais (observação de 2026-11-20):** o AD aplica a política do domínio (recusou a 1.ª password do Isaac); o Ubuntu local é permissivo; o FreeRADIUS (ficheiro `users`) não tem política nenhuma (aceitou `Sara123#`, 8 caracteres). Num modelo federado, cada repositório tem regras diferentes: risco a referir e mitigar (ex.: centralizar todos no AD, ou validar passwords antes de gerar o hash). Comparar com o CIS 1.1.4 (mínimo 14 caracteres), que liga ao meu PL05.
- **Passo 3 (2026-11-20):** Linux juntado ao domínio com Samba/winbind (`net ads join`), `smbd`/`nmbd` desligados (só é preciso o winbind). FreeRADIUS: utilizadores locais pelo `files` + `pap`; quem não está no ficheiro vai para o módulo `ntlm_auth` (PAP) ou `mschap` com `ntlm_auth` (MSCHAPv2), que pergunta ao DC. O FreeRADIUS nunca copia as passwords do AD: pergunta em cada pedido (desativar no AD tem efeito imediato).
- Limitação a referir: o módulo `ntlm_auth` em PAP passa a password por argumento da linha de comandos (`--password=%{User-Password}`), visível momentaneamente na lista de processos do Linux. MSCHAPv2 evita isto mas tem fraquezas conhecidas (crackável offline). Trade-off a discutir.
- Relógio: depois de retomar a VM congelada, o Linux ficou ~90 min adiantado; o Kerberos tolera só 5 min. Acertado com `chronyc makestep` e NTP do DC.
- Dificuldades resolvidas (possível secção): rede da NAT Network, gateway errado no cloud-init, modo NEM do VirtualBox, falta de RAM com 3 VMs, DC a anunciar o IP da placa NAT. Capturas em `evidencias/99-problemas-resolvidos/` e `evidencias/02-dc-promocao/`.
