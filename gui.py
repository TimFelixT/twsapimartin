import eel
import time
if __name__ == '__main__':
    from data import DataStock
    eel.init('web')
    eel.start('main_page.html', size=(800, 600),disable_cache=True,block=False)
    data_stock = DataStock(tickers=[])
    while True:
        data_stock.update()
        time.sleep(1)
