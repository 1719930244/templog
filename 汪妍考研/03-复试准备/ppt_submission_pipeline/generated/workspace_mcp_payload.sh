#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage:"
  echo "  $0 create <your_google_email>"
  echo "  $0 apply  <your_google_email> <presentation_id>"
  exit 1
fi

mode="$1"
shift
base_dir="$(cd "$(dirname "$0")" && pwd)"

if [ "$mode" = "create" ]; then
  email="${1:?missing email}"
  python3.10 - "$email" "$base_dir" <<'PY'
import json, sys, pathlib
email = sys.argv[1]
base = pathlib.Path(sys.argv[2])
p = base / "workspace_mcp_create_args.json"
data = json.loads(p.read_text(encoding="utf-8"))
data["user_google_email"] = email
print(json.dumps(data, ensure_ascii=False))
PY
  exit 0
fi

if [ "$mode" = "apply" ]; then
  email="${1:?missing email}"
  pres_id="${2:?missing presentation_id}"
  python3.10 - "$email" "$pres_id" "$base_dir" <<'PY'
import json, sys, pathlib
email = sys.argv[1]
pres = sys.argv[2]
base = pathlib.Path(sys.argv[3])
p = base / "workspace_mcp_batch_update_args.template.json"
data = json.loads(p.read_text(encoding="utf-8"))
data["user_google_email"] = email
data["presentation_id"] = pres
print(json.dumps(data, ensure_ascii=False))
PY
  exit 0
fi

echo "Unknown mode: $mode"
exit 1
