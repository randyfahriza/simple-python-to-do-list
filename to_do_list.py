import os
from colorama import init, Fore,Style
import json
import datetime

init(True)
 
clear = lambda:os.system("cls")
clear()
tanggal = datetime.datetime.now()
tanggal = tanggal.strftime("%Y-%m-%d")

class Halaman_home:
    def __init__(self):
        print(Style.BRIGHT+Fore.WHITE+"="*3+" Selamat Datang Di To-Do List "+"="*3)
        print(Style.BRIGHT+Fore.GREEN+"Daftar Menu : "
        "\n1. Membuat To-Do List Baru"
        "\n2. Melihat To-Do List (Coming Soon)"
        "\n3. Menghapus To-Do List"
        "\n4. Keluar")
        return self.input_menu()
    
    def input_menu(self):
        while True:
            pilihan = str(input("Masukkan Pilihan Nomor : "))
            if self.masuk_menu(pilihan):
                break

    def masuk_menu(self, pilihan):
        match pilihan:
            case "1":
                print("anda memmilih 1")
                self.buat_list()
                return True
            case "2":
                print("anda memmilih 2")
                self.menu_list()
                return True
            case "3":
                print("anda memmilih 3")
                self.hapus_list()
                return True
            case "4":
                print(Fore.YELLOW+"=== Anda Keluar ===")
                exit()
            
            case _:
                print(Fore.LIGHTRED_EX+"** Tolong Masukkan Pilihan **")
                return False

    def baca_json(self):
        with open("todo.json", "r") as i:
            self.data_json = json.load(i)

    def kembali_ke_menu(self, input_masuk):
        if str(input_masuk).lower().strip() == "!m":
            print(Fore.LIGHTWHITE_EX+"** Kembali Ke Halaman Utama **")
            return Halaman_home()

    def daftar_list(self):
        print(Style.BRIGHT+Fore.LIGHTCYAN_EX+"==== Daftar List ====")
        try:
            self.baca_json()
                
            if not self.data_json:
                print(Fore.LIGHTRED_EX+"** Tidak Ada List **")

            for nomer, key in enumerate(self.data_json, start=1):
                if isinstance(self.data_json[key], dict):
                    print(f"{nomer}. {key}")

        except FileNotFoundError:
            print(Fore.LIGHTRED_EX+"** Tidak Ada List **")
        print("="*21)

    def buat_list(self):
        clear()
        self.daftar_list()
        print(Style.BRIGHT+Fore.CYAN+"="*3+" Buat To-Do List "+"="*3)
        print(Style.DIM+Fore.LIGHTBLUE_EX+"Petunjuk : Masukkan Nama List Yang Ingin Di Buat")
        print(Style.DIM+Fore.LIGHTBLUE_EX+"Petunjuk : Ketik (!m) Untuk Kembali Ke Menu Utama")

        def list_baru():
            while True:
                try:
                    self.baca_json()
                    self.data_json[nama_list] = {}
                    with open("todo.json", "w") as i:
                        json.dump(self.data_json,i,indent=4)
                        break

                except FileNotFoundError:
                    with open("todo.json", "w") as i:
                        json.dump({},i,indent=4)
                        continue

        while True:
            nama_list = str(input("Masukkan Nama To-Do List : "))
            if not nama_list.strip():
                print(Fore.LIGHTRED_EX+"*** Masukkan nama ***")
                continue

            kata_terlarang = "!" # tambahkan jika ingin menambah karakter terlarang
            if any(kata in kata_terlarang for kata in nama_list):
                if self.kembali_ke_menu(nama_list):
                    break

                print(Fore.LIGHTRED_EX+"*** Input Mengandung Karakter"
                    +"\nYang Tidak Diperbolehkan ***")
                continue

            if self.kembali_ke_menu(nama_list):
                break
            
            yakin = str(input("Anda Yakin? (Y/n):"))
            if yakin.lower() in ["y", "iya", "ya"]:  
                list_baru()  
                print(Fore.LIGHTGREEN_EX+"** List Berasil Di Buat! **")
                print(Fore.LIGHTWHITE_EX+"** Kembali Ke Halaman Utama **")
                return Halaman_home()  
                
            else:
                continue
    
    def hapus_list(self):
        clear()
        
        def hapus_list_input():
            while True:
                try:
                    input_list = str(input("Masukkan Nama List : "))
                    if not input_list.strip():
                        print(Fore.LIGHTRED_EX+"*** Masukkan nama ***")
                        continue
        
                    if self.kembali_ke_menu(input_list):
                        break
                    
                    if input_list in self.data_json and isinstance(self.data_json[input_list], dict):

                        yakin = str(input("Anda Yakin? (Y/n):"))
                        if yakin.lower() in ["y", "iya", "ya"]:
                            clear()
                            self.data_json.pop(input_list, None)

                            with open("todo.json", "w") as i:
                                json.dump(self.data_json,i,indent=4)
                            print(Fore.LIGHTGREEN_EX+"** List Berasil Di Hapus! **")
                            return self.hapus_list()
                        else:
                            continue
                    
                    else:
                        print(Fore.LIGHTRED_EX+"** List Tidak Ada **")
                        print(Fore.LIGHTRED_EX+"** Atau Nama List Salah **")
                        continue

                except FileNotFoundError:
                    print(Fore.LIGHTRED_EX+"** Tidak Ada List **")
                    print(Fore.LIGHTRED_EX+"** Buat List Terlebih Dahulu **")
        
        self.daftar_list()

        print(Fore.LIGHTCYAN_EX+"=== Hapus List ===")
        print(Style.DIM+Fore.LIGHTBLUE_EX+"Petunjuk : Masukkan Nama List Yang Ingin Di Hapus")
        print(Style.DIM+Fore.LIGHTBLUE_EX+"Petunjuk : Ketik (!m) Untuk Kembali Ke Menu Utama")

        hapus_list_input()

    
    def menu_list(self):
        clear()
        def cek_file_json(): 
            try:
                self.baca_json()
            except FileNotFoundError:
                clear()
                print(Fore.LIGHTRED_EX+"** Buat List Terlebih Dahulu **")
                input("Masukkan apa saja untuk kembali ke menu")
                Halaman_home()
                return None

        def input_masuk_list():
            while True:
                input_list = str(input("Masukkan Perintah : "))
                if not input_list:
                    print(Fore.LIGHTRED_EX+"*** Masukkan nama list ***")
                    continue

                if self.kembali_ke_menu(input_list):
                    break
                
                hasil = masuk_list(input_list)
                if hasil:
                    return hasil
                    

        def masuk_list(nama_list):
            bagian = str(nama_list).strip().split(maxsplit=1)
            perintah = bagian[0]
            argumen = bagian[1] if len(bagian) > 1 else ""

            if not argumen:
                print(Fore.LIGHTRED_EX+"*** Masukkan perintah dengan benar ***")
                return input_masuk_list()   

            if perintah.lower() == "!ls":
                if argumen in self.data_json and isinstance(self.data_json[argumen], dict):
                    halaman = Halaman_list(argumen)
                    halaman.input_perintah()
                    return halaman
                
                else:
                    print(Fore.LIGHTRED_EX+"** List Tidak Ada **")
                    print(Fore.LIGHTRED_EX+"** Atau Nama List Salah **")
                    return input_masuk_list()
        
        cek_file_json()
        self.daftar_list()
        print(Style.BRIGHT+Fore.LIGHTCYAN_EX+"==== Masuk List ====")

        print(Style.DIM+Fore.LIGHTBLUE_EX+"Petunjuk : Ketik (!ls) Dan Masukkan Nama List Yang Ingin Di Masuki")
        print(Style.DIM+Fore.LIGHTBLUE_EX+"Petunjuk : Ketik (!m) Untuk Kembali Ke Menu Utama")

        return input_masuk_list()
        
