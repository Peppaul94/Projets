import random

dog_list = ["Fido", "Spot", "Sparky"]

def dog_position():
    position = random.randint(0, 99)  # Generate a random position
    return position  # Return the generated position
  
def dog_walking(dog_location):
  time=random.randint(1,10)
  speed=random.randint(1,10)
  dog_new_location= dog_location+(time*speed)
  print("The dog is walking during " + str(time) + " seconds with a speed of "+ str(speed) +" m/s")
  return dog_new_location

def guess_new_position(dog_walking):
  guess=int(input("Guess the new position of the dog: "))
  return guess

def dog_guess(dog_location, guess):
  if guess==dog_location:
    print("Correct!")
  else:
    print("Incorrect!")
    print ("New location is " + str(dog_new_location))

for dog_name in dog_list:
  dog_location = dog_position()  # Get the location using the dog_position function
  print("Actual " + dog_name + " location is " + str(dog_location))
  dog_new_location = dog_walking(dog_location)
  guessing=guess_new_position(dog_new_location)
  dog_guess(dog_new_location, guessing)
