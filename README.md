# Chess Game with React and Flask API

This is a chess game application built with a **React frontend** and a **Flask backend**. The application allows players to play a chess game either against an AI or with another human. It features game-over detection (checkmate, stalemate, insufficient material), and players are notified when the game ends. The AI moves are powered by a custom chess engine and the Flask API manages game logic.

## Features
- **Play against AI**: Users can make their moves and have the AI respond with its own moves.
- **Game Over Detection**: The game detects when checkmate, stalemate, or insufficient material occurs and alerts the player.
- **Move Validation**: Only legal moves are accepted; illegal moves are rejected with an error message.
- **Persistent Game State**: The current state of the game is maintained, and the board is updated after every move.
- **New Game**: Users can start a new game at any time, resetting the board and game state.

## Technologies Used
- **Frontend**: 
  - React (with [chessboardjsx](https://github.com/willb335/chessboardjsx) for rendering the chessboard)
- **Backend**: 
  - Flask (Python with [python-chess](https://python-chess.readthedocs.io/en/latest/))
  - AI engine using Alpha-Beta pruning for move selection
  
## Requirements

- **Python 3.x**
- Vite (for running the React frontend)
- Flask and other Python dependencies (see `requirements.txt`)

## Installation and Setup

### Backend (Flask API)
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/chess-game-flask-react.git
    cd chess-game-flask-react/backend
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask server:
    ```bash
    flask run
    ```

    The server will be running at `http://127.0.0.1:5000/`.

### Frontend (React)
1. Navigate to the frontend directory:
    ```bash
    cd ../frontend
    ```

2. Install dependencies:
    ```bash
    npm install
    ```

3. Start the React development server:
    ```bash
    npm run dev
    ```

    The React app will be running at `http://localhost:5173/`.

## Usage

1. **Start a Game**: Visit `http://localhost:5173/` in your browser and start a new chess game by clicking the "New Game" button.
2. **Play Against AI**: Make your moves by dragging pieces on the chessboard. Click "AI Move" to let the AI make its move.
3. **Game Over**: The game will automatically detect checkmate, stalemate, or insufficient material and alert you when the game is over. After the game ends, you can reset the game by clicking the "New Game" button.

## API Endpoints

- **`/api/newgame`** (POST): Resets the game and starts a new one.
- **`/api/board`** (GET): Returns the current board state (FEN format).
- **`/api/move`** (POST): Submits a move and returns the updated board state.
- **`/api/ai`** (POST): Makes the AI move and returns the updated board state.

