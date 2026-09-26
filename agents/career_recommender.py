from collections import defaultdict


# ============================================================
# CAREERPILOT AI - MULTI CAREER RECOMMENDER
# ============================================================

CAREER_PROFILES = {

    # ---------------- DATA & AI ----------------

    "Data Scientist": {
        "skills": [
            "python",
            "sql",
            "pandas",
            "numpy",
            "matplotlib",
            "statistics",
            "data science",
            "machine learning",
            "data analysis"
        ],
        "keywords": [
            "data scientist",
            "data science",
            "eda",
            "data analysis",
            "predictive modeling"
        ]
    },

    "Machine Learning Engineer": {
        "skills": [
            "python",
            "scikit-learn",
            "machine learning",
            "tensorflow",
            "keras",
            "pytorch",
            "model evaluation",
            "feature engineering"
        ],
        "keywords": [
            "machine learning",
            "classification",
            "regression",
            "model training",
            "ml model"
        ]
    },

    "AI Engineer": {
        "skills": [
            "python",
            "artificial intelligence",
            "machine learning",
            "deep learning",
            "tensorflow",
            "keras",
            "pytorch",
            "generative ai",
            "llm"
        ],
        "keywords": [
            "artificial intelligence",
            "deep learning",
            "generative ai",
            "large language model",
            "llm"
        ]
    },

    "Computer Vision Engineer": {
        "skills": [
            "python",
            "opencv",
            "computer vision",
            "yolo",
            "yolov8",
            "image processing",
            "tensorflow",
            "pytorch",
            "cnn"
        ],
        "keywords": [
            "computer vision",
            "object detection",
            "image classification",
            "image processing"
        ]
    },

    "NLP Engineer": {
        "skills": [
            "python",
            "nlp",
            "natural language processing",
            "spacy",
            "transformers",
            "hugging face",
            "rag",
            "llm"
        ],
        "keywords": [
            "nlp",
            "natural language processing",
            "text classification",
            "sentiment analysis",
            "rag"
        ]
    },

    "Generative AI Engineer": {
        "skills": [
            "python",
            "generative ai",
            "llm",
            "prompt engineering",
            "rag",
            "langchain",
            "hugging face",
            "transformers"
        ],
        "keywords": [
            "generative ai",
            "llm",
            "prompt engineering",
            "retrieval augmented generation"
        ]
    },

    "Agentic AI Engineer": {
        "skills": [
            "python",
            "agentic ai",
            "langchain",
            "langgraph",
            "llm",
            "rag",
            "prompt engineering"
        ],
        "keywords": [
            "agentic ai",
            "ai agent",
            "agents",
            "langgraph",
            "langchain"
        ]
    },


    # ---------------- SOFTWARE ----------------

    "Software Developer": {
        "skills": [
            "python",
            "java",
            "c++",
            "software development",
            "git",
            "api",
            "database"
        ],
        "keywords": [
            "software developer",
            "software development",
            "application development"
        ]
    },

    "Web Developer": {
        "skills": [
            "html",
            "css",
            "javascript",
            "react",
            "angular",
            "node.js",
            "flask",
            "django"
        ],
        "keywords": [
            "web development",
            "frontend",
            "backend",
            "full stack"
        ]
    },

    "Backend Developer": {
        "skills": [
            "python",
            "java",
            "flask",
            "django",
            "node.js",
            "api",
            "sql",
            "mysql",
            "mongodb"
        ],
        "keywords": [
            "backend",
            "backend development",
            "rest api"
        ]
    },

    "Database Developer": {
        "skills": [
            "sql",
            "mysql",
            "mongodb",
            "database",
            "postgresql",
            "oracle"
        ],
        "keywords": [
            "database",
            "database management",
            "database developer"
        ]
    },


    # ---------------- DATA / BI ----------------

    "Data Analyst": {
        "skills": [
            "python",
            "sql",
            "excel",
            "pandas",
            "numpy",
            "matplotlib",
            "data analysis",
            "tableau",
            "power bi"
        ],
        "keywords": [
            "data analyst",
            "data analysis",
            "business analysis",
            "reporting"
        ]
    },

    "Business Intelligence Analyst": {
        "skills": [
            "sql",
            "tableau",
            "power bi",
            "excel",
            "data visualization",
            "business intelligence"
        ],
        "keywords": [
            "business intelligence",
            "bi analyst",
            "dashboard",
            "business reporting"
        ]
    },


    # ---------------- CYBERSECURITY ----------------

    "Cybersecurity Analyst": {
        "skills": [
            "cybersecurity",
            "cyber security",
            "network security",
            "ethical hacking",
            "penetration testing",
            "security"
        ],
        "keywords": [
            "cybersecurity",
            "cyber security",
            "security analyst",
            "threat detection"
        ]
    },


    # ---------------- CLOUD / DEVOPS ----------------

    "Cloud Engineer": {
        "skills": [
            "aws",
            "azure",
            "gcp",
            "cloud computing",
            "docker",
            "kubernetes"
        ],
        "keywords": [
            "cloud",
            "cloud computing",
            "cloud engineer"
        ]
    },

    "DevOps Engineer": {
        "skills": [
            "aws",
            "docker",
            "kubernetes",
            "jenkins",
            "linux",
            "git",
            "ci/cd"
        ],
        "keywords": [
            "devops",
            "continuous integration",
            "continuous deployment"
        ]
    },


    # ---------------- TESTING ----------------

    "Software Tester / QA Engineer": {
        "skills": [
            "testing",
            "software testing",
            "selenium",
            "automation testing",
            "manual testing",
            "qa"
        ],
        "keywords": [
            "software testing",
            "quality assurance",
            "qa",
            "test automation"
        ]
    },


    # ---------------- MANAGEMENT / BUSINESS ----------------

    "Business Analyst": {
        "skills": [
            "sql",
            "excel",
            "data analysis",
            "business analysis",
            "communication",
            "problem solving"
        ],
        "keywords": [
            "business analyst",
            "business analysis",
            "requirements analysis"
        ]
    },

    "Project Coordinator": {
        "skills": [
            "communication",
            "teamwork",
            "project management",
            "time management",
            "leadership"
        ],
        "keywords": [
            "project management",
            "project coordinator",
            "team coordination"
        ]
    },

    "Sales / Business Development": {
        "skills": [
            "sales",
            "communication",
            "negotiation",
            "customer relationship",
            "business development"
        ],
        "keywords": [
            "sales",
            "business development",
            "client management"
        ]
    },

    "Marketing": {
        "skills": [
            "marketing",
            "digital marketing",
            "communication",
            "social media",
            "content marketing"
        ],
        "keywords": [
            "marketing",
            "digital marketing",
            "social media marketing"
        ]
    },

    "Human Resources": {
        "skills": [
            "human resources",
            "recruitment",
            "communication",
            "talent acquisition",
            "employee relations"
        ],
        "keywords": [
            "human resources",
            "hr",
            "recruitment",
            "talent acquisition"
        ]
    },

    "Finance / Accounting": {
        "skills": [
            "finance",
            "accounting",
            "financial analysis",
            "excel",
            "tally"
        ],
        "keywords": [
            "finance",
            "accounting",
            "financial analyst"
        ]
    }
}


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize(text):

    return str(text).lower().strip()


