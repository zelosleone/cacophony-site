"""Mints a MusicKit developer token valid for 180 days and prints it as token.json.

Reads the key from the environment (repository secrets): MUSICKIT_PRIVATE_KEY (the .p8 file's
text), MUSICKIT_KEY_ID and MUSICKIT_TEAM_ID. Cacophony accepts a token from this site only if it
carries this key's signature.
"""

import base64
import json
import os
import time

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature

LIFETIME = 180 * 24 * 60 * 60  # Apple allows at most about six months.


def b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def compact(value: dict) -> bytes:
    return json.dumps(value, separators=(",", ":")).encode()


def main() -> None:
    key = serialization.load_pem_private_key(os.environ["MUSICKIT_PRIVATE_KEY"].encode(), password=None)
    now = int(time.time())
    header = {"alg": "ES256", "kid": os.environ["MUSICKIT_KEY_ID"].strip(), "typ": "JWT"}
    claims = {"iss": os.environ["MUSICKIT_TEAM_ID"].strip(), "iat": now, "exp": now + LIFETIME}
    signing_input = f"{b64(compact(header))}.{b64(compact(claims))}"
    r, s = decode_dss_signature(key.sign(signing_input.encode(), ec.ECDSA(hashes.SHA256())))
    token = f"{signing_input}.{b64(r.to_bytes(32, 'big') + s.to_bytes(32, 'big'))}"
    print(json.dumps({"token": token, "expires": claims["exp"]}, indent=2))


if __name__ == "__main__":
    main()