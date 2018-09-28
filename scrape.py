import sys
from datetime import datetime
from bs4 import BeautifulSoup
from splinter import Browser
from requests import get
from selenium import webdriver
from email import send_email
import re

printers = []
types = ['Centreware -- Full (XEROX Phaser 6700)', 'Centreware -- Small (Xerox WorkCentre 6605)', 'HP Color Laserjet (HP LaserJet CP2025)']



alert_list = []




def analyze_levels(name, list, type, arg):
    global alert_list


    if arg == '':
        alert_list = []





    if type == 'toner':
        for x in range(0, len(list)):
            if int(list[x]) <= 5:

                toner_trimmed = list[1:]  #Gets rid of leading space

                if x == 0:
                    toner_name = 'black'
                    alert = (name + ' is low on ' + toner_name + ' toner(' + list[x] + '%)')
                    alert_list.append(alert)
                elif x == 1:
                    toner_name = 'cyan'
                    alert = (name + ' is low on ' + toner_name + ' toner(' + list[x] + '%)')
                    alert_list.append(alert)
                elif x == 2:
                    toner_name = 'magenta'
                    alert = (name + ' is low on ' + toner_name + ' toner(' + list[x] + '%)')
                    alert_list.append(alert)
                elif x == 3:
                    toner_name = 'yellow'
                    alert = (name + ' is low on ' + toner_name + ' toner(' + list[x] + '%)')
                    alert_list.append(alert)
            else:
                pass

    elif type == 'imaging':
        for x in range(0, len(list)):
            if int(list[x]) <= 5:

                toner_trimmed = list[1:]  #Gets rid of leading space

                if x == 0:
                    toner_name = 'black'
                    alert = (name + ' is low on ' + toner_name + ' imaging(' + list[x] + '%)')
                    alert_list.append(alert)
                elif x == 1:
                    toner_name = 'cyan'
                    alert = (name + ' is low on ' + toner_name + ' imaging(' + list[x] + '%)')
                    alert_list.append(alert)
                elif x == 2:
                    toner_name = 'magenta'
                    alert = (name + ' is low on ' + toner_name + ' imaging(' + list[x] + '%)')
                    alert_list.append(alert)
                elif x == 3:
                    toner_name = 'yellow'
                    alert = (name + ' is low on ' + toner_name + ' imaging(' + list[x] + '%)')
                    alert_list.append(alert)
            else:
                pass
    elif type == 'fuser':
        for x in range(0, len(list)):
            if int(list[x]) <= 5:
                alert = ('Fuser Kit in ' +name+ ' is low(' + list[x] + '%)')
                alert_list.append(alert)
    elif type == 'image_single_percentage':
        for x in range(0, len(list)):
            if int(list[x]) <= 5:
                alert = ('Fuser Kit in ' +name+ ' is low(' + list[x] + '%)')
                alert_list.append(alert)

    elif type == 'maint':
        for x in range(0, len(list)):
            if int(list[x]) <= 5:
                alert = ('Maintenance Kit in ' +name+ ' is low(' + list[x] + '%)')
                alert_list.append(alert)
    elif type == 'waste':
        for x in range(0, len(list)):
            if int(list[x]) <= 5:
                alert = ('Waste Toner in ' +name+ ' is low(' + list[x] + '%)')
                alert_list.append(alert)
    elif type == 'transfer':
        for x in range(0, len(list)):
            if int(list[x]) <= 5:
                alert = ('Transfer Belt in ' +name+ ' is low(' + list[x] + '%)')
                alert_list.append(alert)


    if arg == '':
        compile_alerts(alert_list)



def compile_alerts(list):

    body = ''
    for x in range(0, len(list)):
        body = body + list[x] + '\n'

    if body == '':
        pass
    else:
        print(body)
        send_email(body)

    return




def add_printer_reroute(list, arg):
    id = list[1]
    client_type = list[0]
    specific_name = list[2]

    if id == 0:
        add_centre_full(specific_name, arg)
    elif id == 1:
        add_centre_small(specific_name, arg)
    elif id == 2:
        add_hp(specific_name, arg)
    return

def find_on_page(url, element, unique_char):
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    type(html_soup)
    find = html_soup.find_all(element, unique_char)

    return find


def save_printer(printer_information):

    with open ('printers.txt', 'a') as printer_file:
        printer_file.write(str(printer_information)+'\n')

    return



def checkAllPrinters(list, arg):

    for x in range(0, len(list)):
        add_printer_reroute(list[x][1], arg)

    compile_alerts(alert_list)
    return






