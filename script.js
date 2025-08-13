
const boardDiv = document.getElementById("board");
const statusDiv = document.getElementById("status");

function renderBoard(board, currentPlayer, winner) {
    boardDiv.innerHTML = "";
    board.forEach((row, i) => {
        row.forEach((cell, j) => {
            const cellDiv = document.createElement("div");
            cellDiv.classList.add("cell");

            if (cell === 1) {
                cellDiv.textContent = "🦾"; // Iron Man AI
                cellDiv.classList.add("iron");
            } else if (cell === 2) {
                cellDiv.textContent = "💎"; // Thanos human
                cellDiv.classList.add("thanos");
            }

            // Only human (Thanos, 2) can click if no winner and it is their turn
            if (!winner && cell === 0 && currentPlayer === 2) {
                cellDiv.addEventListener("click", () => makeMove(i, j));
            }

            boardDiv.appendChild(cellDiv);
        });
    });

    if (winner) {
        statusDiv.textContent = winner === 1 ? "Iron Man Wins! 🦾" : "Thanos Wins! 💎";
    } else {
        statusDiv.textContent = currentPlayer === 1 ? "Iron Man's Turn 🦾" : "Thanos's Turn 💎";
    }
}


async function makeMove(row, col) {
    const res = await fetch("/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ row, col })
    });
    const state = await res.json();
    renderBoard(state.board, state.current_player, state.winner);
}

async function resetGame() {
    const res = await fetch("/reset", { method: "POST" });
    const state = await res.json();
    renderBoard(state.board, state.current_player, state.winner);
}

// Load initial board
resetGame();
