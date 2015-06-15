# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json

# </standard imports>

author = 'Benson Njogu'

doc = """
The game is “mini” in that only one round is played and the first mover can only offer none,
half, or all of her endowment. Third-party punishment means that if Player 1 is deciding
for Player 2, Player 3 will have the option to penalize Player 1 based on his decision.
"""


class Constants:

    name_in_url = 'mini_ultimatum'
    players_per_group = 3
    num_rounds = 1

    endowment = c(10)
    payoff_if_rejected = c(0)
    offer_increment = c(2)

    offer_choices = currency_range(0, endowment, offer_increment)
    offer_choices_count = len(offer_choices)
    keep_give_amounts = [(offer, endowment - offer) for offer in offer_choices]


class Subsession(otree.models.BaseSubsession):

    def before_session_starts(self):
        # randomize to treatments
        for g in self.get_groups():
            if 'treatment' in self.session.session_type:
                g.strategy = self.session.session_type[
                    'treatment'] == 'strategy'
            else:
                g.strategy = True # always true


class Group(otree.models.BaseGroup):

    subsession = models.ForeignKey(Subsession)

    strategy = models.BooleanField(
        doc="""Whether this group uses strategy method"""
    )

    amount_offered = models.CurrencyField(choices=Constants.offer_choices)
    amount_punished = models.CurrencyField(choices=Constants.offer_choices)

    offer_accepted = models.BooleanField(
        doc="if offered amount is accepted (direct response method)"
    )

    proposer_punished = models.BooleanField(
        doc="If proposer is punished)"
    )

    response_0 = models.BooleanField(widget=widgets.RadioSelectHorizontal())
    response_2 = models.BooleanField(widget=widgets.RadioSelectHorizontal())
    response_4 = models.BooleanField(widget=widgets.RadioSelectHorizontal())
    response_6 = models.BooleanField(widget=widgets.RadioSelectHorizontal())
    response_8 = models.BooleanField(widget=widgets.RadioSelectHorizontal())
    response_10 = models.BooleanField(widget=widgets.RadioSelectHorizontal())

    def set_payoffs(self):
        p1, p2, p3 = self.get_players()

        if self.amount_punished:
            self.proposer_punished = True

        if self.strategy:
            self.offer_accepted = getattr(
                self, 'response_{}'.format(int(self.amount_offered)))

        if self.offer_accepted:
            if self.proposer_punished:
                p1.payoff = Constants.endowment - self.amount_offered - self.amount_punished
                p2.payoff = self.amount_offered
                p3.payoff = Constants.endowment - self.amount_punished
            else:
                p1.payoff = Constants.endowment - self.amount_offered - self.amount_punished
                p2.payoff = self.amount_offered
                p3.payoff = Constants.endowment - self.amount_punished
        else:
            p1.payoff = Constants.payoff_if_rejected
            p2.payoff = Constants.payoff_if_rejected
            p3.payoff = Constants.endowment


class Player(otree.models.BasePlayer):

    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