def get_added_printers(arg):


    def checkSpecificPrinter(printer_list, arg):

        if arg == '-auto':
            checkAllPrinters(printer_list, arg)
            return

        print('\n')
        printer_selection = int(raw_input('Enter the number that corresponds with the printer you want to check: '))
        printer_list = printer_list
        if printer_selection == len(printer_list):
            checkAllPrinters(printer_list, arg)
        else:
            add_printer_reroute(printer_list[printer_selection][1], arg)
            checkDifferent = raw_input('Would you like to check another printer? (y/n)\n')
            if checkDifferent == 'Y' or checkDifferent == 'y':
                print('\n')
                print('------------------------------------------------------------------')
                print('Printers Added:')
                check_for_printers(arg)
                print('------------------------------------------------------------------\n')
                checkSpecificPrinter(printer_list, arg)

            else:
                print('Have a nice day.')
        return

    def check_for_printers(arg):

        printer_list = []
        list_number = 0
        line_count = 0


        f = open('printers.txt')

        for line in f:
            replaced_line = line.replace("'", "")
            replaced_line = replaced_line.replace('[', '')
            replaced_line = replaced_line.replace(']', '')
            replaced_line = replaced_line.replace('\n', '')
            converted_to_list = replaced_line.split(',')               #Take the line and remove brackets, turn into list

            ## Fixing any formatting errors that may have arisen when copying from the text file ##
            printer_id = int(converted_to_list[1])
            printer_name = converted_to_list[2]
            if printer_name[0] == ' ':
                printer_name = printer_name[1:]


            converted_to_list[1] = printer_id
            converted_to_list[2] = printer_name
            ## ------------------------------------------ ##

            printer_list.append([converted_to_list[2], converted_to_list])  #Append printer name and entire printer properties list in the form of a list within a list
            print('[' +str(list_number)+'] ' + converted_to_list[2])

            list_number +=1
            line_count +=1

        if len(printer_list) != 0: #Don't show 'Run on all' option if there are no printers entered
            print('['+str(list_number) +'] '+ 'Run check on all printers')

        f.close()
        if line_count > 0:
            return [printer_list, True]
        else:
            print('null')
            return [printer_list, False]




    print('------------------------------------------------------------------')
    print('Printers Added:')
    loading_response = check_for_printers(arg)
    printer_list = loading_response[0]   #Returns list of printers with printer information list which will be used to send to add_printer_reroute()
    printersFound = loading_response[1]  #True or False if printers found
    print('------------------------------------------------------------------\n')




    if arg == '-auto':
        checkSpecificPrinter(printer_list, arg)
        return



    if printersFound == False:
        addYN = raw_input("It appears that you have not entered any printers just yet. Would you like to add one now? (y/n)\n")
        if addYN == 'y' or addYN == 'Y':
            add_printer()
        else:
            return

    else:
        useAddedYN = raw_input('Is the printer that you are looking for listed? (y/n)\n')
        if useAddedYN == 'Y' or useAddedYN == 'y':
            checkSpecificPrinter(printer_list, arg)
        else:
            addYN = raw_input("Would you like to add another printer? (y/n)\n")
            if addYN == 'y' or addYN == 'Y':
                add_printer()
            else:
                return







def add_printer():


    print("\nType of printer client:")
    for x in range(0, len(types)):
        print("[" + str(x) + "]" + " " + str(types[x]))
    selected = int(raw_input('Enter corresponding number: '))
    selected_name = types[selected]

    print('What is the name of the printer? (Ex: hersheyprint2)')
    name = raw_input('Name: ')


    printer_information = [selected_name, selected, name]
    add_printer_reroute(printer_information)
    addQuestion = raw_input('Would you like to add this printer to your list of saved printers? (y/n)')
    if addQuestion == 'y' or addQuestion == 'Y':
        save_printer(printer_information)

    addAnotherQuestion = raw_input('Would you like to add another printer? (y/n)')
    if addAnotherQuestion == 'y' or addAnotherQuestion == "Y":
        add_printer()

    return




def add_centre_full(name, arg):


    def percentage_parser(line):

        percent_location = 0
        for x in range(0, len(line)):
            if line[x] == '%':
                percent_location = line[x]
                shortened_line = line[x-3:x]
                for y in range(0, len(shortened_line)):
                    if shortened_line[y] == '"':
                        parsed = shortened_line[y+1:]
                        return(parsed)







    url = 'http://' + name+ '.cshl.edu/status/consumables.php'

    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    type(html_soup)
    find = html_soup.find_all('div', class_ = "horizTherm")




    first_line = str(find[0])
    second_line = str(find[1])
    third_line = str(find[2])
    fourth_line = str(find[3])

    fifth_line = str(find[4])
    sixth_line = str(find[5])
    seventh_line = str(find[6])
    eight_line = str(find[7])
    ninth_line = str(find[8])
    tenth_line = str(find[9])


    black_toner = percentage_parser(first_line)
    cyan_toner = percentage_parser(second_line)
    magenta_toner = percentage_parser(third_line)
    yellow_toner = percentage_parser(fourth_line)

    black_imag = percentage_parser(fifth_line)
    cyan_imag = percentage_parser(sixth_line)
    magenta_imag = percentage_parser(seventh_line)
    yellow_imag = percentage_parser(eight_line)


    fuser = percentage_parser(ninth_line)
    maint_kit = percentage_parser(tenth_line)

    imaging_list = [black_imag, cyan_imag, magenta_imag, yellow_imag]
    toner_list = [black_toner, cyan_toner, magenta_toner, yellow_toner]
    fuser_list = [fuser]
    maint_list = [maint_kit]


    outline = ('----------' +'-'*(len(name)))
    print('\n')
    print(outline)
    print('Printer: ' + name)

    print('\nBlack Toner: '+black_toner)
    print('Cyan Toner: '+cyan_toner)
    print('Magenta Toner: '+magenta_toner)
    print('Yellow Toner: '+yellow_toner)
    print("--------")
    print('Black Imaging: '+black_imag)
    print('Cyan Imaging: '+cyan_imag)
    print('Magenta Imaging: '+magenta_imag)
    print('Yellow Imaging: '+yellow_imag)
    print("--------")
    print('Fuser Kit: ' +fuser)
    print('Maintenance Kit: '+maint_kit)
    print(outline)
    print('\n')

    analyze_levels(name, toner_list, 'toner', arg)
    analyze_levels(name, imaging_list, 'imaging', arg)
    analyze_levels(name, fuser_list, 'fuser', arg)
    analyze_levels(name, maint_list, 'maint', arg)


