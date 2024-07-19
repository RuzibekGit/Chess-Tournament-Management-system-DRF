from django.db import models
from shared.models import BaseModel
from users.models import UserModel

START_SOON, GOING_ON, ENDED = "START_SOON", "GOING_ON", "ENDED"


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




class RoundsModel(BaseModel):
    rounds = models.CharField(max_length=50, blank=True, null=True)
    tournament = models.ForeignKey(TournamentModel, on_delete=models.CASCADE, related_name="tour_rounds")
    side_white = models.ForeignKey(UserModel, on_delete=models.SET_NULL, related_name="side_white", null=True)
    side_black = models.ForeignKey(UserModel, on_delete=models.SET_NULL, related_name="side_black", null=True)

    result = models.ForeignKey(UserModel, on_delete=models.SET_NULL, related_name="win_rounds", null=True)

    data_for_ondelete = models.JSONField(blank=True, null=True)


    def __str__(self) -> str:
        return self.result.first_name

    class Meta:
        verbose_name = 'Round'
        verbose_name_plural = 'Rounds'

    # --------------- Functions -----------------
    def write_ondelete(self):
        if not self.data_for_ondelete:
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
                "who_win": "black" if self.result.first_name == self.side_black.first_name else "white"
            }

    def write_round_id(self):
        if not self.rounds:
            self.rounds = f"{self.tournament.name} - {self.tournament.tour_rounds.count()+1}"


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
        self.write_round_id()


    # ------------------------------
    def save(self, *args, **kwargs):
        if not self.pk:
            self.clean()
        super(RoundsModel, self).save(*args, **kwargs)

