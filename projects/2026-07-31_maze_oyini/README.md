# Simple Canvas Maze Game

## Loyiha nomi va tavsifi
This is a minimalist maze game built using HTML5 Canvas, pure JavaScript, and inline CSS. The objective is to navigate a generated maze from a starting point to an exit point using arrow keys, avoiding walls. Each time you start a new game, a unique maze is generated.

## Qanday ishga tushirish mumkinligi
1.  Save the `index_html_maze_game.html` file to your computer.
2.  Open the saved `index_html_maze_game.html` file with any modern web browser (e.g., Chrome, Firefox, Edge, Safari).
3.  Upon loading, you will see a generated maze and a player at the start.
4.  Press the 'R' key to start a new game.
5.  Use the **Arrow Keys** (Up, Down, Left, Right) to move the player through the maze.
6.  Reach the red square (exit) to win the game.
7.  Press 'R' again at any time to restart with a new maze.

## Xususiyatlar ro'yxati
*   **Dynamic Maze Generation**: A new, solvable maze is generated every time you start or restart the game, using a recursive backtracking algorithm.
*   **Player Movement**: Control the player using the keyboard's arrow keys (↑, ↓, ←, →).
*   **Collision Detection**: The player cannot move through maze walls.
*   **Start and End Points**: Clearly marked green (start) and red (end) squares.
*   **Win Condition**: The game ends when the player reaches the exit point, displaying a congratulatory message.
*   **Restart Functionality**: Pressing the 'R' key instantly generates a new maze and resets the player, allowing for quick replays.
*   **Single File**: All necessary HTML, CSS, and JavaScript are contained within a single `index_html_maze_game.html` file for easy deployment and sharing.
*   **Pure JavaScript**: No external libraries or frameworks are used, relying solely on native browser APIs.