"""Public deployment process entrypoint; rendering stays at the CLI boundary."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
import traceback
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
from contracts import ArchiveReader, DeploymentError, PackageVerifier, TargetOwnership

class DeploymentCli:
    """Compose and render the selected public operation."""
    def main(self) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("command", choices=["check","extract","preflight","bootstrap","verify","recover"])
        parser.add_argument("--package", type=Path)
        parser.add_argument("--archive", type=Path)
        parser.add_argument("--destination", type=Path)
        parser.add_argument("--binding-name", default="")
        parser.add_argument("--action", choices=["Resume","DiscardStaging"], default="Resume")
        args = parser.parse_args()
        try:
            if args.command == "extract":
                if not args.archive or not args.destination:
                    raise DeploymentError("arguments_required")
                ArchiveReader().extract(args.archive, args.destination)
            else:
                if not args.package:
                    raise DeploymentError("package_required")
                manifest = PackageVerifier().verify(args.package)
                if args.command in ("bootstrap","verify","recover"):
                    if not args.destination:
                        raise DeploymentError("destination_required")
                    from provision import Provisioner
                    if args.command == "recover" and args.action == "DiscardStaging":
                        raise DeploymentError("quarantine_preserved_explicit_review_required",4)
                    provisioner=Provisioner()
                    result=provisioner.verify(args.package,args.destination) if args.command == "verify" else provisioner.bootstrap(args.package,args.destination,args.binding_name,args.command=="recover")
                    print(json.dumps(result))
                    return 2
                if args.command == "preflight":
                    if not args.destination:
                        raise DeploymentError("destination_required")
                    TargetOwnership().inspect(args.destination, args.package, manifest)
            print(json.dumps({"status":"completed","code":"verified","command":args.command}))
            return 0
        except DeploymentError as exc:
            print(json.dumps({"status":"blocked","code":exc.code,"command":args.command}))
            return exc.exit_code
        except Exception as exc:
            # Process boundary retains native diagnostics without replacing their meaning.
            print(json.dumps({"status":"failed","code":"execution_failure","diagnostic":repr(exc),"traceback":traceback.format_exc()}))
            return 5

if __name__ == "__main__":
    raise SystemExit(DeploymentCli().main())
