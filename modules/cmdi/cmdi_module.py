#!/usr/bin/env python3
"""
Command Injection (CMDi) Payload Generator - Educational Framework
Author: Offensive Team Zeta
Organization: ITSOLERA (PVT) LTD
Purpose: Educational payload generation for authorized testing only

⚠️ ETHICAL USE ONLY - For learning and authorized penetration testing
❌ All patterns are disabled by default and marked as EXAMPLES ONLY
❌ No system commands are executed by this tool
"""

import argparse
import sys
import os
import json
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict

from .cmdi_docs import get_filter_bypass_explanation, get_module_reference


# ============================================================================
# PAYLOAD DATA MODEL
# ============================================================================

@dataclass
class CMDIPattern:
    """Data class representing a single command injection pattern"""
    pattern:          str
    os_type:          str   # linux | windows | both
    separator:        str   # the character used to chain commands
    description:      str
    why_filter_fails: str
    note:             str = "⚠️  EDUCATIONAL EXAMPLE — NOT EXECUTABLE"


# ============================================================================
# PATTERN LIBRARY
# ============================================================================

class CMDIPatternLibrary:
    """Library of educational command injection patterns"""

    @staticmethod
    def linux_patterns() -> List[CMDIPattern]:
        """Linux-specific command injection patterns"""
        return [
            CMDIPattern(
                pattern="INPUT_VALUE ; example_command",
                os_type="linux",
                separator=";",
                description="Semicolon separator — runs second command unconditionally",
                why_filter_fails=(
                    "Simple blacklists that strip only '&' or '|' miss ';'. "
                    "Semicolons are valid in many input contexts, making detection without "
                    "proper parameterisation difficult."
                ),
            ),
            CMDIPattern(
                pattern="INPUT_VALUE && example_command",
                os_type="linux",
                separator="&&",
                description="AND operator — runs second command only if first succeeds (exit 0)",
                why_filter_fails=(
                    "Some filters only strip single '&' and miss '&&'. "
                    "URL-encoded form (%26%26) bypasses naive string checks."
                ),
            ),
            CMDIPattern(
                pattern="INPUT_VALUE || example_command",
                os_type="linux",
                separator="||",
                description="OR operator — runs second command only if first fails (non-zero exit)",
                why_filter_fails=(
                    "Useful when original command intentionally fails. "
                    "Filters blocking '|' may not block '||' as a two-character sequence."
                ),
            ),
            CMDIPattern(
                pattern="INPUT_VALUE | example_command",
                os_type="linux",
                separator="|",
                description="Pipe — output of first command is stdin of second",
                why_filter_fails=(
                    "Pipe is common in filenames and grep patterns; pure filtering "
                    "causes legitimate failures. Developers often leave it unblocked."
                ),
            ),
            CMDIPattern(
                pattern="INPUT_VALUE `example_command`",
                os_type="linux",
                separator="`",
                description="Backtick substitution — executes and substitutes command output inline",
                why_filter_fails=(
                    "Backtick is rare in normal input, but filters targeting '&', ';', '|' "
                    "entirely skip backtick. Modern shells also accept $() as equivalent."
                ),
            ),
            CMDIPattern(
                pattern="INPUT_VALUE $(example_command)",
                os_type="linux",
                separator="$(",
                description="Dollar-paren substitution — POSIX alternative to backticks, nestable",
                why_filter_fails=(
                    "Filters rarely block '$(' because dollar signs appear in variables. "
                    "Encoding as %24%28 bypasses naive string filters entirely."
                ),
            ),
            CMDIPattern(
                pattern="INPUT_VALUE%0Aexample_command",
                os_type="linux",
                separator="%0A",
                description="URL-encoded newline — shell interprets newline as command separator",
                why_filter_fails=(
                    "Filters applied before URL-decoding miss encoded separators. "
                    "If the application decodes input before passing to shell, newline acts as ';'."
                ),
            ),
            CMDIPattern(
                pattern="${IFS}example_command",
                os_type="linux",
                separator="${IFS}",
                description="Internal Field Separator abuse — replaces spaces to bypass space filters",
                why_filter_fails=(
                    "Filters that block space characters to prevent argument injection "
                    "are bypassed by $IFS, which the shell expands to whitespace."
                ),
            ),
        ]

    @staticmethod
    def windows_patterns() -> List[CMDIPattern]:
        """Windows-specific command injection patterns"""
        return [
            CMDIPattern(
                pattern="INPUT_VALUE & example_command",
                os_type="windows",
                separator="&",
                description="Windows ampersand — runs second command unconditionally (cmd.exe)",
                why_filter_fails=(
                    "Ampersand is common in URL query strings (?a=1&b=2). "
                    "Developers often allow it, creating a blind spot for command chaining."
                ),
            ),
            CMDIPattern(
                pattern="INPUT_VALUE && example_command",
                os_type="windows",
                separator="&&",
                description="Windows AND — second command runs only if first succeeds",
                why_filter_fails=(
                    "Same as Linux: '&' filtered but '&&' missed, "
                    "or URL-encoded form %26%26 bypasses string-level checks."
                ),
            ),
            CMDIPattern(
                pattern="INPUT_VALUE || example_command",
                os_type="windows",
                separator="||",
                description="Windows OR — second command runs only if first fails",
                why_filter_fails=(
                    "Identical double-pipe bypass logic as Linux. "
                    "Useful when original command errors (e.g., invalid path)."
                ),
            ),
            CMDIPattern(
                pattern="INPUT_VALUE | example_command",
                os_type="windows",
                separator="|",
                description="Windows pipe — stdout of first becomes stdin of second",
                why_filter_fails=(
                    "Pipe commonly whitelisted for legitimate use (e.g., dir | findstr). "
                    "URL-encoded %7C may also pass through naive filters."
                ),
            ),
            CMDIPattern(
                pattern="INPUT_VALUE%0D%0Aexample_command",
                os_type="windows",
                separator="%0D%0A",
                description="CRLF encoded newline — cmd.exe treats CR+LF as command delimiter",
                why_filter_fails=(
                    "Filters applied before decoding miss CRLF. "
                    "Useful when the shell processes URL-decoded strings."
                ),
            ),
            CMDIPattern(
                pattern="INPUT_VALUE ^& example_command",
                os_type="windows",
                separator="^&",
                description="Caret-escaped ampersand — cmd.exe caret is an escape character",
                why_filter_fails=(
                    "Filters blocking '&' may not account for '^&' which cmd.exe "
                    "interprets as a literal '&' that then acts as command separator."
                ),
            ),
        ]

    @staticmethod
    def all_patterns() -> List[CMDIPattern]:
        """Return combined list of all patterns"""
        lib = CMDIPatternLibrary()
        return lib.linux_patterns() + lib.windows_patterns()


