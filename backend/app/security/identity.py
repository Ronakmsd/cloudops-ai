from backend.app.security.tenant_authorization import SecurityContext


# Demo server-side identity mapping.
#
# IMPORTANT:
# This is NOT authentication.
# Production should derive the user identity from a verified
# JWT/OIDC identity rather than trusting a request body field.
IDENTITY_MAP: dict[str, SecurityContext] = {
    "ronak-e2e": SecurityContext(
        user_id="ronak-e2e",
        tenant_id="tenant-a",
        role="viewer",
    ),
}


def get_security_context(user_id: str) -> SecurityContext:
    context = IDENTITY_MAP.get(user_id)

    if context is None:
        raise PermissionError(
            f"No server-side security context is configured for user '{user_id}'."
        )

    return context
