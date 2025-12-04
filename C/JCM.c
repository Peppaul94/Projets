#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BCRYPT_USE_SYSTEM_PREFERRED_RNG 0x00000002
/* typedef minimal (évite d'inclure bcrypt.h) */
typedef LONG (WINAPI *BCryptGenRandom_t)(void *hAlgorithm, unsigned char *pbBuffer, unsigned long cbBuffer, unsigned long dwFlags);

void init_rng_with_bcrypt(void) {
    HMODULE h = LoadLibraryA("bcrypt.dll");
    if (!h) return; /* bcrypt.dll absent -> on peut retomber sur srand(time(NULL)) si besoin */

    BCryptGenRandom_t p = (BCryptGenRandom_t)GetProcAddress(h, "BCryptGenRandom");
    if (!p) { FreeLibrary(h); return; }

    unsigned char buffer[sizeof(unsigned int)];
    LONG status = p(NULL, buffer, sizeof(buffer), BCRYPT_USE_SYSTEM_PREFERRED_RNG);
    if (status == 0) { /* STATUS_SUCCESS == 0 */
        unsigned int seed;
        memcpy(&seed, buffer, sizeof(seed));
        srand(seed);
    }

    FreeLibrary(h);
}

const char *names[3] = {"Fido", "Spot", "Sparky"};

int dog_position() {
    return rand() % 99;
}

int dog_walking(int dog_position) {
    int time=rand()%10;
    int speed=rand()%10;
    int move=dog_position+(time*speed);
    printf("The dog is walking during %d seconds at a speed of %d m/s.\n", time, speed);
    return move;
}

int guess_position(int dog_new_position) {
    int guess;
    printf("Guess the new positionof the dog: ");
    scanf("%d", &guess);
    if (guess == dog_new_position) {
        printf("Congratulations! You guessed the correct position. \n");
        return 1;
    } else {
        printf("Incorrect guess! The correct position was %d. \n", dog_new_position);
        return 0;
    }
}

int main(void) {
    init_rng_with_bcrypt();
    for (int i = 0; i < 3; i++) {
        int pos = dog_position();
        printf("%s is at position %d\n", names[i], pos);
        int dog_new_position = dog_walking(pos);
        guess_position(dog_new_position);
    }
    return 0;
}