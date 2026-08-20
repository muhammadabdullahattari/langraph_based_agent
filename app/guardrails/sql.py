import re

BLOCKED_SQL_PATTERN = re.compile(r"\b(DELETE|DROP|UPDATE|TRUNCATE)\b",re.IGNORECASE,)


def validate_sql(sql: str) -> bool:
    """
    Return True when SQL is safe to execute.
    Return False when SQL contains a blocked operation.
    """
    if not sql or not sql.strip():
        return False

    normalized_sql = re.sub(r"/\*.*?\*/|--[^\n]*"," ",sql,flags=re.DOTALL)
    normalized_sql = re.sub(r"\s+", " ", normalized_sql).strip()

    return not bool(BLOCKED_SQL_PATTERN.search(normalized_sql))