"""JWT fra bunden, kun med Pythons standardbibliotek.

Kør:  python3 jwt_lab.py

Et rigtigt projekt bruger et gennemtestet bibliotek (f.eks. PyJWT i Python,
jjwt/Spring Security i Java). Her bygger vi det selv for at se, at der ikke er
noget magisk i det: to stykker JSON og en signatur.
"""

import base64
import hashlib
import hmac
import json
import time


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(tekst: str) -> bytes:
    # base64 kræver en længde, der går op i 4. JWT fjerner fyldet (=), så vi sætter det på igen.
    return base64.urlsafe_b64decode(tekst + "=" * (-len(tekst) % 4))


def signer(besked: str, hemmelighed: str) -> str:
    mac = hmac.new(hemmelighed.encode(), besked.encode(), hashlib.sha256).digest()
    return b64url_encode(mac)


def lav_token(payload: dict, hemmelighed: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    del1 = b64url_encode(json.dumps(header, separators=(",", ":")).encode())
    del2 = b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    return f"{del1}.{del2}.{signer(f'{del1}.{del2}', hemmelighed)}"


def afkod(token: str) -> tuple[dict, dict]:
    """Læs header og payload UDEN at tjekke signaturen. Det kan alle gøre."""
    del1, del2, _ = token.split(".")
    return json.loads(b64url_decode(del1)), json.loads(b64url_decode(del2))


def verificer(token: str, hemmelighed: str) -> dict:
    """Returnér payload, hvis tokenet er ægte og ikke udløbet. Ellers ValueError."""
    del1, del2, signatur = token.split(".")
    if not hmac.compare_digest(signatur, signer(f"{del1}.{del2}", hemmelighed)):
        raise ValueError("ugyldig signatur: tokenet er ændret eller signeret med en anden nøgle")
    _, payload = afkod(token)
    if payload.get("exp", 0) < time.time():
        raise ValueError("tokenet er udløbet")
    return payload


if __name__ == "__main__":
    HEMMELIGHED = "kun-til-laering-aldrig-i-git-i-virkeligheden"

    nu = int(time.time())
    token = lav_token(
        {
            "iss": "https://login.eksempel.dk",
            "sub": "sofie",
            "aud": "maalinger-api",
            "roller": ["laborant"],
            "iat": nu,
            "exp": nu + 15 * 60,
        },
        HEMMELIGHED,
    )

    print("Token (det, der sendes i Authorization-headeren):\n")
    print(token, "\n")

    header, payload = afkod(token)
    print("Header: ", header)
    print("Payload:", payload, "\n")

    print("Verificér med rigtig nøgle:", verificer(token, HEMMELIGHED)["sub"], "er logget ind\n")

    # En angriber ændrer sin rolle til admin, men kender ikke hemmeligheden
    _, payload = afkod(token)
    payload["roller"] = ["admin"]
    del1, _, signatur = token.split(".")
    forfalsket = f"{del1}.{b64url_encode(json.dumps(payload).encode())}.{signatur}"
    try:
        verificer(forfalsket, HEMMELIGHED)
    except ValueError as fejl:
        print("Forfalsket token afvist:", fejl)
