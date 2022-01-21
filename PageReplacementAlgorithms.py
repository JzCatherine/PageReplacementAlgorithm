import os

def displaySimulation(algo, reference_string, frame, arr_data, page_fault, page_fault_arr):
    rows, cols = (frame, len(reference_string))
    line = ["----"]*cols
    print("\n", algo, " PAGE REPLACEMENT ALGORITHM", sep="")
    print("Simulation:")
    print("ReferenceString", end="")  # Print Reference String
    print("\t", ("{:4}"*len(reference_string)).format(*reference_string))
    for i in range(rows):  # Print Frames
        print("\t\t ", ("{:4}"*len(line)).format(*line))
        print("\tFrame#{}".format(i+1), end="")
        print("\t", ("{:4}"*len(arr_data[i][:])).format(*arr_data[i][:]))
    print("\t\t ", ("{:4}"*len(line)).format(*line))
    print("\tFault", end="")
    # Print Fault Columns
    print("\t", ("{:>4}"*len(page_fault_arr)).format(*page_fault_arr))
    print("\n\tTotal Page Fault =", page_fault, "\n")
    input("\n\nPress any key to continue... ")

def SummaryTable(reference_string_inp, frame, output):
    page_faults_arr = [['']*2 for _ in range(6)]
    page_faults_arr[0][1] = (FIFO("FIFO", reference_string_inp, frame, output))
    page_faults_arr[1][1] = (OPT("OPT", reference_string_inp, frame, output))
    page_faults_arr[2][1] = (
        MRU_LRU("LRU", reference_string_inp, frame, output))
    page_faults_arr[3][1] = (
        MRU_LRU("MRU", reference_string_inp, frame, output))
    page_faults_arr[4][1] = (
        LFU_MFU("LFU", reference_string_inp, frame, output))
    page_faults_arr[5][1] = (
        LFU_MFU("MFU", reference_string_inp, frame, output))
    # FIFO > OPT > LRU > MRU > LFU > MFU
    page_faults_arr[0][0] = "First-In-First-Out"
    page_faults_arr[1][0] = "Optimal"
    page_faults_arr[2][0] = "Least Recently Used"
    page_faults_arr[3][0] = "Most Recently Used"
    page_faults_arr[4][0] = "Least Frequently Used"
    page_faults_arr[5][0] = "Most Frequently Used"
    print('_' * 80)
    print("\n\tReference String: ", end="")
    print(*reference_string_inp, sep=",")
    print("\tFrames: ", frame)
    print('_' * 31, " TABLE  SUMMARY ", '_' * 31)
    print("\n\t PAGE REPLACEMENT ALGORITHMS", "\t\t ", "TOTAL PAGE FAULTS")
    for i in range(len(page_faults_arr)):
        print('-' * 80)
        print(
            "\t ", ("{:25}"*len(page_faults_arr[i][:])).format(*page_faults_arr[i][:]))
    print('_' * 80, end="")
    input("\n\nPress any key to continue... ")


def FIFO(algo, reference_string_inp, frame, output):
    reference_string = list(reference_string_inp)
    rows, cols = (frame, len(reference_string))
    arr_data = [['']*cols for _ in range(rows)]  # Store Simulation
    current_pages = []*rows     # Store current pages in memory
    fifo_pages = []*rows        # Store current pages in memory FIFO order
    page_fault_arr = []*cols     # Store current pages in memory
    page_fault = 0
    for i, element in enumerate(reference_string):
        # if all frames are occupied
        if len(current_pages) == rows:
            if (element not in current_pages):
                for n, j in enumerate(current_pages):
                    if j == fifo_pages[0]:
                        current_pages[n] = element
                        page_fault += 1
                        page_fault_arr.append("F")
                        fifo_pages.pop(0)
                        fifo_pages.append(element)
                        break
            else:
                page_fault_arr.append("-")
        # if there is still frame unoccupied
        if len(current_pages) != rows:
            if (element not in current_pages):
                current_pages.append(element)
                page_fault += 1
                page_fault_arr.append("F")
            else:
                page_fault_arr.append("-")
            fifo_pages = list(current_pages)
        # To record simulation
        for k in range(len(current_pages)):
            if page_fault_arr[-1] == "F":
                arr_data[k][i] = current_pages[k]
    if output == "DISPLAY":
        displaySimulation(algo, reference_string, frame,
                          arr_data, page_fault, page_fault_arr)
    if output == "PAGEFAULT":
        return page_fault


