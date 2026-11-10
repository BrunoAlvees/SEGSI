import subprocess, re
from Crypto.Hash import MD4, MD5, HMAC
from Crypto.Cipher import ARC4
TSHARK=r"C:\Program Files\Wireshark\tshark.exe"; CAP="NTLM_LDAP.pcapng"
nthash=MD4.new("admin".encode('utf-16le')).digest(); sbk=MD4.new(nthash).digest()
kxkey=HMAC.new(sbk, bytes.fromhex('3ce65bea9b2dc110')+bytes.fromhex('1e28d3cbd400f676'), MD5).digest()
esk=ARC4.new(kxkey).encrypt(bytes.fromhex('00603c2768a0b060a9640ad6cd8c9025'))
cli=ARC4.new(MD5.new(esk+b"session key to client-to-server sealing key magic constant\x00").digest())
srv=ARC4.new(MD5.new(esk+b"session key to server-to-client sealing key magic constant\x00").digest())
CLIENT="10.0.0.20"
out=subprocess.run([TSHARK,"-r",CAP,"-Y","ntlmssp.verf","-T","fields","-e","frame.number","-e","ip.src","-e","ldap.gssapi_encrypted_payload"],capture_output=True,text=True).stdout
for line in out.strip().splitlines():
    fn,src,ph=line.split('\t')
    data=bytes.fromhex(ph.replace(':',''))
    rc4 = cli if src==CLIENT else srv
    dec=rc4.decrypt(data); rc4.decrypt(b'\x00'*8)
    dirn="C->S" if src==CLIENT else "S->C"
    strings=re.findall(r"[ -~]{4,}", ''.join(chr(b) if 32<=b<127 else '.' for b in dec))
    print(f"[frame {fn} {dirn}] 1byte={hex(dec[0])}  {' | '.join(strings)}")
