# Flood Emergency Response Model

## Starting the Game

Run the following command to initialize the database and start the game in the Central suburb (id=5) with Administrator Alex:

```bash
python flood_response.py
```

### Output:
```
Welcome to the Flood Emergency Response Model.

You are in Central, Alex.
Resources:
- sandbags: 12
- pumps: 8
- barriers: 15
Evacuation Centers:
- 500 Main St: Pet-friendly: Yes, Catered: No, Overnight: Yes
- 501 Elm St: Pet-friendly: No, Catered: Yes, Overnight: No
Streets:
- Street A: normal
- Street B: advice
- Street C: order
Your Inventory:
- Empty
```

---

## Commands and Gameplay

### Command 1: `look`

**Description:** Confirm the current state before moving.

**Input:**
```
look
```

**Output:**  
(Same as the initial state above, confirming Central’s resources, evacuation centers, and street statuses.)

---

### Command 2: `pickup sandbags 5`

**Description:** Pick up 5 sandbags to redistribute later.

**Input:**
```
pickup sandbags 5
```

**Output:**
```
Picked up 5 sandbags.
```

---

### Command 3: `look`

**Description:** Check inventory and updated suburb resources.

**Input:**
```
look
```

**Output:**
```
You are in Central, Alex.
Resources:
- sandbags: 7  (down from 12)
- pumps: 8
- barriers: 15
Evacuation Centers:
- 500 Main St: Pet-friendly: Yes, Catered: No, Overnight: Yes
- 501 Elm St: Pet-friendly: No, Catered: Yes, Overnight: No
Streets:
- Street A: normal
- Street B: advice
- Street C: order
Your Inventory:
- sandbags: 5
```

---

### Command 4: `east`

**Description:** Move to the East suburb (id=6) to check its resources and possibly drop sandbags.

**Input:**
```
east
```

**Output:**
```
You are in East, Alex.
Resources:
- sandbags: 10
- pumps: 14
- barriers: 6
Evacuation Centers:
- 600 Main St: Pet-friendly: Yes, Catered: No, Overnight: Yes
- 601 Elm St: Pet-friendly: No, Catered: Yes, Overnight: No
Streets:
- Street A: normal
- Street B: advice
- Street C: order
Your Inventory:
- sandbags: 5
```

---

### Command 5: `putdown sandbags 3`

**Description:** Drop 3 sandbags to bolster resources in East.

**Input:**
```
putdown sandbags 3
```

**Output:**
```
Dropped 3 sandbags.
```

---

### Command 6: `look`

**Description:** Verify the updated state of East.

**Input:**
```
look
```

**Output:**
```
You are in East, Alex.
Resources:
- sandbags: 13  (up from 10)
- pumps: 14
- barriers: 6
Evacuation Centers:
- 600 Main St: Pet-friendly: Yes, Catered: No, Overnight: Yes
- 601 Elm St: Pet-friendly: No, Catered: Yes, Overnight: No
Streets:
- Street A: normal
- Street B: advice
- Street C: order
Your Inventory:
- sandbags: 2  (down from 5)
```

---

### Command 7: `north`

**Description:** Move to Northeast (id=3) to check its status.

**Input:**
```
north
```

**Output:**
```
You are in Northeast, Alex.
Resources:
- sandbags: 18
- pumps: 5
- barriers: 11
Evacuation Centers:
- 300 Main St: Pet-friendly: Yes, Catered: No, Overnight: Yes
- 301 Elm St: Pet-friendly: No, Catered: Yes, Overnight: No
Streets:
- Street A: normal
- Street B: advice
- Street C: order
Your Inventory:
- sandbags: 2
```

---

### Command 8: `pickup pumps 2`

**Description:** Pick up 2 pumps to redistribute later.

**Input:**
```
pickup pumps 2
```

**Output:**
```
Picked up 2 pumps.
```

---

### Command 9: `look`

**Description:** Check Northeast’s updated resources.

**Input:**
```
look
```

**Output:**
```
You are in Northeast, Alex.
Resources:
- sandbags: 18
- pumps: 3  (down from 5)
- barriers: 11
Evacuation Centers:
- 300 Main St: Pet-friendly: Yes, Catered: No, Overnight: Yes
- 301 Elm St: Pet-friendly: No, Catered: Yes, Overnight: No
Streets:
- Street A: normal
- Street B: advice
- Street C: order
Your Inventory:
- sandbags: 2
- pumps: 2
```

---

### Command 10: `west`

**Description:** Move to North (id=2) to continue resource management.

**Input:**
```
west
```

**Output:**
```
You are in North, Alex.
Resources:
- sandbags: 9
- pumps: 12
- barriers: 17
Evacuation Centers:
- 200 Main St: Pet-friendly: Yes, Catered: No, Overnight: Yes
- 201 Elm St: Pet-friendly: No, Catered: Yes, Overnight: No
Streets:
- Street A: normal
- Street B: advice
- Street C: order
Your Inventory:
- sandbags: 2
- pumps: 2
```

---

### Command 11: `exit`

**Description:** Exit the game.

**Input:**
```
exit
```

**Output:**
```
Exiting model. Goodbye.
```

---

## Summary of Play

The game began in Central, where 5 sandbags were picked up. Moving to East, 3 sandbags were dropped to support its evacuation order. In Northeast, 2 pumps were picked up due to low supply. Finally, the game ended in North. Throughout the game, the `look` command was used to monitor resources, evacuation centers, and street statuses, ensuring informed decisions. The goal was to redistribute resources to suburbs needing them, like East and Northeast, based on their inventory and street conditions.

Let me know if you want to continue playing or focus on specific actions!