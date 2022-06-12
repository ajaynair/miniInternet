import os.path

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from pki_helpers.cert_generator import generate_private_key
from cryptography.hazmat.primitives import serialization

csr_dir = 'csr_dir'
key_dir = 'key_dir'

if not os.path.exists(csr_dir):
    os.makedirs(csr_dir)
if not os.path.exists(key_dir):
    os.makedirs(key_dir)

def generate_csr(private_key, filename, **kwargs):
    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, kwargs["country"]),
            x509.NameAttribute(
                NameOID.STATE_OR_PROVINCE_NAME, kwargs["state"]
            ),
            x509.NameAttribute(NameOID.LOCALITY_NAME, kwargs["locality"]),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, kwargs["org"]),
            x509.NameAttribute(NameOID.COMMON_NAME, kwargs["hostname"]),
        ]
    )

    # Generate any alternative dns names
    alt_names = []
    for name in kwargs.get("alt_names", []):
        alt_names.append(x509.DNSName(name))
    san = x509.SubjectAlternativeName(alt_names)

    builder = (
        x509.CertificateSigningRequestBuilder()
            .subject_name(subject)
            .add_extension(san, critical=False)
    )

    csr = builder.sign(private_key, hashes.SHA256(), default_backend())

    with open(filename, "wb") as csrfile:
        csrfile.write(csr.public_bytes(serialization.Encoding.PEM))

    return csr


server_private_key = generate_private_key(os.path.join(key_dir, "server-private-key.pem"), "server_password")
generate_csr(
    server_private_key,
    filename=os.path.join(csr_dir, "server-csr.pem"),
    country="US",
    state="Maryland",
    locality="Baltimore",
    org="My Company",
    alt_names=["localhost"],
    hostname="my-site.com",
)
