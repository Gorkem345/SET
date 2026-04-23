
# **Case work: The Game Set**  
### **Authors: İsa Görkem Akdoğan, Mingyang Wang, Donna Keurentjes**
### **Group: 1**
### **Course: Advanced Programming in Python (WUR)** 

## ***Instructions:***
### *Recommended Python Version:*
#### *3.12*
### *Install Library: pygame*
#### *Other modules that are used: sys, random, copy*
### *Run Game.py to initiate the game*

---

## **1. DESCRIPTION**
This project is an implementation of the card game **SET**, built using **Pygame** and **object‑oriented programming**.  
In this game, players need to identify valid SETs among cards displayed on the table. If they form a set depends on their color, number, shape and shading. 
The game includes:

- Singleplayer (with computer opponent) and Multiplayer mode for 2 players on one laptop
- Multiple interactive **GUI** screens (Start, Rules, Settings, Pre-Start, Game, Winner, Confirm) with visuals and sound effects 
- Mouse and keyboard **event handling**  
- **Timers** (SET timer and game timer)

The game class is the main controller which stores information and is linked to every screen. Each screen class inherits from the Screen base class.
The game logic is handled by the Table class within set_table.py and the Card class in card_deck.py represents the cards.
Constants contains the colors that are used for displaying in multiple files.

---

## **2. PARAMETERS**
###  Gameplay parameters
- **Game Duration:** 1-20 minutes, adjustable in Settings (game.turn_duration_ms)
- **Point Gain/Loss:** 0-10 points, adjustable in Settings (game.point_gain/game.point_loss)
- - **Player input:**  
  - Player 1 → SPACE to call "Set"  
  - Player 2 → ENTER to call "Set" 
- **SET Answer Timer:** 15 seconds after calling "Set" 
- **Difficulty:** Easy, Normal, or Hard - Determines how fast the computer calls for "Set"

### Internal parameters
- **Card Replacement Delay:** 1.5 seconds after selecting 3 cards  
- **Screen Resolution:** 1080 × 720
- **Deck:** 81 unique cards (4 attributes × 3 values each)
- **Card Grid:** 12 random cards from deck
- **Hint:** 2 random cards from one random set on the table

---

## **3. LIMITATIONS**

- Local multiplayer only (no online mode)   
- Window size is fixed and not resizable (does not fit correctly on every laptop)
- No save/load system (e.g. no highscore)
- The difficulty has standard values, it is not adapted automatically to the player's behavior
- The game cannot be played by more than 2 players
- The cards images are imported from an image with a specific layout, changing this requires updating coordinates

---

## **4. STRUCTURES**
### **Loops and Conditionals**
A while loop is used to keep the game running until QUIT is called. 
For loops are used, for example in find_sets() to loop through cards
Conditionals are used, for example to check valid sets and to determine the winner

### **Classes**
#### **Inheritance**
- Screen is a base class and all screens (StartScreen, PlayScreen, RulesScreen, etc.) inherit from it
- PlayScreen is the parent class for Multiplayer and SingleplayerScreen
#### **Composition**
- Game owns Table and all screens

#### **Game**
- Runs the **main loop** and manages screen switching  
- Holds global state (scores, winner, table)  
- Delegates **event handling** and drawing to the active screen

#### **Table**
- Manages the deck, cards on the table, and selected cards 
- Validates SETs and handles card replacement

#### **Display_board/Display_card (TableDisplay.py)**
- Draws the table layout and individual cards  
- Converts card data into visuals of the cards

#### **StartScreen, RulesScreen, WinnerScreen, ConfirmScreen, PreStartScreen**
- Individual GUI screens with their own event handling and drawing logic

---

## **5. OUTPUTS**

### **Graphical output**
- GUI rendered with pygame
- Screens: Start, Pre‑Start, Singleplayer/Multiplayer, Rules, Settings, Confirm, Winner

### **User Interface elements**
- Game window with background table image  
- Card grid (12 cards)  
  - Selected highlights (yellow)
- Buttons (Hint, Restart, Menu)  
- Message panel displaying: "SET!", "Not a set!", or "Time’s up!"  

### **Audio Output**
- "correct.wav" for valid SET  
- "wrong.wav" for incorrect SET  
- "select.wav" for click on card
- "set.wav" for pressing SPACE/ENTER to call for "Set"

### **Gameplay Output**
- Left‑side panel (in Multiplayer and Singleplayer Screens) showing:  
  - Player scores  
  - Game duration timer  
  - SET timer  
- Highlighted hints (cyan) 
- Winner determination  
- Delayed card replacement
- Computer actions (calling and selecting set)

---