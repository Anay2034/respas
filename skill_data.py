# Dictionary structure: Category -> { Skill Name -> [List of Regex Patterns] }
# \b ensures word boundaries (e.g., "Java" doesn't match "Javascript")
# We use raw strings r"" to handle special regex characters.

SKILL_DB = {
    "Programming Languages": {
        "Python": [r"\bpython\b"],
        "C++": [r"\bc\+\+", r"\bcpp\b"], # Escape +
        "C": [r"\bc\b"], # Hard to match C without matching 'c' in words, context matters but \b helps
        "Java": [r"\bjava\b"], # Matches Java but not JavaScript due to boundary
        "JavaScript": [r"\bjavascript\b", r"\bjs\b", r"\bes6\b"],
        "TypeScript": [r"\btypescript\b", r"\bts\b"],
        "SQL": [r"\bsql\b", r"\bmysql\b", r"\bpostgres\b", r"\bpostgresql\b"],
        "HTML/CSS": [r"\bhtml\d?\b", r"\bcss\d?\b"],
        "R": [r"\br\b"], # Tricky, often false positive
        "MATLAB": [r"\bmatlab\b"],
        "Go": [r"\bgo\b", r"\bgolang\b"],
        "Rust": [r"\brust\b"],
        "Swift": [r"\bswift\b"],
        "Kotlin": [r"\bkotlin\b"],
        "PHP": [r"\bphp\b"],
        "Ruby": [r"\bruby\b"],
        "C#": [r"\bc#", r"\bcsharp\b"]
    },
    
    "Libraries & Frameworks": {
        "React": [r"\breact(?:\.?js)?\b", r"\breact\s*native\b"],
        "Angular": [r"\bangular(?:\.?js)?\b"],
        "Vue.js": [r"\bvue(?:\.?js)?\b"],
        "Node.js": [r"\bnode(?:\.?js)?\b"],
        "Express.js": [r"\bexpress(?:\.?js)?\b"],
        "Django": [r"\bdjango\b"],
        "Flask": [r"\bflask\b"],
        "FastAPI": [r"\bfastapi\b"],
        "Spring Boot": [r"\bspring\s*boot\b", r"\bspring\b"],
        "Pandas": [r"\bpandas\b"],
        "NumPy": [r"\bnumpy\b"],
        "Scikit-learn": [r"\bscikit-?learn\b", r"\bsklearn\b"],
        "TensorFlow": [r"\btensorflow\b", r"\btf\b"],
        "PyTorch": [r"\bpytorch\b"],
        "Keras": [r"\bkeras\b"],
        "OpenCV": [r"\bopencv\b"],
        "NLTK": [r"\bnltk\b"],
        "Spacy": [r"\bspacy\b"],
        "Tailwind CSS": [r"\btailwind(?:css)?\b"],
        "Bootstrap": [r"\bbootstrap\b"]
    },
    
    "Tools & Platforms": {
        "Git": [r"\bgit\b"],
        "GitHub": [r"\bgithub\b"],
        "GitLab": [r"\bgitlab\b"],
        "Docker": [r"\bdocker\b"],
        "Kubernetes": [r"\bkubernetes\b", r"\bk8s\b"],
        "AWS": [r"\baws\b", r"\amazon\s*web\s*services\b"],
        "Azure": [r"\bazure\b"],
        "GCP": [r"\bgcp\b", r"\bgoogle\s*cloud\b"],
        "Linux": [r"\blinux\b", r"\bunix\b", r"\bubuntu\b"],
        "Jenkins": [r"\bjenkins\b"],
        "Jira": [r"\bjira\b"],
        "Postman": [r"\bpostman\b"],
        "Figma": [r"\bfigma\b"],
        "Tableau": [r"\btableau\b"],
        "Power BI": [r"\bpower\s*bi\b"],
        "excel": [r"\bexcel\b", r"\bmicrosoft\s*excel\b"]
    },
    
    "Databases": {
        "MongoDB": [r"\bmongodb\b", r"\bmongo\b"],
        "PostgreSQL": [r"\bpostgresql\b", r"\bpostgres\b"],
        "MySQL": [r"\bmysql\b"],
        "Redis": [r"\bredis\b"],
        "SQLite": [r"\bsqlite\b"],
        "Oracle": [r"\boracle\b"],
        "Cassandra": [r"\bcassandra\b"],
        "DynamoDB": [r"\bdynamodb\b"]
    }
}