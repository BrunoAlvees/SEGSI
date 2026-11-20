# 1. Introdução e Metodologia

O controlo de acessos a sistemas e serviços assenta em três funções, conhecidas por AAA (*Authentication, Authorization and Accounting*): a **autenticação** confirma quem é o utilizador, a **autorização** define o que esse utilizador pode fazer e o ***accounting*** regista o que foi feito, permitindo auditoria e investigação de incidentes. Estas funções respondem tanto a requisitos legais como a políticas internas das organizações.

Este relatório descreve a implementação e o teste de três soluções AAA, correspondentes às três opções do enunciado do M2. Cada elemento do grupo realizou uma opção e um exercício individual das fichas práticas, apresentado em anexo (Tabela 1). A secção 5 reúne as conclusões e a secção 6 as referências.

*Tabela 1 – Distribuição do trabalho pelos elementos do grupo.*

<!-- larguras: 1500, 3380, 3624 -->
| Elemento | Opção do M2 | Exercício individual |
|---|---|---|
| Liane Duarte | Opção 1 – FreeRADIUS (secção 2) | Anexo C – PL06 Ex. 1 – Linux Disk Encryption |
| Bruno Alves | Opção 2 – Federated RADIUS (secção 3) | Anexo A – PL05 Ex. 2 – Hardening Windows |
| Leonor Marinho | Opção 3 – LDAP (secção 4) | Anexo B – PL06 Ex. 2 – Windows BitLocker |

Todas as opções foram implementadas em máquinas virtuais no VirtualBox, ligadas apenas por NAT ou por uma rede interna e, por isso, inacessíveis a partir de outras máquinas, o que permitiu configurar e testar sem afetar sistemas reais. Os sistemas foram atualizados antes de qualquer configuração, para que os serviços não fossem instalados sobre vulnerabilidades conhecidas. O ambiente de cada opção é descrito na respetiva secção.

Em cada opção seguiram-se os mesmos passos: **preparação** (instalação e atualização do sistema e do serviço), **configuração** (utilizadores, grupos e políticas pedidos no enunciado, segundo o princípio do privilégio mínimo), **testes** (confirmar que os acessos permitidos são aceites e, sempre que aplicável, que os restantes são recusados) e **análise de segurança** (medidas aplicadas, riscos que permanecem e mitigações recomendadas).

Cada passo é acompanhado de evidência: capturas de ecrã dos comandos e dos resultados, com as linhas relevantes assinaladas e explicadas na legenda. As passwords e os *secrets* visíveis foram criados apenas para este ambiente de teste; num ambiente real, nunca deveriam ser divulgados.
