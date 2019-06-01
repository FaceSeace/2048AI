from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from AI import AI
import numpy as np
import random
import time
import re

Ai = AI()
driver = webdriver.Chrome()
driver.maximize_window()
#driver.set_page_load_timeout(5)
try:
    driver.get('https://agneei.github.io/2048-game.github.io/')
except:
    pass

html = driver.find_element_by_tag_name('html')

for j in range(1500):

    htmls = driver.page_source
    grid = re.findall(r';">(.*?)</div>', str(BeautifulSoup(htmls, 'lxml').find_all(class_='number-cell')))

    for i in range(16):
        if grid[i]:
            grid[i] = int(grid[i])
        else:
            grid[i] = 0

    grid = np.array(grid).reshape((4, 4)).tolist()

    action = Ai.get_move(grid)
    if action == 'Up':
        html.send_keys(Keys.UP)
    elif action == 'Down':
        html.send_keys(Keys.DOWN)
    elif action == 'Left':
        html.send_keys(Keys.LEFT)
    elif action == 'Right':
        html.send_keys(Keys.RIGHT)
    else:
        break
    time.sleep(0.2)

while(True):
    pass
time.sleep(2)

driver.quit()
