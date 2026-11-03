from nicegui import ui

label = ui.label('Nifty: --')

def update():
    label.text = f'Nifty: {get_nifty_price()}'

ui.timer(1.0, update)   # har 1 second mein sirf label update
ui.run()
