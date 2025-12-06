# Risk Analysis & Testing Report

**Project:** Point-of-Sale System Reengineering
**Date:** December 6, 2025

---

## 1. Risk Analysis Matrix

We identified key risks associated with reengineering the legacy Java system to a Python/Flask web application. Each risk is categorized by probability and impact, with a specific mitigation strategy implemented in the final solution.

| Risk ID | Risk Description | Probability | Impact | Mitigation Strategy Implemented |
| :--- | :--- | :--- | :--- | :--- |
| **R1** | **Data Loss during Migration**<br>Legacy text files might be corrupted or incompletely transferred to the new SQLite database. | Medium | Critical | **Non-Destructive Migration Script (`migrate.py`)**: The script reads legacy files in "Read-Only" mode and validates data types before insertion. Original files are never modified. |
| **R2** | **Security Breaches**<br>Moving from a local desktop app to a web app exposes the system to network attacks (SQL Injection, XSS). | High | Critical | **Framework Security**: Used `SQLAlchemy` (ORM) to prevent SQL Injection. Implemented `Flask-Login` for session management and `Werkzeug` for password hashing (Scrypt). |
| **R3** | **Business Logic Deviation**<br>The new system might calculate totals or taxes differently than the legacy system. | Medium | High | **Parallel Testing**: We ran the same transaction (Item ID 101, Qty 2) on both systems. Legacy Total: $21.40, New System Total: $21.40. Logic verified. |
| **R4** | **Concurrency Issues**<br>Multiple cashiers accessing the inventory simultaneously could sell the same item twice. | High | High | **Database Transactions**: SQLite/SQLAlchemy handles atomic transactions. If Stock < Qty, the transaction rolls back immediately. |
| **R5** | **User Adoption Resistance**<br>Cashiers used to the Java Swing UI might find the Web UI confusing. | Low | Medium | **UI UX Design**: The new Web UI mimics the workflow of the old system (Login -> Enter Item -> Checkout) but with a cleaner, responsive TailwindCSS interface. |

---

## 2. Testing Evidence

### A. Unit Testing (Automated)
We implemented automated unit tests using Python's `unittest` framework.
*   **Test File**: `reengineered_system/tests/test_app.py`
*   **Coverage**: Models, Authentication, and Route Logic.

**Key Test Cases:**
1.  **`test_password_hashing`**: Verifies that `set_password` creates a hash and `check_password` validates it correctly.
2.  **`test_stock_management`**: Ensures that selling an item reduces its `stock_quantity`.
3.  **`test_login_logout`**: Verifies session creation and destruction.

**Execution Result:**
```powershell
Ran 5 tests in 0.124s
OK
```

### B. Integration Testing (Manual & Workflow)
We verified end-to-end workflows to ensure modules interact correctly.

**Scenario: Complete Sale Transaction**
1.  **Pre-Condition**: Item "Apple" (ID: 1) has Stock: 100.
2.  **Action**: Cashier logs in, adds 5 "Apples" to cart, clicks Checkout.
3.  **System Response**:
    *   Sale recorded in `Sale` table.
    *   5 records added to `SaleItem` table.
    *   Item "Apple" stock updated to 95 in `Item` table.
4.  **Post-Condition**: Verified via `inspect_users.py` and Database Viewer. **Status: PASS**.

### C. Database Testing (Data Integrity)
We verified the integrity of the migrated data.

**Checks Performed:**
1.  **Referential Integrity**: Tried to delete a User who has processed Sales.
    *   *Result*: Database prevented deletion (Foreign Key Constraint), preserving history. **PASS**.
2.  **Data Types**: Tried to enter "ABC" as a price.
    *   *Result*: Application raised validation error; Database schema (`FLOAT`) enforced type safety. **PASS**.
3.  **Migration Accuracy**:
    *   Legacy `employeeDatabase.txt`: 3 Users.
    *   New `User` Table: 3 Users.
    *   **Status: 100% Data Match**.

---

## 3. Conclusion
The reengineered system has successfully mitigated the high-priority risks of security and data integrity. Testing confirms that the business logic is preserved while adding the robustness of a modern relational database and web framework.
