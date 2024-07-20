
from tournament.models import MatchModel, TournamentModel
from users.models import UserModel
import random


class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score
        self.opponents = []


class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.result = None  # 1 if player1 wins, 0 if player2 wins, 0.5 for draw


class SwissSystem:

    def pair_players(self, players):
        players = sorted(players, key=lambda x: x.score, reverse=True)
        pairs = []
        used_players = set()
        for player1 in players:
            if player1 in used_players:
                continue
            for player2 in players:
                if player2 not in used_players and player2 != player1 and player2 not in player1.opponents:
                    pairs.append((player1, player2))
                    used_players.add(player1)
                    used_players.add(player2)
                    break
        return pairs



    def update_scores(self, matches):
        for match in matches:
            if match.result == 1:
                match.player1.score += 1
            elif match.result == 0:
                match.player2.score += 1
            elif match.result == 0.5:
                match.player1.score += 0.5
                match.player2.score += 0.5
            match.player1.opponents.append(match.player2)
            match.player2.opponents.append(match.player1)



# def simulate_tournament(players, rounds):
#     for round_number in range(rounds):
#         print(f"\nRound {round_number + 1}")
#         pairs = SwissSystem().pair_players(players)
#         matches = [Match(player1, player2) for player1, player2 in pairs]

#         for match in matches:
#             MatchModel.objects.create(

#             )


#         SwissSystem().update_scores(matches)
#         print("\nScores after round:")
#         for player in players:
#             print(f"{player.name}: {player.score}")

# # Create players
# players = [Player(f"Player {i+1}") for i in range(20)]

# # Simulate a tournament with 5 rounds
# simulate_tournament(players, 10)





def match_generator(tournament, wh_round):
    players = [Player(player.username, player.rating) for player in tournament.participants.all()]
    pairs = SwissSystem().pair_players(players)
    matches = [Match(player1, player2) for player1, player2 in pairs]
    for match in matches:
        MatchModel.objects.create(
            which_round = wh_round,
            tournament = tournament,
            side_white = UserModel.objects.get(username=match.player1.name),
            side_black=UserModel.objects.get(username=match.player2.name)

        )
        print(match.player1.name, match.player2.name)

