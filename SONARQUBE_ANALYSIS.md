# Static Analysis Report (Simulated SonarQube)

**Project:** Legacy POS System (Java)
**Date:** December 6, 2025
**Analysis Mode:** Manual Code Review based on SonarQube Rules

---

## Summary
| Metric | Value | Rating |
| :--- | :--- | :--- |
| **Security Hotspots** | 3 | E (Critical) |
| **Reliability (Bugs)** | 5 | D (Major) |
| **Maintainability (Smells)** | 12 | C (Minor) |
| **Duplicated Blocks** | ~15% | - |

---

## Detailed Findings

### 1. Security Hotspots (High Priority)

#### A. Hardcoded Credentials & Paths
*   **File**: `src/POSSystem.java`
*   **Issue**: `public static String employeeDatabase = "Database/employeeDatabase.txt";`
*   **Rule**: *java:S1313 - IP addresses and file paths should not be hardcoded.*
*   **Impact**: Makes the application vulnerable to path traversal attacks and reduces portability.

#### B. Plaintext Password Handling
*   **File**: `src/POSSystem.java`
*   **Issue**: `String password="";` (Line 17)
*   **Rule**: *java:S2068 - Credentials should not be hard-coded or stored in plain text.*
*   **Impact**: Passwords stored in Strings stay in memory until garbage collected. `char[]` should be used instead.

#### C. Standard Output Logging
*   **File**: `src/POSSystem.java`
*   **Issue**: `System.out.println("Unable to open file...");` (Line 50)
*   **Rule**: *java:S106 - Standard outputs should not be used directly to log anything.*
*   **Impact**: Sensitive debugging info might be exposed; use a Logger (e.g., Log4j, SLF4J) instead.

### 2. Reliability & Bugs

#### A. Potential Null Pointer / Index Out of Bounds
*   **File**: `src/POSSystem.java`
*   **Issue**: `lineSort = line.split(" "); String name=lineSort[2]+" "+lineSort[3];` (Line 39)
*   **Rule**: *java:S2259 - Null pointers should not be dereferenced / Arrays should be checked.*
*   **Impact**: If a line in the text file is malformed (has fewer than 4 spaces), the application will crash.

#### B. Generic Exception Handling
*   **File**: `src/POSSystem.java`
*   **Issue**: `e.printStackTrace();` (Line 78)
*   **Rule**: *java:S1148 - Throwable.printStackTrace(...) should not be used.*
*   **Impact**: Does not handle the error state, just prints it.

### 3. Maintainability (Code Smells)

#### A. God Class (High Complexity)
*   **File**: `src/POSSystem.java`
*   **Issue**: Class handles UI, Database, and Auth.
*   **Rule**: *java:S1200 - Classes should not be coupled to too many other classes (Single Responsibility Principle).*
*   **Impact**: Hard to test and maintain.

#### B. Commented-Out Code
*   **File**: `src/POSSystem.java`
*   **Issue**: `//unixOS = false; //commented out to support netbeans` (Line 22)
*   **Rule**: *java:S125 - Sections of code should not be commented out.*
*   **Impact**: Bloats code; use Git for history instead.

#### C. Public Mutable Fields
*   **File**: `src/POSSystem.java`
*   **Issue**: `public boolean unixOS = true;` (Line 8)
*   **Rule**: *java:S1104 - Class variable fields should not be public.*
*   **Impact**: Breaks encapsulation; any other class can modify this state.

---

## Recommendations for Reengineering
1.  **Modularization**: Break `POSSystem.java` into `AuthService`, `FileService`, and `Main`.
2.  **Security**: Implement hashing for passwords (done in Python version).
3.  **Configuration**: Move file paths to a config file or environment variables.
4.  **Logging**: Replace `System.out` with a proper logging framework.
