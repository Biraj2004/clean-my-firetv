# Security Policy

## Supported Versions

The following table outlines the security support status for Clean My FireTV versions:

| Version | Supported | Minimum Fire OS Version | Android API Level |
| :--- | :--- | :--- | :--- |
| 2.0.x (DumbTV Enhanced) | Yes | Fire OS 7.0+ | API 28+ (Android 9.0) |
| 1.0.x (Plume / Legacy) | No | Fire OS 6.0+ | Deprecated |

## Security Architecture & Design Principles

Clean My FireTV is designed around local execution, zero cloud dependency, and user privacy:

1. **Zero External Data Transmission**:
   - The tooling does not run external telemetry, phone-home reporting, or analytics servers.
   - All ADB interactions take place directly between your local management machine and the Fire TV device over your local area network (LAN).

2. **Private DNS over TLS (DoT)**:
   - System-wide Private DNS is configured using Cloudflare DNS over TLS (`1dot1dot1dot1.cloudflare-dns.com`).
   - Prevents unencrypted DNS queries and local ISP profiling across all media applications and background daemons.

3. **Telemetry & Tracker Starvation**:
   - Telemetry services (`com.amazon.device.software.ota`, `com.amazon.device.messaging`, `com.amazon.firehomestarter`, crash reporters, metrics collectors) are restricted using `appops set <package> RUN_ANY_IN_BACKGROUND ignore` and package disablers.
   - Background wakelocks and network syncs from diagnostic daemons are permanently starved.

4. **Reversible Safety Journaling**:
   - Every system mutation, appop adjustment, or configuration push is recorded in a transactional log (`logs/journal.jsonl`) with an exact forward and reverse command pair.
   - Devices can be rolled back to their original factory state via `scripts/rollback.py`.

5. **No Root Requirement**:
   - Clean My FireTV operates strictly within user-space ADB permissions (`dumpsys`, `settings`, `pm`, `appops`).
   - No unlocked bootloaders, system partition remounts, or dangerous root exploits are utilized.

## Reporting a Vulnerability

If you identify a security issue, vulnerability, or unexpected privilege leak:

1. Do NOT open a public GitHub issue.
2. Please submit your security report directly via GitHub Private Vulnerability Reporting under the **Security** tab of this repository.
3. Include the following details in your report:
   - Device model (e.g., Fire TV Stick 4K Max, Fire TV Stick Lite)
   - Fire OS version and build number
   - Steps to reproduce the issue
   - Potential impact or proof of concept
4. Maintainers will review the submission within 48 to 72 hours and provide a remediation plan.
