from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import reflex as rx

# Allow importing project modules when Reflex runs inside `web/`.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from scoring_service import evaluate_resume_against_jd


class AppState(rx.State):
    resume_text: str = ""
    jd_text: str = ""
    experience_text: str = ""
    result_json: str = ""
    error_text: str = ""
    eligibility_text: str = "Awaiting analysis"
    score_text: str = "--"
    strength_text: str = "No signal"
    skill_preview: List[str] = []
    required_preview: List[str] = []

    def set_resume_text(self, value: str) -> None:
        self.resume_text = value

    def set_jd_text(self, value: str) -> None:
        self.jd_text = value

    def set_experience_text(self, value: str) -> None:
        self.experience_text = value

    def score(self) -> None:
        self.error_text = ""
        self.eligibility_text = "Analyzing..."
        self.score_text = "--"
        self.strength_text = "No signal"

        if not self.resume_text.strip() or not self.jd_text.strip():
            self.error_text = "Resume and JD text are required."
            self.eligibility_text = "Missing required text"
            return

        candidate_experience = None
        if self.experience_text.strip():
            try:
                candidate_experience = int(self.experience_text.strip())
            except ValueError:
                self.error_text = "Experience must be a whole number."
                self.eligibility_text = "Invalid experience value"
                return

        result: Dict[str, Any] = evaluate_resume_against_jd(
            resume_text=self.resume_text,
            jd_text=self.jd_text,
            candidate_experience=candidate_experience,
        )
        self.result_json = json.dumps(result, indent=2)

        eligibility = result.get("eligibility", {})
        eligible = bool(eligibility.get("eligible"))
        reason = str(eligibility.get("reason", ""))
        self.eligibility_text = (
            f"Eligible: {reason}" if eligible else f"Blocked: {reason}"
        )

        candidate_data = result.get("candidate_data", {})
        jd_data = result.get("jd_data", {})
        self.skill_preview = candidate_data.get("skills", [])[:6]
        self.required_preview = jd_data.get("required_skills", [])[:6]

        weighted_ats = result.get("weighted_ats")
        if weighted_ats:
            self.score_text = str(weighted_ats.get("final_ats_score", "--"))
            self.strength_text = str(weighted_ats.get("strength", "No signal"))
        elif not eligible:
            self.score_text = "0"
            self.strength_text = "Ineligible"


def _nav() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.text("RESUME", class_name="nav-brand-key"),
                rx.text("LYTICS", class_name="nav-brand-val"),
                spacing="2",
            ),
            rx.hstack(
                rx.link("Overview", href="#overview", class_name="nav-link"),
                rx.link("Pipeline", href="#pipeline", class_name="nav-link"),
                rx.link("Analyzer", href="#analyzer", class_name="nav-link"),
                rx.link("Footer", href="#site-footer", class_name="nav-link"),
                spacing="4",
                display=rx.breakpoints(initial="none", md="flex"),
            ),
            rx.link(
                rx.button("Launch Scanner", class_name="primary-btn nav-cta"),
                href="#analyzer",
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        class_name="glass-nav reveal",
    )


def _hero() -> rx.Component:
    return rx.box(
        rx.box(class_name="orb orb-a"),
        rx.box(class_name="orb orb-b"),
        rx.vstack(
            rx.text("ATS Intelligence Engine", class_name="hero-chip reveal"),
            rx.heading(
                "Build Resume Confidence Before You Click Apply.",
                class_name="hero-title reveal delay-1",
            ),
            rx.text(
                "Resumelytics scores required skills, preferred skills, and experience fit with a hiring-grade weighted pipeline.",
                class_name="hero-subtitle reveal delay-2",
            ),
            rx.hstack(
                rx.link(
                    rx.button("Run Analyzer", class_name="primary-btn reveal delay-3"),
                    href="#analyzer",
                ),
                rx.link(
                    rx.button("View Pipeline", class_name="ghost-btn reveal delay-4"),
                    href="#pipeline",
                ),
                spacing="3",
            ),
            rx.grid(
                rx.box(
                    rx.text("Weighted Skill Model", class_name="metric-label"),
                    rx.text("Required 70% and Preferred 30%", class_name="metric-value"),
                    class_name="metric-card reveal delay-1",
                ),
                rx.box(
                    rx.text("Eligibility Gate", class_name="metric-label"),
                    rx.text("Required skills and experience checks", class_name="metric-value"),
                    class_name="metric-card reveal delay-2",
                ),
                rx.box(
                    rx.text("Chrome and Web Ready", class_name="metric-label"),
                    rx.text("Single backend scoring contract", class_name="metric-value"),
                    class_name="metric-card reveal delay-3",
                ),
                columns=rx.breakpoints(initial="1", md="3"),
                width="100%",
                spacing="4",
            ),
            spacing="5",
            width="100%",
            max_width="1120px",
        ),
        id="overview",
        class_name="hero-shell",
    )


