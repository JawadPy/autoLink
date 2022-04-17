from win10toast import ToastNotifier
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException   
from sys import exit as ext
from time import sleep
import os

driver = None
wait = None
PAGE = 1
TOTAL_CONNECTIONS = 0

# force to send:
# #<div id="ember134" class="artdeco-modal-overlay artdeco-modal-overlay--layer-default artdeco-modal-overlay--is-top-layer  ember-view">

def notifier(msg):
    t = ToastNotifier()
    t.show_toast(msg, threaded=True, icon_path=None, duration=5)
    while t.notification_active():
        sleep(0.1)


def getLink(PAGE=1):
    return str(entry_4.get() + f'&page={PAGE}')

def init_browser(waitTimeout=3, exePath=(os.getcwd() + '/chromedriver.exe')):
    global driver, wait
    driver = webdriver.Chrome(
        executable_path=(exePath)
        )
    wait = WebDriverWait(driver,waitTimeout)


def login(IN_USERNAME, IN_PASSWORD, IN_LOGLINK=None):
    try:
        if (IN_LOGLINK is None) or (len(IN_LOGLINK) < 10):
            driver.get(r'https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Ffeed%2F&fromSignIn=true&trk=cold_join_sign_in')
            
            wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,('input[id="username"]')))
                ).send_keys(IN_USERNAME,Keys.ENTER)

            wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,('input[id="password"]')))
                ).send_keys(IN_PASSWORD,Keys.ENTER)
        else:
            driver.get(IN_LOGLINK)
    except TimeoutException:
        notifier('Timeout!')
        print('[ERR] Timeout!')
        

def is_limited():
    try:
        driver.find_element_by_css_selector(
        'button[class="artdeco-button ip-fuse-limit-alert__primary-action artdeco-button--2 artdeco-button--primary ember-view"]'
        )
    except NoSuchElementException:
        return False

    return True

def getConnections(PAGE=1):
    try:
        driver.get(getLink(PAGE))
        return driver.find_elements_by_css_selector(
            'button[class="artdeco-button artdeco-button--2 artdeco-button--secondary ember-view"]'
            )
    except TimeoutException:
        notifier('Timeout!')
        print('[ERR] Timeout! ')
        return []

def connect2All(connections, allow=['Follow', 'Connect']):
    try:
        for connect in connections:
            if connect.text in allow:
                connect.click()
                try:
                    if connect.text == 'Connect':
                        wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR,('button[aria-label="Send now"]')))
                            ).click()
                        yield 1
                    else:
                        yield 1
                except ElementClickInterceptedException:
                    if is_limited():
                        notifier('You reached your weekly limit!')
                        print('[INFO] Reached the limits!')
                        ext()

                except Exception as e:
                    print(str(e))
                    yield 0
    except Exception as e:
        print(str(e))
        return 0


def main(ALLOW=['Follow', 'Connect']):
    global TOTAL_CONNECTIONS, PAGE

    init_browser()
    login(entry_1.get(),entry_2.get(),entry_3.get()) #username, 
    while TOTAL_CONNECTIONS <= 500: # set any limit, 500 is like unlimited
        sleep(3)
        for connect in connect2All(getConnections(PAGE=PAGE), allow=ALLOW):
            TOTAL_CONNECTIONS += connect
            print('[CON] New connection made.')
        PAGE+=1
        notifier(f'''
        Connected to {TOTAL_CONNECTIONS} person.
        Reached page number {PAGE}.
        ''')
        print(f'''
        [INFO] Connected to {TOTAL_CONNECTIONS} person.
        [INFO] Reached page number {PAGE}.
        ''')

def relative_to_assets(path: str) -> Path:
    return r'{}\assets\{}'.format(os.getcwd(), path)
def gui():
    global entry_1, entry_2, entry_3, entry_4
    window = Tk()

    window.geometry("784x524")
    window.configure(bg = "#FFFFFF")
    window.title('autoLink - by Jawad')

    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 524,
        width = 784,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        112.5,
        48.5,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#C4C4C4",
        highlightthickness=0
    )
    entry_1.place(
        x=35.0,
        y=29.0,
        width=155.0,
        height=37.0
    )

    canvas.create_text(
        28.0,
        14.0,
        anchor="nw",
        text="Username",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        336.5,
        48.5,
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#C4C4C4",
        highlightthickness=0,
        show="*"
    )
    entry_2.place(
        x=259.0,
        y=29.0,
        width=155.0,
        height=37.0
    )

    canvas.create_text(
        252.0,
        14.0,
        anchor="nw",
        text="Password",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        674.5,
        48.5,
        image=entry_image_3
    )
    entry_3 = Entry(
        bd=0,
        bg="#C4C4C4",
        highlightthickness=0
    )
    entry_3.place(
        x=597.0,
        y=29.0,
        width=155.0,
        height=37.0
    )

    canvas.create_text(
        590.0,
        14.0,
        anchor="nw",
        text="one-time link",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
        382.5,
        297.5,
        image=entry_image_4
    )
    entry_4 = Entry(
        bd=0,
        bg="#C4C4C4",
        highlightthickness=0
    )
    entry_4.place(
        x=133.0,
        y=278.0,
        width=499.0,
        height=37.0
    )

    canvas.create_text(
        126.0,
        263.0,
        anchor="nw",
        text="Connect from:",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_rectangle(
        20.0,
        79.0,
        767.0,
        81.0,
        fill="#000000",
        outline="")

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: main(),
        relief="flat"
    )
    button_1.place(
        x=475.0,
        y=328.0,
        width=172.0,
        height=39.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: main(['Connect']),
        relief="flat"
    )
    button_2.place(
        x=118.0,
        y=328.0,
        width=104.0,
        height=39.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: main(['Follow']),
        relief="flat"
    )
    button_3.place(
        x=232.0,
        y=328.0,
        width=104.0,
        height=39.0
    )

    canvas.create_text(
        244.0,
        155.0,
        anchor="nw",
        text="autoLink",
        fill="#000000",
        font=("Inter Bold", 70 * -1)
    )
    window.resizable(False, False)
    window.mainloop()

if __name__ == '__main__':
    gui()
