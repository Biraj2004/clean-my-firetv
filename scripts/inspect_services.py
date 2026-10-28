import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.adb import ADBClient

client = ADBClient()
client.connect()

_, out, _ = client.run(["shell", "dumpsys activity services"])
lines = out.splitlines()

service_records = []
current_service = None
service_dict = {}

for line in lines:
    line_s = line.strip()
    if "* ServiceRecord{" in line_s:
        # e.g. * ServiceRecord{270b201 u0 tv.dumbtv.home/.Guard}
        parts = line_s.split()
        for p in parts:
            if "/" in p and not p.startswith("u0"):
                svc_name = p.rstrip("}")
                pkg = svc_name.split("/")[0]
                if pkg not in service_dict:
                    service_dict[pkg] = []
                service_dict[pkg].append(svc_name)

print("=" * 70)
print(f"ACTIVE ANDROID SERVICES AUDIT ({len(service_dict)} packages running services)")
print("=" * 70)

for pkg in sorted(service_dict.keys()):
    svcs = service_dict[pkg]
    print(f"\n[Package] {pkg} ({len(svcs)} services):")
    for s in svcs:
        print(f"   - {s}")

