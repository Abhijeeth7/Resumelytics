from typing import List, Dict, Any


class WeightedSkillMatcher:
    def __init__(
        self,
        required_skills: List[str],
        preferred_skills: List[str],
        candidate_skills: List[str],
    ) -> None:

        self.required = set(s.lower() for s in required_skills)
        self.preferred = set(s.lower() for s in preferred_skills)
        self.candidate = set(s.lower() for s in candidate_skills)

    # =============================
    # Required score (heavy weight)
    # =============================
    def _required_score(self) -> float:
        if not self.required:
            return 100.0

        matched = self.required.intersection(self.candidate)
        return (len(matched) / len(self.required)) * 100

    # =============================
    # Preferred score (lighter)
    # =============================
    def _preferred_score(self) -> float:
        if not self.preferred:
            return 100.0

        matched = self.preferred.intersection(self.candidate)
        return (len(matched) / len(self.preferred)) * 100

    # =============================
    # Final weighted skill score
    # =============================
    def compute(self) -> Dict[str, Any]:
        req_score = self._required_score()
        pref_score = self._preferred_score()

        final_skill_score = (0.7 * req_score) + (0.3 * pref_score)

        return {
            "required_score": round(req_score, 2),
            "preferred_score": round(pref_score, 2),
            "final_skill_score": round(final_skill_score, 2),
            "strength": self._label(final_skill_score),
        }

    def _label(self, score: float) -> str:
        if score >= 80:
            return "Strong Skill Fit"
        if score >= 60:
            return "Good Skill Fit"
        if score >= 40:
            return "Moderate Skill Fit"
        return "Weak Skill Fit"