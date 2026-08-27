PRAGMA foreign_keys = ON;

-- ============================================================
-- PLACIFY DATABASE SCHEMA
-- ============================================================

-- ------------------------------------------------------------
-- STUDENT
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS STUDENT (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- PROFILE
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS PROFILE (
    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL UNIQUE,
    phone TEXT,
    education TEXT,
    branch TEXT,
    graduation_year INTEGER,
    cgpa REAL,
    target_job_role_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id),
    FOREIGN KEY (target_job_role_id) REFERENCES JOB_ROLE(job_role_id)
);

-- ------------------------------------------------------------
-- RESUME
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS RESUME (
    resume_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    extracted_text TEXT,
    uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id)
);

-- ------------------------------------------------------------
-- SKILL
-- ESCO standardized skill repository
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS SKILL (
    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    esco_uri TEXT UNIQUE,
    skill_name TEXT NOT NULL,
    skill_type TEXT,
    alternative_labels TEXT,
    description TEXT,
    definition TEXT,
    source TEXT DEFAULT 'ESCO'
);

-- ------------------------------------------------------------
-- STUDENT_SKILL
-- Student ↔ standardized skill
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS STUDENT_SKILL (
    student_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    source TEXT,
    confidence REAL,
    PRIMARY KEY (student_id, skill_id),
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id),
    FOREIGN KEY (skill_id) REFERENCES SKILL(skill_id)
);

-- ------------------------------------------------------------
-- JOB_ROLE
-- ESCO standardized occupations / target roles
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS JOB_ROLE (
    job_role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    esco_uri TEXT UNIQUE,
    role_name TEXT NOT NULL,
    alternative_labels TEXT,
    description TEXT,
    isco_group TEXT,
    occupation_code TEXT,
    source TEXT DEFAULT 'ESCO'
);

-- ------------------------------------------------------------
-- JOB_ROLE_SKILL
-- ESCO occupation ↔ skill relationship
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS JOB_ROLE_SKILL (
    job_role_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    relation_type TEXT NOT NULL,
    skill_type TEXT,
    PRIMARY KEY (job_role_id, skill_id),
    FOREIGN KEY (job_role_id) REFERENCES JOB_ROLE(job_role_id),
    FOREIGN KEY (skill_id) REFERENCES SKILL(skill_id)
);

-- ------------------------------------------------------------
-- JOB_DESCRIPTION
-- User-provided job description
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS JOB_DESCRIPTION (
    job_description_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    job_role_id INTEGER,
    title TEXT,
    source_type TEXT NOT NULL,
    raw_text TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id),
    FOREIGN KEY (job_role_id) REFERENCES JOB_ROLE(job_role_id)
);

-- ------------------------------------------------------------
-- JD_SKILL
-- Skills extracted from a specific job description
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS JD_SKILL (
    job_description_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    requirement_type TEXT,
    confidence REAL,
    PRIMARY KEY (job_description_id, skill_id),
    FOREIGN KEY (job_description_id)
        REFERENCES JOB_DESCRIPTION(job_description_id),
    FOREIGN KEY (skill_id)
        REFERENCES SKILL(skill_id)
);

-- ------------------------------------------------------------
-- TECHNICAL_QUESTION
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS TECHNICAL_QUESTION (
    technical_question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_id INTEGER,
    question TEXT NOT NULL,
    option_a TEXT,
    option_b TEXT,
    option_c TEXT,
    option_d TEXT,
    correct_option TEXT,
    difficulty TEXT,
    FOREIGN KEY (skill_id) REFERENCES SKILL(skill_id)
);

-- ------------------------------------------------------------
-- APTITUDE_QUESTION
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS APTITUDE_QUESTION (
    aptitude_question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT,
    question TEXT NOT NULL,
    option_a TEXT,
    option_b TEXT,
    option_c TEXT,
    option_d TEXT,
    correct_option TEXT,
    difficulty TEXT
);

-- ------------------------------------------------------------
-- ASSESSMENT_ATTEMPT
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ASSESSMENT_ATTEMPT (
    attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    assessment_type TEXT NOT NULL,
    total_questions INTEGER,
    correct_answers INTEGER,
    score REAL,
    started_at TEXT,
    completed_at TEXT,
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id)
);

-- ------------------------------------------------------------
-- LEARNING_RESOURCE
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS LEARNING_RESOURCE (
    resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_id INTEGER,
    title TEXT NOT NULL,
    resource_type TEXT,
    url TEXT,
    difficulty TEXT,
    FOREIGN KEY (skill_id) REFERENCES SKILL(skill_id)
);

-- ------------------------------------------------------------
-- STUDY_PLAN
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS STUDY_PLAN (
    study_plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    title TEXT,
    start_date TEXT,
    end_date TEXT,
    status TEXT,
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id)
);

-- ------------------------------------------------------------
-- STUDY_PROGRESS
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS STUDY_PROGRESS (
    progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
    study_plan_id INTEGER NOT NULL,
    skill_id INTEGER,
    resource_id INTEGER,
    progress_percent REAL DEFAULT 0,
    completed INTEGER DEFAULT 0,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (study_plan_id) REFERENCES STUDY_PLAN(study_plan_id),
    FOREIGN KEY (skill_id) REFERENCES SKILL(skill_id),
    FOREIGN KEY (resource_id) REFERENCES LEARNING_RESOURCE(resource_id)
);

-- ------------------------------------------------------------
-- INTERVIEW_QUESTION
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS INTERVIEW_QUESTION (
    interview_question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_id INTEGER,
    question TEXT NOT NULL,
    question_type TEXT,
    difficulty TEXT,
    FOREIGN KEY (skill_id) REFERENCES SKILL(skill_id)
);

-- ------------------------------------------------------------
-- INTERVIEW_ATTEMPT
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS INTERVIEW_ATTEMPT (
    interview_attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    interview_question_id INTEGER NOT NULL,
    answer TEXT,
    score REAL,
    feedback TEXT,
    attempted_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id),
    FOREIGN KEY (interview_question_id)
        REFERENCES INTERVIEW_QUESTION(interview_question_id)
);

-- ------------------------------------------------------------
-- READINESS_HISTORY
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS READINESS_HISTORY (
    readiness_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    readiness_score REAL,
    match_score REAL,
    assessment_score REAL,
    skill_gap_score REAL,
    recorded_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id)
);

-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_student_skill_student
ON STUDENT_SKILL(student_id);

CREATE INDEX IF NOT EXISTS idx_student_skill_skill
ON STUDENT_SKILL(skill_id);

CREATE INDEX IF NOT EXISTS idx_job_role_skill_role
ON JOB_ROLE_SKILL(job_role_id);

CREATE INDEX IF NOT EXISTS idx_job_role_skill_skill
ON JOB_ROLE_SKILL(skill_id);

CREATE INDEX IF NOT EXISTS idx_jd_skill_jd
ON JD_SKILL(job_description_id);

CREATE INDEX IF NOT EXISTS idx_jd_skill_skill
ON JD_SKILL(skill_id);

CREATE INDEX IF NOT EXISTS idx_resume_student
ON RESUME(student_id);

CREATE INDEX IF NOT EXISTS idx_assessment_student
ON ASSESSMENT_ATTEMPT(student_id);

CREATE INDEX IF NOT EXISTS idx_readiness_student
ON READINESS_HISTORY(student_id);