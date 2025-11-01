import random
from collections import Counter

class Player:
    #constructor
    def __init__(self, name, declared=None, bias=None, hesitancy=0.0, overconfidence=0.0):
        self.name = name
        self.declared = declared
        self.choice = None
        self.bias = bias  # "Yes", "No", or None
        self.hesitancy = hesitancy  # 0.0 to 1.0, chance to second-guess
        self.overconfidence = overconfidence  # 0.0 to 1.0, chance to think they're smarter and do opposite
    
    # basic vote with no information
    def vote_basic(self):
        if self.declared:
            self.choice = self.declared
        else:
            # Basic strategy: pick randomly (with bias if present)
            if self.bias and random.random() < 0.6:
                self.choice = self.bias
            else:
                self.choice = random.choice(["Yes", "No"])
        return self.choice

    # vote with information about others - if someone knows about the others' votes -> always vote minority else random
    def vote_info(self, votes_so_far):
        if self.declared:
            self.choice = self.declared
        else:
            yes_count = votes_so_far.count("Yes")
            no_count = votes_so_far.count("No")
            
            # Determine best minority choice
            if yes_count < no_count:
                minority_choice = "Yes"
            elif no_count < yes_count:
                minority_choice = "No"
            else:
                # Equal votes so far, choose randomly (or with bias)
                if self.bias and random.random() < 0.6:
                    minority_choice = self.bias
                else:
                    minority_choice = random.choice(["Yes", "No"])
            
            # Apply overconfidence (thinks they're smarter, does opposite)
            if random.random() < self.overconfidence:
                self.choice = "No" if minority_choice == "Yes" else "Yes"
            # Apply hesitancy (second-guessing)
            elif random.random() < self.hesitancy:
                self.choice = "No" if minority_choice == "Yes" else "Yes"
            else:
                self.choice = minority_choice
                
        return self.choice
    
    # reliable info (80% trust, 20% doubt)
    def vote_reliable(self, votes_so_far):
        if self.declared:
            self.choice = self.declared
        else:
            yes_count = votes_so_far.count("Yes")
            no_count = votes_so_far.count("No")
            
            # Determine 'correct' choice
            if yes_count < no_count:
                correct_choice = "Yes"
            elif no_count < yes_count:
                correct_choice = "No"
            else:
                if self.bias:
                    correct_choice = self.bias
                else:
                    correct_choice = random.choice(["Yes", "No"])
                
            # 80% chance to trust, 20% chance to doubt
            r = random.random()
            if r < 0.8:
                # Trust the info
                if random.random() < self.overconfidence:
                    self.choice = "No" if correct_choice == "Yes" else "Yes"
                elif random.random() < self.hesitancy:
                    self.choice = "No" if correct_choice == "Yes" else "Yes"
                else:
                    self.choice = correct_choice
            else:
                # Doubt: 10% random, 10% opposite
                if r < 0.9:
                    if self.bias and random.random() < 0.6:
                        self.choice = self.bias
                    else:
                        self.choice = random.choice(["Yes", "No"])
                else:
                    self.choice = "No" if correct_choice == "Yes" else "Yes"
        
        return self.choice
    
    # person with unreliable info 70% doubt, 30% trust
    def vote_unreliable(self, votes_so_far):
        if self.declared:
            self.choice = self.declared
        else:
            yes_count = votes_so_far.count("Yes")
            no_count = votes_so_far.count("No")
            
            # Determine 'correct' choice
            if yes_count < no_count:
                correct_choice = "Yes"
            elif no_count < yes_count:
                correct_choice = "No"
            else:
                if self.bias:
                    correct_choice = self.bias
                else:
                    correct_choice = random.choice(["Yes", "No"])
                
            # 30% chance to trust, 70% chance to doubt (35% random vote, 35% opposite vote)
            r = random.random()
            if r < 0.3:
                # Trust the info
                if random.random() < self.overconfidence:
                    self.choice = "No" if correct_choice == "Yes" else "Yes"
                elif random.random() < self.hesitancy:
                    self.choice = "No" if correct_choice == "Yes" else "Yes"
                else:
                    self.choice = correct_choice
            elif r < 0.65:
                if self.bias and random.random() < 0.6:
                    self.choice = self.bias
                else:
                    self.choice = random.choice(["Yes", "No"])
            else:
                self.choice = "No" if correct_choice == "Yes" else "Yes"
        
        return self.choice

