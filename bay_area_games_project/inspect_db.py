import sqlite3
import sys


def main() -> None:
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    )
    tables = [r[0] for r in cur.fetchall()]
    print("tables:", tables)
    for t in tables:
        print(f"\n{t}")
        cur.execute(f"PRAGMA table_info({t})")
        for cid, name, ctype, notnull, dflt, pk in cur.fetchall():
            sys.stdout.write(
                f"  {name} {ctype}"
                f"{' NOT NULL' if notnull else ''}"
                f"{' PK' if pk else ''}"
                f"{f' DEFAULT {dflt}' if dflt is not None else ''}\n"
            )


if __name__ == "__main__":
    main()

