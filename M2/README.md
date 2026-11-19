# SEGSI – M2

Materiais e trabalhos da UC **Segurança de Sistemas e de Informação** (Mestrado em Engenharia Informática, ISEP, 2026/27).

Grupo: Bruno, Leonor, Liane

## Estrutura

Caminhos relativos à raiz do repositório.

| Pasta | Conteúdo |
|---|---|
| `docs/` | Regras de funcionamento e avaliação |
| `docs/teoricas/` | Slides das aulas teóricas (Topic 1–9) |
| `docs/tp/` | Aulas TP (Business Continuity, Disaster Recovery, Security Plan, Risk Management) |
| `docs/exercicios/` | Guias PL01–PL11, PDFs de apoio e capturas dos exercícios |
| `M1/` | Trabalho M1 – Análise de tráfego |
| `M2/SEGSI-M02.pdf` | Enunciado do M2 |

## Avaliação

- Final = 30% M1 + 30% M2 + 40% M3 (sem exame final)
- Cada momento = 70% documento + 30% discussão individual

## M2 – Authentication, Authorization and Accounting

Implementar e testar um sistema AAA. Há **3 opções** e cada elemento do grupo faz **uma única** opção.
O relatório deve ser objetivo, focado em segurança, organizado e explicar claramente as evidências que suportam as conclusões.

| Opção | Tema | Responsável |
|---|---|---|
| 1 | FreeRADIUS | Liane |
| 2 | RADIUS federado (Windows Server 2019 / AD) | Bruno |
| 3 | OpenLDAP | Leonor |

### Opção 1 – FreeRADIUS

1. Instalar o FreeRADIUS na VM.
2. Criar os utilizadores Bob, Alice, John, Madeleine, Jake, Isaac, Moses, Sara e Abraham.
   Bob e Alice são utilizadores standard, Madeleine é contabilista e Jake é o "IT Guy" (administrador). Criar os grupos necessários.
3. Criar os grupos PU (Privileged Users, todos os privilégios) e NPU (Non-Privileged Users, só tarefas não administrativas).
   Não alterar Bob, Alice, John, Madeleine e Jake. Dos restantes, dois vão para PU e dois para NPU.
4. Configurar o FreeRADIUS para aceitar autenticações apenas de Users e do Administrator e testar com `radtest` (definir o secret da ligação).
5. O relatório deve mostrar, além da configuração principal, evidência dos papéis atribuídos a todos os utilizadores.

### Opção 2 – Federated RADIUS

1. Instalar numa VM o Windows Server 2019 (trial do Microsoft Evaluation Center) com todas as atualizações.
2. Promover o servidor a Domain Controller.
3. Alterar a configuração do FreeRADIUS para usar o Windows como repositório adicional de autenticação e juntá-lo ao novo domínio.
4. Criar as GPO necessárias para que a auditoria fique corretamente implementada.
5. Fazer hardening dos serviços de autenticação:
   - bloquear cifras inseguras na cifra dos tickets Kerberos;
   - garantir LDAP sign and seal;
   - verificar que o servidor Linux continua a ligar-se.
6. Adicionar Isaac e Moses ao Active Directory e Sara e Abraham ao FreeRADIUS. Todos devem poder fazer login na máquina Linux.
7. O relatório deve mostrar evidência de quem consegue e quem não consegue aceder à máquina Windows e à máquina Linux.

### Opção 3 – LDAP

1. Instalar o OpenLDAP na VM Linux com base-dn `gXX.segsi.mei.isep.ipp.pt` (XX = número do grupo).
2. Criar os grupos PU e NPU no LDAP como RDN (Relative Distinguished Name).
3. Adicionar Isaac e Moses a PU e Sara e Abraham a NPU.
4. O relatório deve mostrar evidência do acesso bem-sucedido dos utilizadores.

### Exercícios individuais atribuídos

Grupo 4.

| Elemento | Nº | Guião | Exercício | Tema |
|---|---|---|---|---|
| Bruno | 1260517 | PL05 | 2 | Hardening Windows |
| Leonor | 1230977 | PL06 | 2 | Windows BitLocker (usa a imagem `imgWinBitlocker`, ver README da raiz) |
| Liane | 1260539 | PL06 | 1 | Linux Disk Encryption |

Cada elemento deve guardar as notas e evidências do seu exercício para o anexo individual do relatório M2.

## Entrega

- Máximo de 20 páginas por aluno, sem contar anexos e referências.
- Cada aluno anexa individualmente um exercício dos guias PL que lhe foi atribuído.
- Submetido no Moodle em PDF por um só elemento do grupo, até à data indicada no Moodle.
- Nome do ficheiro: `SIGLA-PROF_NUM1_NUM2_NUM3.PDF`
