from io import BytesIO
from PIL import Image
import requests
import json
import os
from pathlib import Path

# LIMITLESS DECKLIST COPY AND PASTE

deckText = """
Pokémon: 15
4 Gimmighoul SSP 97
4 Gholdengo ex PAR 139
2 Solrock MEG 75
2 Lunatone MEG 74
1 Genesect ex BLK 67
1 Fezandipiti ex SFA 38
1 Munkidori TWM 95

Trainer: 34
4 Arven OBF 186
3 Boss's Orders MEG 114
2 Professor Turo's Scenario PAR 171
1 Lana's Aid TWM 155
4 Superior Energy Retrieval PAL 189
4 Nest Ball SVI 181
4 Fighting Gong MEG 116
3 Earthen Vessel PAR 163
1 Super Rod PAL 188
1 Buddy-Buddy Poffin TEF 144
1 Premium Power Pro MEG 124
1 Prime Catcher TEF 157
2 Air Balloon BLK 79
1 Vitality Band SVI 197
2 Artazon PAL 171

Energy: 11
7 Fighting Energy MEE 6
3 Metal Energy MEE 8
1 Darkness Energy MEE 7
"""


# LOAD AND SAVE######


storageDir = Path.home() / "PokemonStorage"
storageDir.mkdir(exist_ok=True)

jsonFile = storageDir / "cards.json"


def saveCards(cards):
    with open(jsonFile, "w") as f:
        json.dump(cards, f, indent=4)


def loadCards():
    if jsonFile.exists():
        with open(jsonFile, "r") as f:
            return json.load(f)
    return {"Main Storage": [], "Deck Lists": []}

######################################

## INPUT CARDS####


