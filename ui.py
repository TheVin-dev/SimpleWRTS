from nicegui import ui 
arr = ['word 1', 'word 2']

def submit():
    ui.notify('You clicked me!')
    # ui.icon('thumb_up', color='primary').classes('text-5xl')

with ui.card().classes("fixed-center w-full max-w-3xl mx-auto shadow-lg"):
    ui.label("SimpleWRTS").classes("center-top text-h1 font-bold")
    label = ui.label(f"Please translate: Mangare").classes("fixed-center text-xl")
    with ui.row():
        ui.input(label='Text', placeholder='start typing',
                validation={'Input too long': lambda value: len(value) < 20}).on('keydown.enter',submit)

        result = ui.label()
ui.run()