#!/usr/bin/env python3
"""Analyse a vampire infiltration.
Student number: 21006650
"""

import sys
import os.path
from format_list import format_list, format_list_or, str_time, is_initial, period_of_time, day_of_time, time_of_day


# Section 2
def file_exists(file_name):
    """Verify that the file exists.

    Parameter:
        file_name (str): name of the file

    Returns:
        boolean: returns True if the file exists and False otherwise.
    """
    if os.path.isfile(file_name) == True:
        return True
    else:
        return False


# Section 3        
def days_data(days, tokens):
    """
    construct a new days list of pairs including all data above 
    by appending the empty days list by extracting the information about 
    testing data and contact group data of each day from the tokens list 

    Parameters:
        days:   an empty list at the beginning
        tokens: a list where each element represents a line from the file.
    """
    day_number = int(tokens[1])
    k = 1
    for i in range(day_number):
        day_data = []
        testing_data = tokens[1+k]
        if testing_data == '##':  # no test that day
            day_data.append({})
        else:
            tmp_dict = {}
            testing_data_tokens = testing_data.split(',')
            for i1 in range(len(testing_data_tokens)):
                testing_data_token = testing_data_tokens[i1].strip()
                name = testing_data_token.split(':')[0].strip()
                isVampire = testing_data_token.split(':')[1].strip()
                if isVampire == 'V':    
                    tmp_dict[name] = True  # the individual is vampire
                else:
                    tmp_dict[name] = False # the individual is not vampire
            day_data.append(tmp_dict)
        k = k+1
        group_number = int(tokens[1+k])
        contact_list = []
        for j in range(group_number):
            k = k+1
            contact_data = tokens[1+k]
            contact_data_tokens = contact_data.split(',')
            contact_tmp = []
            for name in contact_data_tokens:   # find contacts
                name = name.strip()
                contact_tmp.append(name)
            contact_list.append(contact_tmp)
        k = k+1
        day_data.append(contact_list)
        day_data = tuple(day_data)
        days.append(day_data)


def parse_file(file_name):
    """
    Read the input file, parse the contents and return some data structures
    that contain the associated data for the vampire infiltration.

    Parameter:
        file_name (str): Contains the name of the file.

    Returns:
        participants: list 
            a list of participants.
        days: list of pairs
            the first element of a pair is the result of tests,
            (dictionary from participants to "H"/"V"). 
            the second is a list of contact groups 
    """
    try:
        participants = []
        days = []
        f = open(file_name, 'r')         
        content = f.read()                
        tokens = content.split('\n')     
        participants_string = tokens[0]     # get participants
        tokens_participants = participants_string.split(',')
        for i in range(len(tokens_participants)):
            name = tokens_participants[i]
            name = name.strip()         
            participants.append(name)
        days_data(days, tokens)
        f.close()
        return (participants,days)
    # error situation: the file isn’t somehow formatted correctly
    except Exception as e:
        print('Error found in file, aborting.')
        sys.exit()


# Section 4
def participants_summary(participants, day_number):
    """ 
    find the total number of days and participants from data, 
    then print the summary sentence in the exact required format

    Parameters:
        participants: list
            alphabetize a list of indiviuals 
            without specifying which are humans and which are vampires 
        day_number: int
            the number of days in our file
    """
    participants_str = ''  
    # construct the participants string in the requirred format
    for i in range(len(participants)):
        if i == len(participants) - 1:
            participants_str = participants_str + participants[i] + '.'
        elif i == len(participants) - 2:
            participants_str = participants_str + participants[i] + ' and '
        else:
            participants_str = participants_str + participants[i] + ', '
    # for only 1 day, there is no "s" after day
    if day_number == 1:
        print("{0} day with the following participants: "
        "{1}".format(day_number, participants_str))
    else:
        print("{0} days with the following participants: "
        "{1}".format(day_number, participants_str))


def specific_day_summary(i, number_vampire_test, number_contact_group):
    """ 
    count the number of tests and groups in a specific day
    then print it in the required format.

    Parameters:
        i: int
            the specific day from our file. 
        number_vampire_test: int
            the total number of vampires test did in this specific day.    
        number_contact_group: int
            the total number of contact groups in this specific day.
    """
    if number_vampire_test == 1 and number_contact_group != 1:
        print(f"Day {i + 1} has {number_vampire_test} vampire", end=' ')
        print(f"test and {number_contact_group} contact groups.")
    elif number_vampire_test != 1 and number_contact_group == 1:
        print(f"Day {i + 1} has {number_vampire_test} vampire", end=' ')
        print(f"tests and {number_contact_group} contact group.")
    else:
        print(f"Day {i + 1} has {number_vampire_test} vampire", end=' ')
        print(f"tests and {number_contact_group} contact groups.")


def specificday_detail(i, number_vampire_test, number_contact_group, data):
    """ 
    get the identity detail (human or vampire) for each individual 
    attended the tests and the name from contact groups for each day, 
    then print it in the requied format.

    Parameters:
        i: int
            the specific day from our file. 
        number_vampire_test: int
            the total number of vampires test did in this specific day.    
        number_contact_group: int
            the total number of contact groups in this specific day.
        data: tuple
            the first element in tuple is the list of participants.
            the second element in tuple is a list of tuples,
            each tuple contains the result of tests 
            (if the individual is a vampire then Boolean True, 
            otherwise if its human then Boolean False)
            and the list of contact groups for the specific day.
    """
    if number_vampire_test == 1:     # no “s” after “test”
        print(f"  {str(number_vampire_test)} test")
    else:
        print(f"  {str(number_vampire_test)} tests")
    test_data = data[1][i][0]
    sorted_test_data = sorted(test_data.items())
    for element, is_human in sorted_test_data:
        if is_human == False:  # when this individual is human     
            print(f"    {element} is human.")
        else:
            print(f"    {element} is a vampire!")
    if number_contact_group == 1:   # no “s” after “group”
        print(f"  {str(number_contact_group)} group")
    else:
        print(f"  {str(number_contact_group)} groups")
    for j in range(number_contact_group):
        sorted_contact_data = sorted(data[1][i][1][j])
        string_sort_data1 = ', '.join(map(str, sorted_contact_data[:-1]))
        string_sort_data2 = f" and {sorted_contact_data[-1]}"
        string_sorted_data = string_sort_data1 + string_sort_data2
        print(f"    {string_sorted_data}")