# ============================================================================
# GENERATOR
# ============================================================================

class CMDIGenerator:
    """Main Command Injection educational pattern generator"""

    def __init__(self):
        self._library = CMDIPatternLibrary()

    def get_patterns(self, os_type: str = 'all') -> List[CMDIPattern]:
        """Return patterns filtered by OS"""
        if os_type == 'linux':
            return self._library.linux_patterns()
        elif os_type == 'windows':
            return self._library.windows_patterns()
        else:
            return self._library.all_patterns()

    def display_cli(self, patterns: List[CMDIPattern], include_explanation: bool = False) -> int:
        """Print patterns to terminal in formatted output"""
        current_os = None
        for i, p in enumerate(patterns, 1):
            if p.os_type != current_os:
                current_os = p.os_type
                label = f"{p.os_type.upper()} INJECTION PATTERNS"
                print("\n" + "=" * 80)
                print(f"{label:^80}")
                print("=" * 80 + "\n")

            print(f"[{i}] OS: {p.os_type.upper()} | Separator: {p.separator!r}")
            print(f"Description : {p.description}")
            print(f"Pattern     : {p.pattern}")
            print(f"Note        : {p.note}")
            if include_explanation:
                print(f"Filter Bypass: {p.why_filter_fails}")
            print("-" * 80)
        return len(patterns)

    def export_txt(self, patterns: List[CMDIPattern], os_label: str, output_dir: str = "cmdi_output"):
        """Export patterns to plain-text catalog"""
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"cmdi_{os_label.lower()}_payloads.txt")
        with open(path, 'w') as f:
            f.write(f"# Command Injection Pattern Catalog — {os_label.upper()}\n")
            f.write(f"# Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("# Purpose   : Educational & authorized testing only\n")
            f.write("# WARNING   : Patterns are NON-EXECUTABLE string templates\n\n")
            for p in patterns:
                f.write(f"# [{p.os_type.upper()}] {p.separator} — {p.description}\n")
                f.write(f"{p.pattern}\n\n")
        print(f"  ✅ TXT exported  → {path}")

    def export_burp(self, patterns: List[CMDIPattern], os_label: str, output_dir: str = "cmdi_output"):
        """Export patterns in Burp Suite Intruder format (one per line)"""
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"cmdi_{os_label.lower()}_burp.txt")
        with open(path, 'w') as f:
            for p in patterns:
                f.write(f"{p.pattern}\n")
        print(f"  ✅ Burp export   → {path}")

    def export_zap(self, patterns: List[CMDIPattern], os_label: str, output_dir: str = "cmdi_output"):
        """Export patterns in OWASP ZAP Fuzzer format"""
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"cmdi_{os_label.lower()}_zap.txt")
        with open(path, 'w') as f:
            f.write("# OWASP ZAP Fuzzer Payload List\n")
            f.write(f"# Command Injection — {os_label.upper()}\n\n")
            for p in patterns:
                f.write(f"{p.pattern}\n")
        print(f"  ✅ ZAP export    → {path}")

    def export_json_full(self, patterns: List[CMDIPattern], os_label: str, output_dir: str = "cmdi_output"):
        """Export full pattern data to JSON"""
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"cmdi_{os_label.lower()}_payloads.json")
        data = [
            {
                'pattern':          p.pattern,
                'os_type':          p.os_type,
                'separator':        p.separator,
                'description':      p.description,
                'why_filter_fails': p.why_filter_fails,
                'note':             p.note,
            }
            for p in patterns
        ]
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"  ✅ JSON exported → {path}")

    def display_defensive_notes(self):
        """Display defensive countermeasures"""
        notes = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║          DEFENSIVE NOTES — Command Injection                     ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║  Why WAFs Block CMDi Payloads:                                   ║
    ║  • Signature rules matching ;, &&, ||, |, $(), backtick           ║
    ║  • Anomaly detection on special character density                 ║
    ║  • Context-aware parsers that detect OS command syntax            ║
    ║                                                                  ║
    ║  How Modern Defenses Detect Evasion:                             ║
    ║  • URL/hex decoding before pattern matching                       ║
    ║  • Multi-layered normalisation (double encoding, IFS abuse)       ║
    ║  • Shell-specific syntax analysis (bash vs sh vs cmd.exe)         ║
    ║                                                                  ║
    ║  Best Defenses Against CMDi:                                     ║
    ║  • Never pass user input directly to shell functions ← #1         ║
    ║  • Use language APIs instead of shell: os.listdir() not ls        ║
    ║  • Strict allowlist validation on any input used near shell       ║
    ║  • Disable shell=True in Python subprocess calls                  ║
    ║  • Principle of least privilege on the server process             ║
    ║  • WAF rules + DAST scanning (Burp / ZAP)                         ║
    ║                                                                  ║
    ║  Reference:                                                      ║
    ║  https://owasp.org/www-community/attacks/Command_Injection        ║
    ╚══════════════════════════════════════════════════════════════════╝
        """
        print(notes)

    def display_filter_bypass_note(self):
        """Display the filter bypass educational explanation"""
        print("\n" + "="*70)
        print("  FILTER BYPASS EXPLANATIONS")
        print("="*70)
        print(get_filter_bypass_explanation())


# ============================================================================
# BANNER & ETHICS
# ============================================================================

def print_banner():
    """Display tool banner"""
    banner = """
   ═══════════════════════════════════════════════════════════════

        ██████╗███╗   ███╗██████╗ ██╗
       ██╔════╝████╗ ████║██╔══██╗██║
       ██║     ██╔████╔██║██║  ██║██║
       ██║     ██║╚██╔╝██║██║  ██║██║
       ╚██████╗██║ ╚═╝ ██║██████╔╝██║
        ╚═════╝╚═╝     ╚═╝╚═════╝ ╚═╝

           INJECTION PAYLOAD GENERATOR

   ═══════════════════════════════════════════════════════════════

    Purpose: Command injection pattern study for security learning
    """
    print(banner)


def print_ethical_warning():
    """Display ethical use warning"""
    warning = """
    ⚠️  ETHICAL DISCLAIMER:
    ═══════════════════════════════════════════════════════════════
    This tool is for EDUCATIONAL and AUTHORIZED testing ONLY.

    ✅ Permitted Use:
       • Authorized penetration testing
       • Academic learning and research
       • CTF challenges and security labs
       • Your own systems and environments

    ❌ Prohibited Use:
       • Unauthorized system access
       • Real-world attacks without permission
       • Any illegal activities

    ❌ All patterns are DISABLED by default and marked as EXAMPLES.
    ❌ No system commands are executed by this tool.

    By using this tool, you agree to comply with all applicable laws
    and ethical guidelines (OWASP Code of Ethics).
    ═══════════════════════════════════════════════════════════════
    """
    print(warning)


# ============================================================================
# CLI ENTRY POINT
# ============================================================================

def main():
    """Main function — CLI argument parser"""

    parser = argparse.ArgumentParser(
        description='Educational Payload Generation Framework — CMDi Module',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py --module cmdi
  python3 main.py --module cmdi --os linux
  python3 main.py --module cmdi --os windows --output json
  python3 main.py --module cmdi --os linux --explain
  python3 main.py --module cmdi --output burp --no-banner
  python3 main.py --module cmdi --output zap --no-banner
  python3 main.py --module cmdi --output all --no-banner
  python3 main.py --module cmdi --defensive

For more information: https://owasp.org/www-community/attacks/Command_Injection
        """
    )

    # ── Module selector (consistent with XSS / SQLi style) ───────────────────
    parser.add_argument(
        '--module',
        choices=['cmdi'],
        default='cmdi',
        help='Select vulnerability module (default: cmdi)'
    )

    # ── OS target ─────────────────────────────────────────────────────────────
    parser.add_argument(
        '--os',
        choices=['linux', 'windows', 'all'],
        default='all',
        help='Target OS: linux, windows, or all (default: all)'
    )

    # ── Output format ──────────────────────────────────────────────────────────
    parser.add_argument(
        '--output',
        choices=['cli', 'json', 'txt', 'burp', 'zap', 'all'],
        default='cli',
        help=(
            'Output format: cli, json, txt, burp, zap, all\n'
            '  cli  - Print to terminal\n'
            '  json - Export JSON file\n'
            '  txt  - Export plain text catalog\n'
            '  burp - Export Burp Suite Intruder list\n'
            '  zap  - Export OWASP ZAP Fuzzer list\n'
            '  all  - Export all formats at once\n'
            '(default: cli)'
        )
    )

    parser.add_argument(
        '--explain',
        action='store_true',
        help='Include "why filters fail" explanation for each pattern'
    )

    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show pattern statistics summary'
    )

    parser.add_argument(
        '--bypass',
        action='store_true',
        help='Show filter bypass explanation and why sanitisation fails'
    )

    parser.add_argument(
        '--defensive',
        action='store_true',
        help='Show defensive notes and WAF countermeasures'
    )

    parser.add_argument(
        '--no-banner',
        action='store_true',
        help='Suppress banner and ethical warning prompt'
    )

    args = parser.parse_args()

    # ── Banner / ethics gate ──────────────────────────────────────────────────
    if not args.no_banner:
        print_banner()
        print_ethical_warning()
        confirm = input("\n⚠️  Do you agree to use this tool ethically? (yes/no): ").strip().lower()
        if confirm not in ['yes', 'y']:
            print("\n❌ User declined ethical terms. Exiting...")
            sys.exit(0)
        print("\n✅ Proceeding with pattern generation...\n")

    generator = CMDIGenerator()

    # ── Defensive notes only ──────────────────────────────────────────────────
    if args.defensive:
        generator.display_defensive_notes()
        sys.exit(0)

    # ── Bypass / filter explanation ───────────────────────────────────────────
    if args.bypass:
        generator.display_filter_bypass_note()

    # ── Generate patterns ─────────────────────────────────────────────────────
    patterns = generator.get_patterns(args.os)

    # Stats summary
    if args.stats:
        linux_count   = sum(1 for p in patterns if p.os_type == 'linux')
        windows_count = sum(1 for p in patterns if p.os_type == 'windows')
        print(f"\n📊 Stats: {len(patterns)} patterns total  "
              f"(Linux: {linux_count}, Windows: {windows_count})")

    os_label = args.os

    # ── Output routing ────────────────────────────────────────────────────────
    if args.output == 'all':
        print(f"\n📦 Exporting all formats for OS: {os_label.upper()}...")
        generator.display_cli(patterns, include_explanation=args.explain)
        generator.export_json_full(patterns, os_label)
        generator.export_txt(patterns, os_label)
        generator.export_burp(patterns, os_label)
        generator.export_zap(patterns, os_label)
        print(f"\n✅ All formats exported to cmdi_output/")
    elif args.output == 'cli':
        count = generator.display_cli(patterns, include_explanation=args.explain)
        print(f"\n✅ Generated {count} CMDi pattern templates for OS: {os_label.upper()}")
    elif args.output == 'json':
        generator.export_json_full(patterns, os_label)
    elif args.output == 'txt':
        generator.export_txt(patterns, os_label)
    elif args.output == 'burp':
        generator.export_burp(patterns, os_label)
    elif args.output == 'zap':
        generator.export_zap(patterns, os_label)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error occurred: {e}")
        sys.exit(1)
