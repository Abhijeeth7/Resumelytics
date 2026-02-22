from jd_parser import JDParser
from eligibility_engine import EligibilityEngine
from ats_engine import ATSEngine  # legacy basic matcher (optional)
from resume_parser import ResumeParser
from resume_reader import ResumeReader
from weighted_ats import WeightedATSEngine
from ats_weighted_skill import WeightedSkillMatcher


def main() -> None:
    print("\n========== RESUMELYTICS PIPELINE START ==========\n")

    # ======================================================
    # STEP 1: Read Resume
    # ======================================================
    resume_path = "data/MohanAbhijeethAccenture.pdf"

    reader = ResumeReader(resume_path)
    resume_text = reader.extract_text()

    resume_parser = ResumeParser(resume_text)
    candidate_data = resume_parser.parse()

    print("Candidate Data:", candidate_data)

    # ======================================================
    # STEP 2: Parse JD
    # ======================================================
    jd_sample = """
    Design, develop, and maintain data pipelines and ETL processes using AWS and Snowflake.
    Strong proficiency in AWS and Snowflake. Looking for candidates with 3+ years of experience.
    Preferred skills are basics in AIML.
    """

    jd_parser = JDParser(jd_sample)
    result = jd_parser.parse()

    print("JD Data:", result)

    # ======================================================
    # STEP 3: Eligibility Check
    # ======================================================
    candidate_profile = {
        "experience": candidate_data.get("experience"),
        "skills": candidate_data.get("skills", []),
    }

    engine = EligibilityEngine(result, candidate_profile)
    decision = engine.evaluate()

    print("Eligibility:", decision)

    if not decision["eligible"]:
        print("❌ You might not be a good fit, so better ignore!")
        return

    # ======================================================
    # STEP 4: (Optional) Basic ATS Match
    # ======================================================
    ats = ATSEngine(result["skills"], candidate_data["skills"])
    ats_result = ats.compute_skill_match()
    print("Basic ATS Result:", ats_result)

    # ======================================================
    # STEP 5: Required vs Preferred Skill Matching (CORE)
    # ======================================================
    skill_engine = WeightedSkillMatcher(
        required_skills=result["required_skills"],
        preferred_skills=result["preferred_skills"],
        candidate_skills=candidate_data["skills"],
    )

    skill_result = skill_engine.compute()
    print("Weighted Skill Result:", skill_result)

    # ======================================================
    # STEP 6: Final Weighted ATS Score
    # ======================================================
    weighted = WeightedATSEngine(
        skill_match_percent=skill_result["final_skill_score"],  # ✅ correct signal
        candidate_experience=candidate_data.get("experience"),
        required_experience=result.get("experience_required"),
        resume_text=resume_text,
        required_skills=result["required_skills"],
        preferred_skills=result["preferred_skills"],
    )

    weighted_result = weighted.compute()
    print("Final Weighted ATS:", weighted_result)

    print("\n========== RESUMELYTICS PIPELINE END ==========\n")


# ======================================================
# ENTRY POINT
# ======================================================
if __name__ == "__main__":
    main()