def _pipeline_section() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text("Pipeline", class_name="section-chip reveal"),
            rx.heading("How The Scoring Works", class_name="section-title reveal delay-1"),
            rx.grid(
                rx.box(
                    rx.text("01", class_name="step-index"),
                    rx.text("JD Parsing", class_name="step-title"),
                    rx.text(
                        "Extracts skills, classifies required vs preferred, and detects experience requirements.",
                        class_name="step-body",
                    ),
                    class_name="step-card reveal delay-1",
                ),
                rx.box(
                    rx.text("02", class_name="step-index"),
                    rx.text("Eligibility Engine", class_name="step-title"),
                    rx.text(
                        "Hard-gates missing required skills and experience mismatch before final scoring.",
                        class_name="step-body",
                    ),
                    class_name="step-card reveal delay-2",
                ),
                rx.box(
                    rx.text("03", class_name="step-index"),
                    rx.text("Weighted ATS Output", class_name="step-title"),
                    rx.text(
                        "Computes final fit score and strength labels for faster, data-backed decisions.",
                        class_name="step-body",
                    ),
                    class_name="step-card reveal delay-3",
                ),
                columns=rx.breakpoints(initial="1", md="3"),
                spacing="4",
                width="100%",
            ),
            spacing="4",
            width="100%",
            max_width="1120px",
        ),
        id="pipeline",
        class_name="section-shell",
    )


def _form_panel() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text("Analyzer", class_name="section-chip"),
            rx.heading("Live ATS Simulation", class_name="section-title"),
            rx.text(
                "Paste resume and JD text. The backend pipeline remains the source of truth.",
                class_name="section-subtitle",
            ),
            rx.grid(
                rx.vstack(
                    rx.text("Resume Content", class_name="field-label"),
                    rx.text_area(
                        placeholder="Paste your complete resume text...",
                        value=AppState.resume_text,
                        on_change=AppState.set_resume_text,
                        class_name="input-surface code-font",
                    ),
                    rx.text("Job Description", class_name="field-label"),
                    rx.text_area(
                        placeholder="Paste target JD text...",
                        value=AppState.jd_text,
                        on_change=AppState.set_jd_text,
                        class_name="input-surface code-font",
                    ),
                    rx.text("Experience (Optional, years)", class_name="field-label"),
                    rx.input(
                        placeholder="e.g. 3",
                        value=AppState.experience_text,
                        on_change=AppState.set_experience_text,
                        class_name="input-inline code-font",
                    ),
                    rx.button(
                        "Compute ATS Score",
                        on_click=AppState.score,
                        class_name="primary-btn pulse-on-hover",
                    ),
                    rx.cond(
                        AppState.error_text != "",
                        rx.text(AppState.error_text, class_name="error-text"),
                        rx.fragment(),
                    ),
                    spacing="3",
                    width="100%",
                ),
                rx.vstack(
                    rx.box(
                        rx.hstack(
                            rx.vstack(
                                rx.text("Current ATS", class_name="status-label"),
                                rx.text(AppState.score_text, class_name="score-value"),
                                align="start",
                                spacing="1",
                            ),
                            rx.vstack(
                                rx.text("Strength", class_name="status-label"),
                                rx.text(AppState.strength_text, class_name="strength-value"),
                                align="start",
                                spacing="1",
                            ),
                            justify="between",
                            width="100%",
                        ),
                        class_name="status-card",
                    ),
                    rx.box(
                        rx.text("Eligibility", class_name="status-label"),
                        rx.text(AppState.eligibility_text, class_name="eligibility-value"),
                        class_name="status-card",
                    ),
                    rx.box(
                        rx.text("Candidate Skills Snapshot", class_name="status-label"),
                        rx.hstack(
                            rx.foreach(
                                AppState.skill_preview,
                                lambda item: rx.text(item, class_name="tag-chip"),
                            ),
                            style={"flex_wrap": "wrap"},
                            spacing="2",
                        ),
                        class_name="status-card",
                    ),
                    rx.box(
                        rx.text("Required Skills Snapshot", class_name="status-label"),
                        rx.hstack(
                            rx.foreach(
                                AppState.required_preview,
                                lambda item: rx.text(item, class_name="tag-chip critical"),
                            ),
                            style={"flex_wrap": "wrap"},
                            spacing="2",
                        ),
                        class_name="status-card",
                    ),
                    rx.box(
                        rx.text("Raw Pipeline Result", class_name="status-label"),
                        rx.cond(
                            AppState.result_json != "",
                            rx.code_block(
                                AppState.result_json,
                                language="json",
                                class_name="result-surface",
                            ),
                            rx.text("Run analysis to view JSON output.", class_name="result-placeholder"),
                        ),
                        class_name="status-card",
                    ),
                    spacing="3",
                    width="100%",
                ),
                columns=rx.breakpoints(initial="1", lg="2"),
                spacing="4",
                width="100%",
            ),
            spacing="4",
            width="100%",
            max_width="1120px",
        ),
        id="analyzer",
        class_name="section-shell analyzer-shell reveal",
    )


def _footer() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text("Resumelytics", class_name="footer-brand"),
                rx.text(
                    "Built for software roles where signal quality matters.",
                    class_name="footer-copy",
                ),
                align="start",
                spacing="1",
            ),
            rx.hstack(
                rx.link("Overview", href="#overview", class_name="footer-link"),
                rx.link("Pipeline", href="#pipeline", class_name="footer-link"),
                rx.link("Analyzer", href="#analyzer", class_name="footer-link"),
                spacing="4",
            ),
            justify="between",
            align="center",
            width="100%",
            flex_wrap="wrap",
            gap="12px",
        ),
        id="site-footer",
        class_name="footer-shell",
    )


def index() -> rx.Component:
    return rx.box(
        rx.box(class_name="grid-overlay"),
        rx.vstack(
            _nav(),
            _hero(),
            _pipeline_section(),
            _form_panel(),
            _footer(),
            spacing="6",
            width="100%",
            class_name="page-content",
        ),
        class_name="app-shell",
    )


app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap",
        "/site.css",
    ],
)
app.add_page(index, title="Resumelytics")
