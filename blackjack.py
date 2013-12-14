"""
Python BlackJack implementation
"""
from random import shuffle

MIN_SHOE_LEN = 22
DECK_IN_SHOE = 2


def say(msg):
    print msg


def say_welcome(player="Player"):
    say("Hello %s and Welcome to our Casino!" % player)


def init_round(rnd, balance):
    """
    Welcome message at the beginning of each round.
    """
    say("Welcome to round number %s. Your balance is %.2f" % (rnd, balance))


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


def init_game():
    """
    Set the basic game world variables.
    """
    say_welcome()
    shoecards = init_shoe(num_decks=2)
    staring_balance = 100.0
    min_bet = 1.0
    return shoecards, staring_balance, min_bet


def draw_prompt():
    """
    Ask the player whether to draw a card or not
    """
    inp = ''
    while int not in ('y', 'Y', 'N', 'n'):
        inp = raw_input("Would you like to draw another card (Y/N)? ")
    return inp.lower() == 'y'


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


def player_turn(hand, shoe):
    """
    Run the player's turn
    """
    value = hand_score(hand)
    print "Your current hand is {} with the value of {}".format(hand, value)
    if value >= 21:
        return hand
    if draw_prompt():
        hand.append(shoe.pop())
        print "You draw {}. Current hand: {}".format(hand[-1], hand)
        return player_turn(hand, shoe)
    return hand


def dealer_turn(hand, shoe):
    """
    Run the dealer's turn.
    """
    value = hand_score(hand)
    if value >= 17:
        return hand
    hand.append(shoe.pop())
    print "Dealer drew {}. Current hand: {}".format(hand[-1], hand)
    return dealer_turn(hand, shoe)


def player_won(bet, balance):
    balance += bet * 2
    print "You WON {}! Current balance: {}".format(bet, balance)
    return balance


def player_lost(bet, balance):
    print "YOU LOST {}! Current balance: {}".format(bet, balance)
    return balance


def player_broke(rnd):
    print "You are BROKE after {} rounds of play. Get out of the casino!".format(rnd)


def draw(bet, balance):
    balance += bet
    print "Draw - you got the same score as the dealer. Current balance: {}".format(bet, balance)
    return balance


def ask_for_bet(balance, min_bet):
    """
    Ask the player to bet some amount
    """
    assert min_bet < balance, "You don't have enough money to play"
    while True:
        say("How much would you want to wager this time?")
        try:
            bet = raw_input(">>")  # if input is incorrect it will blow before we have a value for bet
            bet = float(bet)
            if bet > balance:  # if not (bet > min_bet and bet < balance)
                say("You don't have that kind of money on your account!")
            elif bet < 0:
                say("Negative bets are not allowed you ... cheater!")
            else:
                balance -= bet
                say("Bet of %.2f accepted!" % bet)
                return bet, balance
        except ValueError, e:
            say("%s is not a valid bet! Please enter a floating point number." % bet)


def check_outcome(phand, dhand, bet, balance):
    pscore = hand_score(phand)
    dscore = hand_score(dhand)
    if dscore > 21:
        balance = player_won(bet, balance)
    elif dscore == pscore:
        plen, hlen = len(phand), len(dhand)
        if dscore != 21:
            balance = draw(bet, balance)
        elif plen == 2:
            balance = player_won(bet, balance)
        elif hlen == 2:
            balance = player_lost(bet, balance)
        else:
            balance = draw(bet, balance)
    elif dscore > pscore:
        balance = player_lost(bet, balance)
    else:
        balance = player_won(bet, balance)
    return balance


def deal_cards(shoe):
    """
    Gets two cards for the player and one for the dealer
    """
    return [shoe.pop() for i in range(2)], [shoe.pop()]


# like main method is C#
if __name__ == "__main__":
    shoe, balance, min_bet = init_game()
    rnd = 0
    while balance > min_bet:
        rnd += 1
        init_round(rnd, balance)
        bet, balance = ask_for_bet(balance, min_bet)
        init_phand, init_dhand = deal_cards(shoe)
        player_hand = player_turn(init_phand, shoe)
        if hand_score(player_hand) > 21:
            balance = player_lost(bet, balance)
            continue
        else:
            dealer_hand = dealer_turn(init_dhand, shoe)
            balance = check_outcome(player_hand, dealer_hand, bet, balance)
        if len(shoe) < MIN_SHOE_LEN:
            shoe = init_shoe(DECK_IN_SHOE)

    player_broke(rnd)