# ============================================================
# BUILD COMPLETE PROFILE TEXT
# ============================================================

def build_profile_text(profile):

    parts = []

    # Education
    parts.extend(
        profile.get("education", [])
    )

    # Skills
    parts.extend(
        profile.get("skills", [])
    )

    # Experience
    experience = profile.get(
        "experience",
        ""
    )

    parts.append(
        str(experience)
    )

    # Projects
    projects = profile.get(
        "projects",
        []
    )

    parts.extend(
        [str(project) for project in projects]
    )

    # Certifications
    certifications = profile.get(
        "certifications",
        []
    )

    parts.extend(
        [str(cert) for cert in certifications]
    )

    # Resume text
    parts.append(
        profile.get(
            "resume_text",
            ""
        )
    )

    return normalize(
        " ".join(parts)
    )


# ============================================================
# CAREER SCORING
# ============================================================

def calculate_score(
    profile_text,
    career_data
):

    score = 0

    skills = [
        normalize(skill)
        for skill in career_data["skills"]
    ]

    keywords = [
        normalize(keyword)
        for keyword in career_data["keywords"]
    ]


    # Skill matching
    for skill in skills:

        if skill in profile_text:

            score += 3


    # Keyword matching
    for keyword in keywords:

        if keyword in profile_text:

            score += 5


    return score


# ============================================================
# MULTIPLE CAREER RECOMMENDATION
# ============================================================

def recommend_careers(
    profile,
    top_n=5
):

    profile_text = build_profile_text(
        profile
    )

    scores = defaultdict(int)


    # Score every career
    for career, career_data in CAREER_PROFILES.items():

        scores[career] = calculate_score(
            profile_text,
            career_data
        )


    # --------------------------------------------------------
    # Include ML prediction as an additional signal
    # --------------------------------------------------------

    predicted = normalize(
        profile.get(
            "predicted_career",
            ""
        )
    )

    for career in scores:

        if normalize(career) in predicted:

            scores[career] += 5


    # --------------------------------------------------------
    # Rank careers
    # --------------------------------------------------------

    ranked = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )


    # Remove zero-score careers
    ranked = [
        item
        for item in ranked
        if item[1] > 0
    ]


    # --------------------------------------------------------
    # Calculate percentage
    # --------------------------------------------------------

    max_score = (
        ranked[0][1]
        if ranked
        else 1
    )


    recommendations = []

    for career, score in ranked[:top_n]:

        percentage = round(
            (score / max_score) * 100
        )

        recommendations.append({
            "career": career,
            "score": score,
            "match": percentage
        })


    return recommendations