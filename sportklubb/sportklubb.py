import PySimpleGUI as sg
# from register import Member, Address, datetime, Club
from register import datetime, Club # operator
# import operator



Club.CreateDB()
# Converts the Member table into a list that is compatible with pysimpleGUI table element
all_members_query = Club.Select()
members_list = Club.create_table_list(all_members_query)

# Sets theme and font settings
sg.theme('DarkBlue')
sg.set_options(font=('Courier', 12, 'bold'))

# Headings used for the table
headings = ['Medlemsnr', 'Förnamn', 'Efternamn', 'Medlemsdatum', 'Betald Avgift']
active_search = False


hemsida = [
    [sg.Text("",)],
    [sg.Text("SOLIGA SPORTKLUBBEN",)],
    [sg.Text("",)],
    [sg.Text("          I våran app kan ni:"), sg.Push()],
    [sg.Text("               ¤ Söka bland befintliga medlemmar"),sg.Push()],
    [sg.Text("               ¤ ta bort och registrera nya"),sg.Push()],
    [sg.Text("               ¤ administrera medlemsavgifter"), sg.Push()],
    [sg.Text("               ¤ sortera tabellen via rubrikerna"), sg.Push()],
    [sg.Text("",)],
    [sg.Image(filename="homepage_pic.PNG", size=(600,400))],
    [sg.Push(), sg.Button('Exit', button_color = 'white on red')]
]

register = [
    [sg.Table(values=members_list, headings=headings ,max_col_width=35,
                    display_row_numbers=False,
                    auto_size_columns=True,
                    justification='right',
                    num_rows=10,
                    key='-TABLE-',
                    row_height=35,
                    enable_click_events = True, # to be able to click on rows in the table
                    )],
    [sg.Text("Sök efter medlem ->"), sg.Input(size=(35, 30), key='-MEMBER_SEARCH-'), sg.Button('SÖK'), sg.Button('Visa Alla')],
    [sg.Text("Sök med medlemsnummer eller förnamn ↑ ↑ ↑")],
    [sg.Button('Visa Adress'), sg.Button('Ändra medlemsavgfitstatus'), sg.Button('Ta bort medlem')],
    [sg.Push(), sg.Button('Exit', button_color = 'white on red', key='-EXIT2-')]   
]


medlemsregistrering = [
    [sg.Text("Vänligen skriv in medlemsuppgifter nedan")],
    [sg.Text("Förnamn:"), sg.Input(key='-FÖRNAMN-', do_not_clear=True, size=(20, 1)), 
    sg.Text("Efternamn:"), sg.Input(key='-EFTERNAMN-', do_not_clear=True, size=(20, 1))],
    [sg.Text("")],
        
    [sg.Text("Startdatum för medlemskap ->"), sg.CalendarButton("Välj datum", target='-DATE-')],
    [sg.Input(key='-DATE-', visible=True, disabled = True, background_color= 'green', text_color = "black")],  
    [sg.Text("Betald medlemsavgift:"), sg.Radio('Ja', "-RADIO-", key="-RADIO-YES-"), sg.Radio('Nej', "-RADIO-", key="-RADIO-NO-")],
    [sg.Text("")],
    [sg.Text("")],
        
    [sg.Text("Skriv in adressuppgifter:")],
    [sg.Text("Gata:",size=(20, 1)), sg.Input(key="-GATA-", do_not_clear=True, size=(20, 1))],
    [sg.Text("Postnummer:",size=(20, 1)), sg.Input(key='-POSTNUMMER-', do_not_clear=True, size=(20, 1))],
    [sg.Text("Postort:",size=(20, 1)), sg.Input(key='-POSTORT-', do_not_clear=True, size=(20, 1))],
    [sg.Text("")],
    [sg.Button("Registrera klubbmedlem!")],
    [sg.Text("")],
    [sg.Text("Om ni ENBART vill addera en adress till en befintlig klubbmedlem")],
    [sg.Text("ange då medlemsnummret här:"), sg.Input(key='-BEFINTLIG-', size=(7, 1)), sg.Text("samt tryck på ->"), sg.Button("+Adress")],
    [sg.Push(), sg.Button('Exit', button_color = 'white on red', key='-EXIT3-')] 
]

