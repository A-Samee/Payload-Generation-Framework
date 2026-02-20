"""
Command Injection Documentation
Educational Explanations Only
"""

def get_filter_bypass_explanation():
    return """
Why Input Filters Fail in Command Injection:

1. Blacklist Filtering:
   Developers block specific characters like ';' or '&&',
   but attackers use alternative separators or encoding.

2. Incomplete Sanitization:
   Removing one dangerous character does not prevent
   exploitation using others.

3. OS Differences:
   Windows and Linux use different command chaining syntax.

4. Improper Escaping:
   Failure to properly escape user input before passing
   to system shell functions leads to injection.

5. Lack of Parameterization:
   Unlike SQL, many system command calls do not enforce
   strict parameter binding by default.
"""


def get_module_reference():
    return {
        "title": "OWASP Command Injection",
        "reference_url": "https://owasp.org/www-community/attacks/Command_Injection",
        "note": "Study reference only"
    }