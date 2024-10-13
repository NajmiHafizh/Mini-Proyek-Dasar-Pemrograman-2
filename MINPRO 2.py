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
        self.workouts = []

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
    def update_workout(self, user_list):
        self.read_workouts()
        try:
            index = int(input("Pilih nomor workout yang ingin diubah: ")) - 1
            if 0 <= index < len(self.workouts):
                # Perbarui workout di admin
                new_name = input(f"Nama baru (sekarang: {self.workouts[index].name}): ")
                new_duration = int(input(f"Durasi baru (sekarang: {self.workouts[index].duration} menit): "))
                new_repition = input(f"Repetisi baru (sekarang: {self.workouts[index].repition}): ")
                updated_workout = Workout(new_name, new_duration, new_repition)
                updated_workout.id = self.workouts[index].id  # Jaga agar ID tetap sama
                self.workouts[index] = updated_workout
                tabel_workout._rows[index] = [index + 1, new_name, new_duration, new_repition]
                print("Workout berhasil diubah!")
                # Perbarui workout yang ada di progress user
                for user in user_list:
                    user.update_user_workout(updated_workout)
            else:
                print("Nomor workout tidak valid.")
        except ValueError:
            print("Input tidak valid.")

    # Fungsi menghapus workout
    def delete_workout(self, user_list):
        self.read_workouts()
        try:
            index = int(input("Pilih nomor workout yang ingin dihapus: ")) - 1
            if 0 <= index < len(self.workouts):
                removed_workout = self.workouts.pop(index)
                tabel_workout.del_row(index)
                print(f"Workout '{removed_workout.name}' berhasil dihapus!")
                # Hapus workout dari progres user jika workout tersebut ada
                for user in user_list:
                    user.delete_user_workout(removed_workout)
            else:
                print("Nomor workout tidak valid.")
        except ValueError:
            print("Input tidak valid.")

# Kelas untuk User
class UserWorkout:
    def __init__(self, available_workouts):
        self.name = input("Masukkan nama Anda: ")
        self.age = input("Masukkan umur Anda: ")
        self.goal = input("Apa tujuan Anda berolahraga? ")
        self.workout_history = []  # Menyimpan workout yang telah diikuti oleh user
        self.available_workouts = available_workouts
        self.total_duration = 0  # Total durasi dari semua workout yang diikuti
        self.achievements = []  # Daftar pencapaian user

    # Fungsi menambah workout ke progres user
    def add_workout(self):
        if self.available_workouts:
            print(tabel_workout)
            pilihan = int(input("Pilih nomor workout yang ingin diikuti: ")) - 1
            if 0 <= pilihan < len(self.available_workouts):
                selected_workout = self.available_workouts[pilihan]
                self.workout_history.append(selected_workout)
                self.total_duration += selected_workout.duration  # Tambahkan durasi workout
                print(f"Workout '{selected_workout.name}' berhasil ditambahkan ke progres Anda!")
                self.check_achievements()  # Cek apakah ada pencapaian yang diperoleh
            else:
                print("Nomor workout tidak valid.")
        else:
            print("Belum ada workout yang tersedia.")

    # Fungsi update workout dalam progres user
    def update_user_workout(self, updated_workout):
        # Cek apakah workout ada di history user, jika ada update
        for i, workout in enumerate(self.workout_history):
            if workout.id == updated_workout.id:
                self.workout_history[i] = updated_workout
                print(f"Workout '{updated_workout.name}' dalam progres Anda diperbarui.")
    # Fungsi menghapus workout dari progres user
    def delete_user_workout(self, removed_workout):
        self.workout_history = [w for w in self.workout_history if w.id != removed_workout.id]
        print(f"Workout '{removed_workout.name}' telah dihapus dari progres Anda.")
    # Fungsi melihat progress user
    def view_progress(self):
        tabel_user = PrettyTable()
        tabel_user.field_names = ["Atribut", "Data"]
        tabel_user.add_row(["Nama", self.name])
        tabel_user.add_row(["Umur", self.age])
        tabel_user.add_row(["Tujuan", self.goal])
        tabel_user.add_row(["Total Durasi Latihan", f"{self.total_duration} menit"])
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
        
        # Tampilkan pencapaian jika ada
        if self.achievements:
            print("\nPencapaian yang diraih:")
            for achievement in self.achievements:
                print(f"- {achievement}")
        else:
            print("Belum ada pencapaian yang diraih.")

    # Fungsi mengecek pencapaian yang diraih
    def check_achievements(self):
        # Contoh pencapaian berdasarkan total durasi dan jumlah workout
        if self.total_duration >= 20 and "Latihan 20 Menit!" not in self.achievements:
            self.achievements.append("Latihan 20 Menit!")
            print("Selamat! Anda telah mencapai pencapaian: Latihan 20 Menit!")
        if len(self.workout_history) >= 3 and "Menyelesaikan 3 Workout!" not in self.achievements:
            self.achievements.append("Menyelesaikan 3 Workout!")
            print("Selamat! Anda telah mencapai pencapaian: Menyelesaikan 3 Workout!")

# Fungsi login
def login():
    admin = AdminWorkout()  # Admin untuk workout
    user_list = []  # List yang menyimpan semua user
    while True:
        print("\n" + "=" * 5 + "Selamat Datang di Program Latihan Fisik Transformasi Kesehatan" + "=" * 5)
        print("[1]. Admin Workout")
        print("[2]. User Workout")
        pilihan = input("Silakan Pilih Mode Login: ")
        if pilihan == "1":
            admin_workout(admin, user_list)
        elif pilihan == "2":
            user_workout(admin, user_list)
        else:
            print("Pilihan tidak valid. Coba lagi.")

# Login Mode Admin Workout
def admin_workout(admin, user_list):
    while True:
        print("\nMenu Admin Workout:")
        print("1. Tambah Banyak Workout Sekaligus")
        print("2. Lihat Workout")
        print("3. Ubah Workout")
        print("4. Hapus Workout")
        print("5. Keluar")
        fitur = input("Pilih Fitur (1-5): ")
        if fitur == "1":
            admin.create_multiple_workouts()  # Langsung menambah banyak workout
        elif fitur == "2":
            admin.read_workouts()
        elif fitur == "3":
            admin.update_workout(user_list)
        elif fitur == "4":
            admin.delete_workout(user_list)
        elif fitur == "5":
            break
        else:
            print("Pilihan tidak valid.")

# Login Mode User Workout
def user_workout(admin, user_list):
    user = UserWorkout(admin.workouts)  # Menggunakan workout yang sudah dibuat admin
    user_list.append(user)  # Menambahkan user baru ke daftar user
    while True:
        print("\nMenu User Workout:")
        print("1. Lihat Progress")
        print("2. Tambah Workout ke Progress")
        print("3. Keluar")
        fitur = input("Pilih Fitur (1-3): ")
        if fitur == "1":
            user.view_progress()
        elif fitur == "2":
            user.add_workout()
        elif fitur == "3":
            break
        else:
            print("Pilihan tidak valid.")

# Menjalankan program
login()