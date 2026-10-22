# Registo de figuras do relatório

## Captura 1 (LDAP) — Bruno

| Fig. | Ponto | Ficheiro | Legenda |
|---|---|---|---|
| 1 | a. Intervenientes | `cap1-intervenientes.svg` | Intervenientes da captura 1. O cliente (192.168.170.130) comunica com o servidor Active Directory (192.168.170.132) por LDAP sobre TCP/389, sem cifra. A vermelho os pedidos do cliente (bind e search), a azul as respostas do servidor. |
| 2 | b. Protocolo principal | `cap1-protocol-hierarchy-anotada.svg` | Hierarquia de protocolos da captura (Statistics, Protocol Hierarchy). O LDAP corresponde a apenas 13,3% dos pacotes mas a 92,3% dos bytes, confirmando ser o protocolo principal. Os restantes (TLS, SSDP, NBNS, ARP) são tráfego de fundo. |
| 3 | c. Operações | `cap1-diagrama-sequencia.svg` | Diagrama de sequência das operações da captura 1, em 4 fases (ligação, autenticação, consultas, encerramento). A vermelho os pedidos do cliente, a azul as respostas do servidor; indicam-se os números de frame como evidência. |
| 4 | 2.3.1 Estabelecimento da ligação | `cap1-handshake-anotada.svg` | Handshake TCP (frames 1 a 3): SYN, SYN-ACK e ACK dirigidos à porta 389. A frame 4 marca o fim do handshake e o início do bind. A comunicação usa a porta 389 (sem cifra), não a 636 (LDAPS). |
| 5 | 2.3.2 Autenticação (bind) | `cap1-fig5-bind.png` (versão anotada pelo Bruno) | Detalhe do bindRequest (frame 4). O campo name identifica o utilizador (Bob B. Munchies); authentication: simple indica bind simples sem cifra; o campo simple expõe a password em texto claro (!!QAZ22wsx). |
| 6 | 2.3.3 Consultas (política/SID) | `cap1-fig6-politica-final.png` | Resposta ao pedido de todos os atributos do domínio (frame 271). Destacam-se lockoutThreshold=0 (bloqueio de conta desativado), minPwdLength=7 e o objectSid (Domain SID), todos em texto claro. |
| 7 | 2.3.3 Consultas (utilizadores) | `cap1-fig7-utilizadores-anotada.svg` | Enumeração de utilizadores (frame 283): resposta ao searchRequest singleLevel sobre CN=Users. O servidor devolve a lista de 53 contas e grupos do domínio (Administrator, Bob B. Munchies, Domain Admins, etc.), obtida por uma conta normal. |

## Captura 6 (SQL Slammer) — Bruno
| Fig. | Ponto | Ficheiro | Legenda |
|---|---|---|---|
| 1 (Word 13) | 7.1 Intervenientes | `cap6-intervenientes.svg` | Intervenientes da captura 6. Um atacante na internet (218.232.95.60) envia um único pacote UDP para a porta 1434 da vítima, um servidor SQL na rede local (192.168.1.4). O pacote atravessa a fronteira (firewall/router) e não há resposta (UDP). |
| 2 (Word 14) | 7.2 Protocolo principal | `cap6-protocolo-comparacao.svg` | O Wireshark identifica o pacote como DCERPC (Ping), de forma incorreta. Ao desligar esse dissetor, o pacote revela-se como simples datagrama UDP de 376 bytes para a porta 1434. |
| 3 (Word 15) | 7.3 Operações realizadas | `cap6-shellcode-anotada.svg` | Conteúdo do pacote (Follow UDP Stream). Destacam-se nomes de bibliotecas e funções do Windows embutidos no payload (kernel32, ws2_32, GetTickCount, socket, sendto), evidência de shellcode. |

## Notas
- Figuras vetoriais em SVG (inserir diretamente no Word 2016+). PNG disponível quando necessário.
- Regra: sem travessões (—) em legendas nem texto.
