Project: Open Origin Architecture  
Repository: Tactical-Defense-Drone  
Lead Architect: Emanuel Schaaf  
Primary Contact: serviceblend@gmail.com

## Purpose
This document describes the Responsible Disclosure and security reporting process for this repository. Its goal is to enable secure, confidential, and responsible handling of security issues, sensitive data exposures, or misuse potential related to the project.

## Scope
**Materials** covered by this policy include source code, simulation models, telemetry data, documentation, diagrams, and any related files contained in this repository or provided privately by the project maintainers.

## What to Report
Please report only technical security issues or sensitive findings such as:
- Code vulnerabilities with security impact
- Leaked telemetry or personally identifiable information (PII)
- Evidence of misuse, unauthorized distribution, or operationalization risks
- Flaws that enable unauthorized reproduction, field deployment, or harm to third parties

Do **not** submit operational exploitation instructions, weaponization guides, or step‑by‑step deployment procedures.

## How to Report
Preferred reporting channels:
1. **Encrypted email** to serviceblend@gmail.com (PGP recommended).  
2. **Secure upload** (SFTP or encrypted link) by prior arrangement.  
3. Non‑sensitive reports may be sent by unencrypted email, but sensitive data must never be sent unencrypted.

Required information in a report:
- Short summary of the issue  
- Reproduction steps or a safe proof of concept (avoid operational details)  
- Affected files and commit hashes  
- Estimated severity and potential impact (if known)  
- Contact information for follow‑up (email, phone)  
- Optional: reporter PGP public key for encrypted correspondence

PGP: If you plan to encrypt your report, request the project PGP public key by email if it is not yet published in the repository.

## Handling and Timelines
- **Acknowledgement:** within 5 business days.  
- **Initial triage:** within 14 calendar days.  
- **Detailed response or status update:** within 30 calendar days. Complex cases may require up to 90 calendar days.  
- **Confidentiality:** Reports are handled confidentially. Public disclosure will only occur after coordination with the reporter and, if applicable, relevant authorities.

## Reporter Expectations
- Do not publicly disclose the vulnerability before coordination.  
- Do not test or exploit vulnerabilities in production or real‑world environments without explicit written authorization.  
- Cooperate in validation and remediation efforts.  
- Accredited researchers or official bodies may be asked to sign an NDA or formal collaboration agreement.

## Repository Policies
- Public repository content is limited to high‑level models, sanitized simulations, and descriptive documentation.  
- Sensitive artifacts, raw telemetry, or detailed simulation outputs are stored in private locations and shared only after verification and access agreements.  
- Do **not** open public issues for security reports. Public issues containing sensitive information will be removed and redirected to secure channels.

## Legal and Liability Notice
- This project is research‑stage (TRL 2–3) and is **not** certified for operational use.  
- Materials are provided “as is” without warranties. The Lead Architect disclaims all warranties and accepts no liability for damages arising from use, misuse, or attempted implementation.  
- Recipients should consult legal counsel and relevant authorities before conducting tests or field trials.

## Access Control and Verification
Access to non‑public materials will be granted only after verification of organizational status and purpose. The project maintainers may require:
- Proof of official affiliation  
- A signed Non‑Disclosure Agreement (NDA)  
- A designated point of contact

## Export Control and Compliance
Recipients must comply with all applicable export, import, sanctions, and other legal restrictions. It is the recipient’s responsibility to obtain any required authorizations.

## Termination and Return
Authorization may be revoked at any time. Upon termination, recipients must cease use and either destroy or return non‑public materials as directed.

## Contact and Escalation
Primary contact: serviceblend@gmail.com

If no satisfactory response is received within 30 days, resend the report with the subject line: "SECURITY ESCALATION".  
If the issue poses an immediate threat to persons or critical infrastructure, contact the appropriate authorities immediately and notify the project maintainers via the secure channel.

## Responsible Disclosure Acknowledgement
Thank you for acting responsibly. Your reports help ensure research proceeds safely and that risks to the public are minimized.
