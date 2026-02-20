#!/usr/bin/env python3
"""
Offensive Security Tool - Payload Generation Framework
Author: Offensive Team Zeta
Organization: ITSOLERA (PVT) LTD
Purpose: Educational payload generation for authorized testing only

Modules:
  --module xss   → XSS Payload Generator
  --module sqli  → SQL Injection Payload Generator
  --module cmdi  → Command Injection Pattern Generator

⚠️  ETHICAL USE ONLY — Strictly for authorized testing, academic learning,
    and defensive research in line with OWASP ethical standards.
"""

import argparse
import os
import sys

# ── Resolve project root so imports work regardless of cwd ───────────────────
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


# ============================================================================
# BANNER & ETHICS
# ============================================================================

def print_banner():
    banner = r"""
   ═══════════════════════════════════════════════════════════════════════

     ██████╗  █████╗ ██╗   ██╗██╗      ██████╗  █████╗ ██████╗
     ██╔══██╗██╔══██╗╚██╗ ██╔╝██║     ██╔═══██╗██╔══██╗██╔══██╗
     ██████╔╝███████║ ╚████╔╝ ██║     ██║   ██║███████║██║  ██║
     ██╔═══╝ ██╔══██║  ╚██╔╝  ██║     ██║   ██║██╔══██║██║  ██║
     ██║     ██║  ██║   ██║   ███████╗╚██████╔╝██║  ██║██████╔╝
     ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝

           GENERATION FRAMEWORK  —  ITSOLERA (PVT) LTD

   ═══════════════════════════════════════════════════════════════════════

    Modules  : XSS  |  SQL Injection  |  Command Injection
    Usage    : python3 main.py --module <xss|sqli|cmdi> [options]
    Reference: https://owasp.org/www-project-web-security-testing-guide/
    """
    print(banner)


def print_ethical_warning():
    warning = """
    ⚠️  ETHICAL DISCLAIMER:
    ═══════════════════════════════════════════════════════════════════════
    This tool is for EDUCATIONAL and AUTHORIZED testing ONLY.

    ✅ Permitted Use:
       • Authorized penetration testing with written permission
       • Academic learning, research, and CTF challenges
       • Your own systems and controlled lab environments

    ❌ Prohibited Use:
       • Unauthorized access to any systems or databases
       • Real-world attacks without explicit permission
       • Any activity that violates local or international law

    Aligned with OWASP Code of Ethics:
    https://owasp.org/www-project-code-of-ethics/
    ═══════════════════════════════════════════════════════════════════════
    """
    print(warning)


# ============================================================================
# ARGUMENT PARSER
# ============================================================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='main.py',
        description='Offensive Security Payload Generation Framework — ITSOLERA',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
─── XSS Examples ──────────────────────────────────────────────────────────────
  python3 main.py --module xss
  python3 main.py --module xss --type reflected --context html
  python3 main.py --module xss --type stored --encode url --output json
  python3 main.py --module xss --bypass --output burp --no-banner
  python3 main.py --module xss --bypass --output zap  --no-banner
  python3 main.py --module xss --output all --no-banner
  python3 main.py --module xss --defensive

─── SQLi Examples ─────────────────────────────────────────────────────────────
  python3 main.py --module sqli
  python3 main.py --module sqli --db mysql
  python3 main.py --module sqli --db postgresql --type union
  python3 main.py --module sqli --db all --encode base64 --output json
  python3 main.py --module sqli --bypass --output burp --no-banner
  python3 main.py --module sqli --output all --no-banner
  python3 main.py --module sqli --defensive

─── CMDi Examples ─────────────────────────────────────────────────────────────
  python3 main.py --module cmdi
  python3 main.py --module cmdi --os linux --explain
  python3 main.py --module cmdi --os windows --output txt
  python3 main.py --module cmdi --bypass --output zap --no-banner
  python3 main.py --module cmdi --output all --no-banner
  python3 main.py --module cmdi --defensive

