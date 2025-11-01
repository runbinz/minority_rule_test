# Liar Game: Minority Rule Simulation

A Python simulation exploring the game theory behind the "Minority Rule" game from the manga Liar Game.<br>
About the Game<br>
Minority Rule is a psychological game where players must vote "Yes" or "No" on a question, with the goal of being in the minority. Players in the majority are eliminated, and the game continues until winners emerge.

### Rules:

A random player asks any yes/no question<br>
All players vote "Yes" or "No" simultaneously<br>
Players in the majority are eliminated<br>
If there's a tie, the round repeats with a new question<br>
Winners are those who end up in the minority<br>

This game is based on the El Farol Bar problem in game theory - a coordination problem where individuals must decide whether to go to a bar, knowing it's only enjoyable if fewer than 60% of people attend. Since everyone decides simultaneously without knowing others' choices, there's no stable strategy that works for everyone.

### Akiyama's Strategy

In the manga's final round with 4 players remaining, Aki immediately declares he will vote "Yes" before anyone else votes.

The Logic (First Level): <br>
Akiyama publicly commits to "Yes" <br>
The remaining 3 players think: "If I vote No, I'll be in the minority"<br>

The Recursive Trap: <br>
But each player realizes the others are thinking the same thing<br>
If everyone votes "No" to counter Akiyama, it becomes 1 Yes vs 3 No - making Akiyama win<br>
But if I vote "Yes" to counter that, and others vote "No", I lose<br>
But if they also think this and vote "Yes"...<br>
This creates an infinite recursive feedback loop with no stable solution<br>

The Attempted Resolution:<br>
Recognizing this paradox, the remaining players try to force a tie (2-2 split)<br>
This would restart the round and neutralize Akiyama's advantage<br>
They attempt to cooperate and coordinate their votes<br>

The Twist:<br>
In reality, Akiyama had a secret collaborator among the 3 remaining players who voted "Yes" with him, ensuring his victory.<br>

### What This Simulation Explores:

This program models whether Akiyama's public declaration strategy would work without a collaborator, testing it against players with different personality traits and decision making patterns.

Baseline Scenarios:<br>
Basic (Random) - All players vote randomly with no information<br>
Perfect Info - Players see previous votes and always choose rationally (results in ties)<br>
Reliable Info (80% trust) - Players mostly trust information but sometimes doubt<br>
Unreliable Info (30% trust) - Players mostly doubt information, some randomness<br>

Character-Based Scenarios:<br>
The simulation tests Akiyama's strategy against hypothetical personality types:<br>
Fukunaga - Sly and overconfident (thinks he's smarter, does opposite of "obvious" play)<br>
Eto - Cautious and analytical (overthinks and second guesses decisions)<br>
Ishida - Impulsive with bias toward "Yes" votes<br>

Note: These personality traits are not canon to the manga but are hypothetical interpretations created for this simulation.

## Running the Simulation

python3 basic_sim.py
