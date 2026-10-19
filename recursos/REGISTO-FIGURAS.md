# Registo de figuras do relatório

## Captura 1 (LDAP) — Bruno

| Fig. | Ponto | Ficheiro | Legenda |
|---|---|---|---|
| 1 | a. Intervenientes | `cap1-intervenientes.svg` | Intervenientes da captura 1. O cliente (192.168.170.130) comunica com o servidor Active Directory (192.168.170.132) por LDAP sobre TCP/389, sem cifra. A vermelho os pedidos do cliente (bind e search), a azul as respostas do servidor. |
| 2 | b. Protocolo principal | `cap1-protocol-hierarchy-anotada.svg` | Hierarquia de protocolos da captura (Statistics, Protocol Hierarchy). O LDAP corresponde a apenas 13,3% dos pacotes mas a 92,3% dos bytes, confirmando ser o protocolo principal. Os restantes (TLS, SSDP, NBNS, ARP) são tráfego de fundo. |
| 3 | c. Operações | `cap1-diagrama-sequencia.svg` | Diagrama de sequência das operações da captura 1, em 4 fases (ligação, autenticação, consultas, encerramento). A vermelho os pedidos do cliente, a azul as respostas do servidor; indicam-se os números de frame como evidência. |
| 4 | 2.3.1 Estabelecimento da ligação | `cap1-handshake-anotada.svg` | Handshake TCP (frames 1 a 3): SYN, SYN-ACK e ACK dirigidos à porta 389. A frame 4 marca o fim do handshake e o início do bind. A comunicação usa a porta 389 (sem cifra), não a 636 (LDAPS). |
| 5 | 2.3.2 Autenticação (bind) | (screenshot frame 4 detalhe a anotar) | |
| 5 | c. Operações (política/SID) | (screenshot frame 271 a anotar) | |
| 6 | c. Operações (utilizadores) | (screenshot frame 283 a anotar) | |

## Captura 6 (SQL Slammer) — Bruno
| Fig. | Ponto | Ficheiro | Legenda |
|---|---|---|---|
| | | | |

## Notas
- Figuras vetoriais em SVG (inserir diretamente no Word 2016+). PNG disponível quando necessário.
- Regra: sem travessões (—) em legendas nem texto.
