from prettytable import PrettyTable

# Tabel untuk workout
tabel_workout = PrettyTable()
tabel_workout.field_names = ["No", "Nama Workout", "Durasi (menit)", "Repetisi"]

# Kelas Workout untuk program latihan
class Workout:
    id_counter = 1

    def __init__(self, name, duration, repition):
        self.id = Workout.id_counter  # Setiap workout akan punya ID unik
        Workout.id_counter += 1
        self.name = name
        self.duration = duration
        self.repition = repition

# Kelas Admin untuk mengelola workout
class AdminWorkout:
    def __init__(self):
        self.workouts = []  # Daftar workout yang tersedia di prgram latihan fisik transformasi kesehatan

    # Fungsi menambah banyak workout
    def create_multiple_workouts(self):
        jumlah_workout = int(input("Berapa banyak workout yang ingin ditambahkan? "))
        for i in range(jumlah_workout):
            print(f"\nWorkout ke-{i + 1}")
            name = input("Masukkan nama workout: ")
            duration = int(input("Masukkan durasi workout (menit): "))
            repition = input("Masukkan Banyaknya Repetisi: ")
            workout = Workout(name, duration, repition)
            self.workouts.append(workout)
            tabel_workout.add_row([len(self.workouts), name, duration, repition])
        print(f"{jumlah_workout} workout berhasil ditambahkan!")

    # Fungsi melihat semua workout
    def read_workouts(self):
        if self.workouts:
            print(tabel_workout)
        else:
            print("Belum ada workout yang tersedia.")

    # Fungsi mengubah workout
    def update_workout(self):
        self.read_workouts()
        try:
            index = int(input("Pilih nomor workout yang ingin diubah: ")) - 1
            if 0 <= index < len(self.workouts):
                new_name = input(f"Nama baru (sekarang: {self.workouts[index].name}): ")
                new_duration = int(input(f"Durasi baru (sekarang: {self.workouts[index].duration} menit): "))
                new_repition = input(f"Repetisi baru (sekarang: {self.workouts[index].repition}): ")
                self.workouts[index].name = new_name
                self.workouts[index].duration = new_duration
                self.workouts[index].repition = new_repition
                tabel_workout._rows[index] = [index + 1, new_name, new_duration, new_repition]
                print("Workout berhasil diubah!")
            else:
                print("Nomor workout tidak valid.")
        except ValueError:
            print("Input tidak valid.")

    # Fungsi menghapus workout
    def delete_workout(self):
        self.read_workouts()
        try:
            index = int(input("Pilih nomor workout yang ingin dihapus: ")) - 1
            if 0 <= index < len(self.workouts):
                removed_workout = self.workouts.pop(index)
                tabel_workout.del_row(index)
                print(f"Workout '{removed_workout.name}' berhasil dihapus!")
            else:
                print("Nomor workout tidak valid.")
        except ValueError:
            print("Input tidak valid.")

