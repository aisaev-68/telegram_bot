import os
from OpenSSL import crypto

def create_cert(url):
    KEY_FILE = "webhook_pkey.pem"
    CERT_FILE = "webhook_cert.pem"

    def create_self_signed_cert(cert_dir):
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)   #  размер может быть 2048, 4196

        #  Создание сертификата
        cert = crypto.X509()
        cert.get_subject().C = "RU"   #  указываем свои данные
        cert.get_subject().ST = "Dagestan"   #  указываем свои данные
        cert.get_subject().L = "Mackhachkala"   #  указываем свои данные
        cert.get_subject().O = "xazrad"   #  указываем свои данные
        cert.get_subject().OU = "xazrad"   #  указываем свои данные
        cert.get_subject().CN = url   #  указываем свои данные
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10*365*24*60*60)   #  срок "жизни" сертификата
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha1')

        with open(os.path.join(cert_dir, CERT_FILE), "wb") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

        with open(os.path.join(cert_dir, KEY_FILE), "wb") as f1:
            f1.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

    path = os.getcwd()
    create_self_signed_cert(path)