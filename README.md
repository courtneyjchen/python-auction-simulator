# Second-Price Auction Simulator with Strategic Bidding

## Project Overview
In this project, I developed an object-oriented ad auction simulator in Python to model a competitive environment in which advertisers (bidders) vie to place ads for users. The simulation is framed as a second-price sealed-bid auction game, where each round represents a user visit to a website with an available ad slot.

During each round, a user is randomly selected. Each bidder is given the user’s ID and submits a bid based on learned click behavior. The highest bidder wins the round but pays the second-highest bid, and only the winning bidder observes whether the user clicked on the ad. Each user has a fixed, secret click-through probability, drawn from a uniform distribution at the start of the game, and click events are independent across rounds.

I implemented an epsilon-greedy strategy with exponential decay to balance exploration (learning click behavior) and exploitation (maximizing profit by bidding on high-value users). Bidders aim to accumulate as much profit as possible, earning $1 for each click but losing the winning price regardless of click outcome. Bidders are disqualified if their balance drops below -$1000.

The simulator was designed for a competitive testing environment where multiple bidding algorithms compete under the same rules. My strategy succeeded in the competition using a simple yet effective exploration-exploitation framework grounded in reinforcement learning.
