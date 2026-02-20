from jd_parser import JDParser
from eligibility_engine import EligibilityEngine
from ats_engine import ATSEngine
from resume_parser import ResumeParser
from resume_reader import ResumeReader
from weighted_ats import WeightedATSEngine

# ===============================
# STEP 1: Read Resume
# ===============================
resume_path = "data\MohanAbhijeethAccenture.pdf"  # ✅ corrected path

reader = ResumeReader(resume_path)
resume_text = reader.extract_text()

resume_parser = ResumeParser(resume_text)
candidate_data = resume_parser.parse()

print("Candidate Data:", candidate_data)

# ===============================
# STEP 2: Parse JD
# ===============================
jd_sample = """
Design, develop, and maintain data pipelines and ETL processes using AWS and Snowflake.
Strong proficiency in AWS and Snowflake. Looking for candidates with 3+ years of experience.
Preferred skills are basics in AIML.
"""

jd_parser = JDParser(jd_sample)
result = jd_parser.parse()

print("JD Data:", result)

# ===============================
# STEP 3: Build candidate profile
# ===============================
candidate_profile = {
    "experience": candidate_data.get("experience")
}

# ===============================
# STEP 4: Eligibility Check
# ===============================
engine = EligibilityEngine(result, candidate_profile)
decision = engine.evaluate()

print("Eligibility:", decision)

if not decision["eligible"]:
    print("You might not be a good fit, so better ignore!")
else:
    # ===============================
    # STEP 5: ATS Skill Match
    # ===============================
    ats = ATSEngine(result["skills"], candidate_data["skills"])
    ats_result = ats.compute_skill_match()

    print("ATS Result:", ats_result)

    # ===============================
    # STEP 6: Weighted ATS Score
    # ===============================
    weighted = WeightedATSEngine(
        skill_match_percent=ats_result["skill_match_percent"],
        candidate_experience=candidate_data.get("experience"),
        required_experience=result.get("experience_required"),
        resume_text=resume_text,
        required_skills=result["required_skills"],
        preferred_skills=result["preferred_skills"],
    )

    weighted_result = weighted.compute()
    print("Weighted ATS:", weighted_result)