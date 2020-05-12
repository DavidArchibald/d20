import pytest

from d20 import *


def test_comments():
    # standard nonconflicting expressions
    r = roll("1d20 foo bar", allow_comments=True)
    assert 1 <= r.total <= 20
    assert r.comment == "foo bar"

    with pytest.raises(RollSyntaxError):
        roll("1d20 foo bar", allow_comments=False)

    # expressions with ambiguity
    r = roll("1d20 keep something", allow_comments=True)
    assert 1 <= r.total <= 20
    assert r.comment == "keep something"

    # expressions with the possibility of being a dice
    r = roll("1d20 + 10 dungeons and dragons", allow_comments=True)
    assert 11 <= r.total <= 30
    assert r.comment == "dungeons and dragons"

    with pytest.raises(RollSyntaxError):
        roll("1d20 keep something", allow_comments=False)


def test_advantage():
    r = roll("1d20", advantage=AdvType.ADV)
    assert 1 <= r.total <= 20
    assert r.result.startswith("2d20kh1 ")

    r = roll("1d20", advantage=AdvType.DIS)
    assert 1 <= r.total <= 20
    assert r.result.startswith("2d20kl1 ")

    r = roll("1d20", advantage=AdvType.NONE)
    assert 1 <= r.total <= 20
    assert r.result.startswith("1d20 ")

    # adv/dis should do nothing on non-d20s
    r = roll("1d6", advantage=AdvType.ADV)
    assert 1 <= r.total <= 6
    assert r.result.startswith("1d6 ")

    r = roll("1d6", advantage=AdvType.DIS)
    assert 1 <= r.total <= 6
    assert r.result.startswith("1d6 ")


def test_rolling_ast():
    the_ast = parse("1d20")
    r = roll(the_ast)

    assert 1 <= r.total <= 20
    assert r.result.startswith("1d20 ")
