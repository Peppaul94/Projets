/* RPS.c
   Rock-Paper-Scissors simple en C
   Compile avec gcc (MinGW) :
     gcc -o RPS.exe RPS.c
   Exécutez depuis PowerShell :
     .\RPS.exe
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <ctype.h>

#define MAX_INPUT 32 //Pas obligatoire mais bonne pratique

// Convertit la chaîne en minuscules (in-place)
void to_lowercase(char *s) {
    for (; *s; ++s) *s = (char)tolower((unsigned char)*s);
}

// Retourne l'index de l'option: 0=rock, 1=paper, 2=scissors, -1 si invalide
int choice_index(const char *s) {
    if (strcmp(s, "rock") == 0) return 0;
    if (strcmp(s, "paper") == 0) return 1;
    if (strcmp(s, "scissors") == 0) return 2;
    return -1;
}

const char *names[3] = {"rock", "paper", "scissors"};

// Détermine le résultat: 0=tie, 1=player win, 2=computer win
// Faire deux conditions ou une avec "else if" (en C c'est else if) est équivalent ici
int determine_winner(int player, int computer) {
    if (player == computer) return 0;
    // rock(0) beats scissors(2)
    // paper(1) beats rock(0)
    // scissors(2) beats paper(1)
    if ((player == 0 && computer == 2) ||
        (player == 1 && computer == 0) ||
        (player == 2 && computer == 1)) {
        return 1;
    }
    return 2;
}

int main(void) {
    char input[MAX_INPUT]; //Pas obligatoire mais bonne pratique
    char trimmed[MAX_INPUT]; //Pas obligatoire mais bonne pratique
    int player_idx, computer_idx;
    // Init RNG
    srand((unsigned int)time(NULL)); //Initialise la graine du générateur de nombre aléatoire avec le temps actuel. C'est ce qui permet en C de générer un nombre aléatoire différent à chaque programme. On pourrait utilsier d'autre variable comme notamment l'ID du processeur ou BCryptGenRandom() sous Windows (/dev/urandom sous Linux/MacOS)

    printf("Enter a choice: rock, paper or scissors. Player choice: ");
    if (!fgets(input, sizeof(input), stdin)) {
        fprintf(stderr, "Input error\n");
        return 1;
    }

    // Remove newline if present and trim leading/trailing spaces
    size_t len = strlen(input);
    while (len > 0 && (input[len-1] == '\n' || input[len-1] == '\r')) { // Boucle qui gère les fins de ligne Windows et Unix
        input[--len] = '\0';
    }

    // Formatte l'entrée utilisateur en supprimant les espaces inutiles
    char *start = input;
    while (*start && isspace((unsigned char)*start)) start++;
    char *end = input + strlen(input) - 1;
    while (end > start && isspace((unsigned char)*end)) *end-- = '\0';
    strncpy(trimmed, start, sizeof(trimmed)-1); // Copie de manière sécurisée "start" vers "trimmed" en prenant la taille maximale de "trimmed" -1 pour éviter les débordements
    trimmed[sizeof(trimmed)-1] = '\0'; // Assure que "trimmed" se termine avec un caractère nul

    to_lowercase(trimmed); // Convertit "trimmed" qui contient la saisie de l'utilisateur en minuscules
    player_idx = choice_index(trimmed); // Récupère l'index (0, 1, 2 ou -1) de l'option choisie par l'utilisateur
    if (player_idx < 0) {
        printf("Invalid choice: '%s'. Use rock, paper or scissors.\n", trimmed);
        return 1;
    }

    computer_idx = rand() % 3; //Choix aléatoire de l'ordinateur entre 0 et 2

    printf("You chose %s\n", names[player_idx]);
    printf("Computer chose %s\n", names[computer_idx]);

    int result = determine_winner(player_idx, computer_idx);
    if (result == 0) {
        printf("Tie\n");
    } else if (result == 1) {
        printf("You win\n");
    } else {
        printf("You lose\n");
    }

    return 0;
}