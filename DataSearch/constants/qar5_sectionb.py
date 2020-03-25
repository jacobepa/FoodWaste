# qar5_sectionb.py (constants)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# py-lint: disable=C0301

"""TODO Add docstring."""

SECTION_B_TYPES = (
    ('Analytical Methods', 'Analytical Methods'),
    ('Animal Subjects', 'Animal Subjects'),
    ('Cell Culture Models', 'Cell Culture Models'),
    ('Existing Data', 'Existing Data'),
    ('Measurements', 'Measurements'),
    ('Model Application', 'Model Application'),
    ('Model Development', 'Model Development'),
    ('Software Development', 'Software Development')
)

MEASUREMENTS_AND_MONITORING = {
    'b1_1': {
        'label': 'B.1.1',
        'desc': 'Identify the specific analyte(s) of interest and the ' + \
                 'matrix/matrices. Classify each measurement parameter ' + \
                 'as either critical or needed for information only.'
    },
    'b1_2': {
        'label': 'B.1.2',
        'desc': 'Describe sampling and/or experimental design to ' + \
                'generate the data needed to evaluate the research ' + \
                'objectives. A description of the design should ' + \
                'include the rationale for the design and types ' + \
                'and number of samples required, including any ' + \
                'field or experimental QC samples.'
    },
    'b1_3': {
        'label': 'B.1.3',
        'desc': 'Identify sampling locations and frequency of sampling.'
    },
    'b2_1': {
        'label': 'B.2.1',
        'desc': 'If non-synthetic (i.e., real-world sample) ' + \
                'samples are used describe the sampling design that ' + \
                'will be used, and the steps taken to assure that ' + \
                'representative samples are collected.'
    },
    'b2_2': {
        'label': 'B.2.2',
        'desc': 'If synthetic (i.e., laboratory-prepared) ' + \
                'samples are used, describe the preparation of these samples.'
    },
    'b2_3': {
        'label': 'B.2.3',
        'desc': 'Describe the decontamination procedures for any ' + \
                'sampling equipment that will be reused to ' + \
                'prevent cross contamination.'
    },
    'b2_4': {
        'label': 'B.2.4',
        'desc': 'Provide a list of sample containers, sample quantities ' + \
                'to be collected, and the sample amount required for ' + \
                'each analysis, including QC sample analysis.'
    },
    'b2_5': {
        'label': 'B.2.5',
        'desc': 'Describe labeling (information to be included) ' + \
                'and uniquely numbering each sample.'
    },
    'b2_6': {
        'label': 'B.2.6',
        'desc': 'Specify sample preservation requirements ' + \
                '(e.g., refrigeration, acidification, etc.) ' + \
                'and sample hold times.'
    },
    'b2_7': {
        'label': 'B.2.7',
        'desc': 'If non-synthetic (i.e., real-world sample) samples ' + \
                'are used describe procedures for packing and shipping ' + \
                'samples, and provisions for maintaining ' + \
                'chain-of-custody, as applicable.'
    },
    'b3_1': {
        'label': 'B.3.1',
        'desc': 'For field analyses (including in-line measurements), ' + \
                'describe in detail or reference each field sample ' + \
                'analysis method and instrumentation to be used. ' + \
                'Include steps for instrument calibration, ' + \
                'measurement, quality control, and documentation of results.'
    },
    'b3_2': {
        'label': 'B.3.2',
        'desc': 'For laboratory analyses, describe in detail or ' + \
                'reference each sample preparation method (e.g., ' + \
                'sample extractions) and analytical methods, equipment ' + \
                'and instrumentation to be used. Include steps for ' + \
                'preparation, calibration, measurement, quality ' + \
                'control, and reporting.'
    },
    'b3_3': {
        'label': 'B.3.3',
        'desc': 'Include specific calibration procedures, including ' + \
            'linearity checks and initial and continuing calibration ' + \
            'checks, and detection limits.'
    },
    'b4_1': {
        'label': 'B.4.1',
        'desc': 'For each analysis method QC check (e.g., blanks, ' + \
                'control samples, duplicates, matrix spikes, surrogates) ' + \
                'specify the frequencies for performing these checks, ' + \
                'associated acceptance criteria, and corrective actions ' + \
                'to be performed if acceptance criteria are not met.'
    },
}

SECTION_B_INFO = {
    "Existing Data": {},
    "Software Development": {},
    "Model Development": {},
    "Model Application": {},
    "Measurements": MEASUREMENTS_AND_MONITORING,
    "Analytical Methods": {},
    "Cell Culture Models": {},
    "Animal Subjects": {}
}
