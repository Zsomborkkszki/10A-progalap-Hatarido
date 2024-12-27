import hashlib

# Az adatok tárolására szolgáló fájl útvonala
USER_DATA_FILE = "users.py"

# Felhasználók betöltése a fájlból
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

# Jelszó hash-elése biztonságos tároláshoz
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Regisztrációs funkció
def register():
    users = load_users()

    print("\n--- Regisztráció ---")
    username = input("Felhasználónév (Ékezetek nélkül): ").strip()
    if username in users:
        print("A felhasználónév már létezik. Kérlek, próbálj meg egy másikat.")
        return

    email = input("E-mail: ").strip()
    if any(user["email"] == email for user in users.values()):
        print("Ez az e-mail cím már regisztrálva van. Kérlek, próbálj meg egy másikat.")
        return

    password = input("Jelszó: ").strip()
    confirm_password = input("Jelszó megerősítése: ").strip()

    if password != confirm_password:
        print("A jelszavak nem egyeznek. Kérlek, próbáld újra.")
        return

    # Felhasználó mentése
    users[username] = {
        "email": email,
        "password": password  # A jelszót egyszerű szövegként tároljuk az admin láthatóság miatt
    }
    save_users(users)
    print("Sikeres regisztráció!")

# Felhasználói menü bejelentkezés után
def user_menu(username):
    while True:
        print(f"\n--- Felhasználói menü ({username}) ---")
        print("1. Új létrehozása")
        print("2. Meglévő szerkesztése")
        print("3. Meglévő törlése")
        print("4. Kijelentkezés")
        #A többi feladat befejezetével ezek nem ki printelve lesznek
        choice = input("Válassz egy opciót: ").strip()
        if choice == "1":
            print("Új létrehozása folyamatban...")
            # Placeholder a tényleges funkcionalitáshoz
        elif choice == "2":
            print("Meglévő szerkesztése folyamatban...")
            # Placeholder a tényleges funkcionalitáshoz
        elif choice == "3":
            print("Meglévő törlése folyamatban...")
            # Placeholder a tényleges funkcionalitáshoz
        elif choice == "4":
            print("Kijelentkezés folyamatban...")
            break
        else:
            print("Érvénytelen választás. Kérlek, próbáld újra.")

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
    elif username in users and users[username]["password"] == password:
        print(f"Sikeres bejelentkezés! Üdvözöllek, {username}.")
        user_menu(username)
    else:
        print("Érvénytelen felhasználónév vagy jelszó.")

# Főmenü
def main():
    # Az admin felhasználó létezésének biztosítása
    users = load_users()
    if "Admin" not in users:
        users["Admin"] = {
            "email": "",
            "password": "Admin01"  # Az admin jelszó egyszerű szövegként tárolva
        }
        save_users(users)

    while True:
        print("\n--- Főmenü ---")
        print("1. Regisztráció")
        print("2. Bejelentkezés")
        print("3. Kilépés")

        choice = input("Válassz egy opciót: ").strip()
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Viszlát!")
            break
        else:
            print("Érvénytelen választás. Kérlek, próbáld újra.")

if __name__ == "__main__":
    main()