def OPT(algo, reference_string_inp, frame, output):
    reference_string = list(reference_string_inp)
    # Stores future reference_string queue
    opt_ref_str = list(reference_string_inp)
    rows, cols = (frame, len(reference_string))
    arr_data = [['']*cols for _ in range(rows)]  # Store Simulation
    current_pages = []*rows     # Store current pages in memory
    page_fault_arr = []*cols    # Store fault and page hit
    page_fault = 0
    for i, element in enumerate(reference_string):
        # if all frames are occupied
        if len(current_pages) == rows:
            if (element not in current_pages):
                # check if current pages exist in opt_ref_str
                check = all(item in opt_ref_str for item in current_pages)
                # if page in current_page is not on future queue
                if check is not True:
                    for n, j in enumerate(current_pages):
                        if (j not in opt_ref_str):
                            current_pages[n] = element
                            page_fault += 1
                            page_fault_arr.append("F")
                            break
                # if page in current_page is in future queue
                if check is True:
                    longest = 0
                    for n, j in enumerate(current_pages):
                        index = opt_ref_str.index(j)
                        if (index > longest):
                            longest = index
                    index = current_pages.index(opt_ref_str[longest])
                    current_pages[index] = element
                    page_fault += 1
                    page_fault_arr.append("F")
            else:
                page_fault_arr.append("-")
            opt_ref_str.pop(0)
        # if there is still frame unoccupied
        if len(current_pages) != rows:
            if (element not in current_pages):
                current_pages.append(element)
                page_fault += 1
                page_fault_arr.append("F")
            else:
                page_fault_arr.append("-")
            opt_ref_str.pop(0)
        # To record simulation
        for k in range(len(current_pages)):
            if page_fault_arr[-1] == "F":
                arr_data[k][i] = current_pages[k]
    if output == "DISPLAY":
        displaySimulation(algo, reference_string, frame,
                          arr_data, page_fault, page_fault_arr)
    if output == "PAGEFAULT":
        return page_fault


def MRU_LRU(algo_inp, reference_string_inp, frame, output):
    algo = algo_inp
    reference_string = list(reference_string_inp)
    rows, cols = (frame, len(reference_string))
    arr_data = [['']*cols for _ in range(rows)]  # Stores the simulation
    current_pages = []*rows       # Stores current pages in memory
    page_fault_arr = []           # Stores 'F' for page Fault and '-' for Page hit
    page_fault = 0
    # Stores current most/least recently used page
    ru_page = reference_string[0]
    lru_arr = []*rows             # Stores LRU pages
    for i, element in enumerate(reference_string):
        # Frames all occupied
        if len(current_pages) == rows:
            if element not in current_pages:
                for n, j in enumerate(current_pages):
                    if j == ru_page:
                        current_pages[n] = element
                        page_fault += 1
                        page_fault_arr.append("F")
                        if algo == "LRU":
                            lru_arr.pop(0)
                            lru_arr.append(element)
            else:
                if algo == "LRU":
                    lru_arr.remove(element)
                    lru_arr.append(element)
                page_fault_arr.append("-")
        # if there is still frame unoccupied
        if len(current_pages) != rows:
            if element not in current_pages:
                current_pages.append(element)
                page_fault += 1
                page_fault_arr.append("F")
                if algo == "LRU":
                    lru_arr.append(element)
            else:
                if algo == "LRU":
                    lru_arr.remove(element)
                    lru_arr.append(element)
                page_fault_arr.append("-")
        # To record simulation
        for k in range(len(current_pages)):
            if page_fault_arr[-1] == "F":
                arr_data[k][i] = current_pages[k]
        # update most/least recently used page
        if algo == "MRU":
            ru_page = element
        if algo == "LRU":
            ru_page = lru_arr[0]
    if output == "DISPLAY":
        displaySimulation(algo, reference_string, frame,
                          arr_data, page_fault, page_fault_arr)
    elif output == "PAGEFAULT":
        return page_fault


