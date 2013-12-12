from random import shuffle


def say(msg):
    print msg


def say_welcome(player="Player"):
    say("Hello %s and Welcome to our Casino!" % player)


def init_shoe(num_decks=1):
    """
    Generate a shuffled list of cards from num_decks number of decks
    """
    suits = ['s', 'h', 'd', 'c']
    ranks = ['J', 'Q', 'K', 'A'] + [str(i) for i in range(2, 11)]
    cards = [x + y for x in ranks for y in suits] * num_decks
    assert len(cards) == num_decks * 52
    shuffle(cards)
    print "Shuffled %s cards into the dealer shoe. Good luck!" % cards
    return cards


def hand_score(hand):
    """
    Calculate the score of a hand
    >>> hand_score(['As', 'Js'])
    21
    >>> hand_score(['As', 'As', 'As'])
    13
    >>> hand_score(['As', 'As', 'As', '10c']) #All aces now counted as 1
    13
    >>> hand_score(['Qs', '2s', '3h', '4c'])
    19
    >>> hand_score(['10s', '2c', '10c'])
    22
    """
    score = 0
    aces = 0
    for card in hand:
        if card[0].isdigit():
            score += int(card[:-1])
        elif card[0] in ('J', 'Q', 'K'):
            score += 10
        elif card[0] == 'A':
            aces += 1
        else:
            assert False, "WTF did you just give me?"
    score += max([aces - 1, 0]) * 1 # all aces after the first one are counted as 1 pt
    score += min([aces, 1]) * (1 if score >= 11 else 11)
    return score


def deal_cards(shoe):
    """
    Gets two cards for the player and one for the dealer
    """
    return [shoe.pop() for i in range(2)], [shoe.pop()]


def ask_for_bet(balance, min_bet):
    """
    Ask the player to bet some amount
    """
    while True:
        say("How much would you want to wager this time?")
        try:
            bet = raw_input(">>")
            bet = float(bet)
            if bet > balance: #if not (bet > min_bet and bet < balance)
                say("You don't have that kind of money on your account!")
            elif bet < 0:
                say("Negative bets are not allowed you ... cheater!")
            else:
                balance -= bet
                say("Bet of %.2f accepted!" % bet)
                return bet, balance
        except ValueError, e:
            say("%s is not a valid bet! Please enter a floating point number." % bet)


#like main method is C#
if __name__ == "__main__":
    say_welcome()
    print init_shoe()
