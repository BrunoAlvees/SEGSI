# Análise — cap6.pcap (SQL Slammer)

## Resumo
- Captura com **1 único pacote** UDP.
- Origem `218.232.95.60` (externo, porta 3664) → destino `192.168.1.4` (porta **1434/UDP**).
- Payload de **376 bytes** com shellcode: é o worm **SQL Slammer** (2003).

## Pontos descobertos (passo a passo)
1. **Captura feita dentro da rede** (depois do router), por isso só se vê o pacote a chegar à vítima.
2. **Wireshark identifica MAL** o pacote como "DCERPC Ping" (dissetor heurístico engana-se). Não é ping real.
3. **Porta 1434/UDP** = SQL Server Resolution Service (Microsoft SQL Server). Alvo: servidor de base de dados.
4. **Shellcode no payload** (visível em Follow UDP Stream e nos bytes):
   - `kernel32` (hel32hkern)
   - `ws2_32.dll` (ws2_f...32.d)
   - `GetTickCount`, `socket`, `sendto` (funções de rede para auto-propagação)
5. **Desligar o dissetor DCERPC** (Analyze > Enabled Protocols) revela a verdade: `UDP 3664 > 1434 Len=376` + `Data (376 bytes)`.
6. **MACs falsificados/inventados:**
   - Origem `11:22:33:44:55:66` (sequência óbvia)
   - Destino `de:ad:ca:fe:ba:be` ("dead cafe babe", piada)
   - Indica captura didática/montada, não tráfego real.
7. **Worm cabe num só pacote UDP** (376 bytes), sem ligação (UDP não tem handshake) = espalha-se muito rápido.

## Como ataca
- Explora um **buffer overflow** no SQL Server Resolution Service (falha MS02-039).
- O serviço espera um pedido pequeno; o worm envia 376 bytes e transborda a memória.
- O transbordo reescreve o endereço de "o que executar a seguir", apontando para o próprio shellcode.
- O servidor executa o código do atacante, que apenas se **reenvia** para IPs aleatórios (socket/sendto).

## Objetivo e impacto
- Não rouba nem destrói dados; não dá lucro direto.
- Efeito = **negação de serviço (DoS) em massa**: máquinas infetadas disparam pacotes sem parar, entopem redes e esgotam CPU dos servidores.
- Em 2003 afetou bancos, multibancos e companhias aéreas.
- Motivação do autor (nunca identificado): notoriedade / demonstração técnica, não lucro.

## Porque foi tão rápido
- Usa **UDP** (sem handshake): dispara e esquece, não espera resposta.
- O worm **cabe num só pacote** (376 bytes) = cada envio é uma infeção completa.
- Cada máquina dispara milhares de pacotes/segundo; infetou o mundo em ~10 minutos.

## Mitigações
1. **Patch** do SQL Server (MS02-039, já existia 6 meses antes). Manter sistemas atualizados.
2. **Firewall** a bloquear a porta 1434/UDP vinda do exterior.
3. **Segmentação de rede e serviços mínimos**: não expor bases de dados à internet; desligar serviços não usados.

## Estrutura para o relatório
- a. Intervenientes: atacante externo 218.232.95.60 > vítima 192.168.1.4 (servidor SQL)
- b. Protocolo principal: UDP/1434 (SQL Server Resolution Service), explorado pelo Slammer
- c. Operações: 1 datagrama UDP com o worm, sem ligação nem resposta
- d. Problemas de segurança e mitigações: buffer overflow + as 3 mitigações acima
- e. Outras considerações: má identificação do Wireshark, MACs falsos
