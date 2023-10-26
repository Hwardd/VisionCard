from scripts.gameExtractor import gameExtractor
from time import sleep

def main():
    # Script actual
    while True:
        sleep(0.35)  # Pausa de 500 ms
        gameExtractor()

if __name__ == "__main__":
    main()
