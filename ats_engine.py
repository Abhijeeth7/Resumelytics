from typing import List, Dict, Any

# 🔥 MUST match jd_parser aliases
SKILL_NORMALIZATION = {
    "aws": "amazon web services",
    "k8s": "kubernetes",
    "github action": "github actions",
    "gh actions": "github actions",
    "js": "javascript",
    "tf": "terraform",
}


class ATSEngine:
    def __init__(self, jd_skills: List[str], candidate_skills: List[str]) -> None:
        # ✅ normalize JD skills
        self.jd_skills = set(s.lower().strip() for s in jd_skills)

        # 🔥 normalize candidate skills using alias map
        normalized_candidate: List[str] = []

        for skill in candidate_skills:
            s = skill.lower().strip()

            if s in SKILL_NORMALIZATION:
                s = SKILL_NORMALIZATION[s]

            normalized_candidate.append(s)

        self.candidate_skills = set(normalized_candidate)

    def compute_skill_match(self) -> Dict[str, Any]:
        if not self.jd_skills:
            return {
                "skill_match_percent": 0.0,
                "matched_skills": [],
                "missing_skills": [],
                "strength": "No JD skills found",
            }

        matched = self.jd_skills.intersection(self.candidate_skills)
        missing = self.jd_skills.difference(self.candidate_skills)

        match_percent = (len(matched) / len(self.jd_skills)) * 100

        return {
            "skill_match_percent": round(match_percent, 2),
            "matched_skills": sorted(matched),
            "missing_skills": sorted(missing),
            "strength": self._strength_label(match_percent),
        }

    def _strength_label(self, percent: float) -> str:
        if percent >= 80:
            return "Strong Match"
        if percent >= 60:
            return "Good Match"
        if percent >= 40:
            return "Moderate Match"
        return "Weak Match"