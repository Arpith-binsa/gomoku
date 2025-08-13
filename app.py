from flask import Flask, render_template, request, jsonify
from gomoku import GomokuGame, IRON_MAN, THANOS

app = Flask(__name__)
game = GomokuGame()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    data = request.json
    row = data["row"]
    col = data["col"]

    # Human move only if it is human's turn (Thanos == 2)
    if game.current_player == THANOS:
        valid = game.play_move(row, col)
        if not valid:
            return jsonify(game.get_state())

        # After human move, AI plays if no winner yet
        if not game.winner:
            game.ironman_ai_move()

    return jsonify(game.get_state())

@app.route("/reset", methods=["POST"])
def reset():
    game.reset()
    return jsonify(game.get_state())

if __name__ == "__main__":
    app.run(debug=True)