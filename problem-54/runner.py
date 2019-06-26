class Hand:
    def __init__(self, cards):
        self.cards = self.deconstruct_cards(cards)

    def __str__(self):
        return [r["raw"] for r in self.cards].join(" ")

    def __gt__(self, player2):
        # Rank hand, and get the value to match on
        player1_rank, player1_match = self.rank
        player2_rank, player2_match = player2.rank

        # Now that the hand is ranked compare and determine high cards
        # Simple match the rank is higher
        if player1_rank > player2_rank:
            return True

        # If the rank is the same we need to compare for high cards, and high pairs
        if player1_rank == player2_rank:
            # this is an annoying special case where there is no rank, but in the
            # instructions call for high card to win
            if player1_rank == 0 and self.high_card > player2.high_card:
                return True
            elif player1_rank == 0 and self.high_card <= player2.high_card:
                return False

            if player1_match > player2_match:
                return True

            if player1_match == player2_match:
                if self.high_card > player2.high_card:
                    return True

        return False

    @property
    def rank(self):
        # determine highest win and give it a value to compare with
        if self.is_straight and self.is_flush:
            # Royal Flush
            if sorted([c["value"] for c in self.cards]) == [10, 11, 12, 13, 14]:
                return 9, None

            # Straight Flush
            return 8, None

        if self.is_flush:
            return 5, None  # in real poker this could be more convoluted

        if self.is_straight:
            return 4, None  # in real poker this could be more convoluted

        repeats = list(self.repeat_cards())

        # no repeating cards. At this point you lose, probably.
        if len(repeats) == 0:
            return 0, None

        if len(repeats) == 1:
            # 4 of a kind
            if repeats[0]['total'] == 4:
                return 7, repeats[0]['value']

            # 3 of a kind
            if repeats[0]['total'] == 3:
                return 3, repeats[0]['value']

            # 1 pair
            if repeats[0]['total'] == 2:
                return 1, repeats[0]['value']

        if len(repeats) == 2:
            # 2 pair return highest pair match
            if repeats[0]['total'] == 2 and repeats[1]['total'] == 2:
                return 2, max([r['value'] for r in repeats])

            # Full House
            return 6, None

        return 0, None

    def deconstruct_cards(self, raw_cards):
        cards = []
        for c in raw_cards:
            val = c[:1]
            suit = c[1:]

            card_values = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

            if val in card_values:
                val = card_values[val]

            cards.append({"value": int(val), "suit": suit, "raw": c})

        return cards

    @property
    def is_straight(self):
        values = sorted([c["value"] for c in self.cards])

        return values == list(range(values[0], values[-1] + 1))

    @property
    def is_flush(self):
        hand = set([s["suit"] for s in self.cards])

        if len(hand) > 1:
            return False

        return True

    @property
    def high_card(self):
        return max([c["value"] for c in self.cards])

    def repeat_cards(self):
        # Used a generator here to show I know how.
        # Not really necessary other than reduced a couple lines of code
        values = [c["value"] for c in self.cards]

        for v in set(values):
            total = values.count(v)

            if total > 1:
                yield {'total': total, 'value': v}


def split_hands(hands):
    # no need to get fancy in this context we always have 5 cards per player
    # 10 cards total
    return Hand(hands[:5]), Hand(hands[5:])


if __name__ == "__main__":
    wins = 0

    with open("poker.txt") as file:
        for l in file:
            player1, player2 = split_hands(l.strip().split(" "))

            if player1 > player2:
                wins += 1

    print(f"Total Wins: {wins}")
