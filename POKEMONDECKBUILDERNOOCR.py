from io import BytesIO
from PIL import Image
import requests
from pokemontcgsdk import Card
from pokemontcgsdk import Set
import json
import os
from tcgdexsdk import TCGdex, Language
tcgdex = TCGdex()
tcgdex = TCGdex("en")
FILE = r"C:\Users\culon\Coding Things\cards.json"

# LIMITLESS DECKLIST COPY AND PASTE

deck_text = """
Pokémon: 23
4 Dreepy TWM 128
4 Drakloak TWM 129
3 Dragapult ex TWM 130
2 Duskull PRE 35
2 Dusclops PRE 36
1 Dusknoir PRE 37
2 Budew PRE 4
1 Bloodmoon Ursaluna ex TWM 141
1 Fezandipiti ex SFA 38
1 Latias ex SSP 76
7 Munkidori TWM 95
1 Hawlucha SVI 118

Trainer: 30
4 Lillie's Determination MEG 119
4 Iono PAL 185
3 Boss's Orders MEG 114
2 Hilda WHT 84
1 Professor Turo's Scenario PAR 171
4 Buddy-Buddy Poffin TEF 144
4 Ultra Ball MEG 131
3 Counter Catcher PAR 160
4 Night Stretcher SFA 61
1 Nest Ball SVI 181
2 Jamming Tower TWM 153

Energy: 7
3 Luminous Energy PAL 191
2 Psychic Energy MEE 5
1 Fire Energy MEE 2
1 Neo Upper Energy TEF 162
"""


# LOAD AND SAVE######


def load_cards():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []


def save_cards(cards):
    with open(FILE, "w") as f:
        json.dump(cards, f, indent=4)

######################################

## INPUT CARDS####


def inputcards():
    cards = load_cards()
    while True:
        cardstr = input("Input Card Name (or 'quit'): ").strip()
        if cardstr.lower() == "quit":
            break

        cardset = input("Input Card Set: ").strip()

        cardnm = input("Input Card Number: ").strip()

        existing = next(
            (c for c in cards if c["CardName"].lower() == cardstr.lower()
             and c["CardSet"].lower() == cardset.lower()
             and c["CardNumber"] == int(cardnm)),
            None
        )

        if existing:
            existing["Amount"] += 1
            print(f"Incremented amount: {existing}")
        else:
            new_card = {
                "CardName": cardstr,
                "CardSet": cardset,
                "CardNumber": int(cardnm),
                "Amount": 1
            }
            cards.append(new_card)
            print("Saved:", new_card)

        # ✅ Save the full list, not a single card
        save_cards(cards)

##############################################

# RANDOM FUNCTIONS############################


def delete_cards_file():
    file_path = r"C:\Users\culon\Coding Things\cards.json"

    if os.path.exists(file_path):
        os.remove(file_path)
        print("Deleted:", file_path)
    else:
        print("File does not exist.")


def delete_card():
    cards = load_cards()
    name = input("Enter card name to delete or decrement: ").strip()
    matches = [c for c in cards if c["CardName"].lower() == name.lower()]

    if not matches:
        print("Card not found.")
        return

    for card in matches:
        print(f"Found: {card}")

    choice = input(
        "Delete completely or decrement amount? (delete/decrement): ").strip().lower()
    if choice == "delete":
        cards = [c for c in cards if c["CardName"].lower() != name.lower()]
        print(f"Deleted all copies of {name}.")
    elif choice == "decrement":
        for card in matches:
            if card["Amount"] > 1:
                card["Amount"] -= 1
                print(f"Decremented: {card}")
            else:
                cards.remove(card)
                print(f"Removed {card} completely as Amount was 1.")
    else:
        print("Invalid choice.")

    save_cards(cards)

###############################

# STORAGE#########################


