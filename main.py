from nicegui import ui

@ui.page('/')
def index():
    pcr = 1.25  # baad me ye Upstox API se aayega
    stock = "RELIANCE"
    
    if pcr > 1.0:
        signal, col = "LONG", "green"
    elif pcr < 0.9:
        signal, col = "SHORT", "red"
    else:
        signal, col = "NO TRADE", "orange"

    with ui.column().classes('items-center w-full p-8'):
        ui.label('Ustad Stock PCR Dashboard').classes('text-3xl font-bold')
        ui.label(f'{stock} PCR: {pcr}').classes('text-xl')
        ui.button(f'SIGNAL: {signal}').props(f'color={col} size=lg')

ui.run(host='0.0.0.0', port=8080)