def pretty_print_infiltration_data(data):
    """ 
    combine the first three functions together for each day data
    then print the final human-readable format summary

    Parameter:
        data: tuple
            the first element in tuple is the list of participants.
            the second element in tuple is a list of tuples
            each tuple contains the result of tests and 
            the list of contact groups for the specific day.
    """
    days = data[1]
    participants = data[0].copy() 
    participants.sort()
    day_number = len(days)
    print("Vampire Infiltration Data")
    participants_summary(participants, day_number)

    for i in range(day_number):
        number_contact_group = len(data[1][i][1])  # number of groups
        number_vampire_test = len(data[1][i][0])   # number of tests
        specific_day_summary(i, number_vampire_test, number_contact_group)
        specificday_detail(i, number_vampire_test, number_contact_group, data)

    print("End of Days")


# Section 5
def contacts_by_time(participant, time, contacts_daily):
    """ 
    return the name from contacts group for the participant in specific day,
    by converting the time unit parameter to the day and adjust to the list 
    index then to search within the contact groups for that day 
    to find the correct list for the given participant.

    Parameters:
    participant: string
        name of a participant
    time: int
        the units of time
    contacts_daily: list
        a list of the contact groups on each day

    Returns:
    []: empty list
    group_names_tmp: list
        return all names from the contact groups, 
        when the participant met on the specific day.
    """
    day = day_of_time(time)
    # special case: on day 0 there is no contact group.
    if day == 0:
        return []
    else:
        # when the participant didn't meet anyone on that day.
        if day > len(contacts_daily):
            return []
        else:
            groups = contacts_daily[day - 1]
            for group_names in groups:
                # return all names from the contact groups, 
                # when the participant met on the specific day.
                if participant in group_names:
                    group_names_tmp = group_names.copy()
                    group_names_tmp.sort()
                    return group_names_tmp
            # the participant cannot find in contact groups in the given day.
            return []


# Section 6
def create_initial_vk(participants):
    """ 
    return a dictionary called the result_dict 
    to represent everyone's initial status should be unclear (“U”).
    
    Parameter:
        participants: list
            the list of participants.

    Return:
        result_dict: dictionary
            a dictionary where the keys are the participants' names and 
            the values are string “U”.
    """
    result_dict = {}
    for name in participants:
        result_dict[name] = 'U'
    return result_dict


def pretty_print_vampire_knowledge(vk):
    """ 
    print the result of vk structure: output should be 
    three groups (Humans, Unclear individuals, Vampires) of names.

    Parameter:
        vk: dictionary
            key is the participants' names and 
            value is one of three strings “H”, “V”, or “U” at time t.
            three statuses are: 
            definitely human (“H”), definitely vampire (“V”), or unclear (“U”)
    """
    # initially construct empty list 
    human_list = []
    vampire_list = []
    unclear_list = []
    # append into each list
    for name in vk:
        status = vk[name]
        if status == 'H':           # when this individual is human
            human_list.append(name)
        elif status == 'V':         # when this individual is a vampire
            vampire_list.append(name)
        else:
            unclear_list.append(name)
    print('  Humans: {0}'.format(format_list(human_list)))
    print('  Unclear individuals: {0}'.format(format_list(unclear_list)))
    print('  Vampires: {0}'.format(format_list(vampire_list)))
    

# Done by professors
def pretty_print_vks(vks):
    print(f'Vampire Knowledge Tables')
    for i in range(len(vks)):
        print(f'Day {str_time(i)}:')
        pretty_print_vampire_knowledge(vks[i])
    print(f'End Vampire Knowledge Tables')


# Section 7
def update_vk_with_tests(vk, tests):
    """ 
    return the new vk structure by updating vk dictionary, if an individual
    has “U” status, then update their status to “V” or “H” depending on the 
    result of the test. Also, print the three error situations.

    Parameters:
        vk: dictionary
            key is participants and value is one of the status: “H”/“V”/“U”.
        tests: dictionary
            key is participant names and value is the Boolean results of the 
            tests on a given day: True for vampirism and False for humanism.

    Return:
        vk: dictionary
            the new vk structure includes the updated status for 
            each tested participants. 
    """
    for name in vk:
        if name in tests:
            test_result = tests[name]
            # error situation: definite human tests positive for vampirism 
            if test_result == True:       # when this participant is a vampire
                if vk[name] == "H":       # this participant is human
                    print("Error found in data: humans cannot be vampires; " \
                          "aborting.")
                    sys.exit()
                else:
                    vk[name] = "V"
            else:
            # error situation: definite vampire tests negative for vampirism
                if vk[name] == "V":        # this participant is a vampire
                    print("Error found in data: vampires cannot be humans; " \
                          "aborting.")
                    sys.exit()
                else:
                    vk[name] = "H"          
    for name in tests:
        # error situation: when someone has a test but not a participant
        if name not in vk:
            print("Error found in data: test subject is not a participant; " \
                  "aborting.")
            sys.exit()
    return vk


# Section 8
def update_vk_with_vampires_forward(vk_pre, vk_post):
    """ 
    return the new vk_post by updating the vampire status forward 
    for the vk_post structure.
    if participant p is a vampire before, then p must also be a vampire after.

    Parameters:
        vk_pre: a dictionary mapping participants to “H”/“V”/“U”.
            the previous vk structure.
        vk_post: a dictionary mapping participants to “H”/“V”/“U”.
            the vk strcture that occur after the vk_pre.
    
    Return:
        vk_post: a dictionary mapping participants to “H”/“V”/“U”.
            the updated dictionary that allow participants with "U" status in 
            vk_post change to "V" if they have "V" status in vk_pre.
    """
    for name in vk_pre:
        # error situation: if participant is a vampire before but human after
        if vk_pre[name] == "V":       # the participant is a vampire in vk_pre
            if vk_post[name] == "H":  # the participant is human in vk_post
                print("Error found in data: vampires cannot be humans; " \
                      "aborting.")
                sys.exit()
            else:
                vk_post[name] = "V"
    
    return vk_post


