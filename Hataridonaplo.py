import json
import os

# Az adatok tárolására szolgáló fájl útvonala
USER_DATA_FILE = "users.py"

def load_users():
    try:
        from users import user_data
        return user_data
    except ImportError:
        return {}

# Felhasználók mentése a fájlba
def save_users(users):
    with open(USER_DATA_FILE, "w") as file:
        file.write("user_data = ")
        file.write(repr(users))

# Regisztrációs funkció
def register():
    users = load_users()

    print("\n--- Regisztráció ---")
    username = input("Felhasználónév(Ékezetek nélkül): ").strip()
    if username in users:
        print("A felhasználónév már létezik. Kérlek, próbálj meg egy másikat.")
        return

    email = input("E-mail: ").strip()
    if any(user["email"] == email for user in users.values()):
        print("Ez az e-mail cím már regisztrálva van. Kérlek, próbálj meg egy másikat.")
        return
    elif "@" not in email:
        print("Helytelen e-mail-t adtál meg!")
        return

    password = input("Jelszó: ").strip()
    confirm_password = input("Jelszó megerősítése: ").strip()

    if password != confirm_password:
        print("A jelszavak nem egyeznek. Kérlek, próbáld újra.")
        return

    # Felhasználó mentése
    users[username] = {
        "email": email,
        "password": password 
    }
    save_users(users)
    print("Sikeres regisztráció!")
