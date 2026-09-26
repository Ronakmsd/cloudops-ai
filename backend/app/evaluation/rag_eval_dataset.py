RAG_EVALUATION_DATASET = [
    {
        "id": "security_001",
        "question": "Is database access read-only?",
        "expected_concepts": [
            [
                "read-only database access",
                "database access is read-only",
            ],
        ],
    },
    {
        "id": "security_002",
        "question": "Which destructive SQL operations are prohibited?",
        "expected_concepts": [
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
        "id": "security_003",
        "question": "How are sensitive database operations protected?",
        "expected_concepts": [
            ["tool authorization"],
            ["secure SQL validation"],
        ],
    },
    {
        "id": "security_004",
        "question": "Are database rows and sensitive query results written to audit logs?",
        "expected_concepts": [
            ["sensitive query results"],
            ["returned database rows"],
            ["not be written to audit logs"],
        ],
    },
    {
        "id": "security_005",
        "question": "How should prompt injection attempts be handled?",
        "expected_concepts": [
            ["prompt injection"],
            ["untrusted instructions"],
        ],
    },
    {
        "id": "security_006",
        "question": "What security boundaries should the platform respect?",
        "expected_concepts": [
            ["authorization boundaries"],
            ["tenant isolation"],
            ["confidential-data controls"],
        ],
    },
]