# Section 9
def update_vk_with_humans_backward(vk_pre, vk_post):
    """ 
    return the new vk_pre by updating human status backward for the vk_pre.
    (if participant p is a human after, then p must also be a human before)

    Parameters:
        vk_pre: a dictionary mapping participants to “H”/“V”/“U”.
            the previous vk structure.
        vk_post: a dictionary mapping participants to “H”/“V”/“U”.
            the vk strcture that occur after the vk_pre.

    Return:
        vk_pre: a dictionary mapping participants to “H”/“V”/“U”.
            the updated dictionary that allow participants with "U" status in 
            vk_pre change to "H" if they have "H" status in vk_post.                 
    """
    for name in vk_post:
        # error situation: if participant is human after but a vampire before
        if vk_post[name] == "H":      # the participant is human in vk_post
            if vk_pre[name] == "V":   # the participant is a vampire in vk_pre
                print("Error found in data: humans cannot be vampires; " \
                      "aborting.")
                sys.exit()
            else:
                vk_pre[name] = "H"
    return vk_pre


# Section 10
def update_vk_overnight(vk_pre, vk_post):
    """
    return the new vk_post by checking for the two error situations 
    so that no status change overnight, and updated the "U" status 
    in vk_post for the participants depending on the status in vk_pre.

    Parameters:
        vk_pre: a dictionary mapping participants to “H”/“V”/“U”.
            the previous vk structure.
        vk_post: a dictionary mapping participants to “H”/“V”/“U”.
            the vk strcture that occur after the vk_pre.

    Return:
        vk_post: a dictionary mapping participants to “H”/“V”/“U”.
            propagate statuses (both human and vampire) forward to 
            get new vk_post structure.
    """
    for name in vk_pre:
        # error situation:
        # if the participant is human in vk_pre and is a vampire in vk_post
        if vk_pre[name] == "H" and vk_post[name] == "V":
            print("Error found in data: humans cannot be vampires; aborting.")
            sys.exit()
        # error situation:
        # if the participant is a vampire in vk_pre and is human in vk_post
        elif vk_pre[name] == "V" and vk_post[name] == "H":
            print("Error found in data: vampires cannot be humans; aborting.")
            sys.exit()
        # if participant is a vampire in vk_pre and unknown status in vk_post
        elif vk_pre[name] == "V" and vk_post[name] == "U":
            vk_post[name] = "V"
        # if the participant is human in vk_pre and is unknown status in vk_post
        elif vk_pre[name] == "H" and vk_post[name] == "U":
            vk_post[name] = "H" 
    return vk_post


# Section 11
def not_participant_function(contact_name_list, vk_pre):           
    """ 
    Print the error situation: if one of the individuals 
    in a contact group is not a participant.

    Parameters:
        conatct_name_list: list
            all individuals who attended the vampire graduation party 
            at the specific day.
        vk_pre:  a dictionary mapping participants to “H”/“V”/“U”.
            this happens at the same specific day just after AM tests.
    """
    for contact in contact_name_list:
        if contact not in vk_pre: 
            string_part1 = 'Error found in data: contact subject is not '
            string_part2 = 'a participant; aborting.'
            string_part = string_part1+string_part2
            print(string_part)
            sys.exit()

            
def update_vk_conta_g_not_in_contact(name, vk_pre, vk_post):
    """ 
    update the vk_post identity status of individuals who stayed at home, 
    depending on the the identity status from vk_pre and print error situation

    Parameters:
        name: string
            given name for any individuals who are not in any contact groups 
            at the specific day.
        vk_pre: a dictionary mapping participants to “H”/“V”/“U”.
            this happens at the same specific day just after AM tests.
        vk_post: a dictionary mapping participants to “H”/“V”/“U”.
            this happens at the same specific day just after PM contacts.
    """
    # the individual is human after AM test and is unknown status 
    # after PM contacts at that day.
    if vk_pre[name] == "H" and vk_post[name] == "U":    
        vk_post[name] = "H"
    # the individual is a vampire after AM test and is unknown status    
    # after PM contacts at that day.     
    elif vk_pre[name] == "V" and vk_post[name] == "U":
        vk_post[name] = "V"
    # error situation:
    # the individual is human after AM test and is a vampire     
    # after PM contacts at that day    
    elif vk_pre[name] == "H" and vk_post[name] == "V":
        string_part1 = 'Error found in data: '
        string_part2 = 'humans cannot be vampires; aborting.'
        string_part = string_part1+string_part2
        print(string_part)
        sys.exit()

            
def update_vk_conta_g_group(name, vk_pre, contacts, vk_post):
    """ 
    update the human status in the post for the individual who stayed in the 
    all-human contact group and is human in the pre at the same day. 
    also, print the error situation.

    Parameters:
        name: string
            given name for any individual who is inside contact_name_list
            at the specific day.
        vk_pre: a dictionary mapping participants to “H”/“V”/“U”.
            this happens at the same specific day just after AM tests.
        contacts: list
            the list of contact groups (which themselves are lists of 
            participants) for that day.
        vk_post: a dictionary mapping participants to “H”/“V”/“U”.
            this happens at the same specific day just after PM contacts.
    """
    for name_list in contacts:
        if name in name_list:                 
            is_all_human = True      # the individual is in the all-human group
            for nm in name_list:
                # the individual is unknown or vampire status in the pre
                if vk_pre[nm] == 'U' or vk_pre[nm] == 'V':
                    # the individual is not in the all-human group
                    is_all_human = False   
            # the individual is in the all-human group
            if is_all_human == True:
                # error situation: if the individual is human in the pre and 
                # in all-human contact group, but is a vampire in the post.
                if vk_post[name] == 'V':  
                    string_part1 = 'Error found in data: humans c'
                    string_part2 = 'annot be vampires; aborting.'
                    string_part = string_part1+string_part2
                    print(string_part)
                    sys.exit()
                else:
                    vk_post[name] = 'H'

            
