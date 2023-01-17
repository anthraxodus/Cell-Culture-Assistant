import math
from decimal import Decimal
import PySimpleGUI as sg
from datetime import date


modes_list = ['Pre-Assay', 'Colony Assay']


layout = [[sg.Text('Please, choose your mode of operation:'), sg.Push()],
[sg.Push(), sg.Listbox(values=modes_list, size=(12, 2)), sg.Push()],
[sg.Push(),sg.Button('Ok'), sg.Push()]]

window = sg.Window('Insert Plate Type', layout)

while True:                  # the event loop
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Ok':
        if values[0]:    # if something is highlighted in the list

            plate_dish_choice = values[0][0]
            sg.popup(f"You chose {values[0][0]}.")

            op_mode = values[0][0]

            window.close() 

if op_mode == 'Pre-Assay':

    layout = [[sg.Text('Please, insert your cell culture information: ')],            
                 [sg.Text('Experiment Name: '), sg.InputText(size=12), sg.Push()],
                 [sg.Text('Lineage Name:      '), sg.InputText(size=12), sg.Push()],
                 [sg.Text('Cell growth by cm²:'), sg.InputText(size=12), sg.Push()],
                 [sg.Text('Culture Confl. (%): '), sg.InputText(size=12), sg.Push()],
                 [sg.Push(), sg.Submit(), sg.Cancel(), sg.Push()]]      

    window = sg.Window('Cell Culture Info', layout)    

    event, values = window.read()
    window.close()

    # User choices lists

    plate_dish_type_choice_list = []
    number_of_choice_list       = []
    confuence_of_choice_list    = []


    try:

        # User interaction
        experiment_name    = values[0]
        lineage_name       = values[1]
        cell_growth        = float(values[2])
        culture_confluence = float(values[3])
    
    except:


        layout = [[sg.Push(), sg.Text('Possible Causes:'), sg.Push()],
            [sg.Text('1. Empty fields.'), sg.Push()],
            [sg.Text('2. Non-numeric values under "Cell growth by cm²" and'), sg.Push()],
            [sg.Text('"Culture Confl. (%) fields"'), sg.Push()],
            [sg.Push(),sg.Button('End Application'), sg.Push(),]
            ]

        window = sg.Window('Error!', layout,size=(400, 140))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                break
            break
        window.close()

    else:
            
        growth_sciNot = "{:.2e}".format(cell_growth)
        tdayDate = date.today()

        if culture_confluence == 100:
                culture_confluence = 1
        else:
            culture_confluence = culture_confluence / 100

        cell_growth_by_cm = cell_growth

        # Plate availability list

        available_list = ["D60", "D100", "P6", "P12", "P24", "P48", "P96"]

        new_plate = 'Yes'

        while new_plate == 'Yes':

            layout = [[sg.Text('Please, insert the plate/ dish'), sg.Push()],
            [sg.Text('type that you desire to use: '), sg.Push()],
            [sg.Push(), sg.Listbox(values=available_list, size=(6, 5)), sg.Push()],
            [sg.Push(),sg.Button('Ok'), sg.Push()]]

            window = sg.Window('Insert Plate Type', layout)
            
            while True:                  # the event loop
                event, values = window.read()
                if event == sg.WIN_CLOSED:
                    break
                if event == 'Ok':
                    if values[0]:    # if something is highlighted in the list

                        plate_dish_choice = values[0][0]
                        sg.popup(f"You chose {values[0][0]}.")

                        window.close() 
            
            layout = [[sg.Text('Please, insert the number of plate(s)/ dish(es): '), sg.InputText(size=4), sg.Push()],
            [sg.Push(),sg.Button('Ok'), sg.Push()]]

            window = sg.Window('Number of Plates', layout)

            while True:                  # the event loop
                event, values = window.read()
                if event == sg.WIN_CLOSED:
                    break
                if event == 'Ok':
                    if values[0]:    # if something is highlighted in the list
                        unity_number = values[0]
                window.close() 
            
            unity_number = int(unity_number)

            if unity_number <= 0:
                unity_number = 1

            layout = [[sg.Text('Please, insert the desired confluence (%): '), sg.InputText(size=4), sg.Push()],
                        [sg.Push(),sg.Button('Ok'), sg.Push()]]

            window = sg.Window('Plate(s) Confluence', layout)


            while True:                  # the event loop
                event, values = window.read()
                if event == sg.WIN_CLOSED:
                    break
                if event == 'Ok':
                    if values[0]:    # if something is highlighted in the list
                        confluence_choice = values[0]
                window.close()
            
            confluence_choice = float(confluence_choice)

            if confluence_choice >= 100:
                confluence_choice = 1
            else:
                confluence_choice = confluence_choice / 100

            plate_dish_type_choice_list.append(plate_dish_choice)
            number_of_choice_list.append(unity_number)
            confuence_of_choice_list.append(confluence_choice)

            layout = [[sg.Text('Do you want to add another plate or dish?: '), sg.Push()],
            [sg.Push(),sg.Button('Yes'),sg.Button('No'), sg.Push()]]

            window = sg.Window('New Plate?', layout)

            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'Yes':
                new_plate = 'Yes'
                print(new_plate)
            else:
                new_plate = 'No'

                    
        # print(plate_dish_type_choice_list)
        # print(number_of_choice_list)
        # print(confuence_of_choice_list)

        # Flasks, plates and dishes and their (total) usable area
        
        FlasksPlatesDishes = {
        "T-25"  : 25,
        "T-75"  : 75,
        "T-175" : 175,
        "T-225" : 225,
        "D60"   : 20,
        "D100"  : 56,
        "P6"    : 9.6,
        "P12"   : 48,
        "P24"   : 48,
        "P48"   : 52.8,
        "P96"   : 30.72 
        }

        n = 1
        x = 0

        # Calculate the amount necessary by total cultured flask area in the chosen confluence
        # (Cell growth by cm² * flask total cm²)

        f_T25  = cell_growth_by_cm * FlasksPlatesDishes["T-25"] * culture_confluence
        f_T75  = cell_growth_by_cm * FlasksPlatesDishes["T-75"] * culture_confluence
        f_T175 = cell_growth_by_cm * FlasksPlatesDishes["T-175"] * culture_confluence
        f_T225 = cell_growth_by_cm * FlasksPlatesDishes["T-225"] * culture_confluence

        cells_by_plate_list = []

        for info in plate_dish_type_choice_list:

            # Calculate the amount of cell necessary for the essay in the chosen confluence
            # cell_growth_by_cm * plate/ dish * replicates * percentage decimal

            cell_number = cell_growth_by_cm * FlasksPlatesDishes[info] * number_of_choice_list[x] * confluence_choice

            cells_by_plate_list.append(cell_number)

            n += 1
            x += 1

        y = 1
        z = 0

        real_percentage = culture_confluence * 100

        basic_info = '''=====================================================================\n\nExperiment name: %s \nCell lineage: %s \nCell growth rate by cm²: %s \nAverage percentage of confluence of culture flasks %s \nDate: %s\n''' % (experiment_name, lineage_name, growth_sciNot, real_percentage, tdayDate)

        with open("Exports/Pre-Assay_log.txt", "a") as text_file:
                text_file.write(basic_info)


        for info in plate_dish_type_choice_list:

            scientific_notation = "{:.2e}".format(cells_by_plate_list[z])

            message = "\n- %i unity(ies) of %s at %i percent confluence, needs %s cells" % (number_of_choice_list[z], info ,confuence_of_choice_list[z] * 100, scientific_notation)

            with open("Exports/Pre-Assay_log.txt", "a") as text_file:
                text_file.write(message)

            z += 1
            

        list_sum = sum(cells_by_plate_list)
        total_scientific_notation = "{:.2e}".format(list_sum)
        flask25 = math.ceil(list_sum / f_T25)
        flask75 = math.ceil(list_sum / f_T75)
        flask175 = math.ceil(list_sum / f_T175)
        flask225 = math.ceil(list_sum / f_T225)

        message = '''\n\nFor this assay, in total, %s cells will be needed. That's equivalent to:\n- %ix T-25  culture flask(s). OR\n- %ix T-75  culture flask(s). OR\n- %ix T-125 culture flask(s). OR\n- %ix T-225 culture flask(s).\n\nRational:\ncell_growth_by_cm * plate/ dish * replicates * percentage decimal\n''' % (total_scientific_notation, flask25, flask75, flask175, flask225)

        with open("Exports/Pre-Assay_log.txt", "a") as text_file:
            text_file.write(message)
        
        sg.popup('Your assay calculation is done! Check out the "Pre-Assay_log.txt" file.')

