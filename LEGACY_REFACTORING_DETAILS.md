# Legacy Code Refactoring Details

This document details the specific refactoring operations performed on the legacy Java codebase to improve its maintainability, readability, and reliability before or during the reengineering process.

---

### Refactoring 1: Encapsulation and Access Control
**File:** `src/Employee.java`

**Before Code:**
```java
class Employee {
 //attributes
 private String username;
 // ...
 
 //methods
 String getUsername() {return username;}
 String getName() {return name;}
 // ...
 //void setUsername(String usename){this.username = username;};
 void setName(String name){this.name = name;};
}
```

**After Code:**
```java
public class Employee {
 //attributes
 private String username;
 // ...
 
 //methods
 public String getUsername() {return username;}
 public String getName() {return name;}
 // ...
 public void setName(String name){this.name = name;}
}
```

**Explanation:**
Changed the access modifiers of getter and setter methods from package-private (default) to `public`. Also removed commented-out dead code and fixed indentation.

**Quality Impact:**
*   **Encapsulation**: Ensures the class interface is clearly defined and accessible where needed, following standard Java Bean conventions.
*   **Readability**: Removing dead code makes the class easier to understand.

---

### Refactoring 2: Removal of Dead Code (OS Checks)
**File:** `src/POSSystem.java`

**Before Code:**
```java
  private void readFile(){
    if (System.getProperty("os.name").startsWith("W")||System.getProperty("os.name").startsWith("w")){
      //unixOS = false; //commented out to support netbeans 
      //employeeDatabase = "..\\Database\\employeeDatabase.txt";
      //rentalDatabaseFile = "..\\Database\\rentalDatabase.txt"; 
      //itemDatabaseFile = "..\\Database\\itemDatabase.txt";
    }
    // ...
```

**After Code:**
```java
  private void readFile(){
    // OS check removed as paths are now relative to project root
    
    String line = null;
    String[] lineSort;
    // ...
```

**Explanation:**
Removed the commented-out `if` block that was checking for Windows OS to change file paths. This code was inactive and cluttered the logic.

**Quality Impact:**
*   **Maintainability**: Reduces visual noise and confusion for developers reading the code.
*   **Clean Code**: Adheres to the principle that version control (Git) should handle history, not commented-out blocks.

---

### Refactoring 3: Constant Immutability
**File:** `src/POSSystem.java`

**Before Code:**
```java
public class POSSystem{
  public boolean unixOS = true; 
  public static String employeeDatabase = "Database/employeeDatabase.txt";
  public static String rentalDatabaseFile = "Database/rentalDatabase.txt"; 
  // ...
```

**After Code:**
```java
public class POSSystem{
  private boolean unixOS = true; 
  
  private static final String employeeDatabase = "Database/employeeDatabase.txt";
  public static final String rentalDatabaseFile = "Database/rentalDatabase.txt"; 
  // ...
```

**Explanation:**
Added the `final` keyword to database file path variables and changed `employeeDatabase` to `private`.

**Quality Impact:**
*   **Reliability**: Prevents accidental modification of file paths during runtime.
*   **Security**: Restricts access to internal configuration variables (`private`).

---

### Refactoring 4: Proper Error Logging
**File:** `src/Inventory.java`

**Before Code:**
```java
    catch(FileNotFoundException ex) {
        System.out.println(
            "Unable to open file '" + 
                    databaseFile + "'"); 
        ableToOpen = false;
    }
```

**After Code:**
```java
    catch(FileNotFoundException ex) {
        System.err.println(
            "Unable to open file '" + 
                    databaseFile + "'"); 
        ableToOpen = false;
    }
```

**Explanation:**
Replaced `System.out.println` with `System.err.println` in catch blocks.

**Quality Impact:**
*   **Observability**: Separates actual application output from error messages, allowing for better log filtering and debugging.
