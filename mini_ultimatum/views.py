# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):

    timeout_seconds = 600


class Offer(Page):

    form_model = models.Group
    form_fields = ['amount_offered']

    def is_displayed(self):
        return self.player.id_in_group == 1

    timeout_seconds = 600


class WaitForProposer(WaitPage):
    pass


class AcceptStrategy(Page):

    form_model = models.Group
    form_fields = ['response_{}'.format(int(i))
                   for i in Constants.offer_choices]

    def is_displayed(self):
        return self.player.id_in_group == 2 and self.group.strategy


class WaitForResponder(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_if_accepted()
        self.group.calculate_punishable()


class Punish(Page):

    form_model = models.Group
    form_fields = ['amount_punished']

    def is_displayed(self):
        return self.player.id_in_group == 3 and self.group.offer_accepted

    def error_message(self, values):
        if values["amount_punished"] > self.group.amount_punishable:
            return 'The amount punishable should be less or equal to the amount left with the proposer'

    timeout_seconds = 600


class PunishPass(Page):

    def is_displayed(self):
        return self.player.id_in_group == 3 and not self.group.offer_accepted

    timeout_seconds = 600


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    pass


page_sequence = [Introduction,
                 Offer,
                 WaitForProposer,
                 AcceptStrategy,
                 WaitForResponder,
                 Punish,
                 PunishPass,
                 ResultsWaitPage,
                 Results]
