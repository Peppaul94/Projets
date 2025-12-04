import random
import pyfiglet


def ini_game(value, percent):
    if value <= percent:
        return "bomb"
    else:
        return "empty"


def create_game_matrix(rows, cols):
    game_matrix = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(random.randint(1, 100))  # Append random value between 1 and 4
        game_matrix.append(row)
    return game_matrix


def check_cell_position(game_matrix, row, col, rows, cols):
    # Directly return the cell position that matches the given row and col
    if 0 <= row < len(game_matrix) and 0 <= col < len(game_matrix[0]):  # Check if the position is valid
        return (row, col)
    elif row == 69 and col == 69:
            print("You are about to leave the game.")
            confirm=str(input("Continue?\n Yes: Y; No: N.\n Your choice: "))
            if confirm=="Y":
                print("Goodbye!")
                exit()
            elif confirm=="N":
                print("Alright, lets keep it going")
                return pick_cell(game_matrix, rows, cols)
            else:
                print("Please type Y or N to confirm")
                return pick_cell(game_matrix, rows, cols)
    elif col == 66:
        print("Your move has been canceled (you typed 66 in column) (selected row: "+str(row)+")")
        return pick_cell(game_matrix, rows, cols)
    else:
        return "Invalid position"


def print_default_matrix(rows, cols):
    print("   ", end="")  # Padding for row labels
    # Print column headers
    for col_number in range(cols):
        print(f"{col_number:2}", end=" ")
    print()
   
    for row_number in range(rows):
        print(f"{row_number:2} ", end="")  # Print the row number
        for _ in range(cols):
            print("?", end="  ")  # Default placeholder for each cell
        print()  # Move to the next line after each row


def pick_cell(game_matrix, rows, cols):
    print("Note: The first row and column is 0. The last row is "+str(rows-1)+" and the last column is "+str(cols-1)+"\nTo leave the game, type 69 for row and 69 for column. To cancel your move, in column type 66")
    try:
        picked_rows = int(input("Select a row: "))
        picked_cols = int(input("Select a column: "))
        picked_cell = check_cell_position(game_matrix, picked_rows, picked_cols, rows, cols)
        if picked_cell != "Invalid position":
            return picked_cell
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return pick_cell(game_matrix, rows, cols)
       
def print_new_matrix(new_matrix, picked_cell, cell_value, all_near_value):
    print("   ", end="")  # Column header padding
    for col_number in range(len(new_matrix[0])):  # Print column numbers
        print(f"{col_number}", end=" ")
    print()
    print()
   


    for row_index, row in enumerate(new_matrix):
        print(f"{row_index} ", end=" ")  # Print row number
        for col_index, value in enumerate(row):
            cell = (row_index, col_index)
            is_previous_move = False
            for sublist in all_near_value[:-1]:
                if (int(sublist[0]), int(sublist[1])) == cell:
                    print(sublist[2], end=" ")  # Print value from previous moves
                    is_previous_move = True
                    break
            if not is_previous_move:
                if cell == picked_cell and cell_value == "bomb":
                    print("B", end=" ")  # Bomb for current pick
                elif cell == picked_cell and cell_value == "empty":
                    print(all_near_value[-1][-1], end=" ")  # Number of nearby bombs
                else:
                    print("?", end=" ")  # Default placeholder
        print()  # Move to the next row




def check_near_value(game_matrix, picked_cell, percent):
    near_value = 0
    for i in range(picked_cell[0] - 1, picked_cell[0] + 2):
        for j in range(picked_cell[1] - 1, picked_cell[1] + 2):
            if 0 <= i < len(game_matrix) and 0 <= j < len(game_matrix[0]):
                if game_matrix[i][j] <= percent:
                    near_value += 1
           
    all_near_value.append(list(picked_cell) + [near_value])
    return all_near_value


def count_total_bombs(game_matrix, percent):
    total_bombs = 0
    for row in game_matrix:
        for cell in row:
            if cell <= percent:
                total_bombs += 1
   
    return total_bombs


