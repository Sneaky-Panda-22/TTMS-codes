# TTMS-codes

SQL Server (T-SQL) scripts and practical reference material for TTMS.

## Contents

| File | Description |
| --- | --- |
| `TTMS_Phase3.sql` | Phase 3 DDL illustrations — create tables, indexes, constraints, views, and related objects. |
| `TTMS.session.sql` | Working session script with hands-on queries, exercises, and experiments against the `TTMS` database. |

## Prerequisites

- Microsoft SQL Server (or Azure SQL) with a database named `TTMS`
- SQL Server Management Studio, Azure Data Studio, or the `sqlcmd` CLI

## Usage

Open the scripts in your SQL client and run them against the `TTMS` database. `TTMS_Phase3.sql` starts with `USE TTMS;`, so the database must exist before executing it.

> Scripts may create, alter, or drop objects. Review them before running against anything you care about.

## Repository layout

```
TTMS-codes/
├── TTMS_Phase3.sql
├── TTMS.session.sql
└── .gitignore
```

## License

No license specified yet. All rights reserved by the author unless stated otherwise.
