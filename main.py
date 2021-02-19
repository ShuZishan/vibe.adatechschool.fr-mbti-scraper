from selenium import webdriver
from data_vis import visualize
import getpass
import csv
import json
import time
import sys

def update_db():
    wd_path = __file__.split('/')[:-1]
    wd_path.append('./chromedriver')
    wd_path = '/'.join(wd_path)
    login = input('Login for https://vibe.adatechschool.fr/: ')
    password = getpass.getpass(f'Password for {login}: ')
    driver = webdriver.Chrome(wd_path)
    driver.set_window_size(400,200)
    driver.get("https://vibe.adatechschool.fr/login?redirect_to=https%3A%2F%2Fvibe.adatechschool.fr%2Fmembers")
    userbox = driver.find_element_by_name('username-107')
    passbox = driver.find_element_by_name('user_password-107')
    submit_form = driver.find_element_by_id('um-submit-btn')
    userbox.send_keys(login)
    passbox.send_keys(password)
    submit_form.click()
    time.sleep(1)
    learners_names = driver.find_elements_by_css_selector('.um-member-name a')
    links = {}
    for link in learners_names:
        links[link.text] = link.get_attribute('href')
    mbti = {}
    for k,v in links.items():
        driver.get(v)
        try:
            dissected_mbti = []
            mbti_elem = driver.find_element_by_css_selector('div#mbti_profile-108.um-field-value')
            p_txt = mbti_elem.text.split(' / ')[0][:-2]
            for c in p_txt:
                if c == 'I':
                    dissected_mbti.append("Introvert")
                elif c == 'E':
                    dissected_mbti.append("Extrovert")
                elif c == 'T':
                    dissected_mbti.append("Thinker")
                elif c == 'F':
                    dissected_mbti.append("Feeler")
                elif c == 'S':
                    dissected_mbti.append("Sensor")
                elif c == 'N':
                    dissected_mbti.append("Intuitives")
                elif c == 'J':
                    dissected_mbti.append("Judger")
                elif c == 'P':
                    dissected_mbti.append("Perceiver")
            mbti[k] = [p_txt]+dissected_mbti
        except:
            mbti[k] = ['','','','','']
        print(k,mbti[k])
    driver.close()
    with open('mbti.json','w') as f :
        f.write(json.dumps(mbti,sort_keys=True, indent="\t"))
        f.close()
    with open('mbti.csv','w') as f:
        writer = csv.writer(f,delimiter=",",dialect=csv, lineterminator='\n')
        for k,[a,b,c,d,e] in mbti.items():
            writer.writerow([k,a,b,c,d,e])
        f.close()

def main():
    if "--help" in sys.argv or '-h' in sys.argv:
        print(f"Usage: {sys.argv[0]} [-u | --update]")
    elif "--update" in sys.argv or '-u' in sys.argv:
        update_db()
    visualize()


if __name__=='__main__':
    try:
        main()
    except:
        sys.exit(1)