def inputcards(StorageOption):
    cards = loadCards()
    while True:
        cardstr = input("Input Card Name (or 'quit'): ").strip()
        if cardstr.lower() == "quit":
            break
        cardset = input("Input Card Set: ").strip().upper()
        if len(cardset) != 3:
            print("This is not the right cardset")
            print("Redirecting to home page...")
            quequiereshacer()
        cardnm = input("Input Card Number: ").strip()
        try:
            int(cardnm)
        except Exception as e:
            print("This is not the right card number")
            print("Redirecting to home page...")
            quequiereshacer()

        existing = next(
            (c for c in cards[StorageOption] if c["CardName"].lower() == cardstr.lower()
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
            cards[StorageOption].append(new_card)
            print("Saved:", new_card)

        saveCards(cards)

##############################################

# RANDOM FUNCTIONS############################


def delete_cards_file():

    if os.path.exists(jsonFile):
        os.remove(jsonFile)
        print("Deleted:", jsonFile)
    else:
        print("File does not exist.")


def deleteStorageKey(choice2):
    cards = loadCards()
    if choice2 == "Main Storage" or choice2 == "Deck Lists":
        cards[choice2] = []
        saveCards(cards)
    else:
        cards.pop(choice2)
        saveCards(cards)


def delete_card(storageChoice):
    loaded = loadCards()                 # full dict
    cards = loaded[storageChoice]         # reference to target storage list

    name = input("Enter card name to delete or decrement: ").strip()
    matches = [c for c in cards if c["CardName"].lower() == name.lower()]

    if not matches:
        print("Card not found.")
        return

    for card in matches:
        print(f"Found: {card}")

    choice = input(
        "Delete completely or decrement amount? (delete/decrement): "
    ).strip().lower()

    if choice == "delete":
        # Remove matching cards
        loaded[storageChoice] = [
            c for c in cards if c["CardName"].lower() != name.lower()
        ]
        print(f"Deleted all copies of {name}.")

    elif choice == "decrement":
        new_cards = []
        for c in cards:
            if c["CardName"].lower() == name.lower():
                if c["Amount"] > 1:
                    c["Amount"] -= 1
                    new_cards.append(c)
                    print(f"Decremented: {c}")
                else:
                    print(f"Removed {c} completely as Amount was 1.")
            else:
                new_cards.append(c)
        loaded[storageChoice] = new_cards

    else:
        print("Invalid choice.")
        return

    # SAVE FULL STRUCTURE
    saveCards(loaded)

###############################

# STORAGE#########################


def storageDecisionTree(storageChoice):
    loaded = loadCards()
    cards = loaded[storageChoice]
    while True:
        storageChoice = input(
            "what kind of storage? Everythang (1), Look for set or card (2), back (5): ")
        if storageChoice == "1":
            for c in cards:
                print(str(c["Amount"]) + ' ' + c["CardName"] + ' ' +
                      c["CardSet"] + ' ' + str(c["CardNumber"]))
            continue
        elif storageChoice == "2":
            x = input(
                "Are you looking for all cards in a set? (1) or a single card? (2) or back (4) or quit(5): ")
            if x == "1":
                y = input("What set?:")
                if y.upper() in list(map(lambda x: x["CardSet"], cards)):
                    filtered = (
                        list(filter(lambda x: x["CardSet"] == y.upper(), cards)))
                    for c in filtered:
                        print(str(c["Amount"]) + ' ' + c["CardName"] + ' ' +
                              c["CardSet"] + ' ' + str(c["CardNumber"]))
                else:
                    print("Set is currently not in the system please try again later!")
            elif x == "2":
                y = input("What Card?: ")
                if y.lower() in list(map(lambda x: x["CardName"].lower(), cards)):
                    filteredCards = list(
                        filter(lambda x: x["CardName"].lower() == y.lower(), cards))
                    if not filteredCards:
                        x = input("Card is not in the system. Input it? (Y/N)")
                        if x.upper() == "Y":
                            inputcards("Main Storage")
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
                        "Card is currently not in the system. Would you like to input it? (Y/N): ")
                    if x.upper() == "Y":
                        inputcards("Main Storage")
                    else:
                        quequiereshacer()
            elif x == "4":
                continue
            elif x == "5":
                return
            else:
                quequiereshacer()
        elif storageChoice == "5":
            quequiereshacer()


###################

# MAIN MENU

def pickYourStorage(cards):
    while True:
        index = 1
        for i, key in enumerate(cards, start=1):
            print(f"{i}. " + key)
            index += 1
        print(f"{index}. New")
        keychoice = input("Which Storage?: ")
        try:
            int(keychoice)
        except Exception:
            return quequiereshacer()
        keymapped = list(map(lambda x: x, cards))
        try:
            choice2 = keymapped[int(keychoice) - 1]
            if choice2 == "Deck Lists":
                saveCards(cards)
                return choice2
            else:
                choice2 = keymapped[int(keychoice) - 1]
                saveCards(cards)
                return choice2
        except IndexError:
            choice3 = input("Name your storage: ")
            cards[choice3] = []
            saveCards(cards)


def quequiereshacer():
    cards = loadCards()
    choice2 = pickYourStorage(cards)
    while True:
        choice = input(
            "What do you wanna do? inputcards (1), delete storage (2), open storage (3), next page (4), or quit (5): ")
        if choice == "1":
            inputcards(choice2)
        elif choice == "2":
            x = input(
                "The whole file?(1) , Just a card?(2) or This Storage Container?(3): ")
            if x == "1":
                delete_cards_file()
            elif x == "2":
                delete_card(choice2)
            elif x == "3":
                deleteStorageKey(choice2)
                return quequiereshacer()
        elif choice == "3":
            storageDecisionTree(choice2)
        elif choice == "4":
            choice1 = input(
                "What do you wanna do? add decklist to storage (1), do you have the cards to make decklist (2), back (3), or quit (5): ")
            if choice1 == "1":
                addDeckToStorage(choice2)
            elif choice1 == "2":
                enoughcardsinstoragefordeck(deckText, choice2)
            elif choice1 == "3":
                continue
            elif choice1 == "5":
                break
        elif choice == "5":
            break
        else:
            return


######################################


def parseDeck(deckText):
    deck = {"Pokémon": [], "Trainer": [], "Energy": []}
    current_section = None

    for line in deckText.splitlines():
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


parsed_deck = parseDeck(deckText)


def addDeckToStorage(storageChoice):
    deck = parseDeck(deckText)
    loaded = loadCards()
    cards = loaded[storageChoice]
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

    saveCards(loaded)
    print(
        f"Added {sum(list(map(lambda x: x["Amount"], deckcards)))} cards from deck to storage.")


def enoughcardsinstoragefordeck(deckText, storageChoice):
    deck = parseDeck(deckText)
    loaded = loadCards()
    cards = loaded[storageChoice]

    # Build storage lookup: (name, set, number) → amount
    storage_lookup = {
        (c["CardName"].lower(), c["CardSet"].lower(), c["CardNumber"]): c["Amount"]
        for c in cards
    }

    # Group storage cards by name to show alternatives
    storageByName = {}
    for c in cards:
        name = c["CardName"].lower()
        storageByName.setdefault(name, []).append(c)

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
            if name in storageByName:
                print("  Alternatives you DO own:")
                for alt in storageByName[name]:
                    print(
                        f"    - {alt['Amount']}x {alt['CardName']} {alt['CardSet']} {alt['CardNumber']}")
            else:
                print("  You own no copies of this card in any set.")

        print()

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
            if name in storageByName:
                print("  Other sets you DO own:")
                for alt in storageByName[name]:
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
    num = num.zfill(3)
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


# FEATURE CURRENTLY WORKING ON. CHANGE "DECK LISTS" KEY TO POINT TO A LIST OF DICTIONARIES WHERE THE DECK LIST NAME IS THE KEY AND
# POINTS TO A LIST OF DICTIONARIES {"DECK LISTS" :
#            [{"DECK LIST 1" :[{
#             "CardName": "Genesect ex",
#             "CardSet": "BLK",
#             "CardNumber": 67,
#             "Amount": 1
#         },
#         {
#             "CardName": "Fezandipiti ex",
#             "CardSet": "SFA",
#             "CardNumber": 38,
#             "Amount": 1
#         },
#         {
#             "CardName": "Munkidori",
#             "CardSet": "TWM",
#             "CardNumber": 95,
#             "Amount": 1
#         }],
#            {"DECK LIST 2" :[{
#            {
#                "CardName": "Arven",
#                "CardSet": "OBF",
#                "CardNumber": 186,
#                "Amount": 4
#            },
#            {
#                "CardName": "Boss's Orders",
#                "CardSet": "MEG",
#                "CardNumber": 114,
#                "Amount": 3
#            },
#            {
#                "CardName": "Professor Turo's Scenario",
#                "CardSet": "PAR",
#                "CardNumber": 171,
#                "Amount": 2
#            }]]
1

