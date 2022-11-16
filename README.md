# asn1c_sandbox_do_not_use
DO NOT USE! Temporary repo just to reproduce a decoding issue

## Steps to reproduce
```bash
rm -f *.h *.c src/* include/*
asn1c -fcompound-names -fincludes-quoted -gen-OER -fwide-types -pdu=auto -pdu=ScopedLocalPolicyFile $(cat scms-asn1.conf)
make -f ./converter-example.mk
./converter-example -ioer -otext -dd -b 60000 -p ScopedLocalPolicyFile ./fixtures/ScopedLocalPolicyFile_no_maxCertRequest.coer
./converter-example -ioer -otext -dd -b 60000 -p ScopedLocalPolicyFile ./fixtures/ScopedLocalPolicyFile.coer
```
