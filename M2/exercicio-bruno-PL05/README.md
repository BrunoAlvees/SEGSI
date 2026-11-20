# PL05, Exercício 2: Hardening Windows (guia de estudo e execução)

**Objetivo:** endurecer um posto Windows 11 num domínio AD, por GPO, a partir do CIS Benchmark, comparar com uma ferramenta de privacidade (O&O ShutUp10++) e controlar a execução de aplicações com AppLocker, percebendo os limites dessa abordagem (LOLBAS).

> Este guia não traz respostas para colar. Nas alíneas teóricas tens conceitos e perguntas-guia: a resposta escreves tu, para a saberes defender na oral.
> **Nunca faças este exercício no teu PC.** Só na VM.

---

## 1. Preparação do ambiente

**Nota importante:** a avaliação do **Windows 10 Enterprise já não existe** no Evaluation Center (o link redireciona para o fim de suporte do Windows 10). Usa **Windows 11 Enterprise (avaliação, 90 dias, exige registo)**:
https://www.microsoft.com/en-us/evalcenter/evaluate-windows-11-enterprise (versão 26H2 ou LTSC 2024, ISO x64).

1. **Criar a VM** `SEGSI-W11` no VirtualBox: 4 GB RAM (DC 4 + Ubuntu 2 + W11 4 = 10 GB de 16), 2 vCPU, disco 64 GB, **EFI + Secure Boot + TPM 2.0** ligados (requisitos do Windows 11). Rede: a mesma NAT Network 192.168.56.0/24.
2. **IP fixo**, por exemplo 192.168.56.30, **DNS = 192.168.56.10** (o DC). Sem isto não junta ao domínio.
3. **Snapshot "base-limpa"** antes de qualquer alteração.
4. **Juntar ao domínio** `g04.segsi.local` (depois de o DC estar promovido): `Add-Computer -DomainName g04.segsi.local -Restart`.
5. No DC: criar uma **OU** própria (ex.: `OU=Workstations-PL05`) e mover lá o computador. As GPOs do exercício ligam-se só a essa OU (não à raiz do domínio, para não afetar o DC nem o M2).
6. **Central Store de ADMX:** o Server 2019 não traz os modelos administrativos do Windows 11. Copia `C:\Windows\PolicyDefinitions` da VM W11 para `\\g04.segsi.local\SYSVOL\g04.segsi.local\Policies\PolicyDefinitions` no DC, senão muitas definições do CIS não aparecem no GPMC.
7. Novo snapshot "no-dominio" antes de aplicar o hardening.

**Evidências:** `systeminfo` (edição e domínio), `ipconfig /all`, captura da OU no ADUC.

---

## 2. As 10 alíneas

### 1) Obter o CIS Benchmark
**O que fazer:** descarregar o PDF do **CIS Microsoft Windows 11 Enterprise Benchmark** (versão atual na página: **v5.1.1**; o Windows 10 Enterprise está na v4.0.0).
- Página: https://www.cisecurity.org/benchmark/microsoft_windows_desktop
- O PDF é **gratuito para uso não comercial, mas exige preencher um formulário** (nome, email, organização...): https://learn.cisecurity.org/benchmarks
- Os **CIS Build Kits** (GPOs prontas a importar) são **só para membros CIS SecureSuite**. Alternativa gratuita: Microsoft Security Compliance Toolkit (alínea 2).

**Evidências:** primeira página do PDF com a versão; captura do índice com os perfis (confirma no PDF que perfis existem: Level 1, Level 2, BitLocker, Next Generation...).

### 2) Aplicar um hardening completo
**O que fazer (por GPO, na OU do passo 5):**
1. Descarregar o **Microsoft Security Compliance Toolkit** (baseline do Windows 11 da versão que instalaste, + `LGPO.zip` e `PolicyAnalyzer.zip`): https://www.microsoft.com/en-us/download/details.aspx?id=55319
2. No DC, importar a baseline para GPOs com o script da pasta `Scripts` da baseline (confirma o nome do script no ZIP, ex.: `Baseline-ADImport.ps1`) e ligá-las à OU.
3. Criar uma GPO tua, `PL05-CIS-L1`, com as recomendações **CIS Level 1** que a baseline da Microsoft não cobre ou faz de forma diferente. Escolhe secções do PDF (ex.: políticas de conta e password, User Rights Assignment, Security Options, auditoria avançada, Firewall, Defender) e anota para cada uma o **número do controlo tal como está no PDF**.
4. Na VM: `gpupdate /force`, reiniciar, testar se o uso normal ainda funciona.

