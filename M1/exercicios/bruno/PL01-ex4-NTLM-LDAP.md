# PL01 — Exercício 4: NTLM LDAP (Bruno)

**Captura:** `NTLM_LDAP.pcapng`
**Intervenientes:** Cliente `10.0.0.20` (PC) ↔ Servidor LDAP/AD `10.0.0.10` (porta 389)

---

## 1. What is the user logging in?

O utilizador autenticado é **`lab.lan\admin`** (domínio `lab.lan`, user `admin`, host `PC`).

Visível na frame 7 (`bindRequest(6) NTLMSSP_AUTH`), campo *User name*.
> Nota: no painel "Info" aparece `adminsasl` porque o Wireshark concatena o user `admin` com o mecanismo SASL; o username real é `admin`.

## 2. Explain the different interactions of the protocol

A autenticação é um **SASL bind com NTLMSSP** sobre LDAP. Sequência:

| Frames | Operação | Descrição |
|---|---|---|
| 1–4 | LDAP `searchRequest`/`searchResEntry` ao `<ROOT>` (rootDSE) | Cliente sonda o diretório (capacidades, naming contexts) antes de autenticar |
| 5 | `bindRequest NTLMSSP_NEGOTIATE` | **Msg 1 (NEGOTIATE):** cliente anuncia que quer NTLM e as flags que suporta |
| 6 | `bindResponse saslBindInProgress NTLMSSP_CHALLENGE` | **Msg 2 (CHALLENGE):** servidor envia o *Server Challenge* (nonce de 8 bytes) |
| 7 | `bindRequest NTLMSSP_AUTH` | **Msg 3 (AUTHENTICATE):** cliente envia domínio, username, host e a resposta calculada a partir do hash da password + challenge |
| 8 | `bindResponse success` | Servidor valida e aceita a autenticação |
| 9+ | `SASL GSS-API Privacy: payload` | Sessão estabelecida; tráfego LDAP seguinte vai **cifrado** (sealing) |

Princípio challenge-response: a password **nunca** é enviada; o cliente prova que a conhece respondendo ao desafio. O servidor repete o cálculo e compara.

## 3. Extract all pertinent data and crack the password

**Tipo:** NetNTLMv1 com **Extended Session Security (ESS / NTLM2 Session Response)** — a NT Response tem só 24 bytes e a flag *Negotiate Extended Session Security* está ativa. A LM Response contém o *client challenge* (8 bytes) seguido de zeros.

**Dados extraídos:**
| Campo | Valor | Frame |
|---|---|---|
| Server Challenge | `3ce65bea9b2dc110` | 6 |
| Client Challenge | `1e28d3cbd400f676` (início da LM Resp) | 7 |
| LM Response | `1e28d3cbd400f67600000000000000000000000000000000` | 7 |
| NT Response | `3a5c082cc01eeedefa7085caaa0d66b10088220ccb6881ea` | 7 |

**Hash (formato NetNTLMv1, John/Hashcat):**
```
admin::lab.lan:1e28d3cbd400f67600000000000000000000000000000000:3a5c082cc01eeedefa7085caaa0d66b10088220ccb6881ea:3ce65bea9b2dc110
```

**Cracking:**
- Hashcat: `hashcat -m 5500 ntlmv1.hash rockyou.txt`
- John: `john --format=netntlm ntlmv1.hash`

**Resultado: password = `admin`**

Com ESS, o challenge efetivo = `MD5(ServerChallenge ‖ ClientChallenge)[:8]` = `02bc628340352790`. A NT Response = DESL(MD4(UTF-16LE(password)), challenge). Testando candidatas comuns, `admin` reproduz exatamente a NT Response capturada.

### Conceito: o que é o Server Challenge (`3ce65bea9b2dc110`)
É um **nonce** (número aleatório de 8 bytes, usado uma só vez) gerado pelo servidor na frame 6. Serve para o cliente **provar que conhece a password sem a enviar**: o cliente calcula `NTLM Response = f(hash_password, challenge)` e o servidor repete a conta. Muda em cada login → evita *replay* de respostas antigas. Como vai em claro (bind sem cifra), permite ataque offline de dicionário.

Com ESS, o challenge efetivo = `MD5(ServerChallenge ‖ ClientChallenge)[:8]` = `MD5(3ce65bea9b2dc110 ‖ 1e28d3cbd400f676)[:8]` = `02bc628340352790`.

### Comentário sobre a resiliência (segurança)
- A password **nunca circulou em claro**, mas o par *challenge + response* capturado permite **cracking offline** por dicionário/força-bruta.
- **NTLMv1** é especialmente fraco: assenta em DES (chaves de 56 bits), vulnerável mesmo a quebra por hardware dedicado independentemente da força da password.
- Password `admin` é trivial (igual ao username) → quebrada instantaneamente.
- **Mitigações:** desativar NTLMv1 (forçar NTLMv2/Kerberos), impor LDAP signing & sealing / LDAPS, políticas de passwords fortes, e preferir Kerberos para autenticação no AD.