def update_vk_with_contact_group(vk_pre, contacts, vk_post):
    """ 
    return the new vk_post structure that updated the identity status of
    individuals by applying above functions and add new condition: a vampire 
    in pre who is somehow unknown in post is updated in the post).
    also, print the last error situation. 
    
    Parameters:
        vk_pre: a dictionary mapping participants to “H”/“V”/“U”.
            this happens at the same specific day just after AM tests.
        vk_post: a dictionary mapping participants to “H”/“V”/“U”.
            this happens at the same specific day just after PM contacts.
        contacts: list
            the list of contact groups (which themselves are lists of 
            participants) for that day
    Return:
        vk_post: a dictionary mapping participants to “H”/“V”/“U”.
            new vk_post structure that updated the identity status for 
            participants and check about error situations.
    """
    contact_name_list = []
    for name_list in contacts:
        for name in name_list:
# error situation: if one of individuals in contact group is not a participant
            if name not in contact_name_list:
                contact_name_list.append(name)
    not_participant_function(contact_name_list, vk_pre)

    for name in vk_pre:
        # error situation: any vampires in pre that are somehow humans in post
        if vk_pre[name] == "V" and vk_post[name] == "H":
            print("Error found in data: vampires cannot be human; aborting.")
            sys.exit()
        # updated the identity status
        elif vk_pre[name] == "V" and vk_post[name] == "U":
            vk_post[name] = "V"
        if name not in contact_name_list:  # for individuals stay at home
            update_vk_conta_g_not_in_contact(name, vk_pre, vk_post)
        # for individuals who stayed in the all-human contact group
        if name in contact_name_list:
            if vk_pre[name] == "H":  # individual is human in pre
                update_vk_conta_g_group(name, vk_pre, contacts, vk_post)
    return vk_post


# Section 12
def find_infection_windows(vks):
    """ 
    find the shortest start and end time in which individuals who are 
    definite vampires in the data could have been infected.

    Parmeter:
        vks: list
            a list of all of the vk structures first defined in section 6  
            (dictionaries mapping participants to H/U/V statuses).

    Return: 
        windows: dictionary
            keys are participants who are all of the definite vampires 
            in the data.
            the value is a pair tuple (start, end) giving infection window.
            start: time unit just before infection could have occurred. 
            end: the time unit in which infection was confirmed. 
    """
    vks2 = vks.copy()
    windows = {}
    for t in range(len(vks2)):
        vk = vks2[t]
        for name in vk:
            if vk[name] == 'H':  # the individual is human
                if name not in windows:
                    windows[name] = [0]
                if name in windows:
                    if len(windows[name]) == 1: 
                        windows[name][0] = t
            elif vk[name] == 'V': # the individual is a vampire
                if name in windows:
                    if len(windows[name]) == 1: 
                        windows[name].append(t)
                if name not in windows:
                    windows[name] = [0]
                    windows[name].append(t)        
    for name in list(windows.keys()):
        if len(windows[name]) == 1:  # remove invalid data
            del windows[name]
        else:            
            windows[name] = tuple(windows[name])           
    return windows


def pretty_print_infection_windows(iw):
    """ 
    print time data (days) that determine when vampires must have been sired
    in the required format.

    Parameter:
        iw: dictionary
            key is participants who are all of the definite vampires
            in the data.
            value is a pair tuple (start, end) giving infection window.
            start: time unit just before infection could have occurred. 
                    (last definite human status)
            end: the time unit in which infection was confirmed. 
                    (first definite vampire status)
    """
    name_list = []
    for name in iw:
        name_list.append(name)
    name_list.sort()
    for name in name_list:
        time_start = iw[name][0]
        time_end = iw[name][1]
        day_start = str_time(time_start)
        day_end = str_time(time_end)
        print('  {0} was turned between day {1} and day {2}.'
              .format(name, day_start, day_end))


# Section 13
def find_potential_sires(iw, vks, groups):
    """ 
    return the potential_sires dictionary to find in specific time unit, who 
    this individual met in that time unit to figure out who might have sired 
    the various vampires.

    Parameters:
        iw: dictionary
            the infection window structure constructed in section 12
        vks: list
            a list of vampire knowledge structures
        groups: list
            a list of the contact groups indexed by day

    Return: 
        potential_sires: dictionary
            keys are the vampire participants and 
            values are a list with the following format: 
            each list cell contains a tuple pair of a time unit, 
            and a list of the contacts of that participant in that time unit.
    """
    potential_sires = {}
    for name in iw:
        potential_sires[name] = []
        t_start = iw[name][0]
        t_end = iw[name][1]
        for i in range(t_start, t_end+1):
            if i > 1 and i % 2 == 0:   # make sure only PM time unit
                value = []
                value.append(i)        # append time unit 
                day = day_of_time(i)
                for name_list in groups[day - 1]:
                    if name in name_list:
                        name_list2 = name_list.copy()
                        name_list2.sort()
                        value.append(name_list2) 
                if len(value) == 1:    # no contact that day
                    value.append([])
                value = tuple(value)
                potential_sires[name].append(value)
    return potential_sires


def pretty_print_potential_sires(ps):
    """ 
    print the ps structure out in the requirred format (with the names 
    appear in alphabetical order and days are in order of name).

    Parameter:
        ps: dictionary
            a dictionary whose keys are the vampire participants and 
            values are a list with the following format: 
            each list cell contains a tuple pair of a time unit, 
            and a list of the contacts of that participant in that time unit.
    """
    # construct the vampire name list
    name_list = []
    for name in ps:
        name_list.append(name)
    name_list.sort()
    for name in name_list:
        values = ps[name]
        print('  {0}:'.format(name) )
        for value in values:
            t = value[0]
            name_list = value[1]
            print('    On day {0}, met with {1}.'
                  .format(str_time(t), format_list(name_list)))
        if len(values) == 0:
            print('    (None)')
    

