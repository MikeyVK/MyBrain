from toolkit_runtime import WORKROOT, runtime_area
"""Owner-started secure setup only; no e-Boekhouden/network access."""
import sys
from pathlib import Path

import probe_rest as p
from credential_store import CredentialFailure, CredentialStore, WindowsBackend


def setup(store, ask, secret_input) -> None:
    if ask("Is het nieuwe token in de bedoelde administratie aangemaakt? Typ JA: ").strip() != "JA":
        raise CredentialFailure("ADMINISTRATION_NOT_CONFIRMED")
    existing = store.metadata()
    replace = existing is not None
    if replace and ask("MyBrain/eBoekhouden bestaat al. Typ VERVANG om alleen deze referentie te vervangen: ").strip() != "VERVANG":
        raise CredentialFailure("CREDENTIAL_REPLACEMENT_NOT_CONFIRMED")
    first = p.normalize_access_token(secret_input("Nieuw API-token (onzichtbaar): "))
    second = p.normalize_access_token(secret_input("Herhaal API-token (onzichtbaar): "))
    if first != second:
        raise CredentialFailure("TOKEN_CONFIRMATION_MISMATCH")
    store.save(first, replace=replace)
    del first, second


def main() -> None:
    p.protect_directory(runtime_area("rest"))
    store = CredentialStore(WindowsBackend())
    setup(store, input, p.hidden)
    print("Opgeslagen als MyBrain/eBoekhouden in Windows Referentiebeheer, alleen dit Windows-account op deze pc.")


if __name__ == "__main__":
    try:
        main()
    except (CredentialFailure, p.Stop) as exc:
        print("Gestopt:", str(exc))
    except (KeyboardInterrupt, EOFError):
        print("Gestopt: CANCELLED")
    except Exception:
        print("Gestopt: LOCAL_CREDENTIAL_SETUP_FAILURE")
    finally:
        if sys.stdin.isatty():
            try:
                input("Druk Enter om dit venster te sluiten.")
            except (KeyboardInterrupt, EOFError):
                pass
