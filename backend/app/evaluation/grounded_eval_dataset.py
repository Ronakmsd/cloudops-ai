GROUNDED_EVALUATION_DATASET = [
    {
        "id": "grounded_001",
        "question": "Is database access read-only?",
        "required_facts": [
            [
                "database access is read-only",
                "read-only database access",
            ],
        ],
    },
    {
        "id": "grounded_002",
        "question": "Which destructive SQL operations are prohibited?",
        "required_facts": [
            ["INSERT"],
            ["UPDATE"],
            ["DELETE"],
            ["DROP"],
            ["ALTER"],
            ["TRUNCATE"],
            ["GRANT"],
            ["REVOKE"],
        ],
    },
    {
        "id": "grounded_003",
        "question": "How are sensitive database operations protected?",
        "required_facts": [
            ["tool authorization"],
            ["secure SQL validation"],
        ],
    },
    {
        "id": "grounded_004",
        "question": "Are database rows and sensitive query results written to audit logs?",
        "required_facts": [
            ["sensitive query results"],
            ["returned database rows"],
            ["not be written to audit logs"],
        ],
    },
    {
        "id": "grounded_005",
        "question": "How should prompt injection attempts be handled?",
        "required_facts": [
            ["prompt injection"],
            ["untrusted instructions"],
        ],
    },
    {
        "id": "grounded_006",
        "question": "What security boundaries should the platform respect?",
        "required_facts": [
            ["authorization boundaries"],
            ["tenant isolation"],
            ["confidential-data controls"],
        ],
    },
]
