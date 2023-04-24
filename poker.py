# Define the players and deal the cards as before
import random

suits = ["hearts", "clubs", "diamonds", "spades"]
ranks = ["Ace", "2", "3", "4", "5", "6", "7",
         "8", "9", "10", "Jack", "Queen", "King"]
deck = []

for suit in suits:
    for rank in ranks:
        card = rank + " of " + suit
        deck.append(card)

for i in range(len(deck) - 1, 0, -1):
    j = random.randint(0, i)
    deck[i], deck[j] = deck[j], deck[i]

num_players = int(input("How many players? "))
players = [[] for _ in range(num_players)]

for i in range(2):
    for player in players:
        card = deck.pop()
        player.append(card)

# Define the betting rounds
betting_rounds = ["Preflop", "Flop", "Turn", "River"]

for i, round in enumerate(betting_rounds):
    print(f"\n{round}:")

    # Each player makes a bet, call, raise, or fold
    bets = [0] * num_players
    round_over = False

    while not round_over:
        for j, player in enumerate(players):
            print(f"\nPlayer {j+1}'s turn:")
            print(f"Current bet: {max(bets)}")
            print(f"Player {j+1}'s current bet: {bets[j]}")
            action = input(
                "Enter your action (bet, call, raise, or fold): ").lower()

            if action == "bet":
                bet_amount = int(input("Enter your bet amount: "))
                bets[j] += bet_amount

            elif action == "call":
                bets[j] += max(bets) - bets[j]

            elif action == "raise":
                raise_amount = int(input("Enter your raise amount: "))
                bets[j] += max(bets) - bets[j] + raise_amount

            elif action == "fold":
                players[j] = []

            else:
                print("Invalid action. Try again.")
                continue

            if all(bets) or len(set(bets)) == 1:
                round_over = True
                break

    # Determine the winner of the round
    active_players = [player for player in players if player]
    winning_hand = max(
        active_players, key=lambda player: evaluate_hand(player + round_cards))
    winners = [i for i, player in enumerate(
        active_players) if player == winning_hand]

    # If there is only one winner, they take the pot
    if len(winners) == 1:
        print(f"Player {winners[0] + 1} wins the pot of {sum(bets)} chips!")
        players[winners[0]].extend(
            round_cards + [card for card in community_cards if card not in round_cards])
        players[winners[0]].extend([bet for bet in bets if bet])
        for j in range(num_players):
            bets[j] = 0

    # If there are multiple winners, split the pot evenly among them
    else:
        print(
            f"Players {[w + 1 for w in winners]} split the pot of {sum(bets)} chips!")
        split_pot = sum(bets) // len(winners)
        for winner in winners:
            players[winner].extend(
                round_cards + [card for card in community_cards if card not in round_cards])
            players

# Define the hand ranking system


def evaluate_hand(hand):
    ranks = {"Ace": 14, "King": 13, "Queen": 12, "Jack": 11, "10": 10,
             "9": 9, "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2}
    suits = ["hearts", "clubs", "diamonds", "spades"]

    # Check for a straight flush
    for suit in suits:
        flush_cards = [card for card in hand if suit in card]
        if len(flush_cards) >= 5:
            flush_ranks = sorted([ranks[card.split()[0]]
                                 for card in flush_cards], reverse=True)
            for i in range(len(flush_ranks) - 4):
                if flush_ranks[i] == flush_ranks[i+4] + 4:
                    return 9, flush_ranks[i]

    # Check for a four-of-a-kind
    for rank in ranks:
        if hand.count(rank + " of " + suits[0]) == 4:
            return 8, ranks[rank]

    # Check for a full house
    for rank1 in ranks:
        for rank2 in ranks:
            if rank1 != rank2 and hand.count(rank1 + " of " + suits[0]) == 3 and hand.count(rank2 + " of " + suits[0]) == 2:
                return 7, ranks[rank1]

    # Check for a flush
    for suit in suits:
        flush_cards = [card for card in hand if suit in card]
        if len(flush_cards) >= 5:
            flush_ranks = sorted([ranks[card.split()[0]]
                                 for card in flush_cards], reverse=True)
            return 6, flush_ranks[:5]

    # Check for a straight
    ranks_list = sorted([ranks[card.split()[0]]
                        for card in hand], reverse=True)
    if len(set(ranks_list)) == 5 and ranks_list[0] == ranks_list[4] + 4:
        return 5, ranks_list[0]

    # Check for a three-of-a-kind
    for rank in ranks:
        if hand.count(rank + " of " + suits[0]) == 3:
            kickers = sorted([ranks[card.split()[0]]
                             for card in hand if card.split()[0] != rank], reverse=True)
            return 4, (ranks[rank], kickers)

    # Check for two pairs
    pairs = []
    for rank1 in ranks:
        for rank2 in ranks:
            if rank1 != rank2 and hand.count(rank1 + " of " + suits[0]) == 2 and hand.count(rank2 + " of " + suits[0]) == 2:
                pairs.append((ranks[rank1], ranks[rank2]))
    if pairs:
        pairs.sort(reverse=True)
        kickers = [ranks[card.split()[0]]
                   for card in hand if ranks[card.split()[0]] not in pairs[0]]
        return 3, (pairs[0], kickers[0])

    # Check for a pair
    for rank in ranks:
        if hand.count(rank + " of " + suits[0]) == 2:
            kickers = sorted([ranks[card.split()[0]]
                             for card in hand if card.split()[0]])

# Determine the winner of the game based on the hand ranking system


def determine_winner(players):
    player_hands = []
    for player in players:
        hand = player['hand']
        hand_rank, hand_strength = evaluate_hand(hand)
        player_hands.append((player, hand_rank, hand_strength))
    player_hands.sort(key=lambda x: (x[1], x[2]), reverse=True)
    winner = player_hands[0]
    return winner[0]['name']


# Ask the user if they want to play again
play_again = input("Do you want to play again? (y/n): ")

while play_again.lower() == 'y':
    # Reset the deck and players
    deck = create_deck()
    players = create_players()

    # Shuffle the deck
    shuffle_deck(deck)

    # Deal the cards
    deal_cards(players, deck)

    # Play the game
    play_game(players)

    # Determine the winner
    winner = determine_winner(players)
    print(f"The winner is {winner}!")

    # Ask the user if they want to play again
    play_again = input("Do you want to play again? (y/n): ")

print("Thanks for playing!")
