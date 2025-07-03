import random
import numpy as np
# import matplotlib.pyplot as plt

class User:
    '''Class to represent a user with a secret probability of clicking an ad.'''

    def __init__(self):
        '''Generating a probability between 0 and 1 from a uniform distribution'''
        self.__probability = np.random.uniform()

    def __repr__(self):
        '''User object with secret probability'''
        return "User object created with secret click likelihood: " + str(self.__probability)

    def __str__(self):
        '''User object with a secret likelihood of clicking on an ad'''
        return "User object created with secret click likelihood: " + str(self.__probability)

    def show_ad(self):
        '''Returns True to represent the user clicking on an ad or False otherwise'''
        return random.random() < self.__probability

class Auction:
    '''Class to represent an online second-price ad auction'''
    def __init__(self, users, bidders):
        '''Initializing users, bidders, and dictionary to store balances for each bidder in the auction'''
        self.users = users
        self.bidders = bidders
        self.balances = {i: 0 for i in range(len(bidders))}
        self.balances_history = {i: [] for i in range(len(bidders))}
        self.qualified_bidders = 0

    def __repr__(self):
        '''Return auction object with users and qualified bidders'''
        return f"""Users: {self.users}
        Qualified Bidders: {self.qualified_bidders}"""

    def __str__(self):
        '''Return auction object with users and qualified bidders'''
        return f"""Users: {self.users}
        Qualified Bidders: {self.qualified_bidders}"""

    def execute_round(self):
        '''Executes a single round of an auction, completing the following steps:
            - random user selection
            - bids from every qualified bidder in the auction
            - selection of winning bidder based on maximum bid
            - selection of actual price (second-highest bid)
            - showing ad to user and finding out whether or not they click
            - notifying winning bidder of price and user outcome and updating balance
            - notifying losing bidders of price'''
        bids = []
        # selects random user and associated ID / index
        user = random.choice(self.users)
        user_id = self.users.index(user)

        # store qualified bidders and their original indices
        qualified_bidders_indices = [i for i in range(len(self.bidders)) if self.balances[i] >= -1000]
        self.qualified_bidders = [self.bidders[i] for i in qualified_bidders_indices]

        # handle case where there are no qualified bidders
        if not self.qualified_bidders:
            return "No qualified bidders for this round."
        # store bids from every qualified bidder
        for index in qualified_bidders_indices:
            bid = self.bidders[index].bid(user_id)
            if bid is not None:  # Ensure bid is valid
                bids.append(bid)
        # check if bids list is empty
        if not bids:
            return "No bids were placed."

        # select maximum bid(s)
        max_bid = max(bids)
        max_bid_indices = [i for i, bid in enumerate(bids) if bid == max_bid]

        # select winner (if tied, select a highest bidder at random)
        if len(max_bid_indices) == 1:
            winning_index = max_bid_indices[0]
            winner_index = qualified_bidders_indices[winning_index]
        else:
            winning_index = random.choice(max_bid_indices)
            winner_index = qualified_bidders_indices[winning_index]

        # select second-highest bid price
        bids.pop(winning_index)
        # Check if bids list is empty after popping
        if not bids:
            return "No second-highest price available."
        bid_price = max(bids)

        # "show ad" to user and observe if they click
        clicked = user.show_ad()

        # notify bidders
        for index in qualified_bidders_indices:
            if index == winner_index:
                self.bidders[index].notify(True, bid_price, clicked)
                # update balance accordingly
                if clicked:
                    self.balances[winner_index] += 1
                self.balances[winner_index] -= bid_price
                # indicate if bidder is disqualified after payment
                if self.balances[winner_index] < -1000:
                    print(f"Bidder #{winner_index} disqualified due to insufficient balance.")
            else:
                self.bidders[index].notify(False, bid_price, None)
    
        # store balances in history for plotting
        for k, v in self.balances.items():
            self.balances_history[k].append(v)

        return f"""Winner: Bidder #{winner_index}
        User: #{user_id}
        Bid price: ${bid_price:.2f}
        Balance: ${self.balances[winner_index]}
        Clicked: {clicked}"""

    # def plot_history(self):
    #     '''Plot balances for each bidder'''
    #     # create scatter plot of rounds for each bidder
    #     for k, v in self.balances_history.items():
    #         plt.scatter(range(100), v, label=f'Bidder {k}', marker='o')
    #         plt.plot(range(100), v, linestyle='-')

    #     plt.title('Bidder Balance Over Rounds')
    #     plt.xlabel('Auction Round')
    #     plt.ylabel('Balance ($)')
    #     plt.axhline(y=0, color='r', linestyle='--', label='Zero Balance')
    #     plt.legend()
    #     plt.grid(True)
    #     plt.show()