def add_centre_small(name, arg):


    def percentage_parser(line):

        for x in range(0, len(line)):

            if line[x] == '%':
                shortened_line = line[x-5:x]
                for y in range(0, len(shortened_line)):
                    if shortened_line[y] == '>':
                        parsed = shortened_line[y+1:]
                        return(parsed)



    url = 'http://' + name + '/status/statsuppliesx.htm'
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    type(html_soup)
    find = html_soup.find_all('td', class_="stssupl_xog_3")

    first_line = str(find[0])
    second_line = str(find[1])
    third_line = str(find[2])
    fourth_line = str(find[3])

    fifth_line = str(find[4])
    sixth_line = str(find[5])
    seventh_line = str(find[6])
    eight_line = str(find[7])

    black_toner = str(percentage_parser(fourth_line))
    cyan_toner = percentage_parser(first_line)
    magenta_toner = percentage_parser(second_line)
    yellow_toner = percentage_parser(third_line)


    imag_unit = percentage_parser(fifth_line)
    waste_toner_box = percentage_parser(sixth_line)
    fuser = percentage_parser(seventh_line)
    tranfer_belt = percentage_parser(eight_line)

    toner_list = [black_toner, cyan_toner, magenta_toner, yellow_toner]
    imag_list = [imag_unit]
    waste_list = [waste_toner_box]
    fuser_list = [fuser]
    tranfer_list = [tranfer_belt]

    outline = ('----------' + '-' * (len(name)))
    print('\n')
    print(outline)
    print('Printer: ' + name)

    print('\nBlack Toner: ' + black_toner)
    print('Cyan Toner: ' + cyan_toner)
    print('Magenta Toner: ' + magenta_toner)
    print('Yellow Toner: ' + yellow_toner)

    print("--------")
    print('Imaging Unit Kit: '+ imag_unit)
    print('Waste Toner Box: '+ waste_toner_box)
    print('Fuser Kit: ' + fuser)
    print('Transfer Belt: ' + tranfer_belt)

    print(outline)
    print('\n')

    analyze_levels(name, toner_list, 'toner', arg)
    analyze_levels(name, imag_list, 'image_single_percentage', arg)
    analyze_levels(name, waste_list, 'waste', arg)
    analyze_levels(name, fuser_list, 'fuser', arg)
    analyze_levels(name, tranfer_list, 'transfer', arg)

    return






def add_hp(name, arg):

    def percentage_parser(line):
        for x in range(0, len(line)):
            if line[x] == '%':
                shortened_line = line[x - 5:x]
                for y in range(0, len(shortened_line)):
                    if shortened_line[y] != '':
                        parsed = shortened_line[y + 3:]
                        return (parsed)

    url = 'http://' + name + '.cshl.edu/info_suppliesStatus.html?tab=Status&menu=SupplyStatus'

    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    type(html_soup)
    find = html_soup.find_all('td', class_="SupplyName width10")

    first_line = str(find[0])
    second_line = str(find[1])
    third_line = str(find[2])
    fourth_line = str(find[3])

    black_toner = percentage_parser(first_line)
    cyan_toner = percentage_parser(second_line)
    magenta_toner = percentage_parser(third_line)
    yellow_toner = percentage_parser(fourth_line)

    toner_list = [black_toner, cyan_toner, magenta_toner, yellow_toner]

    outline = ('----------' + '-' * (len(name)))
    print('\n')
    print(outline)
    print('Printer: ' + name)

    print('\nBlack Toner: ' + black_toner)
    print('Cyan Toner: ' + cyan_toner)
    print('Magenta Toner: ' + magenta_toner)
    print('Yellow Toner: ' + yellow_toner)
    print(outline)
    print('\n')

    analyze_levels(name, toner_list, 'toner', arg)













    return





if __name__ == "__main__":
    try:
        arg = str(sys.argv[1])
        get_added_printers(arg)

    except:
        get_added_printers('')

