# TTMS-codes

Schema, seed data, and reference scripts for **TTMS** — a table tennis gear & setup management database.

## Contents

| File | Description |
| --- | --- |
| `creation.sql` | MySQL schema — creates the `Player`, `Blade`, `Rubber`, `Glue`, and `Setup` tables. |
| `inserting.sql` | Seed data as batch `INSERT` statements for the five tables, in FK-safe order. |
| `TTMS_Data_Generator.py` | Python script that generates the seed data (uses `Faker`, fixed seed for reproducible output). |
| `part3.sql` | T-SQL practice script — DDL examples plus stored procedures against the `TTMS` database. |

## Prerequisites

- **MySQL 8+** for `creation.sql` and `inserting.sql`
- **SQL Server** for `part3.sql`
- **Python 3.9+** with `faker` (`pip install faker`) to run the generator

## Usage

### 1. Create the schema

```sql
SOURCE creation.sql;
```

### 2. Load the seed data

```sql
SOURCE inserting.sql;
```

### 3. Regenerate the seed data (optional)

```bash
pip install faker
python TTMS_Data_Generator.py
```

This writes `ttms_seed_data.sql` to the current directory. The script uses `SEED = 42`, so running it twice produces identical data.

### 4. Run the T-SQL reference script

Open `part3.sql` in SQL Server Management Studio or Azure Data Studio and execute it against a database named `TTMS`.

> These scripts create and drop objects. Review them before running against anything you care about.

## Repository layout

```
TTMS-codes/
├── README.md
├── creation.sql
├── inserting.sql
├── part3.sql
├── TTMS_Data_Generator.py
└── .gitignore
```