Reference:
  https://owasp.org/www-project-web-security-testing-guide/
        """
    )

    # ── Required ──────────────────────────────────────────────────────────────
    parser.add_argument(
        '--module',
        choices=['xss', 'sqli', 'cmdi'],
        required=True,
        metavar='MODULE',
        help='Vulnerability module to use: xss | sqli | cmdi'
    )

    # ── XSS-specific ──────────────────────────────────────────────────────────
    xss_group = parser.add_argument_group('XSS options')
    xss_group.add_argument(
        '--type',
        default='all',
        metavar='TYPE',
        help=(
            '[xss]  reflected | stored | dom | all  (default: all)\n'
            '[sqli] error | union | blind | time | comment | all  (default: all)'
        )
    )
    xss_group.add_argument(
        '--context',
        choices=['html', 'attribute', 'javascript', 'all'],
        default='all',
        metavar='CTX',
        help='[xss] Injection context: html | attribute | javascript | all  (default: all)'
    )

    # ── SQLi-specific ─────────────────────────────────────────────────────────
    sqli_group = parser.add_argument_group('SQLi options')
    sqli_group.add_argument(
        '--db',
        choices=['mysql', 'postgresql', 'mssql', 'all'],
        default='all',
        metavar='DB',
        help='[sqli] Database type: mysql | postgresql | mssql | all  (default: all)'
    )

    # ── CMDi-specific ─────────────────────────────────────────────────────────
    cmdi_group = parser.add_argument_group('CMDi options')
    cmdi_group.add_argument(
        '--os',
        choices=['linux', 'windows', 'all'],
        default='all',
        metavar='OS',
        help='[cmdi] Target OS: linux | windows | all  (default: all)'
    )

    # ── Shared flags ──────────────────────────────────────────────────────────
    shared = parser.add_argument_group('Shared options')
    shared.add_argument(
        '--encode',
        choices=['none', 'url', 'base64', 'hex'],
        default='none',
        help='Encoding method for payload/bypass demo: none | url | base64 | hex  (default: none)'
    )
    shared.add_argument(
        '--output',
        choices=['cli', 'json', 'txt', 'burp', 'zap', 'all'],
        default='cli',
        help=(
            'Output format:\n'
            '  cli  — print to terminal\n'
            '  json — export JSON file\n'
            '  txt  — export plain-text catalog\n'
            '  burp — export Burp Suite Intruder list\n'
            '  zap  — export OWASP ZAP Fuzzer list\n'
            '  all  — export every format at once\n'
            '(default: cli)'
        )
    )
    shared.add_argument(
        '--bypass',
        action='store_true',
        help='Include WAF/IDS bypass techniques and evasion demonstrations'
    )
    shared.add_argument(
        '--explain',
        action='store_true',
        help='Include detailed explanation for each payload / pattern'
    )
    shared.add_argument(
        '--stats',
        action='store_true',
        help='Display payload / pattern count statistics'
    )
    shared.add_argument(
        '--defensive',
        action='store_true',
        help='Show defensive countermeasures and WAF detection notes, then exit'
    )
    shared.add_argument(
        '--no-banner',
        action='store_true',
        help='Suppress banner and skip the ethics confirmation prompt'
    )

    return parser


# ============================================================================
# MODULE ROUTES
# ============================================================================

def run_xss(args):
    """Route XSS module — imports from modules/xss/xss_module.py"""
    try:
        from modules.xss.xss_module import XSSGenerator
    except ImportError as e:
        print(f"\n❌  Cannot import XSS module: {e}")
        print(f"    Expected: {ROOT_DIR}/modules/xss/xss_module.py")
        sys.exit(1)

    generator = XSSGenerator()

    if args.defensive:
        generator.display_defensive_notes()
        return

    if args.stats:
        s = generator.get_stats()
        print(f"\n📊  XSS Stats  —  total: {s['total_payloads']}  |  "
              f"by type: {s['by_type']}  |  by severity: {s['by_severity']}\n")

    payloads = generator.generate(
        xss_type           = args.type    if args.type    != 'all'  else None,
        context            = args.context if args.context != 'all'  else None,
        encoding           = args.encode  if args.encode  != 'none' else None,
        include_bypass     = args.bypass,
        include_explanation= args.explain,
    )

    xss_out = os.path.join(ROOT_DIR, 'payloads', 'output', 'xss')
    os.makedirs(xss_out, exist_ok=True)

    if args.output == 'all':
        print("\n📦  Exporting all XSS formats …")
        generator.display_cli(payloads)
        generator.export_json(payloads, os.path.join(xss_out, 'xss_payloads.json'))
        generator.export_txt(payloads, os.path.join(xss_out, 'xss_payloads.txt'))
        generator.export_burp(payloads, os.path.join(xss_out, 'xss_burp_payloads.txt'))
        generator.export_zap(payloads, os.path.join(xss_out, 'xss_zap_payloads.txt'))
        print(f"\n✅  All formats saved to {xss_out}/")
    elif args.output == 'cli':
        generator.display_cli(payloads)
        print(f"\n✅  Generated {len(payloads)} XSS payload templates")
    elif args.output == 'json':
        generator.export_json(payloads, os.path.join(xss_out, 'xss_payloads.json'))
    elif args.output == 'txt':
        generator.export_txt(payloads, os.path.join(xss_out, 'xss_payloads.txt'))
    elif args.output == 'burp':
        generator.export_burp(payloads, os.path.join(xss_out, 'xss_burp_payloads.txt'))
    elif args.output == 'zap':
        generator.export_zap(payloads, os.path.join(xss_out, 'xss_zap_payloads.txt'))


def run_sqli(args):
    """Route SQLi module — imports from modules/sqli/sqli_module.py"""
    import urllib.parse, base64
    try:
        from modules.sqli.sqli_module import (
            SQLiPayloadGenerator, DatabaseType, CaseVariationBypass
        )
    except ImportError as e:
        print(f"\n❌  Cannot import SQLi module: {e}")
        print(f"    Expected: {ROOT_DIR}/modules/sqli/sqli_module.py")
        sys.exit(1)

    generator = SQLiPayloadGenerator()

    if args.defensive:
        generator.display_defensive_notes()
        return

    db_map = {
        'mysql':      DatabaseType.MYSQL,
        'postgresql': DatabaseType.POSTGRESQL,
        'mssql':      DatabaseType.MSSQL,
    }
    db_targets = list(db_map.items()) if args.db == 'all' else [(args.db, db_map[args.db])]

    sqli_type_map = {
        'error':   'error_based',
        'union':   'union_based',
        'blind':   'boolean_blind',
        'time':    'time_based',
        'comment': 'comment_bypass',
    }

    for db_label, db_type in db_targets:
        payloads_dict = generator.generate_payloads_by_database(db_type)

        if args.type not in ('all', None):
            key = sqli_type_map.get(args.type)
            if key:
                payloads_dict = {key: payloads_dict.get(key, [])}

        if args.stats:
            total = sum(len(v) for v in payloads_dict.values())
            print(f"\n📊  SQLi Stats [{db_label.upper()}]  —  "
                  f"{total} payloads across {len(payloads_dict)} categories")

        if args.bypass:
            sample = "UNION SELECT user(), version()"
            print(f"\n{'='*70}")
            print(f"  WAF/IDS BYPASS TECHNIQUES — {db_label.upper()}")
            print(f"{'='*70}")
            print(f"\n  Original          : {sample}")
            print("\n  Case variations:")
            for v in CaseVariationBypass.generate_case_variations(sample)[:3]:
                print(f"    {v}")
            print(f"\n  Comment bypass    : {CaseVariationBypass.generate_inline_comment_bypass(sample)}")
            print(f"  Whitespace bypass : {CaseVariationBypass.generate_whitespace_bypass(sample)}")
            print("\n  Encoding variations on 'admin':")
            for enc_type, enc_val in CaseVariationBypass.generate_encoding_variations("admin").items():
                print(f"    {enc_type:8s}: {str(enc_val)[:60]}")

        if args.encode != 'none':
            flat = [p for plist in payloads_dict.values() for p in plist]
            sample_p = flat[0].payload if flat else "1' OR '1'='1"
            print(f"\n  📦  Encoding ({args.encode}) — first payload:")
            if args.encode == 'url':
                print(f"    {urllib.parse.quote(sample_p)}")
            elif args.encode == 'base64':
                print(f"    {base64.b64encode(sample_p.encode()).decode()}")
            elif args.encode == 'hex':
                print(f"    {sample_p.encode().hex()}")

        out_dir = os.path.join(ROOT_DIR, 'payloads', 'output', 'sqli')

        if args.output == 'all':
            print(f"\n📦  Exporting all SQLi formats for {db_label.upper()} …")
            generator.display_cli(payloads_dict, include_explanation=args.explain)
            generator.export_json_full(payloads_dict, db_label, out_dir)
            generator.export_txt(payloads_dict, db_label, out_dir)
            generator.export_burp(payloads_dict, db_label, out_dir)
            generator.export_zap(payloads_dict, db_label, out_dir)
            print(f"\n✅  All formats saved to {out_dir}/")
        elif args.output == 'cli':
            count = generator.display_cli(payloads_dict, include_explanation=args.explain)
            print(f"\n✅  Generated {count} SQLi payload templates for {db_label.upper()}")
        elif args.output == 'json':
            generator.export_json_full(payloads_dict, db_label, out_dir)
        elif args.output == 'txt':
            generator.export_txt(payloads_dict, db_label, out_dir)
        elif args.output == 'burp':
            generator.export_burp(payloads_dict, db_label, out_dir)
        elif args.output == 'zap':
            generator.export_zap(payloads_dict, db_label, out_dir)


def run_cmdi(args):
    """Route CMDi module — imports from modules/cmdi/cmdi_module.py"""
    try:
        from modules.cmdi.cmdi_module import CMDIGenerator
    except ImportError as e:
        print(f"\n❌  Cannot import CMDi module: {e}")
        print(f"    Expected: {ROOT_DIR}/modules/cmdi/cmdi_module.py")
        sys.exit(1)

    generator = CMDIGenerator()

    if args.defensive:
        generator.display_defensive_notes()
        return

    if args.bypass:
        generator.display_filter_bypass_note()

    patterns  = generator.get_patterns(args.os)
    os_label  = args.os
    out_dir   = os.path.join(ROOT_DIR, 'payloads', 'output', 'cmdi')

    if args.stats:
        linux_count   = sum(1 for p in patterns if p.os_type == 'linux')
        windows_count = sum(1 for p in patterns if p.os_type == 'windows')
        print(f"\n📊  CMDi Stats  —  {len(patterns)} patterns  "
              f"(Linux: {linux_count}, Windows: {windows_count})")

    if args.output == 'all':
        print(f"\n📦  Exporting all CMDi formats for OS: {os_label.upper()} …")
        generator.display_cli(patterns, include_explanation=args.explain)
        generator.export_json_full(patterns, os_label, out_dir)
        generator.export_txt(patterns, os_label, out_dir)
        generator.export_burp(patterns, os_label, out_dir)
        generator.export_zap(patterns, os_label, out_dir)
        print(f"\n✅  All formats saved to {out_dir}/")
    elif args.output == 'cli':
        count = generator.display_cli(patterns, include_explanation=args.explain)
        print(f"\n✅  Generated {count} CMDi pattern templates for OS: {os_label.upper()}")
    elif args.output == 'json':
        generator.export_json_full(patterns, os_label, out_dir)
    elif args.output == 'txt':
        generator.export_txt(patterns, os_label, out_dir)
    elif args.output == 'burp':
        generator.export_burp(patterns, os_label, out_dir)
    elif args.output == 'zap':
        generator.export_zap(patterns, os_label, out_dir)


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = build_parser()
    args   = parser.parse_args()

    # ── Banner / ethics gate ──────────────────────────────────────────────────
    if not args.no_banner:
        print_banner()
        print_ethical_warning()
        answer = input("⚠️   Do you agree to use this tool ethically? (yes/no): ").strip().lower()
        if answer not in ('yes', 'y'):
            print("\n❌  User declined ethical terms. Exiting.")
            sys.exit(0)
        print("\n✅  Proceeding with payload generation …\n")

    # ── Route to module ───────────────────────────────────────────────────────
    routes = {
        'xss':  run_xss,
        'sqli': run_sqli,
        'cmdi': run_cmdi,
    }
    routes[args.module](args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️   Operation cancelled by user (Ctrl+C)")
        sys.exit(0)
    except Exception as exc:
        print(f"\n❌  Unexpected error: {exc}")
        import traceback; traceback.print_exc()
        sys.exit(1)
