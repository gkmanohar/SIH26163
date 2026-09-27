from django.db import models
from django.utils import timezone


SEVERITY_CHOICES = [
    ("Critical", "Critical"),
    ("High", "High"),
    ("Medium", "Medium"),
    ("Low", "Low"),
    ("Informational", "Informational"),
]

STATUS_CHOICES = [
    ("Open", "Open"),
    ("In Progress", "In Progress"),
    ("Resolved", "Resolved"),
]

MODULE_CHOICES = [
    ("Web App", "Web App"),
    ("AI Trust Firewall", "AI Trust Firewall"),
    ("Protocol Safety Shield", "Protocol Safety Shield"),
    ("Desktop Trust Guard", "Desktop Trust Guard"),
    ("Data Layer", "Data Layer"),
]


class Finding(models.Model):
    finding_id = models.CharField(max_length=32, unique=True)
    title = models.CharField(max_length=255)
    module = models.CharField(max_length=64, choices=MODULE_CHOICES)
    component = models.CharField(max_length=128)
    severity = models.CharField(max_length=16, choices=SEVERITY_CHOICES)
    cvss = models.DecimalField(max_digits=3, decimal_places=1)
    mission_risk = models.TextField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="Open")
    owner = models.CharField(max_length=64)
    poc_steps = models.TextField(blank=True, default="")
    remediation = models.TextField(blank=True, default="")
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.finding_id} — {self.title}"

    def severity_rank(self):
        order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Informational": 4}
        return order.get(self.severity, 5)


class EvidenceItem(models.Model):
    TYPE_CHOICES = [
        ("Screenshot", "Screenshot"),
        ("HTTP Request/Response", "HTTP Request/Response"),
        ("Code Reference", "Code Reference"),
        ("Log File", "Log File"),
        ("Screen Recording", "Screen Recording"),
        ("Test Payload", "Test Payload"),
        ("Analyst Note", "Analyst Note"),
    ]
    evidence_id = models.CharField(max_length=32, unique=True)
    evidence_type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    finding = models.ForeignKey(Finding, on_delete=models.SET_NULL, null=True, blank=True, related_name="evidence")
    captured_by = models.CharField(max_length=64)
    sha256 = models.CharField(max_length=80)
    redacted = models.BooleanField(default=False)
    content_preview = models.TextField(blank=True, default="")
    captured_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-captured_at"]

    def __str__(self):
        return self.evidence_id


class IPCCommand(models.Model):
    RISK_CHOICES = [("Low", "Low"), ("Medium", "Medium"), ("High", "High"), ("Critical", "Critical")]
    ORIGIN_CHOICES = [("Strict", "Strict"), ("Allowlist", "Allowlist"), ("None", "None")]
    STATUS_CHOICES = [("Allowed", "Allowed"), ("Blocked", "Blocked"), ("Under Review", "Under Review")]

    name = models.CharField(max_length=64, unique=True)
    risk = models.CharField(max_length=16, choices=RISK_CHOICES)
    origin_policy = models.CharField(max_length=16, choices=ORIGIN_CHOICES)
    param_validation = models.CharField(max_length=8, default="Pass")
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="Allowed")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class QuarantineItem(models.Model):
    RISK_CHOICES = [("Low", "Low"), ("Medium", "Medium"), ("High", "High"), ("Critical", "Critical")]
    STATUS_CHOICES = [("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")]

    quarantine_id = models.CharField(max_length=32, unique=True)
    source = models.CharField(max_length=128)
    threat_type = models.CharField(max_length=128)
    risk = models.CharField(max_length=16, choices=RISK_CHOICES)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="Pending")
    detected_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-detected_at"]

    def __str__(self):
        return self.quarantine_id


class SecurityEvent(models.Model):
    LEVEL_CHOICES = [("info", "info"), ("warn", "warn"), ("critical", "critical")]
    message = models.CharField(max_length=255)
    level = models.CharField(max_length=16, choices=LEVEL_CHOICES, default="info")
    occurred_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-occurred_at"]

    def __str__(self):
        return self.message


class ProofOfFixCertificate(models.Model):
    cert_id = models.CharField(max_length=32, unique=True)
    finding = models.ForeignKey(Finding, on_delete=models.CASCADE, related_name="certificates")
    patch_reference = models.CharField(max_length=64)
    test_result = models.CharField(max_length=16, default="Passed")
    evidence_hash = models.CharField(max_length=80)
    signed_by = models.CharField(max_length=128, default="Sentinel Trinity Assessment Engine")
    issued_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-issued_at"]

    def __str__(self):
        return self.cert_id
