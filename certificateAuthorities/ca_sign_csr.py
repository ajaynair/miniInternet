import os.path
import sys

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from datetime import timedelta
from datetime import datetime
from cryptography.hazmat.primitives import serialization
from getpass import getpass

ca_keys = "ca_keys"


def sign_csr(csr_file, new_filename):
    csr_file = open(csr_file, "rb")
    csr = x509.load_pem_x509_csr(csr_file.read(), default_backend())

    ca_public_key_file = open(os.path.join(ca_keys, "ca_public_key.pem"), "rb")
    ca_public_key = x509.load_pem_x509_certificate(
        ca_public_key_file.read(), default_backend()
    )

    ca_private_key_file = open(os.path.join(ca_keys, "ca_private_key.pem"), "rb")
    ca_private_key = serialization.load_pem_private_key(
        ca_private_key_file.read(),
        getpass().encode("utf-8"),
        default_backend(),
    )

    valid_from = datetime.utcnow()
    valid_until = valid_from + timedelta(days=30)

    builder = (
        x509.CertificateBuilder()
            .subject_name(csr.subject)
            .issuer_name(ca_public_key.subject)
            .public_key(csr.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(valid_from)
            .not_valid_after(valid_until)
    )

    for extension in csr.extensions:
        builder = builder.add_extension(extension.value, extension.critical)

    public_key = builder.sign(
        private_key=ca_private_key,
        algorithm=hashes.SHA256(),
        backend=default_backend(),
    )

    with open(new_filename, "wb") as keyfile:
        keyfile.write(public_key.public_bytes(serialization.Encoding.PEM))


csr_file = sys.argv[1]

signed_server_public_key = "server-public-key.pem"
sign_csr(csr_file, signed_server_public_key)
print(signed_server_public_key)
