# Reengineering Project Status & Rubric Tracking

This document tracks the progress of the software reengineering project against the provided rubric.

## 1. Inventory Analysis & Document Restructuring (15 Marks)
- [x] Complete asset inventory (Code, Data, Docs, Configs)
- [x] Classification of assets (Active, Obsolete, Reusable)
- [x] Dependency mapping
- [x] Legacy documentation reconstruction

## 2. Reverse Engineering & Smell Detection (15 Marks)
- [x] Extract architecture/class diagrams (Textual description/Mermaid)
- [x] Identify code smells (with evidence)
- [x] Identify data smells (with evidence)
- [x] Recover business logic workflows

## 3. Code Restructuring (10 Marks)
- [x] Refactoring plan
- [x] Improve modularity and clarity
- [x] Reduce complexity

## 4. Data Restructuring (10 Marks)
- [x] Analyze legacy data (.txt files)
- [x] Design normalized database schema (ER Diagram/SQL)
- [x] Data migration strategy
- [x] Justification of database choice

## 5. Forward Engineering (Improved Architecture) (15 Marks)
- [x] Select technology stack (Python/Flask + SQLite/SQLAlchemy selected)
- [x] Implement Layered Architecture (Presentation, Logic, Data)
- [x] Implement Web-based interface
- [x] Demonstrate modularity

## 6. Reengineering Plan & Migration (10 Marks)
- [x] Timeline and Phases
- [x] Risk Analysis
- [x] Migration Strategy

## 7. Refactoring Documentation (10 Marks)
- [x] Refactoring 1: [Architecture] Monolithic Java Swing -> MVC Flask Web App
- [x] Refactoring 2: [Data] Flat Text Files -> Relational SQLite Database
- [x] Refactoring 3: [Security] Plaintext Passwords -> Scrypt Hashing

## 8. Risk Analysis & Testing (10 Marks)
- [x] Identify Risks (Data loss during migration, downtime)
- [x] Mitigation strategies (Backup legacy data, parallel run)
- [x] Testing evidence (Unit tests implemented in `tests/`)

## 9. Dual Documentation (10 Marks)
- [x] Comparison of Legacy vs Reengineered
- [x] Mapping tables (Legacy Files -> DB Tables)

## 10. Work Distribution (5 Marks)
- [x] Contribution table (Simulated for AI agent)
