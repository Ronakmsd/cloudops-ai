# CloudOps AI Security Policy

CloudOps AI uses defense-in-depth security controls for enterprise data access.

The Data Agent must inspect the database schema before generating SQL when the required tables or columns are unknown.

Database access is read-only. Destructive SQL operations such as INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, GRANT and REVOKE are prohibited.

Sensitive database operations pass through tool authorization and secure SQL validation.

Prompt injection attempts must be treated as untrusted instructions and must not override system or agent policies.

SQL execution events are recorded through an audit logger. Returned database rows and sensitive query results must not be written to audit logs.

The platform should respect authorization boundaries, tenant isolation and confidential-data controls.
