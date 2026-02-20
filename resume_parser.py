import re
from typing import List, Dict

from jd_parser import SKILL_ALIASES  # reuse knowledge


class ResumeParser:
    def __init__(self, resume_text: str) -> None:
        self.raw_text = resume_text
        self.cleaned_text = self._clean_text()

    def _clean_text(self) -> str:
        return self.raw_text.replace("\n", " ").lower()

    def extract_skills(self) -> List[str]:
        BASE_SKILLS = [
            "python",
            "sql",
            "docker",
            "kubernetes",
            "jenkins",
            "terraform",
            "ansible",
            "github actions",
            "grafana",
            "prometheus",
            "helm",
            "golang",
            "datadog",
            "amazon web services",
        ]

        found = set()

        def matches(term: str) -> bool:
            pattern = r"\b" + re.escape(term) + r"\b"
            return re.search(pattern, self.cleaned_text) is not None

        # base skills
        for skill in BASE_SKILLS:
            if matches(skill):
                found.add(skill)

        # alias normalization
        for canonical, aliases in SKILL_ALIASES.items():
            for alias in aliases:
                if matches(alias):
                    found.add(canonical)

        return sorted(found)

    def extract_experience(self) -> int | None:
        match = re.search(r"(\d+)\+?\s*years", self.cleaned_text)
        if match:
            return int(match.group(1))
        return None

    def parse(self) -> Dict:
        return {
            "skills": self.extract_skills(),
            "experience": self.extract_experience(),
        }