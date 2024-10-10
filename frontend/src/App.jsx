import React, { useState, useEffect } from 'react';
import Chessboard from 'chessboardjsx';

const ChessGame = () => {
  const [boardState, setBoardState] = useState('start');
  const [gameOver, setGameOver] = useState(false);
  const [gameStatus, setGameStatus] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);  // New loading state

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/board')
      .then(res => res.json())
      .then(data => {
        setBoardState(data.fen)
      });
  }, []);

  const onDrop = (move) => {
    if (isProcessing) return;  // Prevent moves while processing
    
    setIsProcessing(true);  // Start loading
    const moveData = { move: move.sourceSquare + move.targetSquare };
    
    fetch('http://127.0.0.1:5000/api/move', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(moveData),
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'move made') {
          setBoardState(data.board);
        } else {
          setBoardState(data.board);
          setGameOver(true);
          setGameStatus(data.status);
          alert(data.status);
          console.log(data.status);
        }
      })
      .finally(() => setIsProcessing(false));  // End loading
  };

  const makeAiMove = () => {
    if (isProcessing) return;  // Prevent AI moves while processing
    
    setIsProcessing(true);  // Start loading
    fetch('http://127.0.0.1:5000/api/ai', { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'AI move made') {
          setBoardState(data.board);
        } else {
          setBoardState(data.board);
          setGameOver(true);
          setGameStatus(data.status);
          alert(data.status);
          console.log(data.status);
        }
      })
      .finally(() => setIsProcessing(false));  // End loading
  };

  const newGame = () => {
    if (isProcessing) return;  // Prevent new game while processing
    
    setIsProcessing(true);  // Start loading
    fetch('http://127.0.0.1:5000/api/newgame', { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        setBoardState(data.board);
        setGameOver(false);
        setGameStatus('');
      })
      .finally(() => setIsProcessing(false));  // End loading
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      <h1>Chess Game</h1>
      <Chessboard
        position={boardState}
        onDrop={({ sourceSquare, targetSquare }) => onDrop({ sourceSquare, targetSquare })}
        draggable={!isProcessing}  // Disable drag when processing
      />
      <div style={{ paddingTop: "10px", gap: "10px", display: "flex" }}>
        <button 
          onClick={newGame} 
          disabled={isProcessing}  
        >
          {isProcessing ? 'Processing...' : 'New Game'}
        </button>
        <button 
          onClick={makeAiMove} 
          disabled={isProcessing}  
        >
          {isProcessing ? 'Processing...' : 'AI Move'}
        </button>
      </div>
    </div>
  );
};

export default ChessGame;