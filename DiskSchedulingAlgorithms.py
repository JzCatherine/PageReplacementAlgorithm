
import os
result_seektime = list()
result_sequence = list()
result_name = list()

def save_result(name, head_start, sequence, seektime):
    sequence.insert(0, head_start)
    result_name.append(name)
    result_seektime.append(seektime)
    result_sequence.append(sequence)

def FCFS(queue, head_start, name="FCFS\t"):
    seektime = 0
    saved_start = head_start
    for curr in queue:
        seektime += abs(head_start - curr)
        head_start = curr
    save_result(name, saved_start, queue, seektime)

def SSTF(queue, head_start):
	seektime = 0
	saved_start = head_start
	sequence = list()
	while queue:
		shortest_seektime = -1
		next_head = None
		for curr in queue:
			if shortest_seektime > abs(head_start - curr) or shortest_seektime == -1:
				shortest_seektime = abs(head_start - curr)
				next_head = curr
		head_start = next_head
		sequence.append(next_head)
		queue.remove(next_head)
	FCFS(sequence, saved_start, "SSTF\t")

# SCAN and LOOK combined
def SCAN(queue, head_start, direction, LOOK=False):
	saved_start = head_start
	left = list()
	right = list()
	for curr in queue:
		if curr < head_start:
			left.append(curr)
		elif curr > head_start:
			right.append(curr)
	seektime = 0
	sequence = list()
	LOWER_LIMIT = 0
	UPPER_LIMIT = 199
	left.sort(reverse=True)
	right.sort()
	if direction == "LEFT":
		if right and not LOOK:
			left.append(LOWER_LIMIT)
		sequence = left + right
	elif direction == "RIGHT":
		if left and not LOOK:
			right.append(UPPER_LIMIT)
		sequence = right + left
	name = "SCAN"
	if LOOK: name = "LOOK"
	FCFS(sequence, saved_start, name + " " + direction)

# CSCAN and CLOOK combined
def CSCAN(queue, head_start, direction, CLOOK=False):
	saved_start = head_start
	left = list()
	right = list()
	for curr in queue:
		if curr < head_start:
			left.append(curr)
		elif curr > head_start:
			right.append(curr)
	seektime = 0
	sequence = list()
	LOWER_LIMIT = 0
	UPPER_LIMIT = 199
	if direction == "LEFT":
		left.sort(reverse=True)
		right.sort(reverse=True)
		if right and not CLOOK:
			left.append(LOWER_LIMIT)
			left.append(UPPER_LIMIT)
		sequence = left + right
	elif direction == "RIGHT":
		right.sort()
		left.sort()
		if left and not CLOOK:
			right.append(UPPER_LIMIT)
			right.append(LOWER_LIMIT)
		sequence = right + left
	name = "C-SCAN"
	if CLOOK: name = "C-LOOK"
	FCFS(sequence, saved_start, name + " " + direction)

# Runner section
def cls():
	os.system("cls" if os.name=="nt" else "clear")
	
def print_display(arr, head_start):
	print("\n\t\t", "DISK SCHEDULING ALGORITHMS")
	print("\t\t", "_" * 50, sep = "")
	print("\n\t\t", "Head Start: ", end = "")
	if head_start: print(head_start)
	print("\t\t", "Request Queue: ", end = "")
	if arr: print(", ".join(arr), end = "")
	print()
	print("\t\t", "_" * 50, sep = "")
	print("\n\t\t[1] Input Request"
		,"\t\t[2] FCFS"
		,"\t\t[3] SSTF"
		,"\t\t[4] SCAN"
		,"\t\t[5] C-SCAN"
		,"\t\t[6] LOOK"
		,"\t\t[7] C-LOOK"
		,"\t\t[8] Summary Table"
		,"\t\t[0] Exit"
		,sep = "\n")
	print("\t\t", "_" * 50, sep = "")

def print_table(arr, head_start, Summary=False):
	print('_' * 110)
	print("\n\tHead Start: ", head_start)
	print("\tRequest Queue: ", end="")
	print(*arr, sep = ",")
	if Summary: print('_' * 45, "  TABLE  SUMMARY  ", '_' * 45)
	else: print('_' * 110)
	print("\n\tAlgorithm", "Seek Time", "Seek Sequence", sep = "\t")
	print("-"*110)
	for name, time, sequence in zip(result_name, result_seektime, result_sequence):
		if not Summary:
			str_sequence = list(map(str, sequence))
			sequence = " -> ".join(str_sequence)
		print("", name, time, "", sequence, sep = "\t")
	print('_' * 110)
	input("\n\nPress any key to continue... ")

c = None
default_input = "98 183 37 122 14 124 65 67"
arr = str.split(default_input)
head_start = 53
while c != 0:
    print_display(arr, head_start)
    c = int(input("\t\tEnter Choice: "))
    if c == 1:
        cls()
        head_start = int(input("Enter Head Start: "))
        arr = str.split(input("Enter inputs separated by space: "))
    elif c == 2:
        cls()
        FCFS(list(map(int, arr)), head_start)
    elif c == 3:
        cls()
        SSTF(list(map(int, arr)), head_start)
    elif c == 4:
        cls()
        SCAN(list(map(int, arr)), head_start, "LEFT")
        SCAN(list(map(int, arr)), head_start, "RIGHT")
    elif c == 5:
        cls()
        CSCAN(list(map(int, arr)), head_start, "LEFT")
        CSCAN(list(map(int, arr)), head_start, "RIGHT")
    elif c == 6:
        cls()
        SCAN(list(map(int, arr)), head_start, "LEFT", True)
        SCAN(list(map(int, arr)), head_start, "RIGHT", True)
    elif c == 7:
        cls()
        CSCAN(list(map(int, arr)), head_start, "LEFT", True)
        CSCAN(list(map(int, arr)), head_start, "RIGHT", True)
    elif c == 8:
        cls()
        FCFS(list(map(int, arr)), head_start)
        SSTF(list(map(int, arr)), head_start)
        SCAN(list(map(int, arr)), head_start, "LEFT")
        SCAN(list(map(int, arr)), head_start, "RIGHT")
        CSCAN(list(map(int, arr)), head_start, "LEFT")
        CSCAN(list(map(int, arr)), head_start, "RIGHT")
        SCAN(list(map(int, arr)), head_start, "LEFT", True)
        SCAN(list(map(int, arr)), head_start, "RIGHT", True)
        CSCAN(list(map(int, arr)), head_start, "LEFT", True)
        CSCAN(list(map(int, arr)), head_start, "RIGHT", True)
        print_table(list(map(int, arr)), head_start, True)
        result_name.clear()
        result_seektime.clear()
        result_sequence.clear()

	# To automatic print result and empty the lists for option 2-7
    if c > 1 and c < 8:
        print_table(list(map(int, arr)), head_start)
        result_name.clear()
        result_seektime.clear()
        result_sequence.clear()
    cls()


