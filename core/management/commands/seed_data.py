from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import (
    Finding, EvidenceItem, IPCCommand, QuarantineItem, SecurityEvent, ProofOfFixCertificate
)


class Command(BaseCommand):
    help = "Seed the database with realistic Sentinel Trinity demo data (World Monitor Local Lab)."

    def handle(self, *args, **options):
        now = timezone.now()

        self.stdout.write("Clearing existing data...")
        ProofOfFixCertificate.objects.all().delete()
        EvidenceItem.objects.all().delete()
        Finding.objects.all().delete()
        IPCCommand.objects.all().delete()
        QuarantineItem.objects.all().delete()
        SecurityEvent.objects.all().delete()

        self.stdout.write("Seeding findings...")
        findings_data = [
            ("WM-LOCAL-001", "Session invalidation regression check", "Web App", "Session Manager",
             "Medium", 5.4, "Moderate — stale sessions could persist past logout", "In Progress", "A. Rao", 8),
            ("WM-AI-002", "Indirect prompt injection risk in external article processing", "AI Trust Firewall",
             "AI Summarizer", "Critical", 8.6, "High — could manipulate AI-generated intelligence summaries",
             "Open", "K. Iyer", 6),
            ("WM-PROTO-003", "Missing message freshness validation", "Protocol Safety Shield",
             "Event Stream Gateway", "High", 7.1, "High — replay of stale events could mislead operators",
             "Open", "S. Nair", 7),
            ("WM-TAURI-004", "Over-permissive simulated IPC command policy", "Desktop Trust Guard",
             "Node Sidecar", "High", 6.8, "Moderate — sidecar command surface broader than needed",
             "In Progress", "A. Rao", 9),
            ("WM-API-005", "API response exposes unnecessary metadata", "Protocol Safety Shield",
             "REST API Gateway", "Low", 3.2, "Low — minor information disclosure", "Resolved", "K. Iyer", 16),
            ("WM-WEB-006", "CSP policy improvement opportunity", "Web App", "Web Dashboard",
             "Low", 2.8, "Low — hardening opportunity", "Resolved", "S. Nair", 18),
            ("WM-DATA-007", "Sensitive client-side storage review required", "Data Layer", "Cache Store",
             "Medium", 4.9, "Moderate — cached data retention beyond policy", "Open", "A. Rao", 5),
            ("WM-AUTH-008", "MFA bypass on stale refresh token reuse", "Web App", "Authentication Service",
             "High", 7.4, "High — refresh tokens not revoked after password change", "Open", "K. Iyer", 4),
            ("WM-PROTO-009", "Protocol Buffer field number reuse across versions", "Protocol Safety Shield",
             "Protocol Buffer Services", "Medium", 5.0, "Moderate — schema drift could misinterpret field semantics",
             "Open", "S. Nair", 3),
            ("WM-AI-010", "Insufficient rate limiting on AI summarization endpoint", "AI Trust Firewall",
             "AI Processing Layer", "Medium", 5.6, "Moderate — could enable resource exhaustion via bulk feed submission",
             "In Progress", "K. Iyer", 6),
            ("WM-TAURI-011", "Sidecar process lacks audit log rotation policy", "Desktop Trust Guard",
             "Node Sidecar", "Low", 3.5, "Low — log growth could obscure forensic review over time",
             "Open", "A. Rao", 11),
            ("WM-API-012", "Missing pagination limit on bulk export endpoint", "Protocol Safety Shield",
             "REST API Gateway", "Medium", 4.6, "Moderate — large exports could degrade gateway performance",
             "Resolved", "S. Nair", 15),
            ("WM-WEB-013", "Clickjacking protection missing on embedded widget view", "Web App", "Web Dashboard",
             "Medium", 4.3, "Moderate — dashboard widget could be framed by malicious page", "Open", "S. Nair", 2),
            ("WM-DATA-014", "Encryption key rotation overdue on cache store", "Data Layer", "Cache and Data Store",
             "High", 6.5, "High — key age exceeds internal rotation policy", "Open", "A. Rao", 3),
            ("WM-AUTH-015", "Verbose authentication error messages aid enumeration", "Web App",
             "Authentication Service", "Low", 3.0, "Low — error text distinguishes valid vs invalid usernames",
             "Resolved", "K. Iyer", 21),
            ("WM-TAURI-016", "External URL open command lacks domain allowlist enforcement", "Desktop Trust Guard",
             "Tauri Desktop Renderer", "High", 6.9, "High — arbitrary external navigation from desktop shell",
             "Open", "A. Rao", 4),
        ]
        findings = {}
        for fid, title, module, component, sev, cvss, risk, status, owner, days_ago in findings_data:
            f = Finding.objects.create(
                finding_id=fid, title=title, module=module, component=component,
                severity=sev, cvss=cvss, mission_risk=risk, status=status, owner=owner,
                poc_steps="1. Prepare controlled local test input\n2. Submit via authorized local test harness\n"
                          "3. Observe simulated system response\n4. Record evidence in Evidence Vault",
                remediation="Apply schema-level validation and boundary enforcement at the affected trust layer; "
                            "add regression test to CI.",
                updated_at=now - timedelta(days=days_ago),
            )
            findings[fid] = f

        self.stdout.write("Seeding evidence vault...")
        evidence_data = [
            ("EV-001", "HTTP Request/Response", "WM-AI-002", "K. Iyer", "a3f9c81e00", True),
            ("EV-002", "Log File", "WM-PROTO-003", "S. Nair", "9b1d44aa11", True),
            ("EV-003", "Screenshot", "WM-TAURI-004", "A. Rao", "71ce0f3b22", False),
            ("EV-004", "Code Reference", "WM-LOCAL-001", "A. Rao", "de449a1233", False),
            ("EV-005", "Test Payload", "WM-DATA-007", "K. Iyer", "55aabb9044", True),
            ("EV-006", "Log File", "WM-AUTH-008", "K. Iyer", "6cd111ef55", True),
            ("EV-007", "HTTP Request/Response", "WM-AUTH-008", "K. Iyer", "2b709c0466", True),
            ("EV-008", "Screen Recording", "WM-TAURI-016", "A. Rao", "f01a5d3e77", False),
            ("EV-009", "Code Reference", "WM-PROTO-009", "S. Nair", "88bb2e7788", False),
            ("EV-010", "Test Payload", "WM-API-012", "S. Nair", "c412aa6f99", True),
            ("EV-011", "Analyst Note", "WM-DATA-014", "A. Rao", "0d9e773c00", False),
            ("EV-012", "Screenshot", "WM-WEB-013", "S. Nair", "3a5f66b111", False),
        ]
        for eid, etype, fid, by, h, redacted in evidence_data:
            EvidenceItem.objects.create(
                evidence_id=eid, evidence_type=etype, finding=findings.get(fid),
                captured_by=by, sha256=h, redacted=redacted,
                content_preview="Authorization: Bearer [REDACTED]\nCookie: session=[REDACTED]\nX-Api-Key: [REDACTED]"
                if redacted else "Local file reference / non-sensitive artifact.",
            )

        self.stdout.write("Seeding IPC command inventory...")
        ipc_data = [
            ("get_app_version", "Low", "Strict", "Allowed"),
            ("export_report", "Medium", "Strict", "Allowed"),
            ("open_external_link", "Medium", "Allowlist", "Allowed"),
            ("fetch_local_cache", "Low", "Strict", "Allowed"),
            ("sync_data", "Medium", "Strict", "Allowed"),
            ("read_config", "Low", "Strict", "Allowed"),
            ("write_config", "Medium", "Strict", "Allowed"),
            ("get_system_info", "Low", "Strict", "Allowed"),
            ("save_evidence_file", "Medium", "Allowlist", "Allowed"),
            ("open_devtools", "High", "Allowlist", "Under Review"),
            ("launch_update_checker", "Medium", "Strict", "Allowed"),
            ("clipboard_read", "High", "None", "Blocked"),
            ("simulated_sensitive_command", "Critical", "None", "Under Review"),
        ]
        for name, risk, origin, status in ipc_data:
            IPCCommand.objects.create(name=name, risk=risk, origin_policy=origin, status=status)

        self.stdout.write("Seeding quarantine queue...")
        quarantine_data = [
            ("QC-101", "globalwire-news.example", "Prompt Injection Pattern", "Critical"),
            ("QC-102", "openfeed.example", "Hidden Instruction Block", "High"),
            ("QC-103", "dailybrief.example", "Suspicious Markdown Payload", "Medium"),
            ("QC-104", "newsaggr.example", "Encoded Directive String", "High"),
            ("QC-105", "regionwatch.example", "Source Spoofing Indicator", "Medium"),
            ("QC-106", "freshreports.example", "Excessive Link Redirection", "Low"),
            ("QC-107", "briefnet.example", "Prompt Injection Pattern", "Critical"),
            ("QC-108", "wirefeed.example", "Unicode Obfuscation", "Medium"),
        ]
        for qid, source, threat, risk in quarantine_data:
            QuarantineItem.objects.create(quarantine_id=qid, source=source, threat_type=threat, risk=risk)

        self.stdout.write("Seeding recent security events...")
        events_data = [
            ("Prompt injection attempt quarantined (source: globalwire-news.example)", "info", 2),
            ("Oversized payload rejected (evt-88213, sensor-node-04)", "info", 11),
            ("Unsafe IPC command blocked (simulated_sensitive_command)", "warn", 40),
            ("Session policy regression test passed (WM-LOCAL-001)", "info", 60),
            ("API contract drift detected (client v1.7 vs server v2.0)", "warn", 180),
            ("Replay attempt blocked (duplicate eventId evt-88099)", "info", 300),
            ("MFA bypass finding opened (WM-AUTH-008)", "critical", 480),
            ("Fix verified — encryption key rotation in progress (WM-DATA-014)", "info", 1440),
        ]
        for msg, level, mins_ago in events_data:
            SecurityEvent.objects.create(message=msg, level=level, occurred_at=now - timedelta(minutes=mins_ago))

        self.stdout.write("Seeding proof-of-fix certificates...")
        cert_data = [
            ("POF-2026-0088", "WM-API-005", "commit 7b2fa41", "0d9e773caa"),
            ("POF-2026-0089", "WM-WEB-006", "commit c91ab02", "3a5f66b1bb"),
            ("POF-2026-0090", "WM-API-012", "commit e42fd19", "c412aa6fcc"),
            ("POF-2026-0091", "WM-AUTH-015", "commit a91fe2c", "7fa192bddd"),
        ]
        for cert_id, fid, patch, ehash in cert_data:
            if fid in findings:
                ProofOfFixCertificate.objects.create(
                    cert_id=cert_id, finding=findings[fid], patch_reference=patch,
                    evidence_hash=ehash, test_result="Passed",
                )

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {Finding.objects.count()} findings, {EvidenceItem.objects.count()} evidence items, "
            f"{IPCCommand.objects.count()} IPC commands, {QuarantineItem.objects.count()} quarantine items, "
            f"{SecurityEvent.objects.count()} security events, {ProofOfFixCertificate.objects.count()} certificates."
        ))