# Kelas untuk Pengguna
class PenggunaWorkout:
    def __init__(self, available_workouts, name=None, age=None, goal=None):
        # Memastikan data pengguna hanya diisi sekali
        if name is None:
            self.name = input("Masukkan nama Anda: ")
        else:
            self.name = name
        
        if age is None:
            self.age = input("Masukkan umur Anda: ")
        else:
            self.age = age
        
        if goal is None:
            self.goal = input("Apa tujuan Anda berolahraga? ")
        else:
            self.goal = goal
        
        self.workout_history = []  # Menyimpan workout yang telah diikuti oleh pengguna
        self.available_workouts = available_workouts

    # Fungsi menambah workout ke progress pengguna
    def add_workout(self):
        if self.available_workouts:
            print(tabel_workout)
            pilihan = int(input("Pilih nomor workout yang ingin diikuti: ")) - 1
            if 0 <= pilihan < len(self.available_workouts):
                selected_workout = self.available_workouts[pilihan]
                self.workout_history.append(selected_workout)
                print(f"Workout '{selected_workout.name}' berhasil ditambahkan ke progres Anda!")
            else:
                print("Nomor workout tidak valid.")
        else:
            print("Belum ada workout yang tersedia.")

    # Fungsi sinkronisasi workout pengguna dengan admin
    def sync_workouts(self):
        synced_history = []
        for workout in self.workout_history:
            # Cari workout di list admin 
            for admin_workout in self.available_workouts:
                if workout.id == admin_workout.id:
                    synced_history.append(admin_workout)  # Tambah yang cocok
                    break
        self.workout_history = synced_history  # Update history dengan data yang sudah disinkronkan

    # Fungsi melihat progress pengguna
    def view_progress(self):
        self.sync_workouts()  # Sinkronisasi otomatis sebelum melihat progress

        tabel_user = PrettyTable()
        tabel_user.field_names = ["Atribut", "Data"]
        tabel_user.add_row(["Nama", self.name])
        tabel_user.add_row(["Umur", self.age])
        tabel_user.add_row(["Tujuan", self.goal])

        print(tabel_user)

        if self.workout_history:
            tabel_progres = PrettyTable()
            tabel_progres.field_names = ["No", "Nama Workout", "Durasi (menit)", "Repetisi"]
            for i, workout in enumerate(self.workout_history, 1):
                tabel_progres.add_row([i, workout.name, workout.duration, workout.repition])
            print("Workout yang telah diikuti:")
            print(tabel_progres)
        else:
            print("Anda belum mengikuti workout apapun.")

# Fungsi login
def login():
    admin = AdminWorkout()  # Admin untuk workout
    pengguna_list = []  # List yang menyimpan semua pengguna
    while True:
        print("\n" + "=" * 5 + "Selamat Datang di Program Latihan Fisik Transformasi Kesehatan" + "=" * 5)
        print("[1]. Admin Workout")
        print("[2]. Pengguna Workout")
        pilihan = input("Silakan Pilih Mode Login: ")
        if pilihan == "1":
            admin_workout(admin)
        elif pilihan == "2":
            pengguna_workout(admin, pengguna_list)
        else:
            print("Pilihan tidak valid. Coba lagi.")

# Login untuk Mode Admin Workout
def admin_workout(admin):
    while True:
        print("\nMenu Admin Workout:")
        print("1. Tambah Banyak Workout Sekaligus")
        print("2. Lihat Workout")
        print("3. Ubah Workout")
        print("4. Hapus Workout")
        print("5. Keluar")
        fitur = input("Pilih Fitur (1-5): ")
        if fitur == "1":
            admin.create_multiple_workouts()  # Langsung menambahkan banyak workout
        elif fitur == "2":
            admin.read_workouts()
        elif fitur == "3":
            admin.update_workout()
        elif fitur == "4":
            admin.delete_workout()
        elif fitur == "5":
            break
        else:
            print("Pilihan tidak valid.")

# Login untuk Mode Pengguna Workout
def pengguna_workout(admin, pengguna_list):
    if pengguna_list:
        pengguna = pengguna_list[-1]  # Mengambil data pengguna terakhir
    else:
        pengguna = PenggunaWorkout(admin.workouts)  # Pengguna baru
    
    pengguna_list.append(pengguna)  # Menambahkan pengguna baru 
    while True:
        print("\nMenu Pengguna Workout:")
        print("1. Lihat Progress")
        print("2. Tambah Workout ke Progress")
        print("3. Keluar")
        fitur = input("Pilih Fitur (1-3): ")
        if fitur == "1":
            pengguna.view_progress()
        elif fitur == "2":
            pengguna.add_workout()
        elif fitur == "3":
            print("Terimakasih telah menggunakan program latihan fisik transformasi kesehatan.")
            break
        else:
            print("Pilihan tidak valid.")

# Menjalankan program latihan fisik transformasi kesehatan
login()
