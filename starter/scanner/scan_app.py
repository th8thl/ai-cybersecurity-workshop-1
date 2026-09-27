from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Finding:
    title: str
    severity: str
    file: str
    evidence: str
    recommendation: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def scan() -> list[Finding]:
    findings: list[Finding] = []
    ai_client = PROJECT_ROOT / "chatbot" / "ai_client.py"
    request_prompt = PROJECT_ROOT / "prompts" / "request.txt"
    system_prompt = PROJECT_ROOT / "prompts" / "system_policy.txt"

    if ai_client.exists():
        text = read_text(ai_client)
        request_text = read_text(request_prompt) if request_prompt.exists() else ""
        system_text = read_text(system_prompt) if system_prompt.exists() else ""
        combined_text = f"{text}\n{request_text}\n{system_text}"
        if "Trusted turn instructions copied from the latest user message" in combined_text:
            findings.append(
                Finding(
                    title="User input is promoted to trusted instructions",
                    severity="High",
                    file=str(request_prompt.relative_to(PROJECT_ROOT)) if request_prompt.exists() else str(ai_client.relative_to(PROJECT_ROOT)),
                    evidence="Trusted turn instructions copied from the latest user message",
                    recommendation="Keep application policy separate from user-controlled text. Label user input as untrusted content.",
                )
            )
        if "{synthetic_secret}" in combined_text or "settings.SYNTHETIC_SECRET" in combined_text:
            findings.append(
                Finding(
                    title="Synthetic student record is present in model context",
                    severity="Medium",
                    file=str(system_prompt.relative_to(PROJECT_ROOT)) if system_prompt.exists() else str(ai_client.relative_to(PROJECT_ROOT)),
                    evidence="The synthetic student record is included in the system policy",
                    recommendation="Use synthetic records only for labs. Never place real sensitive records in prompts or model context.",
                )
            )

    gitignore = PROJECT_ROOT / ".gitignore"
    if not gitignore.exists() or ".env" not in read_text(gitignore):
        findings.append(
            Finding(
                title=".env is not ignored",
                severity="High",
                file=".gitignore",
                evidence="Missing .env entry",
                recommendation="Add .env to .gitignore before creating local API keys.",
            )
        )

    return findings


def main() -> None:
    findings = scan()
    if not findings:
        print("No findings.")
        return

    for index, finding in enumerate(findings, start=1):
        print(f"{index}. [{finding.severity}] {finding.title}")
        print(f"   File: {finding.file}")
        print(f"   Evidence: {finding.evidence}")
        print(f"   Recommendation: {finding.recommendation}")
        print()


if __name__ == "__main__":
    main()