def pick_difficulty():
    print("Welcome to Minesweeper game! Before starting, please select the difficulty among these:\n1. Baby (10%, 4X4)\n2. Very easy (10%, 8X8)\n3. Easy (20%, 8X8)\n4. Medium (25%, 8X8)\n5. Hard (50%, 8X8)\n6. Very hard (75%, 8X8)\n7. Impossible (90%, 10X10)\n8. Godlike (95%, 10X10)\n9. SadoMazo (99%, 10X10)\n0. Leave\n")
    option=int(input("Select an option: "))
    if option==1:
        difficulty="Baby"
        ascii_art = pyfiglet.figlet_format(difficulty, font="standard", justify="left")
        print(ascii_art)
        print("This difficulty is for babies!")
        confirm=str(input("Continue?\n Yes: Y; No: N.\n Your choice:  "))
        if confirm=="Y":
            percent=10
            rows=4
            cols=4
            game_matrix = create_game_matrix(rows, cols)
            total_bombs=count_total_bombs(game_matrix, percent)
            print("There are "+str(total_bombs)+" bombs in the game")
            running_game(game_matrix, rows, cols, all_near_value, percent)
            return percent, rows, cols
        elif confirm=="N":
            pick_difficulty()
        else:
            print("Please type Y or N to confirm")
            pick_difficulty()
    elif option==2:
        difficulty="Very easy"
        ascii_art = pyfiglet.figlet_format(difficulty, font="standard", justify="left")
        print(ascii_art)
        print("Easiest difficulty of this game.")
        confirm=str(input("Continue?\n Yes: Y; No: N.\n Your choice: "))
        if confirm=="Y":
            percent=10
            rows=8
            cols=8
            game_matrix = create_game_matrix(rows, cols)
            options(percent, rows, cols, game_matrix)
            return percent, rows, cols
        elif confirm=="N":
            pick_difficulty()
        else:
            print("Please type Y or N to confirm")
            pick_difficulty()
    elif option==3:
        difficulty="Easy"
        ascii_art = pyfiglet.figlet_format(difficulty, font="standard", justify="left")
        print(ascii_art)
        print("Easy difficulty adapted to anyone who want to have fun.")
        confirm=str(input("Continue?\n Yes: Y; No: N.\n Your choice: "))
        if confirm=="Y":
            percent=20
            rows=8
            cols=8
            game_matrix = create_game_matrix(rows, cols)
            options(percent, rows, cols, game_matrix)
            return percent, rows, cols
        elif confirm=="N":
            pick_difficulty()
        else:
            print("Please type Y or N to confirm")
            pick_difficulty()
    elif option==4:
        difficulty="Medium"
        ascii_art = pyfiglet.figlet_format(difficulty, font="standard", justify="left")
        print(ascii_art)
        print("A difficulty made for experimented players.")
        confirm=str(input("Continue?\n Yes: Y; No: N.\n Your choice: "))
        if confirm=="Y":
            percent=25
            rows=8
            cols=8
            game_matrix = create_game_matrix(rows, cols)
            options(percent, rows, cols, game_matrix)
            return percent, rows, cols
        elif confirm=="N":
            pick_difficulty()
        else:
            print("Please type Y or N to confirm")
            pick_difficulty()
    elif option==5:
        difficulty="Hard"
        ascii_art = pyfiglet.figlet_format(difficulty, font="standard", justify="left")
        print(ascii_art)
        print("Hard difficulty made for tough players. Force you to think twice for every move.")
        confirm=str(input("Continue?\n Yes: Y; No: N.\n Your choice: "))
        if confirm=="Y":
            percent=50
            rows=8
            cols=8
            game_matrix = create_game_matrix(rows, cols)
            options(percent, rows, cols, game_matrix)
            return percent, rows, cols
        elif confirm=="N":
            pick_difficulty()
        else:
            print("Please type Y or N to confirm")
            pick_difficulty()
    elif option==6:
        difficulty="Very hard"
        ascii_art = pyfiglet.figlet_format(difficulty, font="epic", justify="left")
        print(ascii_art)
        print("Hardest difficulty before the impossible one. You will have to try multiple time before beating this atleast once")
        confirm=str(input("Continue?\n Yes: Y; No: N.\n Your choice: "))
        if confirm=="Y":
            percent=75
            rows=8
            cols=8
            game_matrix = create_game_matrix(rows, cols)
            options(percent, rows, cols, game_matrix)
            return percent, rows, cols
        elif confirm=="N":
            pick_difficulty()
        else:
            print("Please type Y or N to confirm")
            pick_difficulty()
    elif option==7:
        difficulty="Impossible"
        ascii_art = pyfiglet.figlet_format(difficulty, font="Epic", justify="left", width=100)
        print(ascii_art)
        print("This dificulty has been desigend to be impossible. Trying to beat this is pointless, you should close this game and make something more productive like reading a book.")
        confirm=str(input("Continue?\n Yes: Y; No: N.\n Your choice: "))
        if confirm=="Y":
            percent=90
            rows=10
            cols=10
            game_matrix = create_game_matrix(rows, cols)
            print("Knowing the number of bombs would make it too easy ;)")
            running_game(game_matrix, rows, cols, all_near_value, percent)
            return percent, rows, cols
        elif confirm=="N":
            pick_difficulty()
        else:
            print("Please type Y or N to confirm")
            pick_difficulty()
    elif option==8:
        difficulty="Godlike"
        ascii_art = pyfiglet.figlet_format(difficulty, font="Epic", justify="left")
        print(ascii_art)
        print("Only god can beat this difficulty.")
        confirm=str(input("Continue?\n Yes: Y; No: N.\n Your choice: "))
        if confirm=="Y":
            percent=95
            rows=10
            cols=10
            game_matrix = create_game_matrix(rows, cols)
            print("Knowing the number of bombs would make it too easy ;)")
            running_game(game_matrix, rows, cols, all_near_value, percent)
            return percent, rows, cols
        elif confirm=="N":
            pick_difficulty()
        else:
            print("Please type Y or N to confirm")
            pick_difficulty()
    elif option==9:
        difficulty="SadoMazo"
        ascii_art = pyfiglet.figlet_format(difficulty, font="Epic", justify="left")
        print(ascii_art)
        print("You really like it don't you?")
        confirm=str(input("Continue?\n Yes: Y; No: N.\n Your choice: "))
        if confirm=="Y":
            percent=99
            rows=10
            cols=10
            game_matrix = create_game_matrix(rows, cols)
            print("Knowing the number of bombs would make it too easy ;)")
            running_game(game_matrix, rows, cols, all_near_value, percent)
            return percent, rows, cols
        elif confirm=="N":
            pick_difficulty()
        else:
            print("Please type Y or N to confirm")
            pick_difficulty()
    elif option==0:
                print("Goodbye!")
                exit()