def minority_rule(players, vote_method):
    # Reset all choices
    for player in players:
        player.choice = None
    
    # Collect votes
    all_votes = []
    
    if vote_method == "basic":
        # Everyone votes independently
        for player in players:
            all_votes.append(player.vote_basic())
    
    elif vote_method == "info":
        # Players vote sequentially and can see previous votes
        for player in players:
            all_votes.append(player.vote_info(all_votes))
    
    elif vote_method == "reliable":
        # Players vote sequentially with reliable decision-making (80% trust)
        for player in players:
            all_votes.append(player.vote_reliable(all_votes))
    
    elif vote_method == "unreliable":
        # Players vote sequentially with unreliable decision-making
        for player in players:
            all_votes.append(player.vote_unreliable(all_votes))
    
    else:
        raise ValueError(f"Unknown vote_method: {vote_method}")
    
    # Count votes
    yes_count = all_votes.count("Yes")
    no_count = all_votes.count("No")
    
    # Determine minority (return empty list if tie)
    if yes_count < no_count:
        minority_choice = "Yes"
    elif no_count < yes_count:
        minority_choice = "No"
    else:
        return []
    
    # Find winners
    winners = [player for player in players if player.choice == minority_choice]
    return winners

# Run simulations
def run_simulation(players_config, vote_method, rounds=1000000):
    results = []
    for _ in range(rounds):
        sim_players = [Player(name, declared=decl, bias=bias, hesitancy=hes, overconfidence=over) 
                      for name, decl, bias, hes, over in players_config]
        winners = minority_rule(sim_players, vote_method=vote_method)
        results.extend([player.name for player in winners])
    
    return Counter(results)

print("="*70)
print("BASELINE SCENARIOS")
print("="*70)

# Configuration: (name, declared, bias, hesitancy, overconfidence)
print("\n1. Basic (simultaneous, random voting):")
config_basic = [
    ("Akiyama", "Yes", None, 0.0, 0.0),
    ("Fukunaga", None, None, 0.0, 0.0),
    ("Eto", None, None, 0.0, 0.0),
    ("Ishida", None, None, 0.0, 0.0)
]
wins = run_simulation(config_basic, "basic")
for player, count in wins.most_common():
    print(f"  {player}: {count:,} wins ({count/10000:.1f}%)")

print("\n2. Perfect info (100% rational, always minority):")
config_info = [
    ("Akiyama", "Yes", None, 0.0, 0.0),
    ("Fukunaga", None, None, 0.0, 0.0),
    ("Eto", None, None, 0.0, 0.0),
    ("Ishida", None, None, 0.0, 0.0)
]
wins = run_simulation(config_info, "info")
if wins:
    for player, count in wins.most_common():
        print(f"  {player}: {count:,} wins ({count/10000:.1f}%)")
else:
    print("  No winners (all ties - expected)")

print("\n3. Reliable info (80% trust, 20% doubt):")
config_reliable = [
    ("Akiyama", "Yes", None, 0.0, 0.0),
    ("Fukunaga", None, None, 0.0, 0.0),
    ("Eto", None, None, 0.0, 0.0),
    ("Ishida", None, None, 0.0, 0.0)
]
wins = run_simulation(config_reliable, "reliable")
for player, count in wins.most_common():
    print(f"  {player}: {count:,} wins ({count/10000:.1f}%)")