def LFU_MFU(mode, reference_string_inp, frame, output):
    reference_string = list(reference_string_inp)
    rows, cols = (frame, len(reference_string))
    arr_data = [['']*cols for i in range(rows)]  # Store whole simulation
    # Counter for each item in reference_string
    page_frequency = {element: 0 for element in reference_string}
    memory_pages = list()  # Pages in column occupying memory
    page_fault_arr = list()
    page_fault_count = 0
    fifo_list = list()  # Used to break a tie if it occurs
    for i in range(len(reference_string)):
        curr_page = reference_string[i]
        does_page_fault_occur = False
        if curr_page not in memory_pages:
            if len(memory_pages) < rows:
                memory_pages.append(curr_page)
            else:
                # Do page replacement LFU or MFU
                highest_freq = 0
                lowest_freq = len(reference_string)
                for page in memory_pages:
                    highest_freq = max(page_frequency.get(page), highest_freq)
                    lowest_freq = min(page_frequency.get(page), lowest_freq)
                condition = None
                if mode == "LFU":
                    condition = lowest_freq
                elif mode == "MFU":
                    condition = highest_freq
                # Find pages that matches the condition
                pages_to_replace = list()
                for page in memory_pages:
                    if condition == page_frequency.get(page):
                        pages_to_replace.append(page)
                # Do FCFS for tie breaker
                index_in_fcfs = rows + 1
                for page in pages_to_replace:
                    index_in_fcfs = min(fifo_list.index(page), index_in_fcfs)
                page_to_replace = fifo_list[index_in_fcfs]
                memory_pages.insert(memory_pages.index(
                    page_to_replace), curr_page)
                memory_pages.remove(page_to_replace)
                fifo_list.remove(page_to_replace)
            does_page_fault_occur = True
        # For printing later
        if does_page_fault_occur:
            page_fault_arr.append("F")
            page_fault_count += 1
            # To record simulation
            for j in range(len(memory_pages)):
                arr_data[j][i] = memory_pages[j]
        else:
            page_fault_arr.append("-")
        # To update fifo_list
        if curr_page not in fifo_list:
            fifo_list.append(curr_page)
        page_frequency[curr_page] = page_frequency.get(
            curr_page) + 1  # Add 1 to value of curr_page
    if output == "DISPLAY":
        displaySimulation(mode, reference_string, frame,
                          arr_data, page_fault_count, page_fault_arr)
    if output == "PAGEFAULT":
        return page_fault_count


def clear():
    os.system('cls' if os.name == "nt" else 'clear')


def display(arr):
    clear()
    print('''
          \t.-. .  .-..--  .-..--.-..    .  .-.--.  ..--. .---    .  .  .-..-.----.----. ..  ..-.
          \t|-'/_\ |-.|-   |-'|- |-'|   /_\(  |- |\/||- |\| |    /_\ |  |-.| | |  |  | |-||\/|`-.
          \t' '   ''-''--  '`-'--'  '-''   '`-'--'  ''--' ' '   '   ''-''-'`-' ' -'- ' ' ''  '`-' ''')
    print("\t\t", "_" * 85, sep="")
    print("\n\t\tReference String: ", end="")
    print(*arr, sep=",")
    print("\t\tFrame: ", frame)
    print("\t\t", "_" * 85, sep="")
    print('''
    \t\t[1] First-In-First-Out
    \t\t[2] Optimal Algorithm
    \t\t[3] Least Recently Used
    \t\t[4] Most Recently Used
    \t\t[5] Least Frequently Used
    \t\t[6] Most Frequently Used
    \t\t[7] Summary Table
    \t\t[8] INPUT QUEUE
    \t\t[9] CLEAR QUEUE
    \t\t[0] EXIT''')


choice = None
arr = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
frame = 3
while choice != 0:
    display(arr)
    print("\t\t", "_" * 85, sep="")
    choice = int(input("\t\tSelect: "))
    if choice == 1:
        clear()
        if len(arr) == 0:
            input("Access Queue Empty!\n\nPress any key to continue... ")
        else:
            FIFO("FIFO", list(map(int, arr)), frame, "DISPLAY")
    if choice == 2:
        clear()
        if len(arr) == 0:
            input("Access Queue Empty!\n\nPress any key to continue... ")
        else:
            OPT("OPT", list(map(int, arr)), frame, "DISPLAY")
    if choice == 3:
        clear()
        if len(arr) == 0:
            input("Access Queue Empty!\n\nPress any key to continue... ")
        else:
            MRU_LRU("LRU", list(map(int, arr)), frame, "DISPLAY")
    if choice == 4:
        clear()
        if len(arr) == 0:
            input("Access Queue Empty!\n\nPress any key to continue... ")
        else:
            MRU_LRU("MRU", list(map(int, arr)), frame, "DISPLAY")
    if choice == 5:
        clear()
        if len(arr) == 0:
            input("Access Queue Empty!\n\nPress any key to continue... ")
        else:
            LFU_MFU("LFU", list(map(int, arr)), frame, "DISPLAY")
    if choice == 6:
        clear()
        if len(arr) == 0:
            input("Access Queue Empty!\n\nPress any key to continue... ")
        else:
            LFU_MFU("MFU", list(map(int, arr)), frame, "DISPLAY")
    if choice == 7:
        clear()
        if len(arr) == 0:
            input("Access Queue Empty!\n\nPress any key to continue... ")
        else:
            SummaryTable(list(map(int, arr)), frame, "PAGEFAULT")
    if choice == 8:
        clear()
        arr = list(
            map(int, input("Enter Reference String (separated by whitespace): ").split(" ")))
        frame = int(input("Enter No. of Frame: "))
        input("\n\nPress any key to continue... ")
    if choice == 9:
        arr.clear()
        frame = 0
