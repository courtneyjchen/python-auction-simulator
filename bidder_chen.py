"""
Bidder Class: Epsilon-Greedy Strategy for Second-Price Ad Auctions

This class represents a bidding agent participating in a second-price sealed-bid ad auction.
The agent uses an epsilon-greedy strategy with exponential decay to balance exploration and exploitation.
It tracks click-through behavior by user and dynamically adjusts bid amounts based on learned click probabilities.
"""

import random
import numpy as np

class Bidder:
    '''Class to represent a bidder in an online second-price ad auction'''
    def __init__(self, num_users, num_rounds):
        '''Setting number of users, number of rounds, and round counter'''
        self.num_users = num_users
        self.num_rounds = num_rounds
        self.current_balance = 0
        self.click_history = {i: [] for i in range(0,self.num_users)}
        self.epsilon = 1 # percent of time to explore
        self.current_user = 0
        self.win_history = []

    def __repr__(self):
        return f"""Bidder(current_balance={self.current_balance}
        epsilon={self.epsilon}
        click_history={self.click_history})"""

    def __str__(self):
        return f"""Bidder with balance: ${self.current_balance:.2f}
        Epsilon: {self.epsilon}
        Click history: {self.click_history}"""

    def bid(self, user_id):
        '''Returns a non-negative bid amount'''
        self.current_user = user_id
        if random.random() < self.epsilon: # explore
            bid_amount = np.random.uniform(0, 0.9)
        else: # exploit
            user_clicks = self.click_history[user_id]
            if len(user_clicks) > 0:
                click_rate = sum(user_clicks) / len(user_clicks)
            else:
                click_rate = 0
            bid_amount = min(click_rate * 0.9, 0.9)
        # exponentially decay epsilon
        self.epsilon *= 0.99
        # ensures we explore at least 5% of the time
        self.epsilon = max(self.epsilon, 0.05)
        bid_amount = round(bid_amount, 3)
        return bid_amount

    def notify(self, auction_winner, price, clicked):
        '''Updates bidder attributes based on results from an auction round'''
        self.win_history.append(auction_winner)
        if clicked is not None:
            self.click_history[self.current_user].append(clicked)
