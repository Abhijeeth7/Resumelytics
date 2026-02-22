from typing import Dict, Any


class EligibilityEngine:
    def __init__(self, jd_data: Dict[str, Any], candidate_profile: Dict[str, Any]) -> None:
        self.jd: Dict[str, Any] = jd_data
        self.candidate: Dict[str, Any] = candidate_profile

    def check_required_skills(self) -> tuple[bool, list[str]]:
        required_skills = {
            str(skill).lower().strip()
            for skill in self.jd.get("required_skills", [])
            if str(skill).strip()
        }
        candidate_skills = {
            str(skill).lower().strip()
            for skill in self.candidate.get("skills", [])
            if str(skill).strip()
        }

        missing = sorted(required_skills.difference(candidate_skills))
        return len(missing) == 0, missing

    def check_experience(self) -> bool:
        required = self.jd.get("experience_required")
        candidate_exp = self.candidate.get("experience")

        if required is not None and candidate_exp is not None:
            if candidate_exp < required:
                return False

        return True

    def evaluate(self) -> Dict[str, Any]:
        required_ok, missing_required = self.check_required_skills()
        if not required_ok:
            return {
                "eligible": False,
                "reason": f"Missing required skills: {', '.join(missing_required)}",
            }

        if not self.check_experience():
            return {
                "eligible": False,
                "reason": "Insufficient experience",
            }

        return {
            "eligible": True,
            "reason": "Meets basic requirements",
        }
