import pytest

from app.guardrails.sql import validate_sql


def test_allows_select():
    sql = "SELECT * FROM posts WHERE id = 1"

    assert validate_sql(sql) is True


def test_blocks_delete():
    sql = "DELETE FROM posts WHERE id = 1"

    assert validate_sql(sql) is False


def test_blocks_mixed_case_update():
    sql = "uPdAtE posts SET title = 'hacked' WHERE id = 1"

    assert validate_sql(sql) is False


def test_blocks_drop_with_comments_and_whitespace():
    sql = """
        /* harmless-looking comment */
        DrOp
        TABLE posts
    """

    assert validate_sql(sql) is False


def test_blocks_truncate():
    sql = "TRUNCATE    TABLE posts"

    assert validate_sql(sql) is False


def test_blocks_delete_with_comment():
    sql = "DELETE /* bypass attempt */ FROM posts"

    assert validate_sql(sql) is False


def test_rejects_empty_sql():
    assert validate_sql("") is False