from typing import Dict, Any


class EligibilityEngine:
    def __init__(self, jd_data: Dict[str, Any], candidate_profile: Dict[str, Any]) -> None:
        self.jd: Dict[str, Any] = jd_data
        self.candidate: Dict[str, Any] = candidate_profile

    def check_experience(self) -> bool:
        required = self.jd.get("experience_required")
        candidate_exp = self.candidate.get("experience")

        if required is not None and candidate_exp is not None:
            if candidate_exp < required:
                return False

        return True

    def evaluate(self) -> Dict[str, Any]:
        if not self.check_experience():
            return {
                "eligible": False,
                "reason": "Insufficient experience",
            }

        return {
            "eligible": True,
            "reason": "Meets basic requirements",
        }