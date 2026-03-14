# 🎉 DatarScript: Code That Talks Like Your Best Friend! 🎉

[![DatarScript](https://img.shields.io/badge/DatarScript-Everything%20in%20English-brightgreen)](https://github.com/ForgedInFiles/datarSCRIPT)
[![Version](https://img.shields.io/badge/version-0.0.1--beta.1-orange)](https://github.com/ForgedInFiles/datarSCRIPT/releases)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/ForgedInFiles/datarSCRIPT/actions)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-ff69b4)](https://github.com/astral-sh/ruff)

> **DatarScript** - Where your ideas flow straight into code, no translator needed! 💫  
> Write programs that read like you're explaining them to a friend over coffee. ☕

<div align="center">
  <img src="https://raw.githubusercontent.com/ForgedInFiles/datarSCRIPT/main/docs/banner.png" alt="DatarScript Banner - Programming should feel like storytelling" width="800"/>
  <p><em>🌟 Because the best code is the code you can actually read!</em> 🌟</p>
</div>

## ✨ What Makes DatarScript Special?

Imagine writing code that your grandma could understand. That's DatarScript! We've tossed out the cryptic symbols and awkward syntax of traditional programming languages and replaced them with plain, beautiful English.

### 🚀 Why You'll Love DatarScript

- **📖 Read Like a Story**: `Set counter to 0.` instead of `counter = 0;` - it's literally English!
- **🌈 Instant Gratification**: See results immediately with our friendly REPL
- **🧠 Zero Syntax Stress**: No more hunting for missing semicolons or mismatched brackets
- **🔧 Batteries Included**: 50+ builtins for files, web, graphics, math, and terminal magic
- **🎯 Learn in Minutes, Master in Hours**: Perfect for beginners, powerful enough for experts
- **💡 Think in Solutions, Not Syntax**: Spend brainpower on *what* you want to build, not *how* to write it

## 📦 Getting Started - It's Easier Than Making Toast! 🍞

### 🎯 One-Command Install (Seriously, That's It!)
```bash
# Grab the code and install in one smooth move
git clone https://github.com/ForgedInFiles/datarSCRIPT.git && cd datarSCRIPT && python3 install.py
```
*This installs the `datarscript` and `dtsc` commands to your ~/.local/bin (add it to your PATH if needed)*

### 🚀 Quick Dip Your Toes In
```bash
# No setup needed! Just run:
echo 'Show "Hello, Human!"' > hello.dtsc
datarscript hello.dtsc
```
*Output:*  
`Hello, Human!`  
*Boom. You're a programmer.* 💪

### 💻 Want the Latest and Greatest? (For Developers)
```bash
# For when you want to contribute or tinker under the hood
git clone https://github.com/ForgedInFiles/datarSCRIPT.git
cd datarSCRIPT
pip install -e .  # Development mode - changes take effect immediately!
```

## 🌈 Your First DatarScript Adventure

Let's make something fun together!

### 📝 Create a File Called `fun.dtsc`
```datarscript
Show "🌈 Welcome to the most friendly programming language ever!".

Set yourName to Ask "What's your amazing name? ".
Show "Nice to meet you, " plus yourName plus "! You're about to write your first program.".

Set luckyNumber to Random from 1 to 100.
Show "Your lucky number today is: " plus luckyNumber.

If luckyNumber is greater than 50, then:
    Show "Whoa! That's a big number! You're feeling lucky today! 🍀".
Else:
    Show "Hey, smaller numbers are cool too! They're like hidden gems. 💎".
End if.

Show "Thanks for playing, " plus yourName plus "! Come back anytime!".
```

### ▶️ Run It and Watch the Magic!
```bash
datarscript fun.dtsc
```
*Sample Output:*
```
🌈 Welcome to the most friendly programming language ever!
What's your amazing name? Alex
Nice to meet you, Alex! You're about to write your first program.
Your lucky number today is: 73
Whoa! That's a big number! You're feeling lucky today! 🍀
Thanks for playing, Alex! Come back anytime!
```

### 💬 Or Just Chat With It (REPL Mode)
```bash
datarscript  # No file = instant REPL!
```
*Then type:*
```
>>> Set pizzaSlices to 8.
>>> Set friends to 3.
>>> Show "Each person gets " plus (pizzaSlices divided by friends) plus " slices."
>>> Show "Time to party! 🎉"
```
*Output:*
```
Each person gets 2.6666666666666665 slices.
Time to party! 🎉
>>> quit.
```
*Bye for now!* 👋

## 🛠️ What Can You Build? (Spoiler: Anything!)

DatarScript isn't just for hello worlds - it's a full-featured language that grows with you:

| Feature | What You Can Do | Example |
|---------|----------------|---------|
| **🌐 Web Magic** | Fetch data, post to APIs, parse JSON | `Set weather to Fetch "https://api.weather.com/today"` |
| **🎨 Graphics & Games** | Draw shapes, handle clicks, make animations | `Call draw_circle with 100, 100, 50, "red"` |
| **📁 File Ninja** | Read/write files, list directories, manage files | `Set contents to Read file "notes.txt"` |
| **💻 Terminal Wizard** | Create beautiful CLI apps with colors, spinners, progress bars | `Call clear_screen.` then `Show "Loading..." in blue` |
| **🧮 Math Whisperer** | Trigonometry, statistics, random numbers, logarithms | `Set hypotenuse to SquareRootOf((3 times 3) plus (4 times 4))` |
| **🔤 Text Magician** | Manipulate strings, search, replace, format | `Set shouty to UppercaseOf("hello world")` |
| **⚡ Control Flow** | Make decisions, loop through data, handle errors | `For each item in myList, do: Show item.` |

## 📚 Documentation That Doesn't Suck

We believe docs should be as fun as the language itself!

- 📖 **[Complete Language Guide](docs/README.md)** - Everything you need to know
- 🎓 **[Learn by Example](docs/examples/)** - Copy-paste and run real programs
- 🔧 **[API Reference](docs/api/)** - For when you want to extend or embed DatarScript
- 🌟 **[Community Showcase](https://github.com/ForgedInFiles/datarSCRIPT/discussions)** - See what others are building

## 🧪 Testing - Because Nobody Likes Bugs 🐞

### Run a Single Test (Like a Boss)
```bash
# Test that makes your heart smile
python3 datarscript.py tests/01_hello_world.dtsc
# Or after install:
dtsc tests/09_lists.dtsc
```

### Run All Tests (Because Confidence Feels Good)
```bash
# Feel the satisfaction of all green checks!
for test in tests/*.dtsc; do
  echo "🧪 Running: $(basename "$test")"
  python3 datarscript.py "$test" || { echo "❌ Oh no! $test failed!"; exit 1; }
done
echo "🎉 All tests passed! You're awesome!"
```

### Socket Tests (For the Networking Fans)
```bash
# Terminal 1: Start the server
python3 test_socket_server.py

# Terminal 2: Run a socket test
dtsc tests/test_blocking_input.dtsc
```

## 🤝 Join the Fun - We Save You a Seat! 🪑

We're building a community where everyone belongs - whether you're writing your first line of code or your ten-thousandth.

### 🐞 Found a Quirk?
[File an issue](https://github.com/ForgedInFiles/datarSCRIPT/issues/new) - we'll buy you a virtual coffee while we fix it! ☕

### 💡 Got a Brilliant Idea?
[Start a discussion](https://github.com/ForgedInFiles/datarSCRIPT/discussions) - let's make it happen together!

### 🛠️ Want to Contribute?
1. Fork the repo (top right button - it's friendly!)
2. Create your feature branch (`git checkout -b feature/amazing-thing`)
3. Make your changes (remember: be kind to future readers!)
4. Run the tests (`./test_all.sh` or use the loops above)
5. Format your code (`ruff check --fix . && ruff format .`)
6. Send a pull request - we'll review it with love and high-fives! 🙌

### 📜 Contributor's Golden Rules
- **Be excellent to each other** - no tolerance for toxicity
- **Keep it readable** - if it's not clear English, we'll help you fix it
- **Test your changes** - we want to trust your code
- **Have fun!** - if you're not enjoying it, we're doing it wrong

## 📜 License - Share the Love! ❤️

DatarScript is MIT licensed - which means:
- ✅ Use it in your open-source projects
- ✅ Use it in your commercial projects  
- ✅ Modify it to your heart's content
- ✅ Share it with friends, family, and strangers on the internet
- ❌ Just don't claim you wrote it (we worked hard on this!)

See [LICENSE](LICENSE) for the full legalese (but really, just be excellent to each other).

## 🙋‍♀️ Frequently Asked Questions (Because We've Heard It All!)

**Q: "Is this a real language or just a toy?"**  
A: As real as it gets! People have built web scrapers, games, data analysis tools, and even AI interfaces with DatarScript. It's Python-powered under the hood, so it's serious business.

**Q: "Do I need to know programming to start?"**  
A: Nope! If you can speak English, you can DatarScript. We've had complete beginners write useful scripts on their first day.

**Q: "What about performance?"**  
A: It's interpreted Python, so it's perfect for scripts, tools, and applications. For number-crunching that needs C-speed, you can always call out to Python libraries.

**Q: "Can I use this for my day job?"**  
A: Absolutely! Many developers use it for automation, prototyping, and internal tools. It's especially great when you need to show non-technical stakeholders what you're building.

**Q: "How does it handle... [advanced concept]?"**  
A: Check the [docs](docs/README.md)! We've got you covered with everything from object-oriented patterns to functional programming concepts - all in friendly English.

**Q: "Can I contribute if I'm new to open source?"**  
A: YES! We love helping newcomers make their first contribution. Just ask for help - we're here for you.

## 🚀 Ready to Make Programming Fun Again?

<div align="center">
  <a href="https://github.com/ForgedInFiles/datarSCRIPT">
    <img src="https://img.shields.io/badge/-Star%20Us%20%E2%98%85-%23181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Stars"/>
  </a>
  <a href="https://github.com/ForgedInFiles/datarSCRIPT/discussions">
    <img src="https://img.shields.io/badge/-Join%20The%20Conversation-%232ea44f?style=for-the-badge&logo=github-discussions&logoColor=white" alt="Discussions"/>
  </a>
  <a href="docs/README.md">
    <img src="https://img.shields.io/badge/-Read%20The%20Fun%20Docs-%23ff69b4?style=for-the-badge&logo=bookstack&logoColor=white" alt="Documentation"/>
  </a>
</div>

---

<p align="center">
  <em>Made with ❤️ by humans who believe code should be kind to humans.</em><br>
  <a href="https://github.com/ForgedInFiles/datarSCRIPT">ForgedInFiles</a> • 2026<br>
  <em>"The best programming language is the one you don't have to think about."</em>
</p>