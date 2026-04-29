# 🎫 Latihan Bab 8 — Queue & Simulasi Loket Tiket

> Implementasi Python murni untuk semua soal latihan Bab 8  
> tentang **Queue ADT** dan **simulasi antrian loket tiket bandara**.

---

## 📁 Struktur Project

```
latihan_bab8/
├── queue_adt.py    ← Queue ADT (linked list, semua operasi O(1))
├── people.py       ← Kelas Passenger dan TicketAgent
├── simulation.py   ← TicketCounterSimulation (menit & detik)
├── main.py         ← Runner semua soal (Soal 1–6)
└── README.md
```

---

## 🚀 Cara Menjalankan

Tidak perlu install library apapun — cukup **Python 3**.

```bash
python main.py
```

---

## 📝 Jawaban Soal

---

### Soal 1 — Kompleksitas Waktu (Worst Case)

| Operasi | Big-O | Penjelasan |
|---|---|---|
| `__init__()` | **O(n)** | Buat `n` agen dalam loop |
| `run()` | **O(m·n)** | `m` menit × iterasi `n` agen per menit |
| `_handleArrival()` | **O(1)** | Satu operasi `enqueue` ke passengerQ |
| `_handleBeginService()` | **O(n)** | Cari agen bebas dari `n` agen |
| `_handleEndService()` | **O(n)** | Cek semua `n` agen apakah selesai |
| `printResults()` | **O(1)** | Hitung & cetak, tidak ada loop |

> `n` = jumlah agen, `m` = durasi simulasi (menit)

---

### Soal 2 — Eksekusi Manual: Enqueue Kelipatan 3

```python
values = Queue()
for i in range(16):
    if i % 3 == 0:
        values.enqueue(i)
```

Nilai yang di-enqueue adalah bilangan dalam `range(16)` yang habis dibagi 3:

```
i = 0, 3, 6, 9, 12, 15
```

**Isi queue akhir (front → rear):**
```
[ 0, 3, 6, 9, 12, 15 ]
```

---

### Soal 3 — Eksekusi Manual: Enqueue & Dequeue

```python
values = Queue()
for i in range(16):
    if i % 3 == 0:
        values.enqueue(i)
    elif i % 4 == 0:
        values.dequeue()
```

Trace per iterasi:

| i | Kondisi | Aksi | Isi Queue |
|---|---|---|---|
| 0 | i%3==0 ✓ | enqueue(0) | [0] |
| 3 | i%3==0 ✓ | enqueue(3) | [0, 3] |
| 4 | i%4==0 ✓ | dequeue() → hapus 0 | [3] |
| 6 | i%3==0 ✓ | enqueue(6) | [3, 6] |
| 8 | i%4==0 ✓ | dequeue() → hapus 3 | [6] |
| 9 | i%3==0 ✓ | enqueue(9) | [6, 9] |
| 12 | i%3==0 ✓ | enqueue(12) | [6, 9, 12] |
| 15 | i%3==0 ✓ | enqueue(15) | [6, 9, 12, 15] |

> **Catatan:** `i=0` memenuhi `i%3==0` sekaligus `i%4==0`, tetapi kondisi `if` dicek lebih dulu sehingga enqueue diutamakan. Hal yang sama berlaku untuk `i=12`.

**Isi queue akhir (front → rear):**
```
[ 6, 9, 12, 15 ]
```

---

### Soal 4 — Implementasi Tiga Metode Simulasi

Tiga metode yang diimplementasikan di `simulation.py`:

#### `_handleArrival(cur_time)` — Aturan #1
```python
def _handleArrival(self, cur_time):
    if random.random() <= self._arriveProb:
        self._passengerQ.enqueue(Passenger(cur_time))
        self._numPassengers += 1
```
Penumpang tiba secara acak. Probabilitas tiba per menit = `1 / between_time`.