**Evidências:** `gpresult /h evidencias/02-hardening/gpresult.html`; captura do GPMC com as GPOs ligadas; tabela "controlo CIS, valor, aplicado sim/não, porquê"; (opcional) relatório do PolicyAnalyzer a comparar baseline MS vs. a tua GPO.
**Snapshot** "hardening-aplicado".

### 3) Que funcionalidades se perdem
**Conceitos:** segurança vs. usabilidade; Level 1 (impacto baixo) vs. Level 2 (defesa em profundidade, pode partir funcionalidades); a secção "Impact" de cada controlo no PDF.
**Investiga/verifica:** depois da alínea 2, o que deixou de funcionar na VM? (ex.: contas locais, ligações remotas, armazenamento removível, Store/apps, telemetria, partilhas, scripts.) Lê o campo "Impact" dos controlos que aplicaste.
**Perguntas-guia:** Que controlos têm maior custo para o utilizador? Num posto de um estudante vs. num posto de contabilidade, aplicarias o mesmo nível? Quem decide as exceções e como se documentam?

### 4) Hardening em larga escala
**Conceitos:** GPO em AD (OUs, herança, filtros WMI/segurança, Central Store), Intune/MDM (perfis de configuração, security baselines do Intune), LGPO para máquinas fora do domínio, imagens "gold", DSC/scripts, verificação contínua (CIS-CAT, PolicyAnalyzer).
**Investiga/verifica:** o teu próprio ambiente é a prova (GPO numa OU). Experimenta o `LGPO.exe` para perceber a diferença local vs. domínio.
**Perguntas-guia:** Como garantes que um posto que saiu da rede volta a ficar conforme? Como testas antes de aplicar a 1000 máquinas (OU piloto, faseamento)? Como medes conformidade?

### 5) O&O ShutUp10++
**O que fazer:** snapshot antes. Descarregar de https://www.oo-software.com/en/shutup10 (gratuito, portátil, não precisa de instalação; versão atual 3.7.x; suporta Windows 10 e 11). Exportar a configuração inicial, aplicar as definições recomendadas, exportar a final.
**Evidências:** capturas antes/depois; os dois ficheiros `.cfg` exportados; lista das definições alteradas.
**Atenção:** num PC de domínio, a GPO pode repor ou contrariar definições do ShutUp. Regista se isso acontece depois de `gpupdate /force`.

### 6) Gap analysis CIS vs. O&O ShutUp
**O que fazer:** tabela com colunas: área (telemetria, privacidade, contas, rede, auditoria, firewall...), CIS cobre?, ShutUp cobre?, valor em cada, conflito?
**Perguntas-guia:** Os objetivos das duas ferramentas são os mesmos (segurança vs. privacidade)? O que o CIS faz que o ShutUp nem toca (ex.: auditoria, password policy)? E o contrário? Qual escalas para uma empresa e porquê? Qual tem rastreabilidade (justificação, referência, auditoria)?

### 7) O que é o AppLocker
**Conceitos:** controlo de aplicações por **lista de permissões** (allowlisting); coleções de regras (Executable, Windows Installer, Script, DLL, Packaged apps); condições (Publisher, Path, File hash); modos **Enforce** e **Audit only**; relação com o **App Control for Business (antigo WDAC)**.
**Factos confirmados:**
- Precisa do serviço **Application Identity (AppIDSvc)** a correr; sem ele as regras não são aplicadas.
- Desde o **KB5024351** (atualizações de set./out. 2022), Windows 10 2004+ e **todas as versões do Windows 11 aplicam AppLocker em qualquer edição**, também por GPO. Antes, por GPO, só Enterprise/Education. Com a VM Enterprise não tens problema de qualquer forma.
- Docs: https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/requirements-to-use-applocker

**Perguntas-guia:** Porque é que allowlisting é mais forte do que antivírus (denylisting)? Quais as vantagens/fraquezas de cada tipo de condição? Porque é que a Microsoft recomenda o App Control for Business como alternativa mais robusta?

### 8) Política básica de AppLocker
**Cuidados para não te trancares fora:** snapshot "antes-applocker"; criar sempre as **regras por defeito** primeiro (Windows, Program Files, administradores); começar em **Audit only**; testar com um utilizador de domínio **não administrador**.

