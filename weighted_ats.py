from typing import Dict, Any, List

SKILL_NORMALIZATION = {
    "aws": "amazon web services",
    "k8s": "kubernetes",
    "github action": "github actions",
    "gh actions": "github actions",
    "js": "javascript",
    "tf": "terraform",
}

class WeightedATSEngine:
    def __init__(
        self,
        skill_match_percent: float,
        candidate_experience: int | None,
        required_experience: int | None,
        resume_text: str,
        required_skills: List[str],
        preferred_skills: List[str],
    ) -> None:
        self.skill_match_percent = skill_match_percent
        self.candidate_experience = candidate_experience
        self.required_experience = required_experience
        self.resume_text = resume_text.lower()
        # normalize resume aliases
        for alias, canonical in SKILL_NORMALIZATION.items():
            self.resume_text = self.resume_text.replace(alias, canonical)

        # normalize skill groups
        self.required_skills = [s.lower() for s in required_skills]
        self.preferred_skills = [s.lower() for s in preferred_skills]

    # =============================
    # Experience Score
    # =============================
    def _experience_score(self) -> float:
        if self.required_experience is None:
            return 100.0

        if self.candidate_experience is None:
            return 50.0

        if self.candidate_experience >= self.required_experience:
            return 100.0

        gap = self.required_experience - self.candidate_experience
        penalty = min(gap * 20, 100)
        return max(0.0, 100 - penalty)

    # =============================
    # 🔥 NEW: Weighted Keyword Score
    # =============================
    def _keyword_score(self) -> float:
        total_weight = 0
        hits = 0

        # required skills → weight 2
        for skill in self.required_skills:
            total_weight += 2
            if skill in self.resume_text:
                hits += 2

        # preferred skills → weight 1
        for skill in self.preferred_skills:
            total_weight += 1
            if skill in self.resume_text:
                hits += 1

        if total_weight == 0:
            return 0.0

        return (hits / total_weight) * 100

    # =============================
    # Final Weighted Score
    # =============================
    def compute(self) -> Dict[str, Any]:
        skill_score = self.skill_match_percent
        exp_score = self._experience_score()
        keyword_score = self._keyword_score()

        final_score = (
            0.40 * skill_score
            + 0.25 * exp_score
            + 0.20 * keyword_score
            + 0.15 * 100  # resume quality placeholder
        )

        return {
            "final_ats_score": round(final_score, 2),
            "skill_score": round(skill_score, 2),
            "experience_score": round(exp_score, 2),
            "keyword_score": round(keyword_score, 2),
            "strength": self._label(final_score),
        }

    def _label(self, score: float) -> str:
        if score >= 80:
            return "Excellent Fit"
        if score >= 65:
            return "Strong Fit"
        if score >= 50:
            return "Moderate Fit"
        return "Weak Fit"