class Halaman_list(Halaman_home):
    def __init__(self, nama_list):
        clear()
        self.nama_list = nama_list

    def daftar_menu(self):
        print(Style.BRIGHT+Fore.WHITE+"="*3+f" Selamat Datang Di {Fore.LIGHTCYAN_EX+self.nama_list+Fore.WHITE} "+"="*3)
        print(Style.BRIGHT+Fore.GREEN+"Daftar Perintah : "
        "\nKetik (!b) Untuk Membuat Kegiatan Baru"
        "\nKetik (!h) Untuk Menghapus Kegiatan"
        "\nKetik (!l) Untuk Melihat Kegiatan"
        "\nKetik (!k) Untuk Kembali")
        print(Style.DIM+Fore.LIGHTBLUE_EX+"Petunjuk : Masukkan Perintah Yang Ada Di Atas")
        
    def input_perintah(self):
        self.daftar_menu()
        while True:
            pilihan = str(input("Masukkan Perintah : "))
            if not pilihan.strip():
                print(Fore.LIGHTRED_EX+"*** Masukkan perintah ***")
                continue

            if str(pilihan).lower().strip() == "!k":
                self.menu_list()
                return None

            if self.masuk_perintah(pilihan):
                break

    def masuk_perintah(self, perintah):
        
        match str(perintah).strip().lower():
            case "!b":
                self.buat_kegiatan()
                return True

            case "!h":
                print("cihuy")

            case "!l":
                print("tsst[test case / test masuk method]")
                self.lihat_list()
                return True
            
            case _:
                print(Fore.LIGHTRED_EX+"*** Masukkan perintah ***")
                return False

    def kembali(self, input_perintah):
        if str(input_perintah).lower().strip() == "!k":
            self.input_perintah()
            return False
        else:
            return True
    
    def lihat_list(self):
        self.baca_json()
        
            
        def daftar_kegiatan():
            for nomer, (key, value) in enumerate(self.data_json[self.nama_list].items(), start=1):
                checkbox = "[x]" if value["status"] else "[ ]"
                print(f"{nomer}. {checkbox} {key}")
        
        def edit_kegiatan():
            def clear_cache():
                clear()
                isi_kegiatan()

            def kembali_ke_sebelum(input_perintah, nomer_kembali):
                if nomer_kembali == 1:
                    if str(input_perintah).lower().strip() == "!k":
                        self.lihat_list()
                        return True
                    else:
                        return False
                if nomer_kembali == 2:
                    if str(input_perintah).lower().strip() == "!k":
                        clear()
                        isi_kegiatan()
                        print(Style.NORMAL+Fore.LIGHTGREEN_EX+"Petunjuk : Masukkan Bagian Mana Yang Ingin Diedit"
                        "\nContoh : \"edit bagian : nama kegiatan\""
                        "\nKetik (!k) Untuk Kembali")
                        return True
                    else:
                        return False
                
            def konfirmasi():
                yakin = str(input("Anda Yakin? (Y/n):"))
                if yakin.lower() in ["y", "iya", "ya"]:
                    print(Fore.LIGHTGREEN_EX+"** Berhasil Mengedit **")
                    return True
                else:
                    print(Fore.LIGHTRED_EX+"*** Gagal Mengedit ***")
                    return False
            def isi_kegiatan():
                status = Fore.LIGHTGREEN_EX+"Selesai" if value["status"] else Fore.LIGHTRED_EX+"Belum Selesai"
                print(Fore.LIGHTBLUE_EX + "="*40)
                print(Fore.LIGHTYELLOW_EX+f"Nama Kegiatan : {key}")
                print(Fore.LIGHTCYAN_EX+f"Catatan : {value["catatan"]}")
                print(f"Status : {status}")
                print(Fore.LIGHTMAGENTA_EX+f"Tanggal Dibuat : {value["tanggal dibuat"]}")
                print(Fore.LIGHTBLUE_EX + "="*40)
                
            if self.argumen > len(self.data_json[self.nama_list]):
                print(Fore.LIGHTRED_EX+"*** Nomor Tidak Ada ***")
                return False
            clear()
            for nomer, (key, value) in enumerate(self.data_json[self.nama_list].items(), start=1):
                if self.argumen == nomer:
                    isi_kegiatan()
                    print(Style.NORMAL+Fore.LIGHTGREEN_EX+"Petunjuk : Masukkan Bagian Mana Yang Ingin Diedit"
                    "\nContoh : \"edit bagian : nama kegiatan\""
                    "\nKetik (!k) Untuk Kembali")

                    while True:
                        edit = input(Style.DIM+Fore.WHITE+"Edit Bagian : ")
                        if kembali_ke_sebelum(edit, 1):
                            break

                        header_edit = lambda edit_bagian = str:print(Fore.LIGHTBLUE_EX+"="*10+f" Edit {edit_bagian.capitalize()} "+"="*10)
                        match edit.strip().lower():
                            case "nama kegiatan":
                                clear_cache()
                                header_edit("nama kegiatan")
                                print(Style.NORMAL+Fore.LIGHTGREEN_EX+"Petunjuk : Masukkan Nama Kegiatan Yang Ingin Diganti")
                                edit_nama = str(input("Masukkan Nama Baru : ")).strip()
                                if kembali_ke_sebelum(edit_nama, 2):
                                    continue
                                if not edit_nama:
                                    print(Fore.LIGHTRED_EX+"*** Masukkan Input ***")
                                    continue
                                if konfirmasi():
                                    self.data_json[self.nama_list][edit_nama] = self.data_json[self.nama_list].pop(key)
                                    return True
                                else:
                                    continue
                            case "catatan":
                                clear_cache()
                                header_edit("catatan")
                                print(Style.NORMAL+Fore.LIGHTGREEN_EX+"Petunjuk : Masukkan Nama Catatan Yang Ingin Diganti")
                                edit_catatan = str(input("Masukkan Catatan Baru : ")).strip()
                                if kembali_ke_sebelum(edit_catatan, 2):
                                    continue
                                if not edit_catatan:
                                    print(Fore.LIGHTRED_EX+"*** Masukkan Input ***")
                                    continue

                                if konfirmasi():
                                    self.data_json[self.nama_list][key]["catatan"] = edit_catatan
                                    return True
                                else:
                                    continue
                            case "status":
                                clear_cache()
                                header_edit("status")
                                print(Style.NORMAL+Fore.LIGHTGREEN_EX+"Petunjuk : Masukkan Status Yang Ingin Diganti" \
                                "\nPetunjuk : Hanya Menerima [true / selesai dan false / belum selesai]")
                                edit_status = str(input("Masukkan Status Baru : ")).strip().lower()
                                if kembali_ke_sebelum(edit_status, 2):
                                    continue
                                if not edit_status:
                                    print(Fore.LIGHTRED_EX+"*** Masukkan Input ***")
                                    continue

                                if edit_status in ["true", "selesai", "sudah"]:
                                    self.data_json[self.nama_list][key]["status"] = True
                                elif edit_status in ["false", "belum selesai", "belum"]:
                                    self.data_json[self.nama_list][key]["status"] = False
                                else:
                                    print(Fore.LIGHTRED_EX+"*** Masukkan Status Dengan Benar! ***")
                                    continue
                                if konfirmasi():
                                    return True
                                else:
                                    continue
                            case "tanggal dibuat":
                                clear_cache()
                                header_edit("tanggal dibuat")
                                print(Style.NORMAL+Fore.LIGHTGREEN_EX+"Petunjuk : Masukkan Tanggal Dibuat Baru (YYYY-MM-DD)")
                                print(Style.DIM+Fore.LIGHTYELLOW_EX+"Peringatan : Mengubah Tanggal Dibuat Akan Mempengaruhi Histori.")
                                edit_tanggal = str(input("Masukkan Status Baru : ")).strip().lower()

                                if kembali_ke_sebelum(edit_tanggal, 2):
                                    continue
                                if not edit_tanggal:
                                    print(Fore.LIGHTRED_EX+"*** Masukkan Input ***")
                                    continue
                                    
                                edit_tanggal = edit_tanggal.split("-", maxsplit=3)
                                print(edit_tanggal)
                                print(len(edit_tanggal))
                                break

        def informasi_kegiatan():
            if self.argumen > len(self.data_json[self.nama_list]):
                print(Fore.LIGHTRED_EX+"*** Nomor Tidak Ada ***")
                return False
            clear()
            for nomer, (key, value) in enumerate(self.data_json[self.nama_list].items(), start=1):
                if self.argumen == nomer:
                    status = Fore.LIGHTGREEN_EX+"Selesai" if value["status"] else Fore.LIGHTRED_EX+"Belum Selesai"
                    print(Fore.LIGHTBLUE_EX + "="*40)
                    print(Fore.LIGHTYELLOW_EX+f"Nama Kegiatan : {key}")
                    print(Fore.LIGHTCYAN_EX+f"Catatan : {value["catatan"]}")
                    print(f"Status : {status}")
                    print(Fore.LIGHTMAGENTA_EX+f"Tanggal Dibuat : {value["tanggal dibuat"]}")
                    print(Fore.LIGHTBLUE_EX + "="*40)
                    input(Style.DIM+Fore.WHITE+"Enter Untuk Kembali : ")
                    self.lihat_list()
                    return True

        def check_list():
            if self.argumen > len(self.data_json[self.nama_list]):
                print(Fore.LIGHTRED_EX+"*** Nomor Tidak Ada ***")
                return False
            for nomer, key in enumerate(self.data_json[self.nama_list].keys(), start=1):
                if int(self.argumen) == nomer:
                    status = True if not self.data_json[self.nama_list][key]["status"] else False
                    self.data_json[self.nama_list][key]["status"] = status
                    with open("todo.json", "w") as i:
                        json.dump(self.data_json,i,indent=4)
                    self.lihat_list()
                    return True

        def pemilah_perintah(input_perintah):
            bagian = str(input_perintah).strip().split(maxsplit=1)
            perintah = bagian[0]
            argumen= bagian[1] if len(bagian) > 1 else ""
            try:
                self.argumen = int(argumen)
            except ValueError:
                print(Fore.LIGHTRED_EX+"*** Masukkan Angka Saja! ***")
                return False

            match perintah.lower():
                case "!c":
                    if check_list():
                        return True
                    else:
                        return False
                case "!i":
                    if informasi_kegiatan():
                        return True
                    else:
                        return False
                case "!e":
                    if edit_kegiatan():
                        with open("todo.json", "w") as i:
                            json.dump(self.data_json,i,indent=4)
                        self.lihat_list()
                        return True
                    else:
                        return False
                case _:
                    print(Fore.LIGHTRED_EX+"*** Perintah Tidak Ada! ***")
                    return False

        print(Style.BRIGHT+Fore.LIGHTCYAN_EX+"=== List Kegiatan ===")
        print(Style.DIM+Fore.LIGHTBLUE_EX+
            "Ketik (!i) Untuk Melihat Informasi Kegiatan"
            "\nKetik (!c) Untuk Centang / Menghapus Centang"
            "\nKetik (!e) Untuk Mengedit Kegiatan (Coming Soon)"
            "\nKetik (!k) Untuk Kembali")
        print(Style.NORMAL+Fore.LIGHTGREEN_EX+"Petunjuk : Ketik Perintah Dengan Nomor Kegiatannya")
        print("="*30)

        daftar_kegiatan()

        while True:
            perintah = str(input("Masukkan Perintah : "))
            if not perintah.strip():
                print(Fore.LIGHTRED_EX+"*** Masukkan Perintah! ***")
                continue

            if not self.kembali(perintah):
                break
            
            if pemilah_perintah(perintah):
                break

    def buat_kegiatan(self):

        def kegiatan_json():
            self.baca_json()

            for todo in self.data_json[self.nama_list]:
                if kegiatan in todo:
                    print(Fore.LIGHTRED_EX+"** Nama Kegiatan Tidak Boleh Sama! **")
                    print(Fore.LIGHTRED_EX+f"** Nama Kegiatan Yang Sama : {Fore.LIGHTCYAN_EX+todo+Fore.LIGHTRED_EX} **")
                    return False

            catatan = str(input("Masukkan Catatan Tambahan (Opsional) : "))

            yakin = str(input("Anda Yakin? (Y/n):"))
            if yakin.lower() in ["y", "iya", "ya"]:
                self.data_json[self.nama_list][kegiatan] = {"catatan" : catatan, "status" : False, "tanggal dibuat" : tanggal}
                # urutan pada list = [cttn tmbhan, status:bool, tgl dibuat]

                with open("todo.json", "w") as i:
                    json.dump(self.data_json,i,indent=4)

                print(Fore.LIGHTGREEN_EX+"** Berhasil Membuat Kegiatan **")
                return True
            else:
                print(Fore.LIGHTRED_EX+"** Gagal Membuat Kegiatan **")
                return False
        clear()
        print(Style.BRIGHT+Fore.LIGHTCYAN_EX+"=== Buat Kegiatan ===")
        print(Style.DIM+Fore.LIGHTBLUE_EX+"Petunjuk : Masukkan Nama Kegiatan Yang Ingin Dibuat")
        print(Style.DIM+Fore.LIGHTBLUE_EX+"Petunjuk : Ketik (!k) Untuk Kembali")

        while True:
            kegiatan = str(input("Masukkan Nama Kegiatan : "))
            if not kegiatan.strip():
                print(Fore.LIGHTRED_EX+"*** Masukkan nama kegiatan ***")
                continue
            if not self.kembali(kegiatan):
                break

            if not kegiatan_json():
                continue

if __name__ == "__main__":
    Halaman_home()