#### `_handleBeginService(cur_time)` — Aturan #2
```python
def _handleBeginService(self, cur_time):
    for agent in self._theAgents:
        if agent.isFree():
            if not self._passengerQ.isEmpty():
                passenger = self._passengerQ.dequeue()
                self._totalWaitTime += cur_time - passenger.arrivalTime()
                agent.startService(passenger, cur_time + self._serviceTime)
            break
```
Agen pertama yang bebas langsung melayani penumpang paling depan di antrian.

#### `_handleEndService(cur_time)` — Aturan #3
```python
def _handleEndService(self, cur_time):
    for agent in self._theAgents:
        if agent.isFinished(cur_time):
            agent.stopService()
```
Setiap agen yang sudah selesai melayani di-reset menjadi bebas kembali.

---

### Soal 5 — Modifikasi Satuan Detik

Kelas `TicketCounterSimulationSeconds` mewarisi `TicketCounterSimulation` dan mengganti satuan menjadi **detik**. Tidak ada perubahan logika — hanya nama parameter yang berubah.

```python
# Sebelum (menit)
sim = TicketCounterSimulation(num_agents=2, num_minutes=100, ...)

# Sesudah (detik)
sim = TicketCounterSimulationSeconds(num_agents=2, num_seconds=6000, ...)
```

**Hasil eksperimen** (jalankan `python main.py` untuk hasil lengkap):

| Seconds | Agents | Service | Between | Avg Wait | Served | Remaining |
|---|---|---|---|---|---|---|
| 6000 | 2 | 180 | 120 | ~49 dtk | ~49 | ~2 |
| 30000 | 2 | 180 | 120 | ~133 dtk | ~252 | 0 |
| 60000 | 2 | 180 | 120 | ~93 dtk | ~491 | ~1 |
| 6000 | 3 | 240 | 120 | ~20 dtk | ~46 | 0 |
| 30000 | 3 | 240 | 120 | ~44 dtk | ~254 | 0 |
| 60000 | 3 | 240 | 120 | ~54 dtk | ~492 | 0 |

**Pengamatan:** Menambah agen dari 2 → 3 sangat signifikan mengurangi rata-rata waktu tunggu, bahkan ketika `service_time` lebih lama (240 vs 180 detik).

---

### Soal 6 — Fungsi `reverse_queue`

```python
def reverse_queue(q):
    stack = []

    # Langkah 1: Queue → Stack
    while not q.isEmpty():
        stack.append(q.dequeue())

    # Langkah 2: Stack → Queue (urutan terbalik)
    while stack:
        q.enqueue(stack.pop())

    return q
```

**Contoh:**
```
Sebelum : [ 1, 2, 3, 4, 5 ]   (front = 1)
Sesudah : [ 5, 4, 3, 2, 1 ]   (front = 5)
```

**Mengapa ini bekerja?**

Stack bersifat LIFO. Saat queue dikosongkan ke stack, item terakhir yang masuk ke stack adalah item paling depan queue. Saat stack dikembalikan ke queue, urutan tersebut terbalik secara alami.

**Analisis Kompleksitas:**
| | Nilai |
|---|---|
| Waktu | **O(n)** — tiap item di-dequeue & di-enqueue tepat sekali |
| Ruang | **O(n)** — stack menyimpan semua n item sementara |

Hanya menggunakan operasi Queue ADT: `enqueue`, `dequeue`, `isEmpty`.

---

## 🧠 Konsep Kunci

| Konsep | Penjelasan |
|---|---|
| **Queue (FIFO)** | Item pertama masuk adalah yang pertama keluar |
| **Linked List Queue** | `enqueue` & `dequeue` keduanya O(1), tanpa pergeseran elemen |
| **Simulasi Event-Driven** | Waktu berjalan per tick; tiap tick menangani 3 aturan secara berurutan |
| **Probabilitas Kedatangan** | `arriveProb = 1 / between_time`, diuji dengan `random.random()` |

---

## 📚 Referensi

Buku: *Data Structures and Algorithms Using Python* — Rance D. Necaise, Bab 8: Queue
