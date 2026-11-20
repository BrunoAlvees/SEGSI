# Matriz de acessos (passo 7), testes de 2026-11-20

| Utilizador | Repositório | Linux `segsi-linux` (SSH via PAM → FreeRADIUS) | Windows `SEGSI-DC` (consola) |
|---|---|---|---|
| sara | FreeRADIUS (ficheiro `users`, SHA-512) | ✅ Access-Accept / login SSH OK | ❌ "user name or password is incorrect" (4625, 0xC000006D / 0xC0000064: conta não existe no AD) |
| abraham | FreeRADIUS (ficheiro `users`, SHA-512) | ✅ Access-Accept | ❌ não existe no AD (mesmo caso da Sara) |
| isaac | Active Directory (OU Utilizadores-M2) | ✅ Access-Accept / login SSH OK (validado no DC: 4776 status 0x0 de SEGSI-LINUX) | ❌ "sign-in method isn't allowed" (4625, 0xC000015B: sem o direito "Allow log on locally" num DC) |
| moses | Active Directory (OU Utilizadores-M2) | ✅ Access-Accept (4776 status 0x0) | ❌ igual ao Isaac (utilizador normal do domínio) |
| Administrator | Active Directory (Domain Admins) | não testado no Linux (fora do âmbito) | ✅ entra |
| bruno | conta local do Linux (administrador da VM) | ❌ pelo RADIUS: Access-Reject (4776, 0xC0000064); entra só por `pam_unix` local | ❌ não existe no AD |
| hacker | não existe | ❌ Access-Reject (4776, 0xC0000064) | ❌ |

Códigos: 0xC000006D = logon falhado; 0xC0000064 = utilizador inexistente; 0xC000015B = tipo de logon não concedido; 4768 cifra 0x12 = AES256 (depois do hardening já não aparece RC4 0x17).

Limitação: a máquina Windows testada foi o DC. A VM Windows 11 (SEGSI-W11) não chegou a ser juntada ao domínio; num posto de trabalho do domínio, Isaac e Moses poderiam entrar (Domain Users têm "Allow log on locally" nas workstations) e Sara/Abraham continuariam recusados.

Capturas: `01` a `06` nesta pasta.
