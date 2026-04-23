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
