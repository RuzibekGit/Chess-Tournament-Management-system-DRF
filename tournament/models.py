from django.db import models
from shared.models import BaseModel
from users.models import UserModel

START_SOON, GOING_ON, ENDED = "START_SOON", "GOING_ON", "ENDED"



# -------------------------- Tournament Model -------------------------------
# region tournament
class TournamentModel(BaseModel):
    TOUR_STATE = (
        (START_SOON, START_SOON),
        (GOING_ON, GOING_ON),
        (ENDED, ENDED)
    )

    name = models.CharField(max_length=128, unique=True)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    participants = models.ManyToManyField(UserModel)
    state = models.CharField(max_length=128, choices=TOUR_STATE, default=START_SOON)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Tournament'
        verbose_name_plural = 'Tournaments'
# endregion


# -------------------------- Rounds Model -------------------------------
# region round
class RoundsModel(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    tournament = models.ForeignKey(TournamentModel, on_delete=models.CASCADE, related_name="tour_rounds")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Round'
        verbose_name_plural = 'Rounds'


    def write_round_id(self):
        if not self.name:
            self.name = f"{self.tournament.name} round - {self.tournament.tour_rounds.count()+1}"

    # ------------------------------
    def clean(self) -> None:
        self.write_round_id()

    # ------------------------------

    def save(self, *args, **kwargs):
        if not self.pk:
            self.clean()
        super(RoundsModel, self).save(*args, **kwargs)
# endregion


# -------------------------- Match Model -------------------------------
# region match
class MatchModel(BaseModel):
    rounds = models.CharField(max_length=50, blank=True, null=True)
    which_round = models.ForeignKey(RoundsModel, on_delete=models.CASCADE, related_name="match_rounds")
    tournament = models.ForeignKey(TournamentModel, on_delete=models.CASCADE, related_name="match_rounds")
    side_white = models.ForeignKey(UserModel, on_delete=models.SET_NULL, related_name="side_white", null=True)
    side_black = models.ForeignKey(UserModel, on_delete=models.SET_NULL, related_name="side_black", null=True)

    result = models.SmallIntegerField(blank=True, null=True)

    data_for_ondelete = models.JSONField(blank=True, null=True)


    def __str__(self) -> str:
        return self.rounds

    class Meta:
        verbose_name = 'Match'
        verbose_name_plural = 'Matches'

    # --------------- Functions -----------------
    def write_ondelete(self):
        if not self.data_for_ondelete:
            result = None
            if self.result:
                if self.result == 1:
                    result = "white"
                elif self.result == -1:
                    result = "black"
                else:
                    result = "tie"
            self.data_for_ondelete = {
                "white": {
                    "player": f"{self.side_white.first_name} {self.side_white.last_name}",
                    "country": self.side_white.country,
                    "rating": self.side_white.rating
                },
                "black": {
                    "player": f"{self.side_black.first_name} {self.side_black.last_name}",
                    "country": self.side_black.country,
                    "rating": self.side_black.rating
                },
                "who_win": result
            }

    def write_match_id(self):
        if not self.rounds:
            self.rounds = f"{self.which_round.name} match - {self.which_round.match_rounds.count()+1}"


    # this section is for returning data to admin panel
    def white(self):
        return self.data_for_ondelete["white"]['player']
    def black(self):
        return self.data_for_ondelete["black"]['player']
    def winner(self):
        return self.data_for_ondelete["who_win"]

    # ------------------------------
    def clean(self) -> None:
        self.write_ondelete()
        self.write_match_id()


    # ------------------------------
    def save(self, *args, **kwargs):
        if not self.pk:
            self.clean()
        super(MatchModel, self).save(*args, **kwargs)
# endregion
