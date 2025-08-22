import random

print("Hello mate, how can I help you?")
advice = input("Your answer (Yes/No): ")
def goOut():
    
    Go = input("Today, do you want to go outside? (Yes/No): ")
    Choices = ["Sunny", "Rainy", "Cloudy"]
    Choice = random.choice(Choices)
    print("Weather today is:", Choice)

    if Go == "Yes" and Choice == "Rainy":
        print("You shouldn't go out because the weather today is bad")
        print("But if you want you can go out with an umbrella")
    elif Go == "Yes" and (Choice == "Clody" or Choice == "Sunny"):
        print('Have a good day')
    elif Go == "No":
        Game = bool(input("Do you want play some game? (Yes/No): "))
        if Game == 'Yes':
            Games = ["LOL", "PUBG", "Valorant", "TFT"]
            Game_choice = random.choice(Games)
            print(f"Now, we can play {Game_choice} together")
        else:
            print("Have a good day, maybe we can ddo it later")
    

if __name__ == "__main__":
    goOut()

    
