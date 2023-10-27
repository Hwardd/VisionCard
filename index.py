from scripts.six_players_normal_table_extractor import six_players_normal_table_extractor
from utils.scriptUtils import repeat_script

def main():
   repeat_script(six_players_normal_table_extractor, 0.350)
   # six_players_normal_table_extractor()
   # cards_detector()
   
if __name__ == "__main__":
    main()
