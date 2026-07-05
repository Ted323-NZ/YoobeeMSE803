"""Deterministic demo feedback used when no Gemini API key is configured."""

from __future__ import annotations

import re


DEFAULT_SOFTWARE_ENGINEER_KEYWORDS = [
    "Python",
    "JavaScript",
    "TypeScript",
    "REST API",
    "FastAPI",
    "React",
    "SQL",
    "Git",
    "Docker",
    "testing",
    "cloud deployment",
    "Agile",
]

SECTION_PATTERNS = {
    "summary": r"\b(summary|profile|objective)\b",
    "skills": r"\b(skills|technical skills|technologies)\b",
    "experience": r"\b(experience|employment|work history)\b",
    "projects": r"\b(projects|portfolio)\b",
    "education": r"\b(education|qualification|degree)\b",
}


def normalize_text(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", text.strip())


def detect_sections(cv_text: str) -> dict[str, bool]:
    lower_text = cv_text.lower()
    return {
        section: bool(re.search(pattern, lower_text, flags=re.IGNORECASE))
        for section, pattern in SECTION_PATTERNS.items()
    }


def extract_candidate_name(cv_text: str) -> str:
    for raw_line in cv_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if re.search(r"cv|resume|curriculum", line, flags=re.IGNORECASE):
            continue
        if 2 <= len(line.split()) <= 4 and re.search(r"[A-Za-z]", line):
            return line
    return "Alex Chen"


def analyze_cv(cv_text: str, target_role: str = "Software Engineer") -> dict:
    text = normalize_text(cv_text)
    sections = detect_sections(text)
    words = re.findall(r"\b[\w+#.-]+\b", text)
    bullet_count = len(re.findall(r"(?m)^\s*[-*]\s+", text))
    has_metrics = bool(re.search(r"\b\d+%|\b\d+\+|\$\d+|\b\d+ users\b", text))
    has_links = bool(re.search(r"github\.com|linkedin\.com|portfolio|https?://", text, re.I))

    missing_sections = [name for name, present in sections.items() if not present]
    score = 55
    score += 5 * sum(sections.values())
    score += 8 if bullet_count >= 3 else 0
    score += 8 if has_metrics else 0
    score += 5 if has_links else 0
    score += 4 if 180 <= len(words) <= 750 else 0
    score = max(35, min(score, 92))

    strengths = []
    if sections["skills"]:
        strengths.append("The CV includes a skills section, which helps recruiters scan technical fit quickly.")
    if sections["projects"]:
        strengths.append("Project information is useful for a Software Engineer role because it shows applied capability.")
    if sections["education"]:
        strengths.append("Education details are present and support the candidate's early-career profile.")
    if has_links:
        strengths.append("Online links make it easier for employers to review code, portfolio work, or professional history.")
    if not strengths:
        strengths.append("The CV provides a starting point, but it needs stronger role targeting and clearer evidence.")

    improvement_areas = []
    if missing_sections:
        improvement_areas.append(
            "Add missing sections: " + ", ".join(section.title() for section in missing_sections) + "."
        )
    if not has_metrics:
        improvement_areas.append("Add measurable outcomes, such as performance gains, users supported, or time saved.")
    if bullet_count < 3:
        improvement_areas.append("Use concise achievement bullets instead of paragraph-heavy descriptions.")
    improvement_areas.append("Align the opening summary and skills with the target role: " + target_role + ".")

    return {
        "target_role": target_role,
        "overall_score": score,
        "summary": (
            "The CV is suitable for an early-career application but needs stronger evidence, "
            "clearer structure, and more software engineering keywords."
        ),
        "strengths": strengths,
        "improvement_areas": improvement_areas,
        "content_recommendations": [
            "Rewrite duties as achievements using action verbs and measurable results.",
            "Add 2-3 role-relevant projects with technology stack, problem, action, and outcome.",
            "Include links to GitHub, LinkedIn, or a portfolio if available.",
            "Prioritize recent technical work and remove generic statements that do not prove capability.",
        ],
        "structure_recommendations": [
            "Use this order: header, professional summary, technical skills, projects, experience, education.",
            "Keep each bullet to one or two lines and start with a strong action verb.",
            "Group skills by category, for example languages, frameworks, databases, and tools.",
        ],
        "presentation_recommendations": [
            "Use consistent heading styles, spacing, and bullet formatting.",
            "Keep the CV to one page for an entry-level role unless there is substantial experience.",
            "Avoid dense paragraphs; make the document easy to scan in 30 seconds.",
        ],
        "ats_keywords": DEFAULT_SOFTWARE_ENGINEER_KEYWORDS,
        "revised_summary": (
            "Early-career Software Engineer with hands-on experience building Python and web applications, "
            "designing REST APIs, working with SQL data, and using Git-based development workflows. "
            "Strong interest in clean backend design, testing, and practical problem solving."
        ),
        "provider": "demo",
    }


def generate_optimized_cv_text(cv_text: str, target_role: str = "Software Engineer") -> dict:
    name = extract_candidate_name(cv_text)
    feedback = analyze_cv(cv_text, target_role)
    optimized = f"""{name}
{target_role}
Auckland, New Zealand | alex.chen@example.com | +64 21 000 0000 | github.com/alexchen | linkedin.com/in/alexchen

PROFESSIONAL SUMMARY
{feedback["revised_summary"]}

TECHNICAL SKILLS
- Languages: Python, JavaScript, TypeScript, SQL
- Backend: FastAPI, REST API design, authentication basics, data validation
- Frontend: React, HTML, CSS, responsive interface development
- Databases and tools: PostgreSQL, SQLite, Git, GitHub, Docker, VS Code
- Practices: Unit testing, debugging, Agile teamwork, documentation

PROJECTS
- LLM-Powered CV Feedback API: Built a FastAPI backend that analyses CV text, produces structured feedback, and generates an optimized CV document using Gemini API integration with a local demo fallback.
- Task Management Web App: Developed a full-stack CRUD application with REST endpoints, form validation, SQL persistence, and clean Git commit history.
- Data Dashboard Prototype: Created a Python data workflow to clean CSV data, calculate summary metrics, and present insights through clear visual outputs.

EXPERIENCE
- Applied software engineering practices through academic and personal projects, including requirements analysis, API design, testing, and documentation.
- Improved project readability by separating parsing, LLM prompting, feedback generation, and DOCX export into maintainable modules.
- Collaborated in class activities using GitHub workflows, issue tracking, and iterative improvement based on feedback.

EDUCATION
- Diploma / Coursework in Data Analytics and Software Development, Yoobee College, New Zealand
- Relevant study: Python programming, data analysis, database fundamentals, backend development, and AI-assisted applications

CERTIFICATIONS AND DEVELOPMENT
- Continued learning in FastAPI, cloud deployment, GitHub project documentation, and responsible use of generative AI tools
"""

    return {
        "target_role": target_role,
        "optimized_cv_text": optimized.strip(),
        "changes_made": [
            "Added a targeted Software Engineer summary.",
            "Grouped technical skills into ATS-friendly categories.",
            "Converted generic experience into achievement-style bullets.",
            "Added project evidence aligned with backend and software engineering roles.",
            "Improved structure, spacing, and scanability for recruiters.",
        ],
        "provider": "demo",
    }

