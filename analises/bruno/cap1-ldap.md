# Análise — cap1.pcapng (LDAP)

## a. Intervenientes
- **Cliente:** `192.168.170.130` (porta origem 50442) — quem faz as consultas.
- **Servidor:** `192.168.170.132` (porta 389, LDAP) — Domain Controller / Active Directory do domínio `segsi_domain.local` (hostname `WIN-6LNRNRBKNRO`).
- Tráfego de fundo (não essencial): DNS/UDP e algumas sessões TLS do cliente para IPs externos (`23.47.189.136`, `13.107.213.254` — telemetria Windows), não relacionadas com o LDAP.

## b. Protocolo principal
- **LDAP** (Lightweight Directory Access Protocol) sobre TCP porta **389**, **sem cifra** (sem LDAPS/StartTLS).
- Autenticação por **simple bind** (utilizador + password em texto claro).

## c. Operações do protocolo
Fluxo (cliente `.130` inicia sempre; servidor `.132` responde):

1. **TCP 3-way handshake** (frames 1–3): SYN / SYN-ACK / ACK para a porta 389.
2. **bindRequest(1) simple** — frame 4: autenticação simples com
   - name: `CN=Bob B. Munchies,CN=Users,DC=segsi_domain,DC=local`
   - **password em claro: `!!QAZ22wsx`**
3. **bindResponse(1) success** — frame 5.
4. (Repete bind nas frames 12–13 — nova ligação TCP.)
5. **searchRequest / searchResEntry / searchResDone** — frames 16 em diante:
   - `searchRequest(2) "<ROOT>" baseObject` → leitura do **rootDSE** (naming contexts, capacidades).
   - Consultas ao **Schema** e **Configuration** (`CN=Aggregate,CN=Schema,...`, `CN=Configuration,...`).
   - Enumeração das partições: `DC=ForestDnsZones`, `DC=DomainDnsZones`, `CN=Schema`, etc.
   - `searchRequest(15) "DC=segsi_domain,DC=local" singleLevel` → lista os contentores do domínio (Builtin, Computers, Domain Controllers, Users, System, ...).
   - **`searchRequest(17) "CN=Users,DC=segsi_domain,DC=local" singleLevel`** → **enumera TODOS os utilizadores/grupos** (53 resultados): Administrator, Alice Wonderland, Bob B. Munchies, Neo Matrix, krbtgt, Domain Admins, Enterprise Admins, etc.
6. Cada `searchResDone(n) success` fecha a respetiva pesquisa.

Características: sessão de ~80s, 294 frames no total (39 LDAP), tudo legível em claro.

## d. Problemas de segurança e mitigações
| Problema | Evidência | Mitigação |
|---|---|---|
| **Credenciais em claro** (simple bind) | frame 4: password `!!QAZ22wsx` legível | **LDAPS (636)** ou **StartTLS**; forçar canal cifrado |
| **Sem integridade/confidencialidade** no canal | LDAP porta 389 sem TLS | **LDAP Signing & Sealing** no servidor; desativar binds simples não cifrados |
| **Enumeração completa do diretório** (recon) | searchRequest(17) lista 53 contas | Restringir ACLs de leitura; limitar binds anónimos/não privilegiados; monitorizar queries em massa |
| **Fuga da política de passwords** | frame 271: minPwdLength=7, maxPwdAge=42d, lockoutThreshold=**0** (sem bloqueio!), complexidade on | Cifrar o canal (LDAPS); ativar **account lockout**; aumentar comprimento mínimo |
| **Fuga do Domain SID** | frame 271: `objectSid S-1-5-21-2251112744-3888591931-703240865` | Cifrar o canal; restringir leitura de atributos sensíveis |
| **Autenticação fraca** (bind simples em vez de forte) | bind simple | Preferir **Kerberos** / SASL (GSS-API) para autenticação no AD |

> Nota positiva: **não** foram devolvidos hashes de passwords (`unicodePwd`, `ntPwdHistory`, `supplementalCredentials` ausentes) — o AD não expõe esses atributos numa pesquisa normal. O dano limita-se a credencial em claro + enumeração + política + SID.

## e. Outras considerações
- A password `!!QAZ22wsx` é um padrão de teclado comum ("keyboard walk"), fácil de adivinhar apesar dos símbolos.
- A captura demonstra o valor do LDAP para reconhecimento: um atacante com acesso à rede fica com credenciais válidas **e** o mapa completo de utilizadores/grupos do domínio.

## Verificação do transporte do schema (frames 20–219) — rigor metodológico
- Frame 20: `searchRequest(3)` pede o schema "Aggregate".
- Frames 21–218 (198 frames): apenas **transporte TCP** do schema (segmentos de 1460 bytes), 1 retransmissão (frame 22) inofensiva.
- Frame 219: resposta reagrupada (~220 KB, 152 segmentos) com `attributeTypes`, `objectClasses`, `modifyTimeStamp`.
- **Teste de conteúdo:** isolaram-se os bytes dos frames 21–218 e procuraram-se dados sensíveis (password, utilizadores, IPs, Domain SID). Resultado: **nenhum** — apenas 1780 definições de schema **padrão** (iguais em qualquer AD), sem dados da organização.
- Nota metodológica: um "follow TCP stream" ingénuo dá falso positivo (mistura o login da frame 12 e a lista da frame 283); só isolando os frames corretos se confirma que o schema está limpo.
- **Conclusão:** o schema não acrescenta fugas; as únicas fugas reais são bind em claro (4, 12), enumeração (283/285/286) e política+SID (271).

## Evidências (frames-chave para screenshots)
- Frame 4 — bindRequest simple com name + password em claro.
- Frame 5 — bindResponse success.
- Frame 283/285/286 — searchResEntry(17) com a lista de utilizadores do domínio.
- Filtros úteis: `ldap.bindRequest_element`, `ldap.simple`, `ldap.protocolOp == 3` (searchRequest).