# Section 14
def remov_eventual_vampire(ps_copy, name_list, name):
    """ 
    updated the ps_copy such that on any day where there was contact, 
    removing the eventual vampire.
    
    Parameters:
        ps_copy: dictionary
            the copy of dictionary ps (same structure for Section 13)
        name_list: list
            contain names in ps_copy in alphabetical order.    
        name: string
            names in name_list  
    """
    for i in range(len(ps_copy[name])):
        t = ps_copy[name][i][0]   # time unit
        contacts = ps_copy[name][i][1]
        new_contacts = []
        for name_contact in contacts:
            if name_contact not in name_list or name_contact != name:
                new_contacts.append(name_contact)
        ps_copy[name][i] = list(ps_copy[name][i])
        ps_copy[name][i][1] = new_contacts
        ps_copy[name][i] = tuple(ps_copy[name][i])
            

def remov_definite_human(ps_copy, name, vks):
    """ 
    updated the ps_copy such that removing anyone in contact list 
    who was definitely a human at that time.

    Parameters:
        ps_copy: dictionary
            the copy of dictionary ps (same structure for Section 13)
        name: string
            names in ps_copy in alphabetical order
        vks: list
            the list of vampire knowledge structures
    """ 
    for i in range(len(ps_copy[name])):
        t = ps_copy[name][i][0]
        contacts = ps_copy[name][i][1]
        human_name_list_in_t = []
        vk = vks[t]
        for name_t in vk:
            if vk[name_t] == 'H':     # the individual is human
                human_name_list_in_t.append(name_t)
        new_contacts = []
        for name_contact in contacts:
            if name_contact not in human_name_list_in_t:
                new_contacts.append(name_contact)
        ps_copy[name][i] = list(ps_copy[name][i])
        ps_copy[name][i][1] = new_contacts
        ps_copy[name][i] = tuple(ps_copy[name][i])


def trim_potential_sires(ps,vks):
    """ 
    return simplified ps_copy dictionary that satisfied conditions from above 
    two new constructed functions and also removing any empty contact days.

    Parameters:
        ps: dictionary
            potential sire structure (constructed in Section 13)
            keys are the vampire participants and 
            values are a list with the following format: 
            each list cell contains a tuple pair of a time unit, 
            and a list of the contacts of that participant in that time unit.
        vks: list 
            this is the list of vampire knowledge structures.
            each list cell contains the participant name and 
            their identity status at that time unit.

    Return:
        ps_copy: dictionary
            updated dictionary with same key as in ps dictionary,
            but new values that applying new conditions from above functions
            with same format structure.
    """
    ps_copy = ps.copy()    
    name_list = []
    for name in ps_copy:
        name_list.append(name)
    name_list.sort()
    for name in name_list:
        values = ps_copy[name]
        # removing the eventual vampire
        remov_eventual_vampire(ps_copy, name_list, name)
        # remove anyone in contact list who was definitely a human
        remov_definite_human(ps_copy, name, vks)
        new_values = []
        for value in values:
            t = value[0]
            contacts = value[1]
            if contacts != []:      # if contact list not empty
                new_values.append(value)
        ps_copy[name] = new_values
    return ps_copy


# Section 15
def updated_iw_for_vampire_in_ps(iw, ps):
    """
    updated the new iw structure for names of vampires inside the ps,
    by comparing the earlier infection windows and the trimmed potential sire
    information and tightens the windows appropriately.

    Parameters:
        iw:  the infection window structure constructed in section 12.
        ps:  the trimmed potential sire constructed in section 14.
    """
    for name in iw:
        if name in ps:
            values = ps[name]
            # when the ps dictionary contains the empty contact list
            if values == []:    
                iw[name] = list(iw[name])
                iw[name][0] = 0
                iw[name][1] = 0
                iw[name] = tuple(iw[name])
            else:
                start = iw[name][0]
                end = iw[name][1]                
                time_min = values[0][0]   # find the smallest time unit
                time_max = values[0][0]
                for value in values:
                    t = value[0]
                    if t < time_min:
                        time_min = t
                    elif t > time_max:
                        time_max = t
                if start > 0:     # when start time unit greater than zero
                    iw[name] = list(iw[name])
                    iw[name][0] = time_min
                    iw[name][1] = time_max
                    iw[name] = tuple(iw[name])
                elif start == 0:  # when start time unit equal to zero
                    iw[name] = list(iw[name])
                    iw[name][1] = time_max
                    iw[name] = tuple(iw[name])


def trim_infection_windows(iw,ps):
    """ 
    return the new iw structure by applying the above function and also 
    consider the special case for original vampires.

    Parameters:
        iw: dictionary (from Section 12)
            keys are participants who are all of the definite vampires.
            the values of this dictionary is a pair tuple (start, end) 
            giving the infection window.
            start: time unit just before infection could have occurred. 
                    (last definite human status)
            end: the time unit in which infection was confirmed. 
                    (first definite vampire status)
        ps: dictionary (from Section 14)
            keys are the vampire participants and 
            values are a list with the following format: 
            each list cell contains a tuple pair of a time unit, 
            and a list of the contacts of that participant in that time unit.

    Return:
        iw: dictionary
            same structure as the previous iw, but updated 
            the pair time unit tuple.
    """
    updated_iw_for_vampire_in_ps(iw, ps)
    # special case: a vampire has no potential sires and 
    # then must be the vampire at beginning with a pair time unit (0,0)
    for name in iw:
        if name not in ps:
            iw[name] = list(iw[name])
            iw[name][0] = 0
            iw[name][1] = 0
            iw[name] = tuple(iw[name])
    return iw


