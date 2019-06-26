import pytest

from runner import Hand, split_hands


class TestHand:
    @pytest.mark.parametrize(
        "values,expected",
        [
            (["1D", "2D", "3D", "4D", "5D"], 5),
            (["1D", "2D", "3D", "4D", "TD"], 10),
            (["1D", "2D", "3D", "4D", "JD"], 11),
            (["1D", "2D", "3D", "4D", "QD"], 12),
            (["1D", "2D", "3D", "4D", "KD"], 13),
            (["1D", "2D", "3D", "4D", "AD"], 14),
            (["TD", "JD", "QD", "KD", "AD"], 14),
            (["TD", "JD", "QD", "1D", "2D"], 12),
        ],
    )
    def test_high_card(self, values, expected):
        hand = Hand(values)
        assert hand.high_card == expected

    def test_is_flush_true(self):
        hand = Hand(["1D", "2D", "3D", "4D", "TD"])
        assert hand.is_flush

    def test_is_flush_false(self):
        hand = Hand(["1D", "2D", "3D", "4D", "TS"])

        assert not hand.is_flush

    @pytest.mark.parametrize(
        "values,expected",
        [
            (["1D", "1H", "3D", "4D", "5D"], [{"total": 2, "value": 1}]),
            (["1D", "1S", "1H", "4D", "TD"], [{"total": 3, "value": 1}]),
            (["1D", "1H", "1S", "1C", "JD"], [{"total": 4, "value": 1}]),
            (
                ["1D", "1H", "2S", "2C", "JD"],
                [{"total": 2, "value": 1}, {"total": 2, "value": 2}],
            ),
            (
                ["1D", "1H", "2S", "2C", "2D"],
                [{"total": 2, "value": 1}, {"total": 3, "value": 2}],
            ),
        ],
    )
    def test_repeat_cards(self, values, expected):
        hand = Hand(values)

        assert list(hand.repeat_cards()) == expected

    @pytest.mark.parametrize(
        "values,expected",
        [
            (["1D", "2D", "3D", "4D", "5D"], True),  # All numbers
            (["5D", "6D", "7D", "8D", "TD"], False),  # All numbers plus a royal
            (["8D", "9D", "TD", "JD", "QD"], True),  # 2 numbers 3 royals
            (["TD", "JD", "QD", "KD", "AD"], True),  # Royal Flush
            (["TD", "JD", "QD", "1D", "2D"], False),  # Wrap around straight
        ],
    )
    def test_is_straight(self, values, expected):
        hand = Hand(values)

        assert hand.is_straight == expected

    def test_deconstruct_cards_through_init(self):
        hand = Hand(["8C", "TS", "KC", "9H", "4S"])

        assert hand.cards == [
            {"value": 8, "suit": "C", "raw": "8C"},
            {"value": 10, "suit": "S", "raw": "TS"},
            {"value": 13, "suit": "C", "raw": "KC"},
            {"value": 9, "suit": "H", "raw": "9H"},
            {"value": 4, "suit": "S", "raw": "4S"},
        ]

    @pytest.mark.parametrize(
        "values,expected",
        [
            (["1S", "2S", "3S", "5D", "TC"], (0, None)),  # Nothing
            (["1S", "1C", "3S", "5D", "TC"], (1, 1)),  # 1 Pair
            (["2S", "2D", "3S", "3C", "AC"], (2, 3)),  # 2 Pair
            (["2S", "2C", "2D", "5D", "TC"], (3, 2)),  # 3 of a kind
            (["1D", "2D", "3C", "4D", "5S"], (4, None)),  # Straight
            (["1D", "2D", "3D", "4D", "TD"], (5, None)),  # Flush
            (["1D", "1S", "1C", "2S", "2C"], (6, None)),  # Full House
            (["AD", "AS", "AC", "AH", "5C"], (7, 14)),  # 4 of a kind
            (["1S", "2S", "3S", "4S", "5S"], (8, None)),  # Straight Flush
            (["TD", "JD", "QD", "KD", "AD"], (9, None)),  # Royal Flush
        ],
    )
    def test_rank(self, values, expected):
        hand = Hand(values)

        assert hand.rank == expected

    @pytest.mark.parametrize(
        "player1,player2,expected",
        [
            (  # Player1 ranks higher
                ["1D", "1C", "5D", "6D", "7D"],
                ["1S", "2C", "3C", "5S", "TD"],
                True,
            ),
            (  # Player2 ranks higher
                ["1S", "2C", "3C", "5S", "TD"],
                ["1D", "1C", "5D", "6D", "7D"],
                False,
            ),
            (  # Match and rank is 0, but player 1 high card
                ["1S", "2C", "3C", "5S", "AD"],
                ["1S", "2C", "3C", "5S", "TD"],
                True,
            ),
            (  # Match and rank is 0, but player 2 high card
                ["1S", "2C", "3C", "5S", "TD"],
                ["1S", "2C", "3C", "5S", "AD"],
                False,
            ),
            (  # Same rank above 0 player1 match is higher
                ["2S", "2D", "3C", "5S", "TD"],
                ["1C", "1H", "3C", "5S", "TD"],
                True,
            ),
            (  # Same rank above 0 player2 match is higher
                ["1C", "1H", "3C", "5S", "TD"],
                ["2S", "2D", "3C", "5S", "TD"],
                False,
            ),
            (  # Same rank and match, player 1 has high card
                ["1C", "1H", "3C", "5S", "QD"],
                ["1C", "1H", "3C", "5S", "TD"],
                True,
            ),
            (  # Same rank and match, player 2 has high card
                ["1C", "1H", "3C", "5S", "TD"],
                ["1C", "1H", "3C", "5S", "QD"],
                False,
            ),
        ],
    )
    def test_gt(self, player1, player2, expected):
        player1_hand = Hand(player1)
        player2_hand = Hand(player2)

        assert (player1_hand > player2_hand) == expected
