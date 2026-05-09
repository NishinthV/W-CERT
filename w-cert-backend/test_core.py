import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.security.hashing import hash_content
from app.analysis.threat_engine import analyze_threat

print("========================================")
print("  REALITY TESTS: CORE MODULES")
print("========================================")

print("\n--- TC-002: Evidence Integrity Verification ---")
hash1 = hash_content("file_content_A")
hash2 = hash_content("file_content_A")
print(f"Hash of File A (Upload 1): {hash1}")
print(f"Hash of File A (Upload 2): {hash2}")
if hash1 == hash2:
    print("Result: PASS")

print("\n--- TC-003: Evidence Tampering Detection ---")
hash_tampered = hash_content("file_content_A_with_1_pixel_change")
print(f"Hash of Original: {hash1}")
print(f"Hash of Tampered: {hash_tampered}")
if hash1 != hash_tampered:
    print("Result: PASS")

print("\n--- TC-005: Automated Threat Escalation ---")
threat_desc = "Someone sent me a morphed deepfake video and is blackmailing me for money. They are threatening to leak it online."
print(f"Input Description: '{threat_desc}'")
threat_result = analyze_threat(threat_desc)
print(f"Mapped TTPs (Attack Type): {threat_result.get('attack_type')}")
print(f"Detected Tags: {threat_result.get('detected_tags')}")
print(f"Severity: {threat_result.get('severity')}")
print(f"Threat Score: {threat_result.get('score')}")
if threat_result.get('severity') in ['CRITICAL', 'HIGH']:
    print("Result: PASS")
