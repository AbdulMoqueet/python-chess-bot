from stockfish import Stockfish

stockfish = Stockfish("stockfish_13.exe",
                      parameters={
                          "Write Debug Log": "false",
                          "Contempt": 0,
                          "Min Split Depth": 0,
                          "Threads": 8,
                          "Ponder": "false",
                          "Hash": 3024,
                          "MultiPV": 1,
                          "Skill Level": 20,
                          "Move Overhead": 30,
                          "Minimum Thinking Time": 20,
                          "Slow Mover": 80,
                          "UCI_Chess960": "false",
                      })

# stockfish
# .set_fen_position('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1')
# stockfish.set_position(["e2e3"])
# print(stockfish.get_parameters())
# stockfish.set_depth(30)
print(stockfish.get_board_visual())
print(stockfish.get_best_move())
print(stockfish.get_fen_position())
print(stockfish.get_parameters())
