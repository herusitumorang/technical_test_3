#!/usr/bin/env python
# coding: utf-8

# In[2]:


import sqlite3
import pandas as pd

# contoh data, sesuaikan sendiri kalau perlu
data = [
    ("Asep", 120_000_000, "2024-01-15"),
    ("Ginanjar", 70_000_000, "2024-02-28"),
    ("Slamet", 50_000_000, "2024-03-01"),
    ("Budi", 200_000_000, "2023-02-28"),
]

# bikin database di memory
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE Nasabah (
        Nama           TEXT,
        JumlahHutang   INTEGER,
        TanggalPembayaran  TEXT        -- format: 'YYYY-MM-DD'
    )
""")

cursor.executemany("INSERT INTO Nasabah VALUES (?, ?, ?)", data)
conn.commit()

# query sesuai soal:
# - kolom Keterangan: High / Medium Attention
# - filter hanya sampai akhir Februari, dengan logika tahun kabisat
query = """
SELECT
    Nama,
    JumlahHutang,
    CASE
        WHEN JumlahHutang >= 100000000 THEN 'High Attention'
        ELSE 'Medium Attention'
    END AS Keterangan
FROM Nasabah
WHERE
    date(TanggalPembayaran) <= date(
        printf(
            '%04d-02-%02d',
            CAST(strftime('%Y', TanggalPembayaran) AS INTEGER),
            CASE
                -- tahun kabisat: habis dibagi 400
                -- atau habis dibagi 4 tapi tidak habis dibagi 100
                WHEN (CAST(strftime('%Y', TanggalPembayaran) AS INTEGER) % 400 = 0)
                     OR (CAST(strftime('%Y', TanggalPembayaran) AS INTEGER) % 4 = 0
                         AND CAST(strftime('%Y', TanggalPembayaran) AS INTEGER) % 100 != 0)
                THEN 29      -- akhir Feb di tahun kabisat
                ELSE 28      -- akhir Feb di tahun biasa
            END
        )
    )
ORDER BY TanggalPembayaran, Nama;
"""

# ambil hasil; pakai pandas biar enak dilihat
df = pd.read_sql_query(query, conn)
print(df)


# In[ ]:




