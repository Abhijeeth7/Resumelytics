from __future__ import annotations

from typing import Any, Dict, List, Optional

from ats_weighted_skill import WeightedSkillMatcher
from eligibility_engine import EligibilityEngine
from jd_parser import JDParser
from resume_parser import ResumeParser
from weighted_ats import WeightedATSEngine


def evaluate_resume_against_jd(
    resume_text: str,
    jd_text: str,
    candidate_experience: Optional[int] = None,
) -> Dict[str, Any]:
    resume_data = ResumeParser(resume_text).parse()
    jd_data = JDParser(jd_text).parse()

    if candidate_experience is not None:
        resume_data["experience"] = candidate_experience

    candidate_profile = {
        "experience": resume_data.get("experience"),
        "skills": resume_data.get("skills", []),
    }

    eligibility = EligibilityEngine(jd_data, candidate_profile).evaluate()

    result: Dict[str, Any] = {
        "candidate_data": resume_data,
        "jd_data": jd_data,
        "eligibility": eligibility,
    }

    if not eligibility["eligible"]:
        return result

    weighted_skill = WeightedSkillMatcher(
        required_skills=jd_data["required_skills"],
        preferred_skills=jd_data["preferred_skills"],
        candidate_skills=resume_data["skills"],
    ).compute()

    weighted_ats = WeightedATSEngine(
        skill_match_percent=weighted_skill["final_skill_score"],
        candidate_experience=resume_data.get("experience"),
        required_experience=jd_data.get("experience_required"),
        resume_text=resume_text,
        required_skills=jd_data["required_skills"],
        preferred_skills=jd_data["preferred_skills"],
    ).compute()

    result["weighted_skill"] = weighted_skill
    result["weighted_ats"] = weighted_ats
    return result


def parse_skills_csv(skills_csv: str) -> List[str]:
    return [item.strip().lower() for item in skills_csv.split(",") if item.strip()]
