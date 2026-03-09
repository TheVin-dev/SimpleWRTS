import os 
import csv 
import pathlib 
import numpy as np
from nicegui import ui
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

def main():

    gui = UI()
    gui.run()
    #     choice = arr[choic_idx][0]
    #     print(f"Italian: {choice}")
    #     s = str(input("Your guess: "))
    #     res = evaluate(arr[choic_idx][1],s)
    #     if res:
    #         arr[choic_idx,TOTAL_COLUMN]   = int(arr[choic_idx,TOTAL_COLUMN])  + 1 
    #         arr[choic_idx,CORRECT_COLUMN] = int(arr[choic_idx,CORRECT_COLUMN])+ 1 

    #         continue 
    #     else:
    #         res = try_again(arr, choic_idx, depth=0)
    #         print('On a list maybe?')




class UI():
    DATA_PATH = pathlib.Path(r"M:\1. Personal\Programming\simpleWRTS\data")
    TOTAL_COLUMN = 2 
    CORRECT_COLUMN = 3
    def __init__(self):
        self.input_history = ''  
        self.load_data()
        self.choice_idx = self.choose_idx()
        self.curr_target = self.data[self.choice_idx][0]

        self.init_ui()
    def evaluate(self,guess):
        if "".join(self.curr_target.split())  == "".join(guess.split()):
            return True 
        return False
    
    def load_data(self):
        if not os.path.exists(self.DATA_PATH):
            raise KeyError
        paths = os.listdir(self.DATA_PATH)
        paths = [os.path.join(self.DATA_PATH,paths[i]) for i in range(len(paths))]
        with open(paths[0]) as file:
            reader = csv.reader(file, delimiter=',', quotechar='|')
            arr = []
            for row in reader:
                arr.append(row)
        arr = np.array(arr)
        arr = np.concatenate((arr,np.zeros((arr.shape[0],3)).astype(int)),axis=1)  # Nx4 arr, 3 column is total, 4 column is correct 
        
        self.data = np.array(arr)
        ui.notify(f"Loaded data! {self.data.shape}")

    def choose_idx(self):
        first_choice = np.random.choice(self.data[1:].shape[0])
        if self.data[first_choice,4] == 1:
            while True:
                choice = np.random.choice(self.data[1:].shape[0])
                if self.data[first_choice,4] == 1:
                    continue
                else:
                    return choice
            
        else:
            return first_choice
    
    def validate_input(self):
        val = self.curr_input.value
        res = self.evaluate(val)
        if res:
            self.data[self.choice_idx,self.TOTAL_COLUMN]   = int(self.data[self.choice_idx,self.TOTAL_COLUMN])  + 1 
            self.data[self.choice_idx,self.CORRECT_COLUMN] = int(self.data[self.choice_idx,self.CORRECT_COLUMN])+ 1  
            ui.notify("Correct!")
            # now, we need to set a new word and end this function
        else:
            # res = try_again(self.data, self.choice_idx, depth=0)
            # for now, lets just skip to the new word and end this function
            self.data[self.choice_idx,self.TOTAL_COLUMN]   = int(self.data[self.choice_idx,self.TOTAL_COLUMN])  + 1 

            ui.notify("Booh!")
        self.choice_idx = self.choose_idx()
        self.curr_target = self.data[self.choice_idx][0]
        self.lbl_target.text = self.curr_target
        self.curr_input.value = ''

        return 


    
    def run(self):
        ui.run()

    def init_ui(self):
        ui.colors(primary='#f0f8ff')  # AliceBlue background

        with ui.card().classes("mx-auto w-full max-w-2xl p-6 shadow-lg").style("background-color: #fff0f5;"):  # LavenderBlush card
            # Title row (centered)
            ui.label("SimpleWRTS").classes("text-h3 font-bold text-gray-800").style("text-align: center; width: 100%;")

            # Row for "Please translate to Dutch:" and dropdown menu
            with ui.row().classes("w-full items-center"):
                ui.label("Please translate to Dutch:").classes("text-h6 italic text-gray-700")
                ui.button(icon='more_vert', color='gray').props('flat round').classes('ml-auto')  # Visible icon and styling
                # with ui.menu() as submenu:
                #     ui.menu_item('Settings', lambda: ui.notify('Settings clicked'))
                #     ui.menu_item('Help', lambda: ui.notify('Help clicked'))
                #     ui.menu_item('About', lambda: ui.notify('About clicked'))

            # Target word
            self.lbl_target = ui.label(f"{self.curr_target}").classes("text-h2 font-bold text-gray-800").style("text-align: center; width: 100%;")

            # Add vertical whitespace
            ui.html("<div style='height: 2rem;'></div>")

            # Input row
            self.curr_input = ui.input(
                    placeholder="start typing",
                    validation={"Input too long": lambda value: len(value) < 20},
                ).on("keydown.enter", self.validate_input).classes("w-96 text-h3 p-4")






main()