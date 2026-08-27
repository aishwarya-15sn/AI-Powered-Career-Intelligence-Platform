# Placify – Dataset Specification

## 1. ESCO Skills Dataset

- Source: European Commission – ESCO
- Version: 1.2.1
- File: `skills_en.csv`
- Format: CSV
- Records: 13,960
- Purpose: Provides standardized skills and competencies for skill extraction, normalization, skill-gap analysis, and career intelligence.
- Used by:
  - Skill Extraction
  - Standardized Skill Mapping
  - Skill Gap Analysis
  - Career Intelligence

## 2. ESCO Occupations Dataset

- Source: European Commission – ESCO
- Version: 1.2.1
- File: `occupations_en.csv`
- Format: CSV
- Records: 3,043
- Purpose: Provides standardized occupation/job-role taxonomy.
- Used by:
  - Target Job Role Selection
  - Job Role Mapping
  - Career Intelligence

## 3. ESCO Occupation–Skill Relations Dataset

- Source: European Commission – ESCO
- Version: 1.2.1
- File: `occupationSkillRelations_en.csv`
- Format: CSV
- Records: 126,051
- Purpose: Defines relationships between occupations and their required skills, including essential and optional relationships.
- Used by:
  - Job Role Requirements
  - Skill Matching
  - Skill Gap Analysis
  - Career Intelligence

## 4. Job Description Dataset

- Source: Public job-description dataset
- File: `job_title_des.csv`
- Format: CSV
- Purpose: Provides job titles and job-description text for job-description analysis and resume–JD matching.
- Used by:
  - Job Description Processing
  - Requirement Extraction
  - Resume–JD Matching

## 5. Interview Question Dataset

- Source: Public interview-question dataset
- File: `full_interview_questions_dataset.csv`
- Format: CSV
- Purpose: Provides technical and HR interview questions for interview preparation.
- Used by:
  - Interview Preparation
  - Personalized Interview Practice

## 6. Technical Question Dataset

- Source: Public technical question-answering dataset
- Files:
  - `train.jsonl`
  - `val.jsonl`
  - `test.jsonl`
- Format: JSONL
- Purpose: Provides technical question-answer data for technical assessment and question generation/selection.
- Used by:
  - Technical Assessment
  - Performance Tracking
  - Interview Preparation

## 7. Aptitude Question Bank

- Source: CSE Aptitude Test Practice Hub
- Format: Markdown question banks
- Categories:
  - Quantitative Aptitude
  - Logical Reasoning
  - Verbal Ability
  - Data Interpretation and Analysis
  - Abstract Reasoning
  - Technical Aptitude
- Purpose: Provides aptitude practice questions for assessment and preparation.
- Used by:
  - Aptitude Assessment
  - Performance Tracking
  - Personalized Study Planning

## 8. Online Courses Dataset

- Source: Public online-course dataset
- File: `Online_Courses.csv`
- Format: CSV
- Purpose: Provides learning resources that can be recommended according to identified skill gaps.
- Used by:
  - Learning Resource Recommendation
  - Personalized Learning
  - Study Plan Generation

---

# Dataset-to-Module Mapping

| Dataset | Placify Module |
|---|---|
| ESCO Skills | Skill Extraction & Skill Normalization |
| ESCO Occupations | Target Job Role |
| ESCO Occupation–Skill Relations | Role Requirements & Skill Gap |
| Job Descriptions | JD Processing & Resume–JD Matching |
| Interview Questions | Interview Preparation |
| Technical Questions | Technical Assessment |
| Aptitude Question Bank | Aptitude Assessment |
| Online Courses | Personalized Learning |

# Dataset Integration Strategy

The datasets will not be used directly without preprocessing.

The implementation will:

1. Clean and normalize textual data.
2. Remove invalid or duplicate records where required.
3. Map ESCO skills and occupations to the Placify database.
4. Transform question datasets into structured assessment records.
5. Extract relevant requirements and skills from job descriptions.
6. Map identified skills to standardized ESCO skills where applicable.
7. Store the processed data in the Placify SQLite database.

## Primary Knowledge Base

ESCO is designated as the primary standardized knowledge base for:

- Skills
- Occupations
- Occupation–skill relationships

The remaining datasets supplement ESCO for job descriptions, assessments, interview preparation, and learning-resource recommendation.