elif op_mode == 'Growth Curve':
    pass

elif op_mode == 'Colony Assay':

    layout = [[sg.Text('Please, insert your experiment information: ')],            
                [sg.Text('Experiment Name: '), sg.InputText(size=12), sg.Push()],
                [sg.Text('Lineage Name:      '), sg.InputText(size=12), sg.Push()],
                [sg.Push(), sg.Submit(), sg.Cancel(), sg.Push()]]      

    window = sg.Window('Experiment Info', layout)    

    event, values = window.read()
    window.close()


    try:

        # User interaction
        experiment_name    = values[0]
        lineage_name       = values[1]
    
    except:


        layout = [[sg.Push(), sg.Text('Possible Cause:'), sg.Push()],
            [sg.Text('Empty fields.'), sg.Push()],
            [sg.Push(),sg.Button('End Application'), sg.Push(),]
            ]

        window = sg.Window('Error!', layout,size=(400, 140))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                break
            break
        window.close()

    # Plate availability list

    available_list = ["P6", "P12", "P24", "P48", "P96"]

    PlateWellNumber = {

    "P6"    :  6,
    "P12"   : 12,
    "P24"   : 24,
    "P48"   : 48,
    "P96"   : 96 
    }

    PlateWellMaxVolumeUl = {

    "P6"   :  3000,
    "P12"  :  2000,
    "P24"  :  1000,
    "P48"  :   400,
    "P96"  :   200 
    }

    layout = [[sg.Text('Please, insert the plate/ dish'), sg.Push()],
    [sg.Text('type that you desire to use: '), sg.Push()],
    [sg.Push(), sg.Listbox(values=available_list, size=(6, 5)), sg.Push()],
    [sg.Push(),sg.Button('Ok'), sg.Push()]]
    

    window = sg.Window('Insert Plate Type', layout)
    
    while True:                  # the event loop
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Ok':
            if values[0]:    # if something is highlighted in the list

                plate_dish_choice = values[0][0]
                sg.popup(f"You chose {values[0][0]}.")

                window.close() 
    
    layout = [[sg.Text('Please, insert the number of plate(s)/ dish(es): '), sg.InputText(size=4), sg.Push()],
    [sg.Push(),sg.Button('Ok'), sg.Push()]]

    window = sg.Window('Number of Plates or Dishes', layout)

    while True:                  # the event loop
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Ok':
            if values[0]:    # if something is highlighted in the list
                unity_number = values[0]
        window.close() 
    
    unity_number = int(unity_number)

    if unity_number <= 0:
        unity_number = 1
    
    # Assay information

    layout = [[sg.Text('Please, insert the number of (total) cells desired for each plate: '), sg.InputText(size=4), sg.Push()],
                [sg.Push(),sg.Button('Ok'), sg.Push()]]

    window = sg.Window('Cell Number', layout)


    while True:                  # the event loop
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Ok':
            if values[0]:    # if something is highlighted in the list
                cell_number = values[0]
        window.close()
    
    cell_number = int(cell_number)
    cell_number2 = cell_number

    

    layout = [[sg.Text('Experiment Container Information: ')],            
                [sg.Text('Container size (ML):'), sg.InputText(size=12), sg.Push()],
                [sg.Push(), sg.Text('Desired culture media per well (μl): '), sg.InputText(size=12), sg.Push()],
                [sg.Push(), sg.Submit(), sg.Cancel(), sg.Push()]]      

    window = sg.Window('Cell Culture Info', layout)    

    event, values = window.read()
    window.close()

    try:

        # User interaction

        container_size = float(values[0])
        media_per_well = float(values[1])

    except:


        layout = [[sg.Push(), sg.Text('Possible Causes:'), sg.Push()],
            [sg.Text('1. Empty fields.'), sg.Push()],
            [sg.Text('2. Non-numeric value'), sg.Push()],
            [sg.Push(),sg.Button('End Application'), sg.Push(),]
            ]

        window = sg.Window('Error!', layout,size=(400, 140))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                break
            break

        window.close()

    # Limit the volume per well up to the max well capacity

    if media_per_well > PlateWellMaxVolumeUl[plate_dish_choice]:

        media_per_well = float(PlateWellMaxVolumeUl[plate_dish_choice]) 

    # print(media_per_well)

    # Calculate the experiment:

    # 1. Added 10% to the user value, because in next steps we will add more 10% media to avoid pippeting error

    if cell_number < 0:
        cell_number = 1
    
    additional_cell = cell_number / 10 

    cell_number = cell_number + additional_cell

    # print(cell_number)

    # 2. Calculate the necessary number of dilutions

    dilutions_values_list = []

    dilutions_values_list.append(cell_number)

    number_of_dilutions = 0

    while cell_number < 10000:

        cell_number = cell_number * 10

        number_of_dilutions += 1

        dilutions_values_list.append(cell_number)

    # 3. Calculate the total volume for one plate

    TotalVolume = media_per_well * PlateWellNumber[plate_dish_choice] 

    # Added 10% to the user value, because in next steps we will add more 10% media to avoid pippeting error

    additional_volume = TotalVolume / 10

    TotalVolume = TotalVolume + additional_volume

    # Number of tubes

    total_tubes = number_of_dilutions * unity_number

    #print(dilutions_values_list)

    # Reverse the list and transform to scientific notation

    dilutions_values_list.reverse()

    dilutions_values_list = ["{:.2e}".format(Decimal(member)) for member in dilutions_values_list]

    # print(dilutions_values_list)

    # Printing the protocol'
    
    msg1 = 'Assay Name: {0}'.format(experiment_name)
    msg2 = 'Date: {0}'. format(date.today())
    msg3 = 'Cell Lineage: {0}'.format(lineage_name)
    msg4 = 'Plate of choice: {0}'.format(plate_dish_choice)
    msg5 = 'Total replicates: {0}'.format(unity_number)
    msg6 = 'Total volume per well (μL): {0}'.format(media_per_well)
    msg7 = 'Total number of cells (by plate): {0}'.format(cell_number2)

    protocol_info = 'Materials Required: \n'

    msg8 = '- {0}x {1} ML tubes.'.format(total_tubes, container_size)
    msg9 = '- {0}x {1} plate(s).'.format(unity_number, plate_dish_choice)
    msg10 = '- Culture media and trypsin.'
    msg11 = '- Previously counted cells. \n'

    protocol = 'Protocol'

    msg12 = '1. For each of the {0} replicate(s), prepare 1 stock solution containing {1} cells in {2} ML. \n'.format(unity_number, dilutions_values_list[0] , TotalVolume / 1000)

    dilutions_values_list.pop(0)

    msg13 = '2. For the {0} subsequent dilution(s), add {1} ML of culture media in each tube. \n'.format(number_of_dilutions - 1, (TotalVolume - TotalVolume/10) / 1000)


    # print(msg12)
    # print(msg13)

    msg14 = '3. Now transfer {0} ML from the stock tube to the first dilution tube, then transfer {0} from second tube to the third and so on.'.format((TotalVolume/10)/1000)
    msg15 = 'The sequence of dilutions will contain the following number of cells: '

    final_message1 = (msg1 + '\n' + msg2 + '\n' + msg3 + '\n' + msg4 + '\n' + msg5 + '\n' + msg6 + '\n' +msg7 + '\n'+'\n' + protocol_info + '\n' +
    msg8 + '\n' + msg9 + '\n' + msg10 + '\n' + msg11 + '\n' + protocol + '\n' + '\n' + msg12 + '\n' + msg13 + '\n' + msg14 + '\n' +
    msg15 + '\n')

    with open("Exports/Colony_Assay_log.txt", "a") as text_file:
            text_file.write(final_message1)

    # print(msg14)
    # print(msg15)

    dilution_count = 1

    for element in dilutions_values_list:

        msg16 = '- Dilution {0}: {1} '.format(dilution_count, element)

        with open("Exports/Colony_Assay_log.txt", "a") as text_file:
            text_file.write(msg16 + '\n')

        dilution_count += 1

        # print(msg16)

    msg17 = "4. After reaching the last tube, use it to add {0} μL to each well of the {1}".format(media_per_well, plate_dish_choice)
    msg18 = "* This assay adds 10 percent of media volume and cells to avoid pipetting errors. \n"
    msg19 = '=====================================================================\n\n'

    final_message2 = ('\n' + msg17 + '\n' + msg18 + msg19)

    with open("Exports/Colony_Assay_log.txt", "a") as text_file:
            text_file.write(final_message2)

    sg.popup('Your assay calculation is done! Check out the "Colony_assay_log.txt" file.')
    
