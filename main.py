import os 
import csv 
import pathlib 
import numpy as np
from nicegui import ui, events
import pandas as pd
from io import BytesIO

def main():
    gui = UI()
    gui.run()


class UI():
    DATA_PATH = pathlib.Path(r"M:\1. Personal\Programming\simpleWRTS\data")
    TOTAL_COLUMN = 2 
    CORRECT_COLUMN = 3
    IGNORE_ROW = 0 


    def __init__(self):
        self.input_history = ''  
        self.load_data()
        self.choice_idx = np.random.choice(self.current_data[1:].shape[0]) + 1 
        self.curr_target = self.current_data[self.choice_idx][0]
        self.curr_target_dutch = self.current_data[self.choice_idx][1]
        self.total_guesses      = 0 
        self.correct_guesses    = 0
        self.init_ui()

    def evaluate(self,guess):
        if "".join(self.curr_target_dutch.split())  == "".join(guess.split()):
            return True 
        return False
    
    # This POS needs a lot of refactoring
    def load_data(self, new_path = DATA_PATH,name = ''):
        if name != '':
            path = os.path.join(self.DATA_PATH, name)
            if not os.path.exists(path):
                raise KeyError
            with open(path) as file:
                reader = csv.reader(file, delimiter=',', quotechar='|')
                arr = []
                for row in reader:
                    arr.append(row)
            arr = np.array(arr)
            arr = np.concatenate((arr,np.zeros((arr.shape[0],3)).astype(int)),axis=1)  # Nx4 arr, 3 column is total, 4 column is correct 
            self.current_data = np.array(arr)
            ui.notify(f"Loaded data! {self.current_data.shape}")   
            return 
        print(new_path)
        if not os.path.exists(new_path):
            raise KeyError

        paths = os.listdir(new_path)
        self.current_name = paths[0]
        paths = [os.path.join(self.DATA_PATH,paths[i]) for i in range(len(paths))]
        with open(paths[0]) as file:
            reader = csv.reader(file, delimiter=',', quotechar='|')
            arr = []
            for row in reader:
                arr.append(row)
        arr = np.array(arr)
        arr = np.concatenate((arr,np.zeros((arr.shape[0],3)).astype(int)),axis=1)  # Nx4 arr, 3 column is total, 4 column is correct 
        
        self.current_data = np.array(arr)

    def next_step(self):
        first_choice = np.random.choice(self.current_data[1:].shape[0]) + 1
        if self.current_data[first_choice,4] == 1:
            while True:
                choice = np.random.choice(self.current_data[1:].shape[0]) + 1 
                if self.current_data[first_choice,4] == 1:
                    continue
                else:
                    self.choice_idxx = choice
            
        else:
            self.choice_idx = first_choice
        self.curr_target = self.current_data[self.choice_idx][0]
        self.lbl_target.text = self.curr_target
        self.curr_target_dutch = self.current_data[self.choice_idx][1]
        self.curr_input.value = ''
        self.dbg_lbl.text = f"Correct answer: {self.curr_target_dutch}"
        self.feedback_icon.classes("")
        return 
    
    def validate_input(self):
        val = self.curr_input.value
        res = self.evaluate(val)
        self.feedback_icon.name = ""
        self.feedback_icon.classes("")
        self.total_guesses +=1
        if res:
            self.current_data[self.choice_idx,self.TOTAL_COLUMN]   = int(self.current_data[self.choice_idx,self.TOTAL_COLUMN])  + 1 
            self.current_data[self.choice_idx,self.CORRECT_COLUMN] = int(self.current_data[self.choice_idx,self.CORRECT_COLUMN]) + 1  
            self.correct_guesses +=1 
            self.correct_guesses_label.text =  f"Correct Guesses: {self.correct_guesses}"
            
        else:
            # res = ry_again(self.data, self.choice_idx, depth=0)
            # for now, lets just skip to the new word and end this function
            self.current_data[self.choice_idx,self.TOTAL_COLUMN]   = int(self.current_data[self.choice_idx,self.TOTAL_COLUMN])  + 1 
        self.total_guesses_label.text = f"Total Guesses : {self.total_guesses}"
        self.switch_icon(res)

        self.next_step()
        return 
    
    def switch_icon(self,res):
        if res:
            self.feedback_icon.name = 'check'
            self.feedback_icon.classes("text-green")
        else:
            self.feedback_icon.name = 'cancel'
            self.feedback_icon.classes("text-red")


    
    def run(self):
        ui.run()
    
    def set_new_list(self):
        new_list = self.set_select 
        self.current_name = new_list.value
        self.load_data(name = self.current_name)
        self.curr_list_lbl.text = f"Current list: {self.current_name}"
        self.dialog.close()
        self.next_step()
    def get_current_data(self):
        file_names = os.listdir(self.DATA_PATH)
        return file_names
    
    async def handle_new_file(self, e: events.UploadEventArguments):
        file_bytes = await e.file.read()
        name = e.file.name
        df = pd.read_csv(BytesIO(file_bytes), encoding='utf-8')
        # save new file to file system to be able to open later 
        path_to_save = os.path.join(self.DATA_PATH,name)
        df.to_csv(path_to_save, index=False)
        ui.notify(f"Successfully saved file! {name}")

    def data_viewer(self):  
        with ui.dialog() as self.dialog, ui.card().classes("p-4"):
            ui.label("Select your desired list").classes("text-h4 font-bold")
            ui.label("Select a word set:").classes("text-h6")

            # Example: Dropdown to select word sets
            # get current lists 
            
            word_sets = self.get_current_data()
            self.set_select = ui.select(word_sets,value=f'{self.current_name}')

            # Buttons for actions
            with ui.row().classes("justify-end"):
                ui.button("Cancel", on_click=self.dialog.close).props('color=blue')
                ui.button("Load", on_click=self.set_new_list).props('color=blue')
            
            self.markdown = ui.markdown() 
            self.uploader = ui.upload(on_upload = self.handle_new_file, max_file_size=5_000).classes('max-w-full').props('color=blue accept=.csv')   
        self.dialog.open()      

    def init_ui(self):
        bg_color = ui.colors(primary="#73baede8")  # AliceBlue background
        with ui.card().classes("w-full max-w-4xl p-6 shadow-lg").style("background-color: #73baede8;"):  
            with ui.row().classes('w-full'):
                ui.label("SimpleWRTS").classes("text-h3 font-bold text-gray-800").style("text-align: center; width: 80%;")
                ui.button(icon='more_vert', color='gray',on_click=self.data_viewer).props('flat round')  # Visible icon and styling
            with ui.row().classes("w-full"):
                with ui.element("div").classes("flex-1 items-right bg-gray-100 p-2 rounded-lg"):
                    # Title row (centered)
                    self.curr_list_lbl = ui.label(f"Current list: {self.current_name}").classes("w-full text-left")  
                    # Row for "Please translate to Dutch:" and dropdown menu
                    with ui.row().classes("w-full items-center"):
                        ui.label("Please translate to Dutch:").classes("text-h6 italic text-gray-700")
                        
                    # Target word
                    self.lbl_target = ui.label(f"{self.curr_target}").classes("text-h2 text-gray-800").style("text-align: center; width: 50%;")

                    # Add vertical whitespace
                    # Input row
                    self.curr_input = ui.input(
                            placeholder="start typing",
                        ).on("keydown.enter", self.validate_input).classes("w-70 text-h3 p-4").props('autocomplete="off"')
                    # For debugging and testing the flow of the progam 
                    self.dbg_lbl = ui.label(f"Correct answer: {self.curr_target_dutch}")
                    self.feedback_icon = ui.icon("", size="2rem")
            
                with ui.element("div").classes("w-1/4 items-right bg-gray-100 p-2 rounded-lg"):
                    ui.label("Performance").classes("text-h5 font-bold text-gray-800")
                    self.total_guesses_label = ui.label(f"Total Guesses : {self.total_guesses}").classes("text-h6")
                    self.correct_guesses_label = ui.label(f"Correct Guesses: {self.correct_guesses}").classes("text-h6")

main()