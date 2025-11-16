Security measures implemented

1) Settings
- DEBUG set to False.
- SECURE_BROWSER_XSS_FILTER = True
- X_FRAME_OPTIONS = 'DENY'
- SECURE_CONTENT_TYPE_NOSNIFF = True
- CSRF_COOKIE_SECURE = True
- SESSION_COOKIE_SECURE = True
- SECURE_HSTS_SECONDS = 31536000
- SECURE_HSTS_INCLUDE_SUBDOMAINS = True
- AUTH_USER_MODEL remains 'bookshelf.CustomUser'
- SecurityHeadersMiddleware added to inject CSP and common security response headers.

2) CSRF protection
- All POST forms include {% csrf_token %} in templates.
- CSRF middleware remains enabled in settings.

3) SQL injection protection and input validation
- All create/edit views use Django ModelForm (BookForm) which validates and cleans input.
- Search uses ORM filters with parameterized lookups (icontains), no raw SQL or string formatting.

4) Content Security Policy (CSP)
- CSP header is set by SecurityHeadersMiddleware:
  default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;

5) Additional protections
- Response headers include X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Referrer-Policy.
- Next-URL redirects are validated using url_has_allowed_host_and_scheme.

6) Testing guidance
- Run migrations, create superuser, create groups and assign permissions to test users.
- Test forms for CSRF token presence and that POST without token is rejected.
- Test XSS attempts by trying to submit scripts in text fields and confirm templates escape output.
- Verify CSP by checking browser console for blocked resources if loading from external domains.

7) Notes
- In development, you may keep SECURE_SSL_REDIRECT = False; enable it in production when HTTPS is configured.
- To enforce stricter policies, adjust CSP string in middleware or install django-csp package.