**O que fazer (GPO `PL05-AppLocker` na OU):**
1. Computer Configuration > Policies > Windows Settings > Security Settings > Application Control Policies > AppLocker.
2. Em cada coleção (Executable, Installer, Script, Packaged): "Create Default Rules".
3. Pôr as coleções em **Audit only**.
4. Na mesma GPO: System Services > Application Identity = Automatic.
5. Na VM: `gpupdate /force`, reiniciar; copiar um `.exe` portátil (ex.: o próprio ShutUp10) para `C:\Users\<user>\Downloads` e executá-lo com o utilizador normal.
6. Ver os eventos e depois passar para **Enforce** e repetir o teste (deve ser bloqueado).
7. Opcional: comparar com a "AppLocker Starter Policy" do NSA (https://github.com/nsacyber/AppLocker-Guidance) e as políticas de https://github.com/MotiBa/AppLocker (vêm em modo audit, testar antes).

**Evidências:**
- `Get-Service AppIDSvc` (Running)
- `Get-AppLockerPolicy -Effective -Xml > evidencias/08-applocker/politica-efetiva.xml`
- `Get-AppLockerFileInformation -EventLog -EventType Audited` (o que teria sido bloqueado)
- Event Viewer > Applications and Services Logs > Microsoft > Windows > AppLocker > *EXE and DLL*: eventos **8003** (audit, seria bloqueado) e **8004** (bloqueado)
- captura da mensagem de bloqueio no utilizador; `gpresult /h`.

### 9) Permitir só binários assinados?
**Conceitos:** regras de Publisher (certificado, produto, nome do ficheiro, versão); assinatura prova **origem e integridade**, não **intenção**.
**Investiga/verifica:** quantos executáveis do Windows são assinados pela Microsoft? Malware assinado com certificados roubados ou comprados existe?
**Perguntas-guia:** "Qualquer assinatura" vs. "editores específicos": que diferença faz? O que acontece com scripts, DLLs e ferramentas internas não assinadas? Quem gere os certificados aceites?

### 10) LOLBAS e o threat model
**Conceitos:** LOLBAS (Living Off The Land Binaries, Scripts and Libraries): binários, scripts e bibliotecas **legítimos e assinados pela Microsoft** que podem ser abusados (download, execução, *AWL bypass*, dump de credenciais...). Exemplos no catálogo: `certutil.exe`, `mshta.exe`, `msbuild.exe`, `comsvcs.dll`. Cada entrada mapeia para técnicas MITRE ATT&CK (ex.: T1218).
- Catálogo: https://lolbas-project.github.io/
- Lista de bloqueio recomendada da Microsoft (procura "Microsoft recommended block rules" no Microsoft Learn).

**Investiga/verifica:** na tua VM com a política da alínea 8, um LOLBin (ex.: `mshta.exe` ou `msbuild.exe`, se existir) é permitido pelas regras por defeito? Testa só com algo inofensivo e regista o evento.
**Perguntas-guia:** Se "só assinados" permite LOLBins, o atacante precisa de trazer binários? Que pressupostos do teu threat model da alínea 9 caem? Que medidas complementares fazem sentido (regras de deny para LOLBins, DLL rules, Constrained Language Mode do PowerShell, auditoria, App Control)?

---

## 3. Ordem de trabalho sugerida

1. Ler o enunciado e o índice do PDF do CIS (alínea 1).
2. Preparar a VM, snapshot, domínio, OU, ADMX (secção 1).
3. Hardening por GPO e evidências (alíneas 2 e 4), snapshot.
4. Anotar o que deixou de funcionar (alínea 3).
5. ShutUp10++ e gap analysis (alíneas 5 e 6), voltar ao snapshot se necessário.
6. Estudar AppLocker e implementar em Audit, depois Enforce (alíneas 7 e 8).
7. Assinatura e LOLBAS, com o teste prático (alíneas 9 e 10).
8. Escrever o relatório pelas tuas palavras e treinar a explicação oral de cada alínea.

## 4. Pastas para evidências

```
evidencias/
  00-ambiente/      systeminfo, ipconfig, OU, snapshots
  01-cis/           versão do PDF, perfis
  02-hardening/     gpresult.html, GPMC, tabela de controlos
  03-impacto/       o que partiu
  05-shutup/        capturas, .cfg antes e depois
  06-gap/           tabela CIS vs ShutUp
  08-applocker/     politica-efetiva.xml, eventos 8003/8004, bloqueio
  10-lolbas/        teste e evento
```

## 5. Por confirmar
- Nomes exatos dos perfis e números dos controlos: **sempre no PDF do CIS**.
- Nome do script de importação para AD dentro do ZIP da baseline do SCT.
- Nome final do domínio (`g04.segsi.local`) e IP da VM W11.
