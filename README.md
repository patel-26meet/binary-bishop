# binary-bishop

## Overview
binary-bishop is an advanced chess engine developed using Python and the python-chess library. With an estimated Elo rating of approximately 1300, Defeated me once :)...
## Key Features
- Implements the Universal Chess Interface (UCI) protocol
- Utilizes advanced algorithms including Alpha-Beta pruning
- Employs dynamic programming techniques with transposition tables and Zobrist hashing for efficient position caching
- Features a comprehensive chess evaluation algorithm
- Includes extensive logging and testing functionalities
- Compatible with most UCI-supported chess interfaces

## Technical Details
The engine incorporates several sophisticated techniques to enhance its performance:

- **Alpha-Beta Pruning**: Improves the efficiency of the minimax algorithm by eliminating branches that don't need to be searched.
- **Dynamic Programming**: Utilizes transposition tables and Zobrist hashing for quick position lookup and reduced redundant calculations.
- **Evaluation Algorithm**: A complex evaluation function that considers:
  - Piece values
  - Positional tables
  - Mobility metrics
  - Space control factors
  - Distinct midgame and endgame weightings

## Tools and Technologies
- Python
- python-chess library

## Usage
The main engine with UCI protocol is compatible with the `test-bot-2.py` file. To use the engine:

1. Most UCI-supported chess games accept the provided `.bat` or `.exe` files.
2. A `.bat` file is included in this repository, which executes the `test-bot-2.py` file.

## Development Status
This repository contains a development version of the code, which includes extensive logging and testing features. While this may impact performance, it provides valuable insights for further improvements.

## Future Plans
- A more optimized version is planned for release as a Lichess bot in the near future.
- Continuous improvement of the evaluation algorithm and search techniques.

## Getting Started
To get started with binary-bishop:

1. Clone this repository
2. Ensure you have Python installed on your system
3. Install the required dependencies (e.g., python-chess)
4. Run the provided `.bat` file or execute `test-bot-2.py` directly

## Contributions
Contributions, issues, and feature requests are welcome. Feel free to check the issues page if you want to contribute.

---

**Note**: This README is subject to updates as the project evolves. 