abc = []
# Felhasználói menü bejelentkezés után
class HataridonaploApp:
    def __init__(self, username):
        self.username = username
        self.file = f"hataridonaplo_{username}.json"
        self.adatok = {nap: ["" for _ in range(24)] for nap in ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek", "Szombat", "Vasárnap"]}
        self.keszre = []
        self.adatok_betoltes()

    def adat_mentes(self):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump({"hataridonaplo": self.adatok, "keszre": self.keszre}, f, ensure_ascii=False, indent=4)

    def adatok_betoltes(self):
        if os.path.exists(self.file):
            with open(self.file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.adatok = data.get("hataridonaplo", self.adatok)
                self.keszre = data.get("keszre", [])

    def hataridonaplo_kiir(self):
        print("\nHatáridőnapló:")
        napok = ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek", "Szombat", "Vasárnap"]
        print(f"{'':<8}" + " ".join(f"{nap:<10}" for nap in napok))
        for ora in range(24):
            sor = f"{ora:02d}:00  "
            for nap in napok:
                bejegyzes = self.adatok[nap][ora]
                sor += f"{bejegyzes:<12}"
            print(sor)

    def keszre_allitas(self, nap, ora):
        if nap in self.adatok and 0 <= ora < 24:
            bejegyzes = self.adatok[nap][ora]
            if bejegyzes != "":
                self.keszre.append((nap, ora, bejegyzes))
                self.adatok[nap][ora] = ""
                self.adat_mentes()
                print(f"Bejegyzés készre állítva: {nap}, {ora}:00 - {bejegyzes}")
            else:
                print("Nincs bejegyzés az adott időpontban!")
        else:
            print("Hiba: nincs ilyen nap vagy idő.")

    def keszre_hataridonaplo_kiir(self):
        print("\nKészre állított bejegyzések:")
        napok = ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek", "Szombat", "Vasárnap"]
        print(f"{'':<8}" + " ".join(f"{nap:<12}" for nap in napok))
        for nap, ora, bejegyzes in self.keszre:
            sor = f"{ora:02d}:00  "
            for napok_iter in napok:
                if nap == napok_iter:
                    sor += f"{bejegyzes:<12}"
                else:
                    sor += f"{'':<12}"
            print(sor)

    def uj_bejegyzes(self, nap, ora, bejegyzes):
        if nap in self.adatok and 0 <= ora < 24:
            self.adatok[nap][ora] = bejegyzes
            self.adat_mentes()
            print(f"Bejegyzés mentve: {nap}, {ora}:00 - {bejegyzes}")
        else:
            print("Hiba: nincs ilyen nap vagy idő.")

    def torles(self, nap, ora):
        if nap in self.adatok and 0 <= ora < 24:
            self.adatok[nap][ora] = ""
            self.adat_mentes()
            print(f"Bejegyzés törölve: {nap}, {ora}:00")
        else:
            print("Hiba: nincs ilyen nap vagy idő.")

    def nap_beker(self):
        napok = ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek", "Szombat", "Vasárnap"]
        while True:
            nap = input("Melyik nap? (Hétfő, Kedd, stb.): ").capitalize()
            if nap in napok:
                return nap
            print("Hibás nap, próbáld újra!")

    def ora_beker(self):
        while True:
            try:
                ora = int(input("Óra (0-23): "))
                if 0 <= ora < 24:
                    return ora
                print("Hibás óra. Csak 0-23 között!")
            except ValueError:
                print("Hibás adat. Kérlek, számot adj meg!")
    
    def bejegyzesek_listazasa(self, szuro):
        print("\nBejegyzesek listázása:")
        if szuro == "elvegzendo":
            print("Elvégzendő feladatok:")
            for nap, orak in self.adatok.items():
                for ora, bejegyzes in enumerate(orak):
                    if bejegyzes:
                        print(f"{nap}, {ora}:00 - {bejegyzes}")
       
        elif szuro == "abcsorrend":
            print("A hátralévő bejegyzések ABC sorrend szerinti kiírása:")
            abc = []
            for nap, orak in self.adatok.items():
                for ora, bejegyzes in enumerate(orak):
                    if bejegyzes:
                        abc.append((bejegyzes, nap, ora))
            abc.sort(key=lambda x: x[0])

        # Kiírás rendezett sorrendben
            for bejegyzes, nap, ora in abc:
                print(f"{bejegyzes} - {nap}, {ora}:00")
        else:
            print("Ismeretlen szűrő!")

    def fut(self):
        while True:
            self.hataridonaplo_kiir()
            print("\nMit szeretnél csinálni?")
            print("1. Új bejegyzés hozzáadása vagy módosítása")
            print("2. Bejegyzés törlése")
            print("3. Készre állított bejegyzések megtekintése")
            print("4. Bejegyzés készre állítása")
            print("5. Bejegyzések listázása")
            print("6. Kilépés")
            valasz = input("Választás (1-6): ")

            if valasz == "1":
                nap = self.nap_beker()
                ora = self.ora_beker()
                bejegyzes = input("Mi legyen a bejegyzes?: ")
                self.uj_bejegyzes(nap, ora, bejegyzes)
            elif valasz == "2":
                nap = self.nap_beker()
                ora = self.ora_beker()
                self.torles(nap, ora)
            elif valasz == "3":
                self.keszre_hataridonaplo_kiir()
            elif valasz == "4":
                nap = self.nap_beker()
                ora = self.ora_beker()
                self.keszre_allitas(nap, ora)
            elif valasz == "5":
                print("\nVálassz egy szűrőt:")
                print("1. Elvégzendő feladatok")
                print("2. A hátralévő bejegyzések ABC sorrend szerinti kiírása: ")
                szuro_valasz = input("Választás (1-2): ")
                if szuro_valasz == "1":
                    self.bejegyzesek_listazasa("elvegzendo")
                elif szuro_valasz == "2":
                    self.bejegyzesek_listazasa("abcsorrend")
                else:
                    print("Hibás választás!")
            elif valasz == "6":
                print("Viszlát!")
                break
            else:
                print("Hibás választás, próbáld újra!")

object = HataridonaploApp(username=True)
# Bejelentkezési funkció
def login():
    users = load_users()

    print("\n--- Bejelentkezés ---")
    username = input("Felhasználónév: ").strip()
    password = input("Jelszó: ").strip()

    if username == "Admin" and password == "Admin01":
        print("Sikeres bejelentkezés! Üdvözöllek, Admin.")
        print("\n--- Összes felhasználó ---")
        for user, details in users.items():
            print(f"Felhasználónév: {user}, E-mail: {details['email']}, Jelszó: {details['password']}")
        return None  # Az admin nem használja a határidőnaplót
    elif username in users and users[username]["password"] == password:
        print(f"Sikeres bejelentkezés! Üdvözöllek, {username}.")
        return username
    else:
        print("Érvénytelen felhasználónév vagy jelszó.")
        return None

# Alap menü
def main():
    while True:
        print("\n--- Főmenü ---")
        print("1. Regisztráció")
        print("2. Bejelentkezés")
        print("3. Kilépés")
        valasz = input("Választás (1-3): ")

        if valasz == "1":
            register()
        elif valasz == "2":
            username = login()
            if username:  # Csak akkor folytatjuk, ha nem admin és sikeres a bejelentkezés
                app = HataridonaploApp(username)
                app.fut()
        elif valasz == "3":
            print("Kilépés...")
            break
        else:
            print("Hibás választás, próbáld újra!")

if __name__ == "__main__":
    main()
