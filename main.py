import os 
import csv 
import pathlib 
import numpy as np
from nicegui import ui 


DATA_PATH = pathlib.Path(r"M:\1. Personal\Programming\simpleWRTS\data")
TOTAL_COLUMN = 2 
CORRECT_COLUMN = 3 
def load_list(path: pathlib.Path):
    if not os.path.exists(path):
        raise KeyError
    paths = os.listdir(path)
    paths = [os.path.join(DATA_PATH,paths[i]) for i in range(len(paths))]
    with open(paths[0]) as file:
        reader = csv.reader(file, delimiter=',', quotechar='|')
        arr = []
        for row in reader:
            arr.append(row)
    return np.array(arr)

def evaluate(target,guess):
    
    if "".join(target.split())  == "".join(guess.split()):
        return True 
    return False

def try_again(arr, idx, depth):
    print("You have three more guesses")
    while depth < 3:
        choice = arr[idx][0]
        print(f"Italian: {choice} ----- for testing: {arr[idx][1]}")
        s = str(input("Your guess: "))
        res = evaluate(arr[idx][1],s)
        arr[idx,TOTAL_COLUMN] =  int(arr[idx,TOTAL_COLUMN])+ 1 
        if res: 
            arr[idx,CORRECT_COLUMN] = int(arr[idx,CORRECT_COLUMN]) + 1 

            return res
        depth += 1 
    return res 

def choose_idx(arr):
    first_choice = np.random.choice(arr[1:].shape[0])
    if arr[first_choice,4] == 1:
        while True:
            choice = np.random.choice(arr[1:].shape[0])
            if arr[first_choice,4] == 1:
                continue
            else:
                return choice
            
    else:
        return first_choice
def main():
    arr = load_list(DATA_PATH)
    arr = np.concatenate((arr,np.zeros((arr.shape[0],3)).astype(int)),axis=1)  # Nx4 arr, 3 column is total, 4 column is correct 
    PLAYING = True
    print("Welcome to my SimpleWRTS\nA simple tool to learn words (hopefully)")
    print("Translate the following words to the other language:")
    while PLAYING:     
        choic_idx = choose_idx(arr)# np.random.choice(arr[1:].shape[0])  lets keep track of what already did instead. 

        choice = arr[choic_idx][0]
        print(f"Italian: {choice}")
        s = str(input("Your guess: "))
        res = evaluate(arr[choic_idx][1],s)
        if res:
            arr[choic_idx,TOTAL_COLUMN]   = int(arr[choic_idx,TOTAL_COLUMN])  + 1 
            arr[choic_idx,CORRECT_COLUMN] = int(arr[choic_idx,CORRECT_COLUMN])+ 1 

            continue 
        else:
            res = try_again(arr, choic_idx, depth=0)
            print('On a list maybe?')

            
if __name__ == "__main__":
    main()