"""
main.py
Menjalankan semua soal latihan Bab 8 secara berurutan.

Soal 1 — Kompleksitas waktu (penjelasan di simulation.py)
Soal 2 — Eksekusi manual: enqueue kelipatan 3
Soal 3 — Eksekusi manual: enqueue & dequeue
Soal 4 — Jalankan simulasi lengkap
Soal 5 — Simulasi satuan detik + tabel eksperimen
Soal 6 — Fungsi reverse_queue
"""

import random
from queue_adt import Queue
from simulation import TicketCounterSimulation, TicketCounterSimulationSeconds


# ======================================================================= #
#  Soal 1 — Kompleksitas Waktu                                             #
# ======================================================================= #

def soal_1():
    print("=" * 62)
    print("SOAL 1 — Kompleksitas Waktu (Worst Case)")
    print("=" * 62)
    rows = [
        ("__init__(self, ...)",       "O(n)",    "Membuat n agen dalam loop"),
        ("run(self)",                 "O(m·n)",  "m tick × n agen per tick"),
        ("_handleArrival(t)",         "O(1)",    "Satu enqueue ke passengerQ"),
        ("_handleBeginService(t)",    "O(n)",    "Cari agen bebas dari n agen"),
        ("_handleEndService(t)",      "O(n)",    "Cek semua n agen apakah selesai"),
        ("printResults()",            "O(1)",    "Hitung & cetak, tidak ada loop"),
    ]
    print(f"  {'Operasi':<30} {'Big-O':<10} {'Keterangan'}")
    print("  " + "-" * 58)
    for op, bigo, note in rows:
        print(f"  {op:<30} {bigo:<10} {note}")
    print()


# ======================================================================= #
#  Soal 2 — Eksekusi Manual: enqueue kelipatan 3                           #
# ======================================================================= #

def soal_2():
    print("=" * 62)
    print("SOAL 2 — Eksekusi Manual: Enqueue Kelipatan 3")
    print("=" * 62)
    print("  Kode:")
    print("    values = Queue()")
    print("    for i in range(16):")
    print("        if i % 3 == 0:")
    print("            values.enqueue(i)")
    print()

    values = Queue()
    enqueued = []
    print(f"  {'i':>3}  {'i % 3':>6}  {'Aksi':<18}  Isi Queue")
    print("  " + "-" * 52)
    for i in range(16):
        if i % 3 == 0:
            values.enqueue(i)
            enqueued.append(i)
            aksi = f"enqueue({i})"
        else:
            aksi = "-"
        print(f"  {i:>3}  {i % 3:>6}  {aksi:<18}  {enqueued}")

    print()
    print(f"  ► Isi Queue Akhir (front→rear): {enqueued}")
    print()


# ======================================================================= #
#  Soal 3 — Eksekusi Manual: enqueue & dequeue                             #
# ======================================================================= #

def soal_3():
    print("=" * 62)
    print("SOAL 3 — Eksekusi Manual: Enqueue & Dequeue")
    print("=" * 62)
    print("  Kode:")
    print("    values = Queue()")
    print("    for i in range(16):")
    print("        if i % 3 == 0:")
    print("            values.enqueue(i)")
    print("        elif i % 4 == 0:")
    print("            values.dequeue()")
    print()

    values = Queue()
    current = []   # representasi list untuk ditampilkan

    print(f"  {'i':>3}  {'Kondisi':<20}  {'Aksi':<22}  Isi Queue")
    print("  " + "-" * 65)
    for i in range(16):
        if i % 3 == 0:
            values.enqueue(i)
            current.append(i)
            kondisi = f"i%3==0 ✓"
            aksi = f"enqueue({i})"
        elif i % 4 == 0:
            removed = current.pop(0) if current else None
            if not values.isEmpty():
                values.dequeue()
            kondisi = f"i%4==0 ✓"
            aksi = f"dequeue() → hapus {removed}"
        else:
            kondisi = "keduanya ✗"
            aksi = "-"
        print(f"  {i:>3}  {kondisi:<20}  {aksi:<22}  {current}")

    print()
    print(f"  ► Isi Queue Akhir (front→rear): {current}")
    print()


# ======================================================================= #
#  Soal 4 — Jalankan Simulasi (menit)                                      #
# ======================================================================= #

def soal_4():
    print("=" * 62)
    print("SOAL 4 — Simulasi TicketCounterSimulation")
    print("=" * 62)
    random.seed(42)   # seed agar reproducible

    sim = TicketCounterSimulation(
        num_agents=2,
        num_minutes=25,
        between_time=2,
        service_time=3
    )
    print("  Parameter: 2 agen, 25 menit, betweenTime=2, serviceTime=3")
    sim.run()
    sim.printResults()


# ======================================================================= #
#  Soal 5 — Simulasi Satuan Detik + Tabel Eksperimen                       #
# ======================================================================= #

