from pki_helpers.cert_generator import generate_private_key, generate_public_key
import os

CA_PWD = "secret_password"

ca_keys_dir = "ca_keys"
if not os.path.exists(ca_keys_dir):
    os.makedirs(ca_keys_dir)

private_key = generate_private_key(os.path.join(ca_keys_dir, "ca_private_key.pem"), CA_PWD)
generate_public_key(
    private_key,
    filename=os.path.join(ca_keys_dir, "ca_public_key.pem"),
    country="US",
    state="Maryland",
    locality="Baltimore",
    org="My CA Company",
    hostname="my-ca.com")
