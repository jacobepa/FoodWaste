# qar5_section_a.py (constants)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# py-lint: disable=C0301

# Constants and Strings for the QAR5 module Section A.

A3_DISTRIBUTION_LIST = """
    Quality Assurance Project Plans and Standard Operating Procedures shall be
    controlled through documented approvals as required by Section 5.3 of the
    Office of Research and Development Quality Management Plan. The project
    lead will be responsible for distribution of the current signed approved
    version of the QA Project Plan to project participants shown in Section
    A.4. Signed approved versions of SOPs will be available to project staff
    through the ORD@Work SOP intranet site. Signature approved electronic
    copies of this QA Project Plan, SOPs, and any associated QA assessment
    reports, will also be maintained in ORD QA Track. The project lead will be
    responsible for timely communications with all involved participants and
    will retain copies of all management reports, memoranda, and correspondence
    between research task personnel.
"""

# A4 Note: Need to be able to add an organizational chart
#          see QA Template docs folder
A4_PROJECT_TASK_ORGANIZATION = """
    Identify the individuals and organizations participating in the research
    and discuss their specific roles and responsibilities. Include and all
    persons responsible for implementation. QA manager position must indicate
    independence from unit collecting/using data.  A table summarizing this
    information is recommended.
"""

A5_PROBLEM_DEFINITION_BACKGROUND = """
    State the specific problem to be solved, decision to be made, or outcome to
    be achieved. Include sufficient background information to provide a
    historical, scientific, and regulatory perspective for this particular
    project.
"""

A6_PROJECT_DESCRIPTION = """
    Provide a high-level discussion of how, when, and where the research effort
    will be conducted over the duration of the study.  Include any research
    questions or hypotheses, purpose objectives, any dependencies e.g., on
    other projects, certain funding levels, a certain measure of success at
    early stages of the project, etc., and any critical issues. This could
    optionally include information on potential impact or customer partner
    concerns. or equipment requirements. Provide an estimated timeline for
    completion of key tasks e.g., QA Project Plan and Health and Safety Plan
    development, data collect, etc. with respect to the target dates for the
    research project deliverables.
"""

A7_QUALITY_OBJECTS_CRITERIA = """
    Discuss the quality objectives for the project and the performance criteria
    to achieve those objectives. EPA requires the use of a systematic planning
    process to define these quality objectives and performance criteria. State
    project objectives and limits, both qualitatively and quantitatively. State
    and characterize measurement quality objectives as to applicable action
    levels or criteria.
"""

A8_SPECIAL_TRAINING_CERTIFICATION = """
    Identify and describe any specialized training or certifications needed by
    personnel in order to successfully complete the project or task. Discuss
    how such training will be provided and how the necessary skills will be
    assured and documented.
"""

# This TEXT needs to be added automatically for A.9
# TODO: Add link to the EXISTING DATA WEB PAGE IN TOOL
# TODO: Need to be able to enter path to drive insert here:
#       (List file path where files are stored.)
A9_DOCUMENTS_RECORDS = """
    Research activities must be documented according to the requirements of
    ORD QA Policies titled Scientific Recordkeeping: Paper, Scientific
    Recordkeeping Electronic, and Quality Assurance Quality Control Practices
    for ORD Laboratory and Field-Based Research, as well as requirements
    defined in this QA Project Plan. The ORD QA Policies require the use of
    research notebooks and the management of research records, both paper
    and electronic, such that project research data generation may continue
    even if a researcher or an analyst participating in the project leaves
    the project staff. Electronic project records can be maintained by the
    project lead on using this EXISTING DATA SEARCH TOOL or can be stored
    on the ORD network drive, List file path where files are stored.
    Electronic Records shall be maintained in a manner that maximizes the
    confidentiality, accessibility, and integrity of the data. ORD PPM Section
    13.6 provides guidance on the maintenance of electronic records for ORD.
"""

A9_RECORDS_RETENTION = """
    Records retention: Records that are generated under this research effort will
    be retained in accordance with EPA Records Schedule 1035, and as required by
    Section 5.1 of the ORD Quality Management Plan for QA Category A Projects.
"""

SECTION_A_DEFAULTS = {
    'A.3 Distribution List': A3_DISTRIBUTION_LIST,
    'A.4 Project Task Organization': A4_PROJECT_TASK_ORGANIZATION,
    'A.5 Problem Definition Background': A5_PROBLEM_DEFINITION_BACKGROUND,
    'A.6 Project Description': A6_PROJECT_DESCRIPTION,
    'A.7 Quality Objectives and Criteria': A7_QUALITY_OBJECTS_CRITERIA,
    'A.8 Special Training Certification': A8_SPECIAL_TRAINING_CERTIFICATION,
    'A.9 Documents and Records': [A9_DOCUMENTS_RECORDS, A9_RECORDS_RETENTION]
}