def storageDecisionTree():
    storageChoice = input(
        "what kind of storage? (1. Names of cards , 2. Names and sets, 3. Everythang, 4. Look for set or card, 5. back): ")
    cards = load_cards()
    if storageChoice == "1":
        print([c["CardName"] for c in cards])
        storageDecisionTree()
    elif storageChoice == "2":
        print(
            list(map(lambda x: {"CardName": x['CardName'], "CardSet": x['CardSet']}, cards)))
        storageDecisionTree()
    elif storageChoice == "3":
        print(cards)
        storageDecisionTree()
    elif storageChoice == "4":
        x = input(
            "Are you looking for all cards in a set? or the amount of single card? (1 or 2): ")
        if x == "1":
            y = input("What set?:")
            if y.upper() in list(map(lambda x: x["CardSet"], cards)):
                print(list(filter(lambda x: x["CardSet"] == y.upper(), cards)))
            else:
                print("Set is currently not in the system please try again later!")
        elif x == "2":
            y = input("What Pokemon?: ")
            if y.lower() in list(map(lambda x: x["CardName"].lower(), cards)):
                filteredCards = list(
                    filter(lambda x: x["CardName"].lower() == y.lower(), cards))
                if not filteredCards:
                    x = input("Card is not in the system. Input it? Y/N")
                    if x.upper() == "Y":
                        inputcards()
                    else:
                        quequiereshacer()
                print("Cards found:")
                for c in filteredCards:
                    print(
                        f"- {c['CardName']} {c['CardSet']} {c['CardNumber']} (Amount: {c['Amount']})")

                y2 = input("Would you like to view that card? Y/N: ")
                if y2.upper() == "Y":
                    if len(filteredCards) == 1:
                        selected_card = filteredCards[0]
                        openurl(selected_card)
                    elif len(filteredCards) > 1:
                        print(
                            "You have multiple cards with the same name, which copy?")
                        for i, c in enumerate(filteredCards, start=1):
                            print(
                                f"{i}. {c['CardSet']} {c['CardNumber']} (Amount: {c['Amount']})")

                    choice = int(input("Which copy?: "))

                    if not (1 <= choice <= len(filteredCards)):
                        print("Invalid choice.")
                        quequiereshacer()
                    selected_card = filteredCards[choice - 1]
                    openurl(selected_card)
                else:
                    quequiereshacer()

            else:
                x = input(
                    "Card is currently not in the system. Would you like to input it? Y/N: ")
                if x.upper() == "Y":
                    inputcards()
                else:
                    quequiereshacer()
    elif storageChoice == "5":
        quequiereshacer()


###################

# MAIN MENU

def quequiereshacer():
    while True:
        choice = input(
            "What do you wanna do? (inputcards(1), delete storage(2), open storage(3), next page(4), or quit(5)): ")
        if choice == "1":
            inputcards()
        elif choice == "2":
            x = input("The whole file or one card? 1 or 2: ")
            if x == "1":
                delete_cards_file()
            elif x == "2":
                delete_card()
        elif choice == "3":
            storageDecisionTree()
        elif choice == "4":
            choice1 = input(
                "What do you wanna do? (add your deck to storage? (1),check if decklist can be made through storage(2), (back(3), or quit(5)): ")
            if choice1 == "1":
                addDeckToStorage()
            elif choice1 == "2":
                enoughcardsinstoragefordeck(deck_text)
            elif choice1 == "3":
                continue
            elif choice1 == "5":
                break
        elif choice == "5":
            break
        else:
            return


######################################


def parse_deck(deck_text):
    deck = {"Pokémon": [], "Trainer": [], "Energy": []}
    current_section = None

    for line in deck_text.splitlines():
        line = line.strip()
        if not line:
            continue

        # Detect section headers
        if line.startswith("Pokémon:"):
            current_section = "Pokémon"
            continue
        elif line.startswith("Trainer:"):
            current_section = "Trainer"
            continue
        elif line.startswith("Energy:"):
            current_section = "Energy"
            continue

        # Parse card line
        parts = line.split()
        amount = int(parts[0])
        card_number = int(parts[-1])
        card_set = parts[-2]
        card_name = " ".join(parts[1:-2])

        card_entry = {
            "CardName": card_name,
            "CardSet": card_set,
            "CardNumber": card_number,
            "Amount": amount
        }

        deck[current_section].append(card_entry)

    return deck


parsed_deck = parse_deck(deck_text)


def addDeckToStorage():
    deck = parse_deck(deck_text)
    cards = load_cards()
    deckcards = deck["Pokémon"] + deck["Trainer"] + deck["Energy"]
    for card in deckcards:
        existing = next((c for c in cards
                         if c["CardName"].lower() == card["CardName"].lower()
                         and c["CardSet"].lower() == card["CardSet"].lower()
                         and c["CardNumber"] == card["CardNumber"]), None)
        if existing:
            existing["Amount"] += card["Amount"]
        else:
            cards.append(card)

    save_cards(cards)
    print(f"Added {len(cards)} cards from deck to storage.")


