"""Fresh-create source-description admission; legacy receipt readers stay read-only."""
import hashlib
import json
from repair_contract import require, validate_source_contract

def admit(item, root):
    binding = item.get("sourceDescriptionContract")
    require(isinstance(binding, dict), "BOOK_SOURCE_DESCRIPTION_REQUIRED")
    reference = binding.get("sourceSnapshot")
    require(isinstance(reference, dict) and set(reference) == {"path", "sha256"}, "BOOK_SOURCE_REFERENCE_REQUIRED")
    path = (root / reference["path"]).resolve()
    require(path.is_relative_to(root.resolve()) and path.is_file()
            and hashlib.sha256(path.read_bytes()).hexdigest() == reference["sha256"], "BOOK_SOURCE_REFERENCE_CHANGED")
    validate_source_contract(item, json.loads(path.read_text(encoding="utf-8")))