# Section 16
def update_vks_with_windows(vks,iw):
    """ 
    updated the identity status of participants in vks depending on times 
    before and after the window; also check two error situations.

    Parameters:
        vks: list of vampire knowledge structures (in Section 14).
            each list cell contains the participant name and 
            their identity status at that time unit.
        iw: the infection window structure constructed in Section 15.

    Returns:
        vks: the updated vks list
            same structure as previous vks but with updated identity status.
        changes: int
            an integer indicating the number of changes made to the vks list
    """
    changes = 0
    for t in range(len(vks)):
        vk = vks[t]
        for name in vk:
            if name in iw:
                start = iw[name][0]
                end = iw[name][1]
# for all times after our window, the individual must have been a vampire
                if vk[name] == 'U':
                    if t >= end:
                        vk[name] = 'V'
                        changes = changes + 1
# error situation: propagating vampire status backward
                elif t >= end and vk[name] == 'H':
                    string_part1 = 'Error found in data: '
                    string_part2 = 'vampires cannot be human; aborting.'
                    string_part = string_part1+string_part2
                    print(string_part)
                    sys.exit()
# error situation: propagating human status forward
                elif t < start and vk[name] == 'V':
                    string_part1 = 'Error found in data: '
                    string_part2 = 'humans cannot be vampires; aborting.'
                    string_part = string_part1+string_part2
                    print(string_part)
                    sys.exit()
    return (vks,changes)


# Section 17; done by professors
def cyclic_analysis(vks,iw,ps):
    count = 0
    changes = 1
    while(changes != 0):
        ps = trim_potential_sires(ps,vks)
        iw = trim_infection_windows(iw,ps)
        (vks,changes) = update_vks_with_windows(vks,iw)
        count = count + 1
    return (vks,iw,ps,count)


# Section 18: vampire strata
def vampire_strata(iw):
    """ 
    return a triple of three sets: originals, unknowns and newborns 
    respectively by checking the start and end time unit 
    for participants from iw.
    
    Parameter:
        iw: dictionary (from Section 17)
            a dictionary whose keys are participants who are all of the 
            definite vampires in the data.
            the values of this dictionary is a pair tuple (start, end) 
            giving the infection window.
            start: time unit just before infection could have occurred. 
            end: the time unit in which infection was confirmed. 

    Returns:
        originals: set
            participants that are original vampires from Day 0.
        unclear_vamps: set
            participants that might be original vampires but not sure. 
        newborns: set
            participants that are new vampires (they are human at beginning).
    """
    # create empty set at beginning
    originals = set()
    unclear_vamps = set()
    newborns = set()
    for name in iw:
        start = iw[name][0]
        end = iw[name][1]
    # a vampires has an infection window that both starts and ends with zero
    # then they are definitely original vampires
        if start == 0 and end == 0:  # start and end time both equal to zero
            originals.add(name)
    # if starts after zero, they are definitely new vampires
        elif start > 0:     
            newborns.add(name)
    # starts but ends strictly greater than zero
        elif start == 0 and end > 0: 
            unclear_vamps.add(name)
    return (originals,unclear_vamps,newborns)


def pretty_print_vampire_strata(originals, unclear_vamps, newborns):
    """ 
    print the participants of originals vampires,unknown strata vampires and 
    newborn vampires respectively in the required format.
    
    Parameters:
        originals: set
            participants that are original vampires from Day 0.
        unclear_vamps: set
            participants that might be original vampires but not sure. 
        newborns: set
            participants that are new vampires (they are human at beginning).
    """
    # list in alphabetical order
    originals_list = list(originals)
    originals_list.sort()            
    unclear_vamps_list = list(unclear_vamps)
    unclear_vamps_list.sort()        
    newborns_list = list(newborns)
    newborns_list.sort()             

    # print first set: original vampires
    print('  Original vampires: {0}'.format(format_list(originals_list)))

    # print second set: unknown strata vampires
    string_part = '  Unknown strata vampires: {0}'
    format_part = format_list(unclear_vamps_list)
    print(string_part.format(format_part))

    # print the last set: newborn vampires
    print('  Newborn vampires: {0}'.format(format_list(newborns_list)))


# Section 19: vampire sire sets
def calculate_sire_sets(ps):
    """
    return the dictionary ss which is a map from vampire names to 
    sets of possible sires.

    Parameters:
        ps: dictionary
            key is vampire name, value is the list of tuples with 2 elements. 
            the first element of tuple is time, 
            the second element is list of contact names.

    Return:
        ss: dictionary 
            key is vampire name, value is list of contact names.
    """
    ss = {}                    
    for name in ps:       
        # get values by name of dictionary ps     
        values = ps[name]      
        if values == []:
        # for original vampires, this will be the empty set
            ss[name] = set([])
        else:
            sire_name_set = set([])
            # iterate each value
            for value in values:
                contacts = value[1]  # contacts name
                if contacts != []:   # if has contacts
            # get sets of possible sires, and insert conatct bames into set
                    for contact in contacts:
                        sire_name_set.add(contact)
            # add vampire name set to dictionary            
            ss[name] = sire_name_set   
    return ss


def unknown_strata_print_sire_sets(ss, iw, vamps, newb):
    """ 
    print the output for vapires of unknown strata in the requirred format.

    Parameters:
        ss: dictionary
            key is vampire name, value is list of contact names.
        iw: dictionary
            keys are participants who are all of the definite vampires.
            value is a pair time tuple (start, end) giving infection window.
        vamps: set
            a set of vampires (a subset of the vampires in ss). 
        newb: a Boolean flag
            True = newborns; False = unknown status.
    """ 
    if newb == False:     # vampires are unknown strata
        print('Vampires of unknown strata:')
        if vamps == set([]):
            print('  (None)')
        else:
            vamps_list = list(vamps)
            vamps_list.sort()    # vampires list in sorted order
            for name in vamps_list:
                name_list = list(ss[name])
                name_list.sort()
                start = iw[name][0]
                end = iw[name][1]
                # when the infection window is exactly one time period long
                # end time not equal to zero but equal to start time
                if end != 0 and start == end:    
                    string_part1 = '  {0} could have been '
                    string_part2 = 'sired by {1} on day {2}.'
                    string_part = string_part1+string_part2                
                    print(string_part.format(name, 
                        format_list_or(name_list),str_time(start) ))
                # end time not equal to start time and not equal to zero    
                elif end != 0 and start != end: #the infection window is wider
                    string_part1 = '  {0} could have been sired by '
                    string_part2 = '{1} between day {2} and day {3}.'
                    string_part = string_part1+string_part2
                    # print for one or more than one possible sire case
                    print(string_part.format( name, format_list_or(name_list),
                    str_time(start), str_time(end) ))