def enoughcardsinstoragefordeck(deck_text):
    deck = parse_deck(deck_text)
    cards = load_cards()

    # Build storage lookup: (name, set, number) → amount
    storage_lookup = {
        (c["CardName"].lower(), c["CardSet"].lower(), c["CardNumber"]): c["Amount"]
        for c in cards
    }

    # Group storage cards by name to show alternatives
    storage_by_name = {}
    for c in cards:
        name = c["CardName"].lower()
        storage_by_name.setdefault(name, []).append(c)

    deckcards = deck["Pokémon"] + deck["Trainer"] + deck["Energy"]

    missing = []
    insufficient = []

    for card in deckcards:
        key = (card["CardName"].lower(),
               card["CardSet"].lower(), card["CardNumber"])
        needed = card["Amount"]

        if key not in storage_lookup:
            missing.append(card)
        else:
            available = storage_lookup[key]
            if available < needed:
                insufficient.append({
                    "Card": card,
                    "Needed": needed,
                    "Available": available
                })

    # No problems
    if not missing and not insufficient:
        print("You have enough cards in storage for this deck.")
        return True

    print("You do NOT have enough cards to build this deck.\n")

    # --- MISSING CARDS ---
    if missing:
        print("Missing cards:")
        for c in missing:
            print(
                f"- {c['Amount']}x {c['CardName']} {c['CardSet']} {c['CardNumber']}")

            # Show alternative sets if available
            name = c["CardName"].lower()
            if name in storage_by_name:
                print("  Alternatives you DO own:")
                for alt in storage_by_name[name]:
                    print(
                        f"    - {alt['Amount']}x {alt['CardName']} {alt['CardSet']} {alt['CardNumber']}")
            else:
                print("  You own no copies of this card in any set.")

        print()

    # --- INSUFFICIENT COPIES ---
    if insufficient:
        print("Insufficient copies:")
        for item in insufficient:
            c = item["Card"]
            need = item["Needed"]
            have = item["Available"]

            print(
                f"- {c['CardName']} {c['CardSet']} {c['CardNumber']}: Need {need}, Have {have}")

            # Show alternative sets
            name = c["CardName"].lower()
            if name in storage_by_name:
                print("  Other sets you DO own:")
                for alt in storage_by_name[name]:
                    # Don't reprint the same set unless different number
                    if not (alt["CardSet"] == c["CardSet"] and alt["CardNumber"] == c["CardNumber"]):
                        print(
                            f"    - {alt['Amount']}x {alt['CardName']} {alt['CardSet']} {alt['CardNumber']}")
            else:
                print("  You own no other copies of this card in any set.")


def openurl(y):
    names = names = {
        "sv": {
            "SV1": "sv01", "PAL": "sv02", "OBF": "sv03", "MEW": "sv03.5",
            "SVP": "svp", "PAR": "sv04", "PAF": "sv04.5", "TEF": "sv05",
            "TWM": "sv06", "SFA": "sv06.5", "SCR": "sv07", "SSP": "sv08",
            "PRE": "sv08.5", "JTG": "sv09", "DRI": "sv10", "WHT": "sv10.5w",
            "BLK": "sv10.5b"
        },
        "me": {
            "MEG": "me01", "PFL": "me02"
        }
    }

    # url2 = "https://assets.tcgdex.net/en/sv/sv02/001/low.png"
    # url = "https://assets.tcgdex.net/en/me/me02/001/low.png"
    setCode = y["CardSet"]
    num = str(y["CardNumber"])
    if len(num) > 3:
        print("This aint a real card number")
        quequiereshacer()
    elif len(num) == 2:
        num = '0' + num
    elif len(num) == 1:
        num = '00' + num
    if setCode in names['sv']:
        family = 'sv'
        mapped = names['sv'][setCode]
    elif setCode in names['me']:
        family = 'me'
        mapped = names['me'][setCode]
    else:
        print("Set not recognized")
        quequiereshacer()

    url = f"https://assets.tcgdex.net/en/{family}/{mapped}/{num}/high.png"
    print("Fetching:", url)

    resp = requests.get(url)
    if resp.status_code != 200:
        print("Image not found.")
        return

    img = Image.open(BytesIO(resp.content))
    img.show()


quequiereshacer()
