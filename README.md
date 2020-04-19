
These are assignments from the CSCI 561 - Foundations of Artificial Intelligence class.

# State Space Search

Understanding state spaces, time complexity using a variant of N-Queens problems ~ p-Queens 

Checkout the description and my solution to the problem posed. This is a very good way to get an introduction about state space, search tree and exponential time complexity. Please use the time modules to understand the running time complexity. 

A basic N-Queens brute force model was adapted to a p-Queens structure and heuristics were added to prune the search tree and reduce the running time

# Game Playing - Resource Allocation 

A game between two social organisations to maximise profits. We try to maximise the score for SPLA organisation while also maximising LAHSA. This is contrary to a min-max game which minimises and maximises. Try to think of this as a max-max game. 

A lot of code optimization went into this as there is no possible way to prune the search tree if it's a max-max game. If it were a min-max game, Alpha-Beta Pruning can be done to reduce the running time considerably. Some heuristics are added to the algorithm to generate a better run time.


# Markov Decision Process
A MDP algorithm for simulating a car from start to end position. The two popular methods to implement a MDP is using value iteration or policy iteration. This project uses Value Iteration after thinking about both the pros and cons of policy and value iteration. 

The value iteration algorithm is based on bellman equation. We set rewards for obstacles and goals in the grid (i.e state space).By using reinforcement learning and probability (decision theory) we generate policies (maps) to guide the car from the start to end position. 

The convergence of policy and time taken per car are the factors to consider for the running time. A class based implementation is provided in the code. 
