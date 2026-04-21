
# **Case work: The game Set **  
### **Authors: Donna Keurentjes, ..., ...**
### **Group: 1**
### **Course: Advanced Programming in Python (WUR)**

---

## **1. DESCRIPTION**
This project is an implementation of the card game **SET**, built using **Pygame** and **object‑oriented programming**.  
Players need to identify valid SETs among cards displayed on the table. The game includes:

- Multiple **GUI** screens (Start, Rules, Pre-Start, Game, Winner, Confirm)  
- Mouse and keyboard **event handling**  
- **Timers** (SET timer and game timer)  
- Sound effects and visual feedback

### **1.1 Game**
### **1.2 Set table**
### **1.3 Image dictionary**
### **1.4 Screen**
#### **1.4.1 Start**
#### **1.4.2 Rules**
#### **1.4.3 Pre-start**
#### **1.4.4 Play**
##### **1.4.4.1 Multiplayer**
##### **1.4.4.2 Singleplayer**
#### **1.4.5 Confirm**
#### **1.4.6 Winner**
#### **1.4.7 Settings**
### **1.5 Constants**

---

## **2. PARAMETERS**

- **SET Timer:** 15 seconds per turn  
- **Game Duration:** 5 minutes  
- **Card Replacement Delay:** 1.5 seconds after selecting 3 cards  
- **Screen Resolution:** 1080 × 720  
- **Player input:**  
  - Player 1 → SPACE to call SET  
  - Player 2 → ENTER to call SET  
- **Deck:** 81 unique cards (4 attributes × 3 values each)

### **1.1 Game**
### **1.2 Set table**
### **1.3 Image dictionary**
### **1.4 Screen**
#### **1.4.1 Start**
#### **1.4.2 Rules**
#### **1.4.3 Pre-start**
#### **1.4.4 Play**
##### **1.4.4.1 Multiplayer**
##### **1.4.4.2 Singleplayer**
#### **1.4.5 Confirm**
#### **1.4.6 Winner**
#### **1.4.7 Settings**

---

## **3. LIMITATIONS**

- Local multiplayer only (no online mode)   
- Window size is fixed and not resizable (does not fit correctly on every laptop)
- No save/load system (e.g. no highscore)
- The difficulty has standard values, it is not adapted automatically to the player's behavior

---

## **4. STRUCTURES**

### **Main Classes**

#### **Game**
- Runs the main loop and manages screen switching.  
- Holds global state (scores, winner, table).  
- Delegates event handling and drawing to the active screen.

#### **GameScreen**
- Core gameplay interface.  
- Handles timers, scoring, UI buttons, and card interaction.  
- Communicates with the Table class for SET logic.

#### **Table**
- Manages the deck, cards on the table, and selected cards.  
- Validates SETs and handles card replacement.  
- Implements the 1.5‑second delay before clearing/replacing cards.

#### **Display_board / Display_card**
- Draws the table layout and individual cards.  
- Converts card data into visual elements.

#### **StartScreen, RulesScreen, WinnerScreen, ConfirmScreen, PreStartScreen**
- Individual GUI screens with their own event handling and drawing logic.

---

## **5. OUTPUTS (Including Interfaces)**

### **Visual Output**
- Game window with background table image  
- Card grid (12–15 cards)  
- Left‑side panel showing:  
  - Player scores  
  - Game timer  
  - SET timer  
  - Buttons (Hint, Restart, Menu)  
- Message panel displaying:  
  - “SET!”  
  - “Not a set!”  
  - “Time’s up!”  
  - “Press set when ready”

### **Audio Output**
- `correct.wav` for valid SET  
- `wrong.wav` for incorrect SET  

### **Gameplay Output**
- Updated scores  
- Highlighted hints  
- Winner screen at end of game  
- Delayed card replacement animation  

---

## **6. CLASS & METHOD SUMMARIES (Mini‑README)**

### **Table.handle_click(index)**
- Adds a card to the current selection.  
- When 3 cards are selected, triggers `handle_selection()`.

### **Table.handle_selection()**
- Checks if the selected cards form a SET.  
- Starts a 1.5‑second delay before clearing or replacing cards.

### **Table.finish_set_replacement()**
- After the delay, replaces cards (if correct) or clears selection (if wrong).

### **GameScreen.handle_event(event)**
- Processes keyboard and mouse input.  
- Routes card clicks to the Table.  
- Updates scores, timers, and messages.

### **Game.run()**
- Main loop:  
  1. Handle events  
  2. Check delayed card replacement  
  3. Draw the active screen  

---

## **7. HOW TO RUN**
1. Install Python and Pygame  
2. Run:  
   ```bash
   python main.py
   ```
3. Use SPACE (Player 1) or ENTER (Player 2) to call SET.

---