# I decided to go with tabs instead of multiple windows
tab_group = [
    [sg.TabGroup(
        [[sg.Tab('Hemsida', hemsida, element_justification= 'center'),
        sg.Tab('Medlemsregister', register),
        sg.Tab('Ny Medlem', medlemsregistrering)]], 
                    
        tab_location='centertop',
        title_color='white',selected_title_color='white',
        selected_background_color='#111fc2', border_width=5)]]

window =sg.Window("Sportsklubbregister",tab_group, resizable=True)

while True:
    event, values=window.read()
    # if event == "Exit" or event == sg.WIN_CLOSED:
    if event in (sg.WINDOW_CLOSED, 'Exit', '-EXIT2-', '-EXIT3-'):
        break
    
    # only table events are in tuple form so is instance tuple = table event
    if isinstance(event, tuple):
        if event[0] == '-TABLE-':
            # checks if any of the headers are clicked
            if event[2][0] == -1 and event[2][1] != -1:
                col_num_clicked = event[2][1]
                # sorts the selected column by the sorting function key
                new_table = Club.sort_table(members_list, col_num_clicked)
                if active_search:
                    found_member = new_table
                    # reloads the sorted table
                    window['-TABLE-'].update(found_member)
                if not active_search:
                    members_list = new_table
                    # reloads the sorted table
                    window['-TABLE-'].update(members_list)
    
    if event == "SÖK":      
        memberSearch = values['-MEMBER_SEARCH-']
        
        # if teh user puts in a digt (for memberID) then the search_by_id method gets run
        # else we assume its a string and a first name (since that is waht we are asking for)
        if memberSearch.isdigit():  
            found_member =  Club.search_by_id(memberSearch)
            window['-TABLE-'].update(values=found_member)
            active_search = True
        else:
            found_member = Club.search_by_name(memberSearch)
            window['-TABLE-'].update(values=found_member)
            active_search = True
            

    # reloads the current members in the Member table
    if event == 'Visa Alla':    
        # reloads the table to get the active members displayed    
        all_members_query = Club.Select()
        members_list = Club.create_table_list(all_members_query)
        window['-TABLE-'].update(values=members_list)        
        # sets active search to False so that members_list becomes the default list_lookup
        active_search = False
        
    
    if event == 'Ta bort medlem':
        # get index the selected member from the table in int format      
        del_index = values['-TABLE-'][0]
        # use that index in the members list to get the memberID
        
        # check if a search is ongoing (which determines which list is loaded byt the table element)
        if active_search:
            member_to_remove = found_member[del_index][0]
            memberName = found_member[del_index][1]
            
        if not active_search:
            member_to_remove = members_list[del_index][0]
            memberName = members_list[del_index][1]
        
        # uses the memberID to delete the member
        Club.Delete(member_to_remove)
        # reloads the table to get the active members    
        all_members_query = Club.Select()
        members_list = Club.create_table_list(all_members_query)
        window['-TABLE-'].update(values=members_list)
        # generate popup to make it extra clear
        sg.Popup(f"{memberName} (medlem {member_to_remove}) har tagits bort från registret")
        # since the table has been repopulated , active search is reset
        active_search = False
    
    if event == 'Visa Adress':
        # get index the selected member from the table in int format      
        address_index = values['-TABLE-'][0]
        # use that index in either the members_list or found_member depending if the user has an active query/search ...
        # which is what the active search flag checks for    
        if active_search:
            address_to_display = found_member[address_index][0]
        if not active_search:
            address_to_display = members_list[address_index][0]
       
        # get the address from the Members table by using the relation it has with the address table
        member = Club.get_member(address_to_display)
        # format the __repr__ dunder into better looking string
        display_address = Club.format_address(member)
        sg.Popup(f"{member.first_name} bor här: \n {display_address}")
        
    if event == 'Ändra medlemsavgfitstatus':
        # get index the selected member from the table in int format      
        selected_member = values['-TABLE-'][0]
            
        if active_search:
            # get memberID from the selected member in the table
            member = found_member[selected_member][0]
            # # use the index of selected member to get the member's name and due fee status
            memberName = found_member[selected_member][1]
            current_due_fee = found_member[selected_member][4]
        if not active_search:
            # get memberID from the selected member in the table
            member = members_list[selected_member][0]
            # use the index of selected member to get the member's name and due fee status
            memberName = members_list[selected_member][1]
            current_due_fee = members_list[selected_member][4]

        # the change_due_date converts string into bool and changes the value in the database
        Club.change_due_date(member, current_due_fee)
        # # Reload the database to get current member information
        all_members_query = Club.Select()
        members_list = Club.create_table_list(all_members_query)            
        
        # check if a search is ongoing (which determines which list is loaded byt the table element)     
        if active_search:
            if memberSearch.isdigit():  
                found_member =  Club.search_by_id(memberSearch)
                window['-TABLE-'].update(values=found_member)
            else:
                found_member = Club.search_by_name(memberSearch)
                window['-TABLE-'].update(values=found_member)
        if not active_search:
            window['-TABLE-'].update(values=members_list)
        # generate popup to make it extra clear
        sg.Popup(f"{memberName} medlemsavgfitstatus har ändrats!")
        
    if event == 'Registrera klubbmedlem!':
        
        # checks if the values from the input elements are empty (besides the radio element)
        if not all([values['-FÖRNAMN-'], values['-EFTERNAMN-'], values['-DATE-'], 
                                    values["-GATA-"], values["-POSTNUMMER-"], values["-POSTORT-"]]):
            sg.Popup(f"Fyll i ALLA fält som hör till registreringen av ny medlem!")
            continue
         
        # checking the state of the radio buttons and assigning that state to the due_fee variable
        if values['-RADIO-YES-']:
            betald_medlemsavgift = False
        elif values['-RADIO-NO-']:
            betald_medlemsavgift = True
        
        # converting pysimplegui native string time format into dateTime
        datetime_object = datetime.strptime(values['-DATE-'], '%Y-%m-%d %H:%M:%S')   
        
        # Getting all the info from the form (besides the ones relating to existing member and new address)
        member_information_list = [values['-FÖRNAMN-'], values['-EFTERNAMN-'], datetime_object, betald_medlemsavgift, 
                                    values["-GATA-"], values["-POSTNUMMER-"], values["-POSTORT-"]]
        
        
        # calling the insert method that puts the member information into the Member table
        # and the address information into the Address table.
        Club.Insert(member_information_list)
        
        # Reload the database to get current member information
        all_members_query = Club.Select()
        members_list = Club.create_table_list(all_members_query)
        window['-TABLE-'].update(values=members_list)
        
        # generate popup to make it extra clear
        sg.Popup(f"{values['-FÖRNAMN-']} är vår nya medlem!")
          
    if event == "+Adress":
        
        # checks if the values from the relevant input elements are empty or zero
        if not all([values["-GATA-"], values["-POSTNUMMER-"], values["-POSTORT-"], int(values['-BEFINTLIG-'])]):
            sg.Popup(f"Fyll i ALLA fält som hör till registrering av en till adress!")
            continue    
        
    
        # converts the memberID from string to int
        memberID_int = int(values['-BEFINTLIG-']) 
        # Gets the address info from the form
        address_info = [values["-GATA-"], values["-POSTNUMMER-"], values["-POSTORT-"], memberID_int]
        
        # runs the Club method that checks if the address is already registerd on the current user
        # the method returns a bool which is used to decide which popup to display
        if (Club.insert_only_address(address_info)):
            # generate popup to make it extra clear
            sg.Popup(f"Den här adressen är redan registrerad på denna medlem")
        else:
            # generate popup to make it extra clear
            sg.Popup(f"Ny address registrerad!")
        
        # Reload the database to get current member information
        all_members_query = Club.Select()
        members_list = Club.create_table_list(all_members_query)
        window['-TABLE-'].update(values=members_list)
            
window.close()