import random
jenis = ('Hati', 'Sekop', 'Clover', 'Berlian')
rank = ('Dua', 'Tiga', 'Empat', 'Lima', 'Enam', 'Tujuh', 'Delapan', 'Sembilan', 'Sepuluh' ,'Jack', 'King', 'Queen', 'Ace')
value = {'Dua' : 2, 'Tiga' : 3, 'Empat' : 4, 'Lima' : 5, 'Enam' : 6, 'Tujuh' : 7, 'Delapan' : 8, 'Sembilan' : 9, 'Sepuluh' : 10,
         'Jack' : 10, 'King' : 10, 'Queen' : 10, 'Ace' : 11}

class Card:
    def __init__(self, j , r):
        self.rank = r
        self.jenis = j
        self.value = value[r]

    def __str__(self):
        return  self.rank + " " + self.jenis

class Deck:
    def __init__(self):
        self.cards = []
        self.sum = 0
        for j in jenis:
            for r in rank:
                self.cards.append(Card(j,r))

    def shuffle(self):
        random.shuffle(self.cards)

    def drawCard(self):
        return self.cards.pop()

    def __str__(self):
        deckComp = ''
        for c in self.cards:
            deckComp += '\n' + c.__str__()
        return 'Di deck terdapat kartu : ' + deckComp


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def addCard(self, c):
        if 'Ace' == c.rank:
            self.aces +=1

        self.value += c.value
        self.cards.append(c)

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def winBet(self):
        self.total += self.bet

    def loseBet(self):
        self.total -= self.bet


def takeBet(chips):
    while True:
        try:
            chips.bet = int(input("berapa banyak chips yang ingin kamu pertaruhkan: "))
        except:
            print("masukkan anda tidak diketahui")
        else:
            if chips.bet > chips.total:
                print(f'Maaf chips anda tidak cukup! Chips anda {chips.total}')
            else:
                break

def hit(deck, hand):
    hand.addCard(deck.drawCard())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop

    while True:
        p = input("Apakah anda mau hit atau tidak(y/t): ")

        if p[0].lower() == 'y':
            hit(deck, hand)
        elif p[0].lower() == 'n':
            print('giliran dealer')
            playing = False
        else:
            print('Maaf masukkan anda tidak sesuai')
            continue
        break

def show_some(player, dealer):
    print("kartu Dealer:")
    print(" <card hidden>")
    print(dealer.cards[1])
    print("Kartu Player:",*player.cards,sep='\n')

def show_all(player, dealer):
    print("Karti dealer: ",*dealer.cards,sep='\n')
    print(f"Memiliki nilai : {dealer.value}")
    print("Karti Player: ",* player.cards,sep='\n')
    print(f"Memiliki nilai : {player.value}")


def playerBusts(p, d, c):
    print('Bust Player')
    c.loseBet()

def playerWins(p, d, c):
    print('Player Win')
    c.winBet()

def dealerBusts(p ,d ,c):
    print('Bust Player, Dealer Busted')
    c.winBet()

def dealerWins(p, d, c):
    print('Dealer Wins')
    c.loseBet()

def push(p, d):
    print("Dealer dan Player seri, Push")

newDeck = Deck()
while True:
    # Print an opening statement
    print("Welcome to BlackJack")
    playing = True
    # Create & shuffle the deck, deal two cards to each player
    newDeck.shuffle()
    p1 = Hand()
    dealer = Hand()

    p1.addCard(newDeck.drawCard())
    p1.addCard(newDeck.drawCard())

    dealer.addCard(newDeck.drawCard())
    dealer.addCard(newDeck.drawCard())
    # Set up the Player's chips
    pChips = Chips()
    # Prompt the Player for their bet
    takeBet(pChips)
    # Show cards (but keep one dealer card hidden)
    show_some(p1,dealer)
    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(newDeck,p1)
        # Show cards (but keep one dealer card hidden)
        show_some(p1,dealer)
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if p1.value > 21:
            playerBusts(p1, dealer, pChips)
            break
        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        if dealer.value < 21:
            while dealer.value < 17:
                hit(newDeck,dealer)
            # Show all cards
            show_all(p1,dealer)
            # Run different winning scenarios
            if dealer.value > 21:
                dealerBusts(p1,dealer,pChips)
            elif dealer.value > p1.value:
                dealerWins(p1,dealer,pChips)
            elif dealer.value < p1.value:
                playerWins(p1,dealer,pChips)
            else:
                push(p1,dealer)
        break
    # Inform Player of their chips total
    print(f"Total Players Chips adalah {pChips.total}")
    # Ask to play again
    t = True
    while t:
        a = input("apakah mau bermainlagi(y/t)?")
        if a[0].lower() == 'y':
            t = False
            continue
        elif a[0].lower() == 't':
            t = False
        else:
            print("masukkan tidak dikenal")
    break

