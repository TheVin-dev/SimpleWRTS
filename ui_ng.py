# from nicegui import ui 
# arr = ['word 1', 'word 2']
# target = "mangare"
# def submit():
#     ui.notify('You clicked me!')
#     # ui.icon('thumb_up', color='primary').classes('text-5xl')
# #  mx-auto shadow-lg
# with ui.card().classes("fixed-center w-full max-w-5xl"):
#     with ui.column():
#         ui.label("SimpleWRTS").classes('text-h2')
#         ui.label("Please translate to Dutch:").classes("text-h5 text-italic")
#         target = ui.label(f"{target}").classes('text-h4 text-bold')
#         ui.input(label='Type here', placeholder='start typing',
#                 validation={'Input too long': lambda value: len(value) < 20}).on('keydown.enter',submit).classes('center')
#     # label = ui.label(f"Please translate: Mangare").classes("fixed-center text-xl")
#     # with ui.row():
#     #     ui.input(label='Text', placeholder='start typing',
#     #             validation={'Input too long': lambda value: len(value) < 20}).on('keydown.enter',submit)

#     #     result = ui.label()
# ui.run()

from nicegui import ui

arr = ['word 1', 'word 2']
target = "mangare"

def submit():
    ui.notify('You clicked me!')

# Set a pastel background for the entire page
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
    ui.label(f"{target}").classes("text-h2 font-bold text-gray-800").style("text-align: center; width: 100%;")

    # Add vertical whitespace
    ui.html("<div style='height: 2rem;'></div>")

    # Input row
    with ui.row().classes("w-full justify-center"):
        ui.input(
            placeholder="start typing",
            validation={"Input too long": lambda value: len(value) < 20},
        ).on("keydown.enter", submit).classes("w-96 text-h3 p-4")

ui.run(title="Italian Practice")
