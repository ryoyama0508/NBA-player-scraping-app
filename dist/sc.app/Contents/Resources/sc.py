import requests
from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv
import os
import shutil
from datetime import datetime


import tkinter as tk
from tkinter import messagebox


def scrape():
    hashtable = {"POR": "",
                 "OKC": "",
                 "MIA": "",
                 "SAS": "",
                 "NOP": "",
                 "BKN": "",
                 "ORL": "",
                 "MIL": "",
                 "PHX": "",
                 "CHA": "",
                 "SAC": "",
                 "DAL": "",
                 "NYK": "",
                 "DEN": "",
                 "WAS": "",
                 "CLE": "",
                 "ATL": "",
                 "IND": "",
                 "DET": "",
                 "GSW": "",
                 "BOS": "",
                 "CHI": "",
                 "HOU": "",
                 "LAC": "",
                 "MEM": "",
                 "MIN": "",
                 "UTA": "",
                 "PHI": "",
                 "TOR": "",
                 "LAL": "",
                 }
    input_team1 = txtBox1.get()
    input_team2 = txtBox2.get()

    if input_team1 == input_team2:
        messagebox.showerror("チーム選択エラー", "同じチームを選んでいます")
        return
    elif input_team1 not in hashtable.keys():
        messagebox.showerror("チーム選択エラー", "一つ目のチームがリーグにありません")
        return
    elif input_team2 not in hashtable.keys():
        messagebox.showerror("チーム選択エラー", "二つ目のチームがリーグにありません")
        return

    tk.messagebox.showinfo(
        title="start scraping", message="スクレイプスタート")

    url = "https://jp.global.nba.com/playerindex/"
    options = Options()
    """ options.add_argument('--headless') """
    driver = webdriver.Chrome(
        executable_path='/usr/local/bin/chromedriver', chrome_options=options)
    driver.set_window_size(1350, 640)
    driver.get(url)
    time.sleep(3)

    tk.messagebox.showinfo(
        title="finished scraping", message="click")

    driver.find_element_by_xpath(
        "/html/body/div[3]/div[3]/div/div/div[2]/div/div/button").click()

    time.sleep(5)

    tk.messagebox.showinfo(
        title="finished scraping", message="before")

    a_to_z_buttons = driver.find_elements_by_xpath(
        "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/section/div/div/div/div/div[3]/div[2]/div[2]/div")

    href_list_team1, href_list_team2 = [], []
    for i in range(1, len(a_to_z_buttons)):
        elems = driver.find_elements_by_xpath("//tbody/tr")
        for j in range(0, len(elems)):
            if input_team1 in elems[j].text:
                elem = elems[j].find_element_by_xpath(".//td/a[2]")
                href_list_team1.append(elem.get_attribute('href'))
            if input_team2 in elems[j].text:
                elem = elems[j].find_element_by_xpath(".//td/a[2]")
                href_list_team2.append(elem.get_attribute('href'))
        a_to_z_buttons[i].click()
        time.sleep(2)

    elems = driver.find_elements_by_xpath("//tbody/tr")
    for i in range(0, len(elems)):
        if input_team1 in elems[i].text:
            elem = elems[i].find_element_by_xpath(".//td/a[2]")
            href_list_team1.append(elem.get_attribute('href'))
        if input_team2 in elems[i].text:
            elem = elems[i].find_element_by_xpath(".//td/a[2]")
            href_list_team2.append(elem.get_attribute('href'))

    driver.get(url)
    time.sleep(3)

    current_time = datetime.now()

    with open('player_info_' + input_team1 + "_" + str(current_time)[5:10] + "_" + str(current_time)[11:16]+'.csv', mode='w', newline='') as csvfile:
        tk.messagebox.showinfo(
            title="start scraping", message="file is opened")
        writer = csv.writer(csvfile)
        result = []
        for link in href_list_team1:
            driver.get(link)
            time.sleep(5)
            name = driver.find_element_by_xpath(
                "//h2/a/span[1]").text + driver.find_element_by_xpath("//h2/a/span[3]").text

            body_info = driver.find_element_by_xpath(
                "//section/div/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[2]/p[2]").text

            ppg = driver.find_element_by_xpath(
                "//*[@id='cs-ppg']/span").text

            rpg = driver.find_element_by_xpath(
                "//*[@id='cs-rpg']/span").text

            apg = driver.find_element_by_xpath(
                "//*[@id='cs-apg']/span").text

            ft_per = driver.find_element_by_xpath(
                "//*[@id='cs-ftpct']/span").text

            three_per = driver.find_element_by_xpath(
                "//*[@id='cs-tppct']/span").text
            single_row = [name, body_info, ppg, rpg, apg, ft_per, three_per]
            result.append(single_row)
            driver.back()
            time.sleep(3)

        writer.writerows(result)

    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, "../../../../../")
    shutil.move(str(script_dir) + 'player_info_' + input_team1 + "_" + str(current_time)
                [5:10] + "_" + str(current_time)[11:16]+'.csv', str(abs_file_path))

    with open('player_info_' + input_team2 + "_" + str(current_time)[5:10] + "_" + str(current_time)[11:16]+'.csv', mode='w', newline='') as csvfile:
        tk.messagebox.showinfo(
            title="start scraping", message="2nd file is opened")
        writer = csv.writer(csvfile)
        result = []
        for link in href_list_team2:
            driver.get(link)
            time.sleep(5)
            name = driver.find_element_by_xpath(
                "//h2/a/span[1]").text + driver.find_element_by_xpath("//h2/a/span[3]").text

            body_info = driver.find_element_by_xpath(
                "//section/div/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[2]/p[2]").text

            ppg = driver.find_element_by_xpath(
                "//*[@id='cs-ppg']/span").text

            rpg = driver.find_element_by_xpath(
                "//*[@id='cs-rpg']/span").text

            apg = driver.find_element_by_xpath(
                "//*[@id='cs-apg']/span").text

            ft_per = driver.find_element_by_xpath(
                "//*[@id='cs-ftpct']/span").text

            three_per = driver.find_element_by_xpath(
                "//*[@id='cs-tppct']/span").text
            single_row = [name, body_info, ppg, rpg, apg, ft_per, three_per]
            result.append(single_row)
            driver.back()
            time.sleep(3)

        writer.writerows(result)
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, "../../../../../")
    shutil.move(str(script_dir) + 'player_info_' + input_team2 + "_" + str(current_time)
                [5:10] + "_" + str(current_time)[11:16]+'.csv', str(abs_file_path))

    driver.close()
    tk.messagebox.showinfo(
        title="finished scraping", message="スクレイプが終了しました")


win = tk.Tk()
win.title("NBA Scraping")
win.geometry("400x300")

label1 = tk.Label(text='write teams')
label1.place(x=5, y=5)

txtBox1 = tk.Entry()
txtBox1.configure(state='normal', width=30)
txtBox1.place(x=100, y=5)

txtBox2 = tk.Entry()
txtBox2.configure(state='normal', width=30)
txtBox2.place(x=100, y=50)

button = tk.Button(text='excel表を作る', command=scrape, width=30)
button.place(x=90, y=120)

win.mainloop()
