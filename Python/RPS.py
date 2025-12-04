import random


def get_choices():
  player_choice = input("Enter a choice: rock, paper or scissors. Player choice: ")
  options = ["rock", "paper", "scissors"]
  computer_choice = random.choice(options)
  choices = {"player": player_choice, "computer": computer_choice}
  return choices

def check_win(player, computer):
  print("You chose " + player)
  print("Computer chose " + computer)
  if player == computer:
    return "Tie"
  elif player == "rock" and computer == "scissors":
    return "You win"
  elif player == "rock" and computer == "paper":
    return "You lose"
  elif player == "paper" and computer == "rock":
    return "You win"
  elif player == "paper" and computer == "scissors":
    return "You lose"
  elif player == "scissors" and computer == "rock":
    return "You lose"
  elif player == "scissors" and computer == "paper":
    return "You win"

choices = get_choices()
result = check_win(choices["player"], choices["computer"])
print (result)
