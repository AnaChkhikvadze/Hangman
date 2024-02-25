import random
import json

class HangmanGame:
    def __init__(self): # HangmanGame თამაშის class ის ინიციალიზება
        self.word = self.get_word()
        self.word_to_guess = "_" * len(self.word)
        self.guessed = False
        self.guessed_letters = []
        self.state = 5

    @staticmethod
    def display_intro(): # ვაცნობთ თამაშის წესებს
        with open('hangman-intro.txt', 'r') as file:
            intro_ascii = file.read()
        print(intro_ascii)

    @staticmethod
    def display_end(result): # თამაშის შედეგის გამოტანა
        if result:
            with open('hangman-win.txt', 'r') as file:
                end_ascii = file.read()
            print(end_ascii)
        else:
            with open('hangman-lose.txt', 'r') as file:
                end_ascii = file.read()
            print(end_ascii)

    @staticmethod
    def display_hangman(state): # hangman -ის მიმდინარე მდგომარეობის გამოტანა
        with open('hangman_states.json', 'r') as file:
            hangman_states = json.load(file)
        return hangman_states[str(state)]

    @staticmethod
    def get_word(): # სიტყვის არჩევა შემთხვევითობით hangman-words.txt ფაილიდან
        words = open('hangman-words.txt').read().split()
        return random.choice(words)

    @staticmethod
    def valid(c): # სიმბოლოს ვალიდურობის შემოწმება
        return len(c) == 1 and 'a' <= c <= 'z'

    def play(self): #თამაშის ლოგიკა
        print(self.display_hangman(self.state)) # გამოგვაქვს hangman-ის საწყისი მდგომარეობა
        while not self.guessed and self.state > 0: # თამაში გრძელდება სანამ სიტყვა არ გამოგვიცნია და 0-ზე მეტი სიცოცხლე გვაქვს
            print("Guess the word: " + self.word_to_guess)
            guess = input("Enter the letter:\n<")
            if self.valid(guess):
                if guess not in self.word:
                    self.state -= 1
                    self.guessed_letters.append(guess) # ვამატებთ ასოს გამოცნობილი ასოების სიას, რათა ხელახლა არ დააკლდეს ქულა
                else:
                    self.guessed_letters.append(guess)
                    indexes = [i for i, letter in enumerate(self.word) if letter == guess] # გამოცნიბილი ასობგერის ინდექსებს ვეძებთ გამოსაცნობ სიტყვაში
                    for i in indexes:
                        word_as_list = list(self.word_to_guess) #სიტყვა გადაგვყავს სტრინგიდან ლისტში შესაცვლელად
                        word_as_list[i] = guess # _ ებს ვცვლით გამოცნობილი ასოებით შესაბამის ინდექსებზე
                        self.word_to_guess = "".join(word_as_list) # სიტყვას ვაბრუნებთ სტრინგში
                    if "_" not in self.word_to_guess:  #თუ _ აღარ დარჩა სიტყვაში, თამაში მოვიგეთ
                        self.guessed = True
            print(self.display_hangman(self.state))
        print("Hidden word was: " + self.word)
        return self.guessed

def hangman(): # მთავარი ფუნქცია Hangman თამაშის გასაშვებად
    while True: # ლუპი გრძელდება მანამ, სანამ უარს არ ვიტყვით თამაშის გაგრძელებაზე
        game = HangmanGame()
        HangmanGame.display_intro()
        result = game.play()
        HangmanGame.display_end(result)
        repeat = input("Do you want to play again? Yes/No")
        while repeat.lower() not in ["yes", "no"]:
            repeat = input("Please enter 'Yes' or 'No': ")
        if repeat.lower() == "no":
            break

if __name__ == "__main__":
    hangman()