print("\n4. Unreliable info (30% trust, 70% doubt):")
config_unreliable = [
    ("Akiyama", "Yes", None, 0.0, 0.0),
    ("Fukunaga", None, None, 0.0, 0.0),
    ("Eto", None, None, 0.0, 0.0),
    ("Ishida", None, None, 0.0, 0.0)
]
wins = run_simulation(config_unreliable, "unreliable")
for player, count in wins.most_common():
    print(f"  {player}: {count:,} wins ({count/10000:.1f}%)")

print("\n" + "="*70)
print("CHARACTER-BASED SCENARIOS (Testing what happens if certain personalities impact actions)")
print("="*70)

print("\n5. Fukunaga is sly & overconfident (reliable info, 40% overconfidence):")
print("   (Fukunaga thinks he's smarter and often does opposite of 'correct' choice)")
config_fukunaga = [
    ("Akiyama", "Yes", None, 0.0, 0.0),
    ("Fukunaga", None, None, 0.0, 0.4),  # Sly & overconfident
    ("Eto", None, None, 0.0, 0.0),
    ("Ishida", None, None, 0.0, 0.0)
]
wins = run_simulation(config_fukunaga, "reliable")
for player, count in wins.most_common():
    print(f"  {player}: {count:,} wins ({count/10000:.1f}%)")

print("\n6. Eto is cautious & analytical (reliable info, 25% hesitancy):")
print("   (Eto overthinks and second-guesses decisions)")
config_eto = [
    ("Akiyama", "Yes", None, 0.0, 0.0),
    ("Fukunaga", None, None, 0.0, 0.0),
    ("Eto", None, None, 0.25, 0.0),      # Cautious, overthinks
    ("Ishida", None, None, 0.0, 0.0)
]
wins = run_simulation(config_eto, "reliable")
for player, count in wins.most_common():
    print(f"  {player}: {count:,} wins ({count/10000:.1f}%)")

print("\n7. Ishida is impulsive with Yes bias (reliable info):")
print("   (Ishida tends to vote Yes when uncertain)")
config_ishida = [
    ("Akiyama", "Yes", None, 0.0, 0.0),
    ("Fukunaga", None, None, 0.0, 0.0),
    ("Eto", None, None, 0.0, 0.0),
    ("Ishida", None, "Yes", 0.0, 0.0)    # Impulsive Yes bias
]
wins = run_simulation(config_ishida, "reliable")
for player, count in wins.most_common():
    print(f"  {player}: {count:,} wins ({count/10000:.1f}%)")

print("\n8. All characters combined (reliable info 80% trust):")
print("   Akiyama declares Yes, Fukunaga overconfident, Eto hesitant, Ishida biased")
config_all = [
    ("Akiyama", "Yes", None, 0.0, 0.0),
    ("Fukunaga", None, None, 0.0, 0.4),  # Sly & overconfident
    ("Eto", None, None, 0.25, 0.0),      # Cautious, overthinks
    ("Ishida", None, "Yes", 0.0, 0.0)    # Impulsive Yes bias
]
wins = run_simulation(config_all, "reliable")
for player, count in wins.most_common():
    print(f"  {player}: {count:,} wins ({count/10000:.1f}%)")

print("\n9. All characters combined (unreliable info 30% trust):")
print("   Same setup but with lower trust in information")
wins = run_simulation(config_all, "unreliable")
for player, count in wins.most_common():
    print(f"  {player}: {count:,} wins ({count/10000:.1f}%)")

print("\n10. Extreme overconfidence (Fukunaga 60% overconfident, reliable info):")
print("   Testing if very high overconfidence helps Akiyama")
config_extreme = [
    ("Akiyama", "Yes", None, 0.0, 0.0),
    ("Fukunaga", None, None, 0.0, 0.6),  # Very overconfident
    ("Eto", None, None, 0.25, 0.0),
    ("Ishida", None, "Yes", 0.0, 0.0)
]
wins = run_simulation(config_extreme, "reliable")
for player, count in wins.most_common():
    print(f"  {player}: {count:,} wins ({count/10000:.1f}%)")


