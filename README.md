# 🎬 Sandalwood (.sw) Programming Language

Custom interpreted **Kanglish-inspired** programming language built in Python for DSA, compiler design, and runtime experimentation. 

No boilerplate, no over-complicated semantics—just pure mass-coding with the flavor of our favorite cinematic slangs! 🍿🔥

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10 or higher
- `pip` (Python package manager)

### Quick Setup

**Option 1: Automated Setup (Recommended)**
Run the automated setup script to bootstrap the compiler engine:
```bash
bash init.sh

```

This will verify your environment, install the Sandalwood engine in development mode, and ensure the `sandal` binary helper is active.

**Option 2: Manual Setup**

```bash
# Navigate to the project folder
cd sandalwood-lang

# Install the module locally in editable mode
pip install -e .

# Verify deployment
sandal --help

```

### Running Sandalwood Programs

Run any active `.sw` source script dynamically from your terminal:

```bash
sandal examples/hello.sw

```

---

## 📜 Language Features Tracker

| Block Primitive | Keyword Status | Current Support |
| --- | --- | --- |
| **Variables (`let`)** | `idhu` | Implemented (Mutable) |
| **Constants (`const`)** | `pakka` | *Coming Soon* |
| **Functions (`def`)** | `scene` / `packup` | Implemented (Full Scope) |
| **Conditionals (`if/else`)** | `nodona` / `illandre` / `climax` | Implemented |
| **Loops (`while/for`)** | `retake` / `cut` / `mundhe` | *Coming Soon* 🚧 |
| **Output (`print`)** | `dialogue` | Implemented |

> 💡 **Source of Truth for Syntax:** All compiler maps, token keywords, and terminal built-ins are managed explicitly in config configurations at `/config/syntax.json`.

---

## 🛠️ High-Voltage Code Examples

### Recursive Fibonacci Tracker (`examples/fibonacci.sw`)

```sw
scene fibonacci(n) {
  nodona (n <= 1) {
    packup n
  }
  packup fibonacci(n - 1) + fibonacci(n - 2)
}

scene main() {
  idhu result = fibonacci(10)
  dialogue(result)
}

```

### Recursive Binary Search (`examples/binary_search.sw`)

```sw
scene recursive_search(arr, target, left, right) {
  nodona (left > right) {
    packup -1
  }

  idhu mid = (left + right) // 2

  nodona (arr[mid] == target) {
    packup mid
  } illandre (arr[mid] < target) {
    packup recursive_search(arr, target, mid + 1, right)
  } climax {
    packup recursive_search(arr, target, left, mid - 1)
  }
}

scene main() {
  idhu prime_movies = [1, 3, 5, 7, 9, 11]
  idhu target_hit = 7
  idhu position = recursive_search(prime_movies, target_hit, 0, 5)
  dialogue(position) // Output: 3
}

```

---

## 🤝 Become a Co-Producer (Contribute & Raise a PR!)

ಯಾರೋ ಬರೆದಿರೋ ಲ್ಯಾಂಗ್ವೇಜ್ ಯೂಸ್ ಮಾಡೋದು ಹಳೇ ಸ್ಟೈಲ್... ನಮ್ಮ ಸ್ವಂತ ಲ್ಯಾಂಗ್ವೇಜ್‌ನ ನಾವೇ ಬಿಲ್ಡ್ ಮಾಡೋದು ಒಂಥರಾ **ನೆಕ್ಸ್ಟ್ ಲೆವೆಲ್ ಕಿಕ್!** 😎

We are building a highly-optimized, community-driven language engine, and we need your support to take it to the silver screen. **`retake`** (looping engine), logical operations (`&&`, `||`), and array helpers need to be integrated into the lexical structure!

### How to Join the Crew:

1. **Fork the Script:** Click that Fork button at the top and spin up your local set-up.
2. **Write the Screenplay:** Create a fresh development branch:
```bash
git checkout -b feature/mass-update


```



```
3. **Debug the Scene:** Implement your compiler tokens, expand `parser.py` or `interpreter.py`, and test with a `.sw` file.
4. **Release the Trailer:** Commit your changes cleanly:
   ```bash
   git commit -m "feat: Added high-voltage looping mechanisms using retake"
   

```

5. **Raise the PR (The Grand Entry):** Push to your branch and open a Pull Request.

Whether it's squashing interpreter anomalies, optimizing recursion stacks, or adding brand new Kanglish builtins—**your PRs are highly welcome!**

Let's make this engine a massive block-buster tracking codebase. **Fork, code, dialogue, and pull-request!** 🚀🎬

```