def options(percent, rows, cols, game_matrix):
    print("Would you like to know how many bombs are in the game? (It makes the game pretty easier) 1. Yes 2. No")
    option=int(input("Select an option: "))
    if option==1:
        total_bombs=count_total_bombs(game_matrix, percent)
        print("There are "+str(total_bombs)+" bombs in the game")
        running_game(game_matrix, rows, cols, all_near_value, percent)
    else:
        running_game(game_matrix, rows, cols, all_near_value, percent)
    return option


def end_game(game_matrix, rows, cols, all_near_value, cell_position, cell_value, percent):
    total_bombs=count_total_bombs(game_matrix, percent)
    total_cells=rows*cols
    number_move=len(all_near_value)
    is_game_over=total_cells-number_move
    if is_game_over==total_bombs:
        print("You won! There are only "+str(total_bombs)+" bombs left")
        print_end_matrix(game_matrix, all_near_value)
    else:
        print_new_matrix(game_matrix, cell_position, cell_value, all_near_value)
        running_game2(game_matrix, rows, cols, cell_value, cell_position, all_near_value, percent)


def check_different_move(picked_cell, all_near_value):
    for sublist in all_near_value:
        if (int(sublist[0]), int(sublist[1])) == picked_cell:
            print("You already picked this cell, take another")
            return True
    return False


def print_end_matrix(game_matrix, all_near_value):
    print("  ", end="")  # Column header padding
    for col_number in range(len(game_matrix[0])):  # Print column numbers
        print(f"{col_number}", end=" ")
    print()


    for row_index, row in enumerate(game_matrix):
        print(f"{row_index} ", end="")  # Print row number
        for col_index, value in enumerate(row):
            cell = (row_index, col_index)
            is_previous_move = False
            for sublist in all_near_value:
                if (int(sublist[0]), int(sublist[1])) == cell:
                    print(sublist[2], end=" ")  # Print value from previous moves
                    is_previous_move = True
                    break
            if not is_previous_move:
                print("!", end=" ")  # Placeholder for unrevealed cells
        print()  # Move to the next row


   
def check_selected_cell_value(game_matrix, rows, cols, picked_cell, all_near_value, percent):
    for row_index, row in enumerate(game_matrix):
        for col_index, value in enumerate(row):
            # Check the value and initialize the game cell accordingly
            checked_positions=row_index, col_index
            #print(picked_cell)
            if (checked_positions==picked_cell):
                cell_value=ini_game(value, percent)
                if cell_value=="bomb":
                    print("You picked a bomb! Game over")
                    print_new_matrix(game_matrix, picked_cell, cell_value, all_near_value)
                else:
                    print("You selected an empty cell! You did well!")
                    end_game(game_matrix, rows, cols, all_near_value, picked_cell, cell_value, percent)
                   
                return cell_value


#def check_selected_cell_value2(updated_matrix, cell_position, cell_value, all_near_value):
    #for row_index, row in enumerate(game_matrix):
        #for col_index, value in enumerate(row):
            # Check the value and initialize the game cell accordingly
            #checked_positions=row_index, col_index
            #if (checked_positions==cell_position):
                #cell_value=ini_game(value)
                #if cell_value=="bomb":
                    #print("You picked a bomb! Game over")
                    #print_new_matrix(updated_matrix, cell_position, cell_value, all_near_value)
                #else:
                    #print("You selected an empty cell! You did well!")
                    #print_new_matrix(updated_matrix, cell_position, cell_value, all_near_value)
                    #running_game2(updated_matrix, rows, cols, cell_value, cell_position, all_near_value)
                #return cell_value
# Example usage
def running_game(game_matrix, rows, cols, all_near_value, percent):
    print_default_matrix(rows, cols)
    picked_cell=pick_cell(game_matrix, rows, cols)
    check_near_value(game_matrix, picked_cell,percent)
    check_selected_cell_value(game_matrix, rows, cols, picked_cell, all_near_value, percent)


def running_game2(updated_matrix, rows, cols, cell_near_value, cell_position, all_near_value, percent):
    picked_cell=pick_cell(updated_matrix, rows, cols)
    is_move_different=check_different_move(picked_cell, all_near_value)
    if not is_move_different:
        previous_cells_position=check_near_value(updated_matrix, picked_cell, percent)
        check_selected_cell_value(updated_matrix, rows, cols, picked_cell, previous_cells_position, percent)
    else:
        running_game2(updated_matrix, rows, cols, cell_near_value, cell_position, all_near_value, percent)


all_near_value = []
pick_difficulty()