def newborn_vampires_print_sire_sets(ss, iw, vamps, newb):
    """ 
    print the output for newborn vampires in the requirred format.

    Parameters:
        ss: dictionary
            key is vampire name, value is list of contact names.
        iw: dictionary
            keys are participants who are all of the definite vampires.
            value is a pair time tuple (start, end) giving infection window.
        vamps: set
            a set of vampires (a subset of the vampires in ss). 
        newb: a Boolean flag
            True = newborns; False = unknown status.     
    """
    if newb == True:       # vampires are newborn
        print('Newborn vampires:')
        if vamps == set([]):
            print('  (None)')
        else:
            vamps_list = list(vamps)
            vamps_list.sort()    # vampires list in sorted order
            for name in vamps_list:
                name_list = list(ss[name])
                name_list.sort()
                start = iw[name][0]
                end = iw[name][1]
                # when the infection window is exactly one time period long
                if start != 0 and end != 0 and start == end:
                    string_part1 = '  {0} was sired by '
                    string_part2 = '{1} on day {2}.'
                    string_part = string_part1+string_part2
                    # print for one or more than one possible sire case
                    print(string_part.format(name,format_list_or(name_list), 
                        str_time(start) ))
                # when the infection window is wider
                elif start != 0 and end != 0 \
                    and start != end:
                    string_part1 = '  {0} was sired by {1} between day '
                    string_part2 = '{2} and day {3}.'
                    string_part = string_part1+string_part2
                    print(string_part.format( name,format_list_or(name_list), 
                    str_time(start), str_time(end) ))


def pretty_print_sire_sets(ss,iw,vamps,newb):
    """ 
    print the output for both vampires of unknown strata and newborn vampires
    in the required format by combinning the above functions.

    Parameters:
        ss: dictionary
            key is vampire name, value is list of contact names.
        iw: dictionary
            keys are participants who are all of the definite vampires.
            value is a pair time tuple (start, end) giving infection window.
        vamps: set
            a set of vampires (a subset of the vampires in ss). 
        newb: a Boolean flag
            True = newborns; False = unknown status. 
    """
    # print the output for vampires of unknown strata
    unknown_strata_print_sire_sets(ss, iw, vamps, newb)
    # print the output for newborn vampires
    newborn_vampires_print_sire_sets(ss, iw, vamps, newb)


# Section 20: vampire sire sets
def find_hidden_vampires(ss,iw,vamps,vks):
    """ 
    return a pair of an updated list of vk structures (when a newborn vampire 
    has only one potential sire, that individual must be a vampire).
    and the number of changes made to the vk structures (as in section 16).

    Parameters:
        ss: dictionary (same structure from section 19)
        iw: dictionary (same structure from section 12)
        vamps: a set of (newborn) vampires
        vks: the time-indexed list of vk structures

    Returns:
        vks: dictionary with updated identity status (unkown to vampire) 
        changes(int): the number of changes made in previous vks.
    """
    changes = 0
    for name in vamps:      # find the sires of all of the newborns vampires 
        sires = ss[name]
        if len(sires)==1:   # if the sire set is a singleton
            start = iw[name][0]
            end = iw[name][1]
            sires_list = list(sires)
            sire_name = sires_list[0]  # get sire name
            if start != 0:    # starts after zero, thus newborn vampires
                for t in range(end, len(vks)):
                    vk = vks[t]
                    if vk[sire_name] == 'U':   # updated the identity status 
                        vk[sire_name] = 'V'
                        changes = changes + 1
                        is_am = period_of_time(t)
                        if is_am == False and t > 1:   # happens at PM   
                            vk_am = vks[t-1]           # change AM also
                            if vk_am[sire_name] == 'U': # again updated status
                                vk_am[sire_name] = 'V'
                                changes = changes + 1
                            elif vk_am[sire_name] == 'H': # error situation
                                print("Error found in data: vampires cannot" \
                                      " be humans; aborting.")
                                sys.exit()
                    elif vk[sire_name] == 'H':  # error situation
                        print("Error found in data: vampires cannot be "
                              "humans; aborting.")
                        sys.exit()
    return (vks,changes)


# Section 21; done by professor
def cyclic_analysis2(vks,groups):
    count = 0
    changes = 1
    while(changes != 0):
        iw = find_infection_windows(vks)
        ps = find_potential_sires(iw, vks, groups)
        vks,iw,ps,countz = cyclic_analysis(vks,iw,ps)
        o,u,n = vampire_strata(iw)
        ss = calculate_sire_sets(ps)
        vks,changes = find_hidden_vampires(ss,iw,n,vks)        
        count = count + 1
    return (vks,iw,ps,ss,o,u,n,count)


