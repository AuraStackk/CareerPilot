import json
import webbrowser
import os

FILE = "reels.json"

# load saved data
if os.path.exists(FILE):
    with open(FILE, "r") as f:
        reels = json.load(f)
else:
    reels = []

while True:
    print("\n--- Reel Saver ---")
    print("1. Add Reel")
    print("2. View Reels")
    print("3. Open Reel")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        link = input("Enter reel link: ")
        reels.append(link)
        with open(FILE, "w") as f:
            json.dump(reels, f)
        print("Saved!")

    elif choice == "2":
        for i, r in enumerate(reels):
            print(f"{i+1}. {r}")

    elif choice == "3":
        num = int(input("Enter reel number: "))
        webbrowser.open(reels[num-1])

    elif choice == "4":
        break
