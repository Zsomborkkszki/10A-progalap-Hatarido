import os
import json

class OrarendApp:
    def __init__(self):
        self.file = "orarend.json"
        self.adatok = {nap: ["" for _ in range(24)] for nap in ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek", "Szombat", "Vasárnap"]}
        self.keszre = []
        self.adatok_betoltes()

    def adat_mentes(self):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump({"orarend": self.adatok, "keszre": self.keszre}, f, ensure_ascii=False, indent=4)

    def adatok_betoltes(self):
        if os.path.exists(self.file):
            with open(self.file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.adatok = data.get("orarend", self.adatok)
                self.keszre = data.get("keszre", [])

    def orarend_kiir(self):
        print("\nÓrarend:")
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

    def keszre_orarend_kiir(self):
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

    def fut(self):
        while True:
            self.orarend_kiir()
            print("\nMit szeretnél csinálni?")
            print("1. Új bejegyzés hozzáadása vagy módosítása")
            print("2. Bejegyzés törlése")
            print("3. Készre állított bejegyzések megtekintése")
            print("4. Bejegyzés készre állítása")
            print("5. Kilépés")
            valasz = input("Választás (1-5): ")

            if valasz == "1":
                nap = self.nap_beker()
                ora = self.ora_beker()
                bejegyzes = input("Mi legyen a bejegyzés?: ")
                self.uj_bejegyzes(nap, ora, bejegyzes)
            elif valasz == "2":
                nap = self.nap_beker()
                ora = self.ora_beker()
                self.torles(nap, ora)
            elif valasz == "3":
                self.keszre_orarend_kiir()
            elif valasz == "4":
                nap = self.nap_beker()
                ora = self.ora_beker()
                self.keszre_allitas(nap, ora)
            elif valasz == "5":
                print("Viszlát!")
                break
            else:
                print("Hibás választás, próbáld újra!")

if __name__ == "__main__":
    app = OrarendApp()
    app.fut()
