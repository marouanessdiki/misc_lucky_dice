# Lucky Dice - CTF Challenge

This project contains the solution for the **Lucky Dice** challenge, a programming/misc task found in CTF competitions.

## Challenge Overview

The challenge is a dice-summing game with the following characteristics:
*   **Rounds**: 100 rounds of dice rolls.
*   **Players**: Between 8 and 13.
*   **Dice**: The number of dice increases with each round (`dice_nr = rnd * 2 + 2`).
*   **Timeout**: A strict **0.3-second timeout** per round for receiving the answer.
*   **Tie-Breaking Rule**: If multiple players have the same highest score, the player who rolled last (highest player number) wins.

The challenge is effectively impossible for a human to solve manually within the given time constraints, requiring an automation script.

## Solution

The provided `solve.py` script automates the process by:
1.  Connecting to the challenge server via TCP.
2.  Parsing the dice rolls for each player from the server output using regular expressions.
3.  Calculating the winner for each round while correctly implementing the tie-breaking logic.
4.  Sending the winner's player number immediately to the server to beat the timeout.
5.  Retrieving the flag upon completing all 100 rounds.

### Usage

To run the solution, provide the target host and port as arguments:

```bash
python solve.py <host> <port>
```

## Flag

The retrieved flag is:
`HTB{r0LL1ng-1n-t43_D33P-b0t_n3T-cRe4t10n}`
