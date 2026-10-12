# Student Management System (Easy Version)

Ye ek simple Python + SQLite project hai jisme sirf 4 kaam hote hain:
**Add, View/Search, Update, Delete** — student ka record.

Koi framework nahi, koi extra library nahi. Sirf plain Python.

---

## Files kya kya hai

```
sms_easy/
├── main.py         -> Menu chalta hai isse, user se baat cheet
├── database.py     -> Database ka sara kaam yaha hota hai
├── sample_data.py  -> Test ke liye demo students daal deta hai
└── README.md       -> Ye file jo tum padh rahe ho
```

**Kyun 2 files alag rakhi?**
`main.py` sirf menu dikhata hai aur input leta hai.
`database.py` sirf SQLite se baat karta hai.
Isse code samajhna easy hota hai — jisko jo dhundhna hai, seedha usi file me jaake dekh sakta hai.

---

## Kaise chalayein

1. Python already installed hona chahiye (3.6+). SQLite ke liye kuch install
   karne ki zarurat nahi — `sqlite3` Python ke andar hi aata hai.

2. Pehle demo data daal lo (optional):
   ```
   python sample_data.py
   ```

3. Fir program chalao:
   ```
   python main.py
   ```

4. Menu me se choice daalo (1 se 5 tak). Exit karne ke liye 5 daalo.

Jaise hi program chalega, ek `students.db` file khud ban jayegi — usi me sara data save hota hai.

---

## Database Table

Table ka naam: `students`

| Column     | Kya hai |
|------------|---------|
| student_id | Unique ID (PRIMARY KEY) |
| name       | Naam |
| email      | Email |
| phone      | Phone number |
| course     | Course ka naam |
| marks      | Marks (0-100) |

---

## Kaise kaam karta hai (Simple Words Mein)

1. `main.py` jab chalta hai, sabse pehle `database.create_table()` call
   hota hai — ye table bana deta hai agar pehle se nahi hai.
2. User menu se koi option choose karta hai (jaise "Add Student").
3. `main.py` user se input leta hai (Name, Email, etc), aur check karta hai
   ki sahi hai ya nahi (jaise Marks 0-100 ke beech honi chahiye).
4. Fir `main.py`, `database.py` ke function ko call karta hai
   (jaise `database.add_student(...)`).
5. `database.py` ye kaam karta hai:
   - `sqlite3.connect("students.db")` se database khulta hai
   - SQL query chalti hai (`?` placeholders ke saath, taki hacking na ho)
   - `commit()` se changes save hote hain
   - `close()` se connection band hota hai
6. Result wapas `main.py` ko milta hai, jo user ko screen pe dikhata hai.

Bas itna hi! Python ↔ sqlite3 module ↔ students.db file — yahi pura flow hai.

---

## Test Data (sample_data.py chalane se ye add hoga)

| ID  | Naam         | Course              | Marks |
|-----|--------------|---------------------|-------|
| 101 | Aarav Sharma | Computer Science    | 88.5  |
| 102 | Priya Verma  | Information Tech    | 92.0  |
| 103 | Rohan Gupta  | Mechanical          | 74.25 |
| 104 | Sneha Iyer   | Electronics         | 65.0  |
| 105 | Karan Mehta  | Computer Science    | 55.5  |

---

## Kuch Important Points (Interview ke liye bhi kaam aayenge)

- **student_id PRIMARY KEY hai** → matlab ye unique hoga, duplicate nahi ban sakta.
- **`?` placeholders use kiye hain** SQL me → isse "SQL Injection" attack se bacha jata hai.
- **Marks check hota hai 0-100 ke beech** → agar galat number daalo to phir se poochega.
- **Agar ID nahi milti** (search/update/delete me) → program crash nahi hota, sirf "ID nahi mili" bolta hai.
- **commit() zaroori hai** har Add/Update/Delete ke baad, warna data save nahi hoga.

Bas itna samajh liya to poora project easily explain kar paoge interview me. 👍