def soal_5():
    print("=" * 62)
    print("SOAL 5 — Simulasi Satuan DETIK + Tabel Eksperimen")
    print("=" * 62)
    print("  (1 menit = 60 detik, nilai disesuaikan)\n")

    experiments = [
        # (num_agents, num_seconds, between_time, service_time)
        (2, 6000,  120, 180),
        (2, 30000, 120, 180),
        (2, 60000, 120, 180),
        (2, 6000,  120, 240),
        (2, 30000, 120, 240),
        (2, 60000, 120, 240),
        (3, 6000,  120, 240),
        (3, 30000, 120, 240),
        (3, 60000, 120, 240),
    ]

    header = (
        f"  {'Seconds':>8} {'Agents':>7} {'Service':>8} "
        f"{'Between':>8} {'AvgWait':>9} {'Served':>8} {'Remaining':>10}"
    )
    print(header)
    print("  " + "-" * 65)

    random.seed(0)
    for num_agents, num_seconds, between_time, service_time in experiments:
        sim = TicketCounterSimulationSeconds(
            num_agents, num_seconds, between_time, service_time
        )
        sim.run()
        served, remaining, avg_wait = sim.printResults.__wrapped__(sim) \
            if hasattr(sim.printResults, '__wrapped__') \
            else _run_silent(sim)

        print(
            f"  {num_seconds:>8} {num_agents:>7} {service_time:>8} "
            f"{between_time:>8} {avg_wait:>9.2f} {served:>8} {remaining:>10}"
        )
    print()


def _run_silent(sim):
    """Helper: ambil hasil tanpa mencetak ke layar."""
    served = sim._numPassengers - len(sim._passengerQ)
    avg_wait = sim._totalWaitTime / served if served > 0 else 0.0
    return served, len(sim._passengerQ), avg_wait


# ======================================================================= #
#  Soal 6 — Fungsi reverse_queue                                           #
# ======================================================================= #

def reverse_queue(q):
    """
    Membalik urutan item dalam queue q.

    Strategi:
        1. Pindahkan semua item dari queue ke stack (list Python).
        2. Pindahkan kembali dari stack ke queue (urutan terbalik otomatis).

    Kompleksitas:
        Waktu : O(n) — setiap item di-dequeue dan di-enqueue satu kali
        Ruang : O(n) — stack menyimpan semua n item sementara

    Hanya menggunakan operasi Queue ADT: enqueue, dequeue, isEmpty, __len__.
    """
    stack = []
    while not q.isEmpty():
        stack.append(q.dequeue())   # Queue → Stack
    while stack:
        q.enqueue(stack.pop())      # Stack → Queue (terbalik)
    return q


def soal_6():
    print("=" * 62)
    print("SOAL 6 — Fungsi reverse_queue")
    print("=" * 62)

    q = Queue()
    original = [1, 2, 3, 4, 5]
    for item in original:
        q.enqueue(item)

    print(f"  Queue sebelum : {original}  (front=1, rear=5)")

    reverse_queue(q)

    result = []
    temp = Queue()
    while not q.isEmpty():
        val = q.dequeue()
        result.append(val)
        temp.enqueue(val)

    print(f"  Queue sesudah : {result}  (front=5, rear=1)")
    print()
    print("  Penjelasan algoritma:")
    print("    Langkah 1 — dequeue semua item ke stack : O(n)")
    print("    Langkah 2 — pop stack, enqueue kembali  : O(n)")
    print("    Total : O(n) waktu, O(n) ruang")
    print()


# ======================================================================= #
#  Entry point                                                             #
# ======================================================================= #

if __name__ == "__main__":
    soal_1()
    soal_2()
    soal_3()
    soal_4()

    # Soal 5 perlu simulasi berat — jalankan langsung
    print("=" * 62)
    print("SOAL 5 — Simulasi Satuan DETIK + Tabel Eksperimen")
    print("=" * 62)
    print("  (1 menit ≈ 60 detik, parameter disesuaikan)\n")

    experiments = [
        (2, 6000,  120, 180),
        (2, 30000, 120, 180),
        (2, 60000, 120, 180),
        (2, 6000,  120, 240),
        (2, 30000, 120, 240),
        (2, 60000, 120, 240),
        (3, 6000,  120, 240),
        (3, 30000, 120, 240),
        (3, 60000, 120, 240),
    ]

    header = (
        f"  {'Seconds':>8} {'Agents':>7} {'Service':>8} "
        f"{'Between':>8} {'AvgWait':>9} {'Served':>8} {'Remaining':>10}"
    )
    print(header)
    print("  " + "-" * 65)

    random.seed(0)
    for num_agents, num_seconds, between_time, service_time in experiments:
        sim = TicketCounterSimulationSeconds(
            num_agents, num_seconds, between_time, service_time
        )
        sim.run()
        served = sim._numPassengers - len(sim._passengerQ)
        avg_wait = sim._totalWaitTime / served if served > 0 else 0.0
        remaining = len(sim._passengerQ)
        print(
            f"  {num_seconds:>8} {num_agents:>7} {service_time:>8} "
            f"{between_time:>8} {avg_wait:>9.2f} {served:>8} {remaining:>10}"
        )
    print()

    soal_6()