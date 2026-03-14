# DatarScript: A Natural Language Programming Language Specification

## Executive Summary

DatarScript is a revolutionary programming language designed to bridge the gap between human language and machine code. By leveraging natural English syntax and eliminating traditional programming symbols, DatarScript enables developers to write software using intuitive, readable language that requires minimal learning curve.

## Table of Contents
1. [Language Overview](#language-overview)
2. [File Conventions and Execution](#file-conventions-and-execution)
3. [Core Syntax Rules](#core-syntax-rules)
4. [Data Types and Variables](#data-types-and-variables)
5. [Operators and Expressions](#operators-and-expressions)
6. [Control Structures](#control-structures)
7. [Functions and Procedures](#functions-and-procedures)
8. [Data Structures](#data-structures)
9. [Error Handling](#error-handling)
10. [File and System Operations](#file-and-system-operations)
11. [Scope and Block Structure](#scope-and-block-structure)
12. [Comments and Documentation](#comments-and-documentation)
13. [Standard Library](#standard-library)
14. [Implementation Guidelines](#implementation-guidelines)
15. [Success Criteria](#success-criteria)
16. [Example Programs](#example-programs)
17. [Terminal Control (Plain English)](#terminal-control-plain-english)


## File Conventions and Execution

DatarScript files use `.dtsc` as the standard file extension, with `.datar` also supported for compatibility. The language can be executed from the command line using the following commands:

- `datarscript <filename>.dtsc`
- `datarscript <filename>.datar`
- `dtsc <filename>.dtsc` (alias)
- `dtsc <filename>.datar` (alias)

The interpreter will automatically detect the file based on content regardless of extension.



## Language Overview

DatarScript is designed for developers who want to focus on problem-solving rather than syntax memorization. The language uses natural English words, commas, and periods exclusively, making it accessible to both programmers and non-programners.

### Key Design Principles
- **Readability**: Code should be understandable by English speakers
- **Simplicity**: Minimal syntax rules and no special symbols
- **Expressiveness**: Powerful enough for real-world applications
- **Consistency**: Predictable behavior across all language features

## Core Syntax Rules

### Statement Structure
- All statements must end with a period
- Commas separate items in lists, parameters, or multiple expressions
- No other punctuation symbols allowed
- Keywords are case-insensitive but typically written in lowercase

### Whitespace and Formatting
- Indentation is significant for block structure
- Multiple spaces/tabs are treated as single space
- Line breaks are ignored except for readability

**Valid Examples:**
```
Set age to 25.
Create name as "John Doe".
Make is_active equal to true.
Define numbers as 1, 2, 3, 4, 5.
Ask for user name and store in input_name.
Show "Hello, " plus name plus "! Welcome to our program.".
```

## Data Types and Variables

### Primitive Types
- **Number**: Integer and floating-point values
- **String**: Text data enclosed in double quotes
- **Boolean**: true or false values
- **Null**: Represents absence of value

### Complex Types
- **List**: Ordered collection of values
- **Dictionary**: Key-value pairs
- **Function**: Callable code blocks

### Variable Declaration and Assignment

#### Basic Assignment
```
Set variable_name to value.
Create variable_name as value.
Make variable_name equal to value.
Define variable_name as value.
```

#### Type Inference
```
Set age to 25.              # Number
Create name as "John".       # String
Make is_active equal to true. # Boolean
Define numbers as 1, 2, 3.    # List
```

#### Multiple Assignment
```
Set x, y, z to 1, 2, 3.
Create first_name, last_name as "John", "Doe".
Make a, b, c equal to true, false, true.
```

## Operators and Expressions

DatarScript supports various arithmetic, comparison, and logical operators for building expressions. All operators work with the expected data types (numbers for arithmetic, booleans for logical, etc.). Parentheses can be used to group expressions and override precedence.

### Operator Precedence

Operator precedence determines the order of evaluation when multiple operators appear in the same expression. Higher precedence operators are evaluated first. Parentheses can override this order.

The precedence levels (from highest to lowest) are:

1. **Parenthesized Expressions**: `(expression)`
2. **Unary Operators**: `not`
3. **Arithmetic: Powers**: `raised to`
4. **Arithmetic: Multiplication, Division, Modulo**: `times`, `divided by`, `modulo`
5. **Arithmetic: Addition and Subtraction**: `plus`, `minus`
6. **Comparisons**: `is equal to`, `is not equal to`, `differs from`, `is greater than`, `is greater than or equal to`, `is at least`, `is less than`, `is less than or equal to`, `is at most`, `equals`, `is not`
7. **Logical AND**: `and`
8. **Logical OR**: `or`
9. **Pipe Operator**: `|>` (left-associative)

**Precedence Visualization:**
```
Highest → | → or → and → comparisons → + - → × ÷ % → ^ → not → parentheses ← Lowest
```

### Pipe Operator

The pipe operator (`|>`) takes the value on its left and passes it as the first argument to the function on its right. This enables a readable, left-to-right flow of data transformation.

**Syntax:**
```
value |> function_name
value |> function_name with arg1, arg2
```

**Examples:**
```
# Basic usage
Set name to "alice".
Set capitalized_name to name |> convert to uppercase.

# With additional arguments
Set result to numbers |> sort in ascending order.

# Chaining multiple operations
Set processed_data to raw_data
    |> trim whitespace
    |> convert to lowercase
    |> replace "test" with "production".
```

### Arithmetic Operations

Arithmetic operators perform mathematical calculations on numbers.

| Operator | Syntax | Example | Result | Description |
|----------|--------|---------|--------|-------------|
| Addition | `plus`, `+` | `Set sum to 5 plus 3.` | `8` | Adds two numbers |
| Subtraction | `minus`, `-` | `Set diff to 10 minus 4.` | `6` | Subtracts second from first |
| Multiplication | `times` | `Set product to 4 times 5.` | `20` | Multiplies two numbers |
| Division | `divided by` | `Set quotient to 15 divided by 3.` | `5` | Divides first by second |
| Modulo | `modulo` | `Set remainder to 17 modulo 5.` | `2` | Finds remainder of division |
| Exponentiation | `raised to` | `Set power to 2 raised to 3.` | `8` | Raises first to power of second |

**Additional Arithmetic Patterns:**
- `Add 5 to counter.` → `(counter = counter + 5)`
- `Subtract 3 from counter.` → `(counter = counter - 3)`
- `Multiply counter by 2.` → `(counter = counter * 2)`
- `Divide counter by 2.` → `(counter = counter / 2)`

### Comparison Operations

Comparison operators test relationships between values and return boolean results (true/false).

| Operator | Syntax | Example | Result | Description |
|----------|--------|---------|--------|-------------|
| Equal to | `is equal to`, `equals` | `If age is equal to 18, then...` | `true` if values are identical | Tests equality |
| Not equal to | `is not equal to`, `differs from`, `is not` | `If name is not equal to "John", then...` | `true` if values differ | Tests inequality |
| Greater than | `is greater than` | `If age is greater than 18, then...` | `true` if first > second | Tests greater than |
| Greater than or equal | `is greater than or equal to`, `is at least` | `If score is at least 90, then...` | `true` if first ≥ second | Tests greater or equal |
| Less than | `is less than` | `If temperature is less than 0, then...` | `true` if first < second | Tests less than |
| Less than or equal | `is less than or equal to`, `is at most` | `If count is at most 10, then...` | `true` if first ≤ second | Tests less or equal |

### Logical Operations

Logical operators combine or modify boolean values.

| Operator | Syntax | Example | Result | Description |
|----------|--------|---------|--------|-------------|
| Logical AND | `and` | `If age is greater than 18 and has_permission, then...` | `true` if both are true | True only if both operands true |
| Logical OR | `or` | `If age is less than 18 or is_emergency, then...` | `true` if either is true | True if at least one operand true |
| Logical NOT | `not` | `If not is_admin, then...` | Negates the boolean value | Inverts true/false |

**Compound Examples:**
- `If (age is greater than 18 and name is not empty) or is_admin, then...`
- `If not (age is less than 18 or name equals Guest), then...`

## Control Structures

### Conditional Statements

#### Basic If-Else
```
If condition, then:
    # code block
Else:
    # alternative code block
End if.
```

#### If-Elif-Else
```
If age is greater than 18, then:
    Show "Adult".
Else if age is less than 18, then:
    Show "Minor".
Else:
    Show "Exactly 18".
End if.
```

#### Nested Conditions
```
If age is greater than 18, then:
    If name is not empty, then:
        Show "Hello " plus name plus "!".
    Else:
        Show "Hello anonymous adult!".
    End if.
Else:
    Show "Hello minor!".
End if.
```

### Loop Structures

#### While Loops
```
Set counter to 0.
While counter is less than 10, do:
    Show counter.
    Add 1 to counter.
End while.
```

#### For Loops
```
For each item in numbers, do:
    Show item.
End for.

For i from 1 to 10, do:
    Show i.
End for.

For each key in user, do:
    Show key plus ": " plus value of key in user.
End for.
```

#### Break and Continue
```
Set found to false.
Set index to 0.
While not found and index is less than list_length, do:
    If item at index equals target, then:
        Set found to true.
        Break.
    Else:
        Add 1 to index.
    End if.
End while.

For each item in numbers, do:
    If item is less than 0, then:
        Continue.
    End if.
    Show item.
End for.
```

## Functions and Procedures

### Function Definition

#### Basic Function
```
Create a function called calculate_sum that takes two numbers:
    Set result to first number plus second number.
    Return result.
End function.
```

#### Function with Multiple Parameters
```
Create a function called greet that takes name and age:
    If age is greater than 18, then:
        Set message to "Hello " plus name plus ", you're an adult!".
    Else:
        Set message to "Hello " plus name plus ", you're a minor!".
    End if.
    Return message.
End function.
```

#### Function with Default Parameters
```
Create a function called format_name that takes first_name and last_name equals "Unknown":
    If last_name is empty, then:
        Return first_name.
    Else:
        Return first_name plus " " plus last_name.
    End if.
End function.
```

### Function Calling

#### Basic Call
```
Set sum_result to call calculate_sum with 5 and 3.
Set greeting to call greet with John and 25.
```

#### Multiple Arguments
```
Set result to call calculate_sum with 10, 20, and 30.
Set formatted to call format_name with John and Doe.
```

#### Return Values
```
Set area to call calculate_area with 10 and 5.
Show "Area is: " plus area.
```

## Data Structures

### Lists

#### Creation and Initialization
```
Set numbers to 1, 2, 3, 4, 5.
Create names as "John", "Jane", "Doe".
Make empty_list equal to.
```

#### List Operations
```
Add 6 to numbers.
Remove the first item from numbers.
Get the third item from numbers and store in third_number.
Set the second item in numbers to 10.
```

#### List Methods
```
Sort numbers in ascending order.
Reverse numbers.
Check if 3 is in numbers.
Get the length of numbers and store in count.
Clear numbers.
```

### Dictionaries

#### Creation and Initialization
```
Set user to name: John, age: 25, city: New York.
Create empty_dict as.
Make config equal to setting1: true, setting2: false.
```

#### Dictionary Operations
```
Get the value of name from user and store in user_name.
Set the value of age in user to 26.
Add email: john@example.com to user.
Remove city from user.
```

#### Dictionary Methods
```
Check if email exists in user.
Get all keys from user and store in keys.
Get all values from user and store in values.
Get the length of user and store in size.
Clear user.
```

## Error Handling

### Try-Catch Blocks

#### Basic Error Handling
```
Try:
    Set result to call divide with 10 and 0.
Catch division by zero error:
    Show "Cannot divide by zero!".
    Set result to 0.
End try.
```

#### Multiple Exceptions
```
Try:
    Open file "data.txt" for reading.
    Set content to read all from file.
    Show content.
    Close file.
Catch file not found error:
    Show "File not found! Creating new file.".
    Open file "data.txt" for writing.
    Write "New file created." to file.
    Close file.
Catch permission denied error:
    Show "Cannot access file due to permissions.".
End try.
```

#### Finally Block
```
Try:
    Open file "data.txt" for reading.
    Set content to read all from file.
    Show content.
Catch file not found error:
    Show "File not found.".
Finally:
    Close file.
End try.
```

### Custom Error Handling

#### Raising Errors
```
If age is less than 0, then:
    Raise invalid age error with message "Age cannot be negative.".
End if.
```

#### Error Types
```
Catch invalid argument error:
    Show "Invalid argument provided.".
Catch index out of bounds error:
    Show "Index is out of range.".
Catch type mismatch error:
    Show "Type mismatch detected.".
```

## File and System Operations

### File Operations

#### File Opening and Closing
```
Open file "data.txt" for reading.
Open file "output.txt" for writing.
Open file "log.txt" for appending.
Close file.
```

#### Reading from Files
```
Set content to read all from file.
Set line to read line from file.
While line is not empty, do:
    Show line.
    Set line to read line from file.
End while.
```

#### Writing to Files
```
Write "Hello World" to file.
Write "This is a test." to file.
Write newline to file.
Write variable to file.
```

### Directory Operations

#### Directory Management
```
List files in directory "documents".
Set files to result.
Show files.

Create directory "new_folder".
Delete directory "old_folder".
Check if file "data.txt" exists.
```

#### Path Operations
```
Set current_path to get current directory.
Set full_path to combine "documents" and "file.txt".
Set file_name to get file name from "documents/file.txt".
```

## Scope and Block Structure

### Block Delimiters

#### Control Structures
```
End if.
End while.
End for.
End function.
End try.
End with.
```

#### Nested Blocks
```
If condition1, then:
    If condition2, then:
        Show "Both conditions true.".
    End if.
    Show "First condition true.".
End if.

While condition, do:
    For each item in list, do:
        If item meets criteria, then:
            Process item.
        End if.
    End for.
End while.
```

### Variable Scope

#### Global Variables
```
Set global_var to "This is global.".

Create a function called test:
    Show global_var.
End function.
```

#### Local Variables
```
Create a function called calculate:
    Set local_var to "This is local.".
    Return local_var.
End function.

# local_var is not accessible here
```

## Comments and Documentation

### Single-Line Comments
```
# This is a comment explaining the next step
# Calculate the total price including tax

Set total to price times quantity. # Calculate subtotal
Add tax to total. # Add sales tax
```

### Multi-Line Comments
```
# This is a
# multi-line comment
# explaining a complex operation

Create a function called complex_operation:
    # First, validate inputs
    If input is invalid, then:
        Raise invalid input error.
    End if.
    
    # Process data
    Set result to process(input).
    
    # Return final result
    Return result.
End function.
```

## Standard Library

### String Functions

#### String Manipulation
```
Set upper_name to convert name to uppercase.
Set lower_name to convert name to lowercase.
Set trimmed to trim whitespace from name.
Set replaced to replace "John" with "Jane" in name.
```

#### String Information
```
Set length to get length of name.
Set starts_with_j to check if name starts with "J".
Set contains_ohn to check if name contains "ohn".
Set index to find "John" in name.
```

### Math Functions

#### Mathematical Operations
```
Set absolute to get absolute value of -5.
Set rounded to round 3.14159 to 2 decimal places.
Set max_value to get maximum of 5, 10, 15.
Set min_value to get minimum of 5, 10, 15.
```

#### Random Numbers
```
Set random_number to generate random number between 1 and 100.
Set random_choice to pick random item from collection.
```

### User Input Functions

#### Reading User Input
```
# Basic user input
Ask for "What is your name?" and store in user_name.
Ask for "How old are you?" and store in age.

# Using input in calculations
Ask for "Enter first number:" and store in num1.
Ask for "Enter second number:" and store in num2.
Set sum to num1 plus num2.
Show "Sum: " plus sum.
```

#### Input Syntax
- `Ask for "prompt message" and store in variable_name.`
- Prompts must be enclosed in double quotes
- Variable receives the user's input as a string
- Input is read from stdin (keyboard input)

### Terminal and Console Functions
These functions control the terminal/console output and input.

| Function | Description |
|----------|-------------|
| `key_read()` | Reads a single key press and returns it as a string. |
| `clear_screen()` | Clears the entire screen and returns cursor to home position (1,1). |
| `sleep_ms(ms)` | Sleeps for specified milliseconds. |
| `wait(ms)` | Alias for `sleep_ms`. Waits for specified milliseconds. |
| `ansi_color(color)` | Returns ANSI color code by name. |
| `ansi_reset()` | Resets all ANSI formatting. |
| `cursor_hide()` | Hides cursor. |
| `cursor_show()` | Shows cursor. |
| `cursor_up(lines)` | Moves cursor up N lines. |
| `cursor_down(lines)` | Moves cursor down N lines. |
| `cursor_right(cols)` | Moves cursor right N columns. |
| `cursor_left(cols)` | Moves cursor left N columns. |
| `cursor_goto(row, col)` | Moves cursor to specific row and column (1-based). |
| `clear_line()` | Clears current line. |
| `clear_to_end()` | Clears from cursor to end of line. |
| `print_raw(text)` | Prints text without adding newline. |
| `flush_output()` | Flushes stdout. |
| `get_terminal_size()` | Gets terminal size as {width, height}. |
| `is_tty()` | Checks if stdout is a TTY. |

### Date and Time Functions

#### Current Time
```
Set current_time to get current time.
Set current_date to get current date.
Set timestamp to get current timestamp.
```

#### Date Manipulation
```
Set tomorrow to add 1 day to current_date.
Set next_week to add 7 days to current_date.
Set formatted to format date as "YYYY-MM-DD".
```

## Implementation Guidelines

### Parser Design

#### Lexical Analysis
1. Tokenize input using natural language patterns
2. Map English words to programming concepts
3. Handle optional commas for readability
4. Use periods to terminate statements

#### Syntax Analysis
1. Build abstract syntax tree from tokens
2. Validate grammar rules
3. Handle nested structures
4. Resolve variable references

### Runtime Environment

#### Memory Management
1. Automatic garbage collection
2. Reference counting for objects
3. Memory pool for small objects

#### Execution Model
1. Stack-based virtual machine
2. Just-in-time compilation support
3. Bytecode interpretation

### Error Recovery

#### Syntax Errors
1. Provide line and column information
2. Suggest possible corrections
3. Continue parsing when possible

#### Runtime Errors
1. Stack trace with function calls
2. Variable values at error point
3. Recovery options when available

## Success Criteria

### Functional Requirements
- [ ] All basic data types supported
- [ ] Complete set of operators implemented
- [ ] Control structures work correctly
- [ ] Functions with parameters and return values
- [ ] Data structures (lists, dictionaries) functional
- [ ] Error handling mechanisms operational
- [ ] File I/O capabilities implemented
- [ ] Comments and documentation supported

### Non-Functional Requirements
- [ ] Code readability for non-programmers
- [ ] Minimal learning curve for English speakers
- [ ] Consistent and predictable behavior
- [ ] Efficient execution performance
- [ ] Comprehensive error messages
- [ ] Extensible architecture for future features

### MVP Validation
- [ ] Hello World program works
- [ ] Basic calculator functionality
- [ ] File reading and writing operations
- [ ] Simple data processing tasks
- [ ] Error handling demonstrations
- [ ] Documentation examples

## Example Programs

### Complete Application: User Management System
```
# User Management System

# Define user structure
Set users to.

# Function to add user
Create a function called add_user that takes name, age, email:
    Set user to name: name, age: age, email: email.
    Add user to users.
    Return "User added successfully!".
End function.

# Function to find user
Create a function called find_user that takes email:
    For each user in users, do:
        If value of email in user equals email, then:
            Return user.
        End if.
    End for.
    Return null.
End function.

# Main program
Try:
    # Add users
    Call add_user with "John Doe", 30, "john@example.com".
    Call add_user with "Jane Smith", 25, "jane@example.com".
    
    # Find user
    Set found_user to call find_user with "john@example.com".
    If found_user is not null, then:
        Show "Found user: " plus value of name in found_user.
        Show "Age: " plus value of age in found_user.
        Show "Email: " plus value of email in found_user.
    Else:
        Show "User not found.".
    End if.

    # List all users
    Show "All users:".
    For each user in users, do:
        Show value of name in user plus " (" plus value of age in user plus ")".
    End for.

Catch any error:
    Show "An error occurred: " plus error message.
End try.
```

### Complete Application: File Processor
```
# File Processor Application

# Function to process file
Create a function called process_file that takes input_file and output_file:
    Try:
        Open file input_file for reading.
        Open file output_file for writing.
        
        Set line_count to 0.
        Set word_count to 0.
        Set char_count to 0.
        
        Set line to read line from file.
        While line is not empty, do:
            Add 1 to line_count.
            
            Set words to split line by spaces.
            Set word_count to word_count plus length of words.
            
            For each word in words, do:
                Set char_count to char_count plus length of word.
            End for.
            
            Write "Line " plus line_count plus ": " plus line to output_file.
            Write newline to output_file.
            
            Set line to read line from file.
        End while.
        
        Write newline to output_file.
        Write "Statistics:" to output_file.
        Write "Lines: " plus line_count to output_file.
        Write "Words: " plus word_count to output_file.
        Write "Characters: " plus char_count to output_file.
        
        Close file.
        Close file.
        
        Return "File processed successfully!".
        
    Catch file not found error:
        Return "Input file not found.".
    Catch permission denied error:
        Return "Permission denied for file access.".
    End try.
End function.

# Main program
Set result to call process_file with "input.txt" and "output.txt".
Show result.
```

## Terminal Control (Plain English)

For full-screen terminal apps, keep everything in natural language:

- `Start screen.` — enter the alternate screen buffer, hide the cursor, disable echo/canonical input, and clear once.
- `Stop screen.` — leave the alternate buffer, show the cursor, and restore terminal settings (also runs on interpreter exit).
- `Clearscreen.` — clear the viewport and scrollback, then move the cursor home.
- `Newscreen.` — enter the alternate buffer without changing echo/cursor state.
- `Cursorhome.` — move the cursor to row 1, column 1.
- `Clearbelow.` — clear from the cursor to the end of the screen.
- `Hide cursor.` / `Unhide cursor.` — explicit cursor control (automatically restored on exit).

## Future Enhancements

### Advanced Features
- **Object-Oriented Programming**: Classes and inheritance
- **Concurrency**: Parallel processing and threading
- **Networking**: HTTP requests and socket programming
- **Database Integration**: SQL and NoSQL database support
- **Web Development**: HTML generation and web frameworks
- **GUI Development**: Desktop application interfaces

### Performance Optimizations
- **Just-in-Time Compilation**: Dynamic code optimization
- **Native Code Generation**: Direct machine code output
- **Parallel Execution**: Multi-core processing support
- **Memory Pooling**: Efficient memory allocation strategies

### Tooling and Ecosystem
- **Debugger**: Step-through debugging capabilities
- **Profiler**: Performance analysis tools
- **Package Manager**: Library and dependency management
- **IDE Integration**: Syntax highlighting and code completion
- **Testing Framework**: Unit testing and integration testing

---

This specification provides a comprehensive foundation for creating DatarScript, a natural language programming language that prioritizes readability and accessibility while maintaining the power and flexibility needed for real-world software development.