def main():
    """Main logic for the program.  Do not change this (although if 
       you do so for debugging purposes that's ok if you later change 
       it back...)
    """
    filename = ""
    # Get the file name from the command line or ask the user for a file name
    args = sys.argv[1:]
    if len(args) == 0:
        filename = input("Please enter the name of the file: ")
    elif len(args) == 1:
        filename = args[0]
    else:
        print("""\n\nUsage\n\tTo run the program type:
        \tpython contact.py infile
        where infile is the name of the file containing the data.\n""")
        sys.exit()

    # Section 2. Check that the file exists
    if not file_exists(filename):
        print("File does not exist, ending program.")
        sys.exit()

    # Section 3. Create contacts dictionary from the file
    # Complete function parse_file().
    data = parse_file(filename)
    participants, days = data
    tests_by_day = [d[0] for d in days]
    groups_by_day = [d[1] for d in days]

    # Section 4. Print contact records
    pretty_print_infiltration_data(data)

    # Section 5. Create helper function for time analysis.
    print("********\nSection 5: Lookup helper function")
    if len(participants) == 0:
        print("  No participants.")
    else:
        p = participants[0]
        if len(days) > 1:
            d = 2
        elif len(days) == 1:
            d = 1
        else:
            d = 0
        t = time_of_day(d,False)
        t2 = time_of_day(d,True)
        print(f"  {p}'s contacts for time unit {t} (day {day_of_time(t)}) are {format_list(contacts_by_time(p,t,groups_by_day))}.")
        print(f"  {p}'s contacts for time unit {t2} (day {day_of_time(t)}) are {format_list(contacts_by_time(p,t2,groups_by_day))}.")
        assert(contacts_by_time(p,t,groups_by_day) == contacts_by_time(p,t2,groups_by_day))

    # Section 6.  Create the initial data structure and pretty-print it.
    print("********\nSection 6: create initial vampire knowledge tables")
    vks = [create_initial_vk(participants) for i in range(1 + (2 * len(days)))]
    pretty_print_vks(vks)

    # Section 7.  Update the VKs with test results.
    print("********\nSection 7: update the vampire knowledge tables with test results")
    for t in range(1,len(vks),2):
        vks[t] = update_vk_with_tests(vks[t],tests_by_day[day_of_time(t)-1])
    pretty_print_vks(vks)

    # Section 8.  Update the VKs to push vampirism forwards in time.
    print("********\nSection 8: update the vampire knowledge tables by forward propagation of vampire status")
    for t in range(1,len(vks)):
        vks[t] = update_vk_with_vampires_forward(vks[t-1],vks[t])
    pretty_print_vks(vks)

    # Section 9.  Update the VKs to push humanism backwards in time.
    print("********\nSection 9: update the vampire knowledge tables by backward propagation of human status")
    for t in range(len(vks)-1, 0, -1):
        vks[t-1] = update_vk_with_humans_backward(vks[t-1],vks[t])
    pretty_print_vks(vks)

    # Sections 10 and 11.  Update the VKs to account for contact groups and safety at night.
    print("********\nSections 10 and 11: update the vampire knowledge tables by forward propagation of contact results and overnight")
    for t in range(1, len(vks), 2):
        vks[t+1] = update_vk_with_contact_group(vks[t],groups_by_day[day_of_time(t)-1],vks[t+1])
        if t + 2 < len(vks):
            vks[t+2] = update_vk_overnight(vks[t+1],vks[t+2])
    pretty_print_vks(vks)

    # Section 12. Find infection windows for vampires.
    print("********\nSection 12: Vampire infection windows")
    iw = find_infection_windows(vks)
    pretty_print_infection_windows(iw)

    # Section 13. Find possible vampire sires.
    print("********\nSection 13: Find possible vampire sires")
    ps = find_potential_sires(iw, vks, groups_by_day)
    pretty_print_potential_sires(ps)

    # Section 14. Trim the potential sire structure.
    print("********\nSection 14: Trim potential sire structure")
    ps = trim_potential_sires(ps,vks)
    pretty_print_potential_sires(ps)

    # Section 15. Trim the infection windows.
    print("********\nSection 15: Trim infection windows")
    iw = trim_infection_windows(iw,ps)
    pretty_print_infection_windows(iw)

    # Section 16. Update the vk structures with infection windows.
    print("********\nSection 16: Update vampire information tables with infection window data")
    (vks,changes) = update_vks_with_windows(vks,iw)
    pretty_print_vks(vks)
    str_s = "" if changes == 1 else "s"
    print(f'({changes} change{str_s})')

    # Section 17.  Cyclic analysis for sections 14-16 
    print("********\nSection 17: Cyclic analysis for sections 14-16")
    vks,iw,ps,count = cyclic_analysis(vks,iw,ps)
    str_s = "" if count == 1 else "s"    
    print(f'Detected fixed point after {count} iteration{str_s}.')
    print('Potential sires:')
    pretty_print_potential_sires(ps)
    print('Infection windows:')
    pretty_print_infection_windows(iw)
    pretty_print_vks(vks)       

    # Section 18.  Calculate vampire strata
    print("********\nSection 18: Calculate vampire strata")
    (origs,unkns,newbs) = vampire_strata(iw)
    pretty_print_vampire_strata(origs,unkns,newbs)

    # Section 19.  Calculate definite sires
    print("********\nSection 19: Calculate definite vampire sires")
    ss = calculate_sire_sets(ps)
    pretty_print_sire_sets(ss,iw,unkns,False)
    pretty_print_sire_sets(ss,iw,newbs,True)    

    # Section 20.  Find hidden vampires
    print("********\nSection 20: Find hidden vampires")
    (vks, changes) = find_hidden_vampires(ss,iw,newbs,vks)
    pretty_print_vks(vks)           
    str_s = "" if changes == 1 else "s"
    print(f'({changes} change{str_s})')

    # Section 21.  Cyclic analysis for sections 14-20
    print("********\nSection 21: Cyclic analysis for sections 14-20")
    (vks,iw,ps,ss,o,u,n,count) = cyclic_analysis2(vks,groups_by_day)
    str_s = "" if count == 1 else "s"    
    print(f'Detected fixed point after {count} iteration{str_s}.')
    print("Infection windows:")
    pretty_print_infection_windows(iw)
    print("Vampire potential sires:")
    pretty_print_potential_sires(ps)
    print("Vampire strata:")
    pretty_print_vampire_strata(o,u,n)
    print("Vampire sire sets:")    
    pretty_print_sire_sets(ss,iw,u,False)
    pretty_print_sire_sets(ss,iw,n,True)
    pretty_print_vks(vks)       
    

if __name__ == "__main__":
    main()
