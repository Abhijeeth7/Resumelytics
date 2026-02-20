import re
from typing import List, Dict, Optional

SKILL_ALIASES: Dict[str, List[str]] = {
    "kubernetes": ["k8s"],
    "javascript": ["js"],
    "github actions": ["github action", "gh actions"],
    "golang": ["go language"],
    "amazon web services": ["aws"],
    "terraform": ["tf"],
}

REQUIRED_HINTS = [
    "must have",
    "required",
    "strong proficiency",
    "mandatory",
    "expertise in",
]

PREFERRED_HINTS = [
    "good to have",
    "nice to have",
    "plus",
    "preferred",
    "preferred skills",
    "familiarity with",
    "exposure to",
]


class JDParser:
    def __init__(self, jd_text: str) -> None:
        self.raw_text: str = jd_text
        self.cleaned_text: str = self.clean_text()

    def clean_text(self) -> str:
        text: str = self.raw_text.replace("\n", " ")
        return text.strip()

    # =========================================
    # Skill Extraction
    # =========================================
    def extract_skills(self) -> List[str]:
        BASE_SKILLS: List[str] = [
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
            "snowflake",
            "AIML"
        ]

        lower_text: str = self.cleaned_text.lower()
        found: set[str] = set()

        def matches(term: str) -> bool:
            pattern = r"\b" + re.escape(term.lower()) + r"\b"
            return re.search(pattern, lower_text) is not None

        # Base skills
        for skill in BASE_SKILLS:
            if matches(skill):
                found.add(skill)

        # Alias normalization
        for canonical, aliases in SKILL_ALIASES.items():
            for alias in aliases:
                if matches(alias):
                    found.add(canonical)

        return sorted(found)

    # =========================================
    # NEW: Required vs Preferred Classification
    # =========================================
    def classify_skills(self) -> Dict[str, List[str]]:
        base_skills = self.extract_skills()
        text = self.cleaned_text.lower()

        required = set()
        preferred = set()

        for skill in base_skills:
            pattern = r".{0,80}" + re.escape(skill) + r".{0,80}"
            matches = re.findall(pattern, text)
            context = " ".join(matches)

            if any(hint in context for hint in REQUIRED_HINTS):
                required.add(skill)
            elif any(hint in context for hint in PREFERRED_HINTS):
                preferred.add(skill)
            else:
                preferred.add(skill)
        return {
            "required_skills": sorted(required),
            "preferred_skills": sorted(preferred),
        }

    # =========================================
    # Experience Extraction
    # =========================================
    def extract_experience(self) -> Optional[int]:
        match = re.search(r"(\d+)\+?\s*years", self.cleaned_text.lower())
        if match:
            return int(match.group(1))
        return None

    # =========================================
    # Final Parse
    # =========================================
    def parse(self) -> Dict[str, object]:
        skill_groups = self.classify_skills()

        return {
            "skills": self.extract_skills(),
            "required_skills": skill_groups["required_skills"],
            "preferred_skills": skill_groups["preferred_skills"],
            "experience_required": self.extract_experience(),
        }