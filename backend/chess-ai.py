import chess
import chess.svg
import chess.polyglot
import chess.pgn
import chess.engine
from flask import Flask, Response,jsonify, request
from flask_cors import CORS
import time
pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]
bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]
rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]
queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]
kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]


def calcMaterial():
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
    return (100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq))

def evaluateBoard():
 
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0
    material = calcMaterial()
    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)]) + sum([-pawntable[chess.square_mirror(i)]
                        for i in board.pieces(chess.PAWN, chess.BLACK)])
   
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)]) + sum([-knightstable[chess.square_mirror(i)]
                            for i in board.pieces(chess.KNIGHT, chess.BLACK)])

    bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)]) + sum([-bishopstable[chess.square_mirror(i)]
                            for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) + sum([-rookstable[chess.square_mirror(i)]
                        for i in board.pieces(chess.ROOK, chess.BLACK)])
  
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) + sum([-queenstable[chess.square_mirror(i)]
                            for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)]) + sum([-kingstable[chess.square_mirror(i)]
                        for i in board.pieces(chess.KING, chess.BLACK)])
    
    eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    if board.turn:
        return eval
    else:
        return -eval
def alphabeta(alpha, beta, depthleft):
    bestscore = -9999
    if (depthleft == 0):
        return quiesce(alpha, beta)
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(-beta, -alpha, depthleft - 1)
        board.pop()
        if (score >= beta):
            return score
        if (score > bestscore):
            bestscore = score
        if (score > alpha):
            alpha = score
    return bestscore

def quiesce(alpha, beta):
    stand_pat = evaluateBoard()
    if (stand_pat >= beta):
        return beta
    if (alpha < stand_pat):
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce(-beta, -alpha)
            board.pop()

            if (score >= beta):
                return beta
            if (score > alpha):
                alpha = score
    return alpha

def selectmove(depth):
    try:
        move = chess.polyglot.MemoryMappedReader(r"C:\Chess-Ai2\Chess-AI\backend\human.bin").weighted_choice(board).move
        return move
    except:
        try:
            bestMove = chess.Move.null()
            bestValue = -99999
            alpha = -100000
            beta = 100000
            
           
            moves = list(board.legal_moves)
            if not moves:  # If no legal moves available
                return None
            
            start_time = time.time()
            MAX_SEARCH_TIME = 10  
            
            for move in moves:
                if time.time() - start_time > MAX_SEARCH_TIME:
                    return bestMove if bestMove != chess.Move.null() else moves[0]
                
                board.push(move)
                boardValue = -alphabeta(-beta, -alpha, depth - 1)
                board.pop()
                
                if boardValue > bestValue:
                    bestValue = boardValue
                    bestMove = move
                if boardValue > alpha:
                    alpha = boardValue
            
            return bestMove 
            
        except Exception as e:
            print(f"Error in selectmove: {str(e)}")
            moves = list(board.legal_moves)
            return moves[0] if moves else None


def check_endgame_conditions():
    if board.is_checkmate():
            return jsonify(status='checkmate', board=board.fen())
    elif board.is_stalemate():
            return jsonify(status='stalemate', board=board.fen())
    elif board.is_insufficient_material():
            return jsonify(status='insufficient material', board=board.fen())
    else:
        return False
app = Flask(__name__)

board = chess.Board()
CORS(app)

@app.route('/api/newgame', methods=['POST'])
def new_game():
    board.reset()
    return jsonify(status='new game started', board=board.fen())

@app.route('/api/move', methods=['POST'])
def make_move():
    move = request.json.get('move')
    if board.is_legal(chess.Move.from_uci(move)):
        board.push_uci(move)
        
        if board.is_checkmate():
            return jsonify(status='Checkmate! Game over.', board=board.fen())
        elif board.is_stalemate():
            return jsonify(status='Stalemate! Game over.', board=board.fen())
        elif board.is_insufficient_material():
            return jsonify(status='Draw due to insufficient material! Game over.', board=board.fen())
        
        return jsonify(status='move made', board=board.fen())
        
    else:
        return jsonify(status='Illegal move',  board=board.fen())


@app.route('/api/ai', methods=['POST'])
def ai_move():
    move = selectmove(3)
    
    if move is None:
        return jsonify(status='No legal moves available', board=board.fen())
    
    try:
        board.push(move)
        
        if board.is_checkmate():
            return jsonify(status='Checkmate! Game over.', board=board.fen())
        elif board.is_stalemate():
            return jsonify(status='Stalemate! Game over.', board=board.fen())
        elif board.is_insufficient_material():
            return jsonify(status='Draw due to insufficient material! Game over.', board=board.fen())
        
        return jsonify(status='AI move made', move=move.uci(), board=board.fen())
        
    except Exception as e:
        return jsonify(status=f'Error making AI move: {str(e)}', board=board.fen())
@app.route('/api/board', methods=['GET'])
def get_board():
    return jsonify(fen=board.fen())




if __name__ == 'main':
    app.run(debug=True)