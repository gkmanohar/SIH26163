from django.contrib import admin
from .models import Finding, EvidenceItem, IPCCommand, QuarantineItem, SecurityEvent, ProofOfFixCertificate


@admin.register(Finding)
class FindingAdmin(admin.ModelAdmin):
    list_display = ("finding_id", "title", "module", "severity", "status", "owner", "updated_at")
    list_filter = ("severity", "status", "module")
    search_fields = ("finding_id", "title")


@admin.register(EvidenceItem)
class EvidenceItemAdmin(admin.ModelAdmin):
    list_display = ("evidence_id", "evidence_type", "finding", "captured_by", "captured_at", "redacted")
    list_filter = ("evidence_type", "redacted")


@admin.register(IPCCommand)
class IPCCommandAdmin(admin.ModelAdmin):
    list_display = ("name", "risk", "origin_policy", "status")
    list_filter = ("risk", "status")


@admin.register(QuarantineItem)
class QuarantineItemAdmin(admin.ModelAdmin):
    list_display = ("quarantine_id", "source", "threat_type", "risk", "status", "detected_at")
    list_filter = ("risk", "status")


@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = ("message", "level", "occurred_at")


@admin.register(ProofOfFixCertificate)
class ProofOfFixCertificateAdmin(admin.ModelAdmin):
    list_display = ("cert_id", "finding", "test_result", "issued_at")
