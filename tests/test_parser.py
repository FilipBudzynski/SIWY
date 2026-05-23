import pytest
from siwy.inference.parser import parse_ratings


def test_parse_comma_separated():
    assert parse_ratings("1,2,3,4,5,1,2,3,4,5") == [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]


def test_parse_with_labels():
    assert parse_ratings("1: 4\n2: 3\n3: 5\n4: 2\n5: 4\n6: 3\n7: 5\n8: 2\n9: 4\n10: 3") == [4, 3, 5, 2, 4, 3, 5, 2, 4, 3]


def test_parse_invalid():
    assert parse_ratings("abcdef") is None


def test_parse_partial():
    assert parse_ratings("1,2,3") is None


def test_rejects_out_of_range():
    assert parse_ratings("1,2,3,4,5,6,7,8,9,10") is None


def test_parse_inline_labeled():
    assert parse_ratings("1: 5, 2: 2, 3: 5, 4: 3, 5: 4, 6: 5, 7: 5, 8: 2, 9: 4, 10: 3") == [
        5, 2, 5, 3, 4, 5, 5, 2, 4, 3
    ]


def test_parse_labeled_with_annotation():
    raw = "1: 4 (Agree moderately)\n2: 2 (Disagree moderately)\n3: 5\n4: 4\n5: 5\n6: 5\n7: 5\n8: 1\n9: 3\n10: 2"
    assert parse_ratings(raw) == [4, 2, 5, 4, 5, 5, 5, 1, 3, 2]
