# DatarScript 

[![DatarScript](https://img.shields.io/badge/DatarScript-Everything%20in%20English-brightgreen)](https://github.com/datarscript/datarscript)
[![Version](https://img.shields.io/badge/version-2.0-blue)](.)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB)](.)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **DatarScript** - A revolutionary programming language that bridges natural English and machine code, enabling developers to write software using intuitive, readable language.

<div align="center">
  <img src="https://via.placeholder.com/800x300/007acc/white?text=DatarScript+-+Programming+in+English" alt="DatarScript Banner" width="100%">
  <p><em>Revolutionary programming: code that reads like plain English</em></p>
</div>

## ✨ What is DatarScript?

DatarScript eliminates traditional programming syntax barriers by allowing code in natural English. Designed for accessibility and productivity, it supports complex applications while maintaining readability for non-programmers.

### 🚀 Key Features

<div style="display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0;">
  <span style="background: #28a745; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">📖 Human-Readable Code</span>
  <span style="background: #007bff; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">🌐 No Programming Knowledge Required</span>
  <span style="background: #17a2b8; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">🔧 Powerful Builtins</span>
  <span style="background: #ffc107; color: black; padding: 5px 10px; border-radius: 5px; font-weight: bold;">🎯 Minimal Learning Curve</span>
  <span style="background: #e83e8c; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">⚡ Fast Execution</span>
  <span style="background: #6f42c1; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">🏗️ Extensible Architecture</span>
</div>

- **Readable**: Statements like "Set x to 10." instead of complex syntax
- **Accessible**: Works for programmers and English speakers alike
- **Modular**: Builtins for files, HTTP, graphics, math, and more
- **Educational**: Great for teaching programming concepts
- **Productive**: Rapid prototyping and script development

## 📦 Installation

### System Requirements
- **Python**: 3.8 or higher
- **Platform**: Linux, macOS, Windows
- **Dependencies**: Standard library only (graphics requires PySide6)

### Automated Install
```bash
# Clone the repository
git clone https://github.com/your-github/datarscript.git
cd datarscript

# Install command-line tools
python3 install.py
```

This installs `datarscript` and `dtsc` commands globally.

### Manual Install
```bash
# For development
pip install -e .
```

## 🚀 Quick Start

### Hello World
Create `hello.dtsc`:
```datarscript
Show "Hello, DatarScript!".

Set name to "World".
Show "Hello, " plus name plus "!".
```

Run it:
```bash
datarscript hello.dtsc
# Output: Hello, DatarScript!
# Output: Hello, World!
```

### Interactive REPL
```bash
datarscript  # No arguments starts REPL

>>> Set x to 42 plus 8.
>>> Show x.
50
>>> quit.
```

### Sample Programs

#### Calculator
```datarscript
Set a to 15.
Set b to 7.
Show "Sum: " plus (a plus b).
Show "Difference: " plus (a minus b).
Show "Product: " plus (a times b).
Show "Quotient: " plus (a divided by b).
```

#### FizzBuzz
```datarscript
For i from 1 to 15, do:
    Set mod3 to i modulo 3.
    Set mod5 to i modulo 5.
    If mod3 equals 0 and mod5 equals 0, then:
        Show "FizzBuzz".
    Else if mod3 equals 0, then:
        Show "Fizz".
    Else if mod5 equals 0, then:
        Show "Buzz".
    Else:
        Show i.
    End if.
End for.
```

## 🎯 Language Capabilities

### 30+ Builtin Functions
- **Math**: `sqrt`, `sin`, `cos`, `random`, `abs`, `log`
- **Files**: `read_file`, `write_file`, `list_files`, `delete_file`
- **Networking**: `fetch`, `post`, JSON parsing
- **System**: `input`, `print`, `trim`, `exit`
- **Graphics** (Qt): Drawing, events, animations
- **Terminal**: ANSI colors, cursor control, progress bars

### Complete Feature Set
✅ Variables & Assignment (`Set x to 10.`)  
✅ Arithmetic & Comparison (`x plus y`, `is greater than`)  
✅ Control Flow (`If ... then:`, `While ... do:`, `For ...`)  
✅ Functions (`Create function called name ...`)  
✅ Data Structures (`Lists`, `Dictionaries`)  
✅ Error Handling (`Try: ... Catch: ...`)  
✅ File I/O & Networking  
✅ Graphics & GUI  
✅ Extensions Support  

## 📚 Documentation

<div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
📖 <strong>Complete Documentation:</strong> <a href="docs/README.md">📎 docs/README.md</a><br>
🌟 <strong>Features at a Glance:</strong> Everything documented with examples<br>
🎨 <strong>Advanced HTML Styling:</strong> Beautiful, navigable docs with dark mode support
</div>

### Key Documentation Sections

| Section | Description |
|---------|-------------|
| [**Language Overview**](docs/language/overview.md) | Introduction and key features |
| [**Reference**](docs/language/reference.md) | Complete syntax and grammar |
| [**Data Types**](docs/language/datatypes.md) | Numbers, strings, lists, dictionaries |
| [**Operators**](docs/language/operators.md) | Arithmetic, comparison, logical |
| [**Control Structures**](docs/language/control.md) | If/else, loops, error handling |
| [**Builtins**](docs/builtins/all.md) | 50+ function reference with examples |
| [**Examples**](docs/examples/index.md) | Real-world programs and patterns |
| [**API Docs**](docs/api/interpreter.md) | Embedding and extending the language |

## 🔧 Testing & Linting

This project uses **Ruff** for fast linting and formatting:

```bash
# Check for lint errors
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .
```

### Run Tests

```bash
# Run single DatarScript test
python3 datarscript.py tests/hello_world.dtsc

# Run all tests
for f in tests/*.dtsc; do echo "=== $f ==="; python3 datarscript.py "$f" || exit 1; done
```

Test cases include: arithmetic, strings, booleans, loops, functions, I/O, and more.

## 🚀 Example Applications

### 🤖 AI Chat Bot (Terminal)
```datarscript
# Sample from examples/openrouter_chat.dtsc
Set api_key to "your-key-here".
Set model to "nvidia/nemotron-3-nano-30b-a3b:free".
Set api_url to "https://openrouter.ai/api/v1/chat/completions".
# ... (tool-based chat with JSON, HTTP, file ops)
```

### 🐍 Snake Game (GUI)
```datarscript
# Sample from examples/snake_game.dtsc
Call graphics_init with "Snake Game", 400, 400.
# Drawing, events, game loop with random direction
```

### 🤖 CLI AI Assistant
```datarscript
# examples/dataragent.dtsc
# Colors, spinners, JSON, HTTP for AI responses
```

## 🤝 Contributing

We welcome contributions! See [Contributing Guide](docs/api/contributing.md) for details.

- 🐛 **Report Issues**: [GitHub Issues](https://github.com/datarscript/datarscript/issues)
- 📝 **Enhance Documentation**: PRs welcome for docs improvements
- 🛠️ **Add Features**: Extend builtins or syntax
- 🧪 **Write Tests**: Add test cases in `tests/`

### Development Setup
```bash
git clone https://github.com/your-github/datarscript.git
cd datarscript
pip install -e .
ruff check .  # Run lints
```

## 📜 License

**MIT License** - See [LICENSE](LICENSE) file for details.

## 🙋 FAQ

**Q: Is this a toy language?**  
A: No! DatarScript supports real applications: games, AI chat, file processing, web services.

**Q: Why English syntax?**  
A: Reduces cognitive load, makes programming accessible to more people.

**Q: Performance?**  
A: Interpreted Python-based, suitable for scripts and applications (not systems programming).

**Q: Can I embed it?**  
A: Yes! Use the Interpreter class in Python code. See API docs.

**Q: Graphics support?**  
A: Optional Qt/PySide6 integration for 2D drawing and GUI.

---

<div align="center">
  <p><strong>Ready to code in English? 🚀</strong></p>
  <p>⭐ Star this repo • 📖 Read the docs • 🎯 Start coding!</p>
</div>

---

*[DatarScript Interpreter v2.0 - Making programming universal]*</content>
<parameter name="filePath">README.md