#!/usr/bin/python3
from tkinter import *
import subprocess
import os.path
import os

row = 0
column = 0
s = solv_select = 1
g = gen_select = 1



master = Tk()
var1 = IntVar()
var1.set(1)
var2 = IntVar()
var2.set(1)

def quit_loop():
    global column
    global row

    global s
    global g
    column = columnbox.get("1.0", "end-1c")
    row = rowbox.get("1.0", "end-1c")
    g = var1.get()
    s = var2.get()

    master.quit()

master.geometry("350x450")
#master['background']='#103E36'





Label(master, text = "Maze Generator And Solver", bg='#103E36',fg='white').grid(row = 0, columnspan=2)


Label(master, text="").grid(row=1)

columnbox = Text(master, height=1, width=10)
columnbox.grid(row=2, column=1)
Label(master, text = "Number of Columns").grid(row=2, column=0, sticky=W)

rowbox = Text(master, height=1, width=10)
rowbox.grid(row=3, column=1)
Label(master, text = "Number of Rows").grid(row=3, column=0, sticky=W)

Label(master, text="").grid(row=4)

Label(master, text = "Select a Generation Algorithm", bg = '#103E36', fg='white').grid(row=5, sticky=W)
Radiobutton(master, text = "Randomized Prim's", variable=var1, value = 1).grid(row=6, sticky=W)
Radiobutton(master, text = "Randomized Depth-First Search", variable=var1, value = 2).grid(row=7, sticky=W)
Radiobutton(master, text = "Randomized Kruskal's", variable = var1, value = 3).grid(row=8, sticky=W)
Label(master, text="").grid(row=9)
Label(master, text = "Select a Solving Algorithm", bg = '#103E36', fg='white').grid(row=10, sticky=W)
#Radiobutton(master, text = "Player Controlled", variable=var2, value = 1).grid(row=11, sticky=W)
Radiobutton(master, text = "Recursive Backtracking", variable=var2, value = 2).grid(row=12, sticky=W)
Radiobutton(master, text = "Breadth First Search", variable = var2, value = 3).grid(row=13, sticky=W)
Radiobutton(master, text = "Depth First Search", variable = var2, value = 4).grid(row=14, sticky=W)
#Radiobutton(master, text = "A*", variable = var2, value = 5).grid(row=15, sticky=W)
Label(master, text="").grid(row=16)
Button(master, text = "Submit", command=quit_loop).grid(row=17, columnspan=2)
#submit = Button(master, height=1, width=10, text="submit", command=quit_loop)
#submit.grid(row=12, columnspan=2)
master.mainloop()
def main():

    #check_for_binaries()

    generate_call, unsolved = get_generation_call()
    solve_call = get_solve_call(unsolved)

    subprocess.call(generate_call.split())
    subprocess.call(solve_call.split())


def get_generation_call():


    #rows = check_range(0, 100)
    rows = int(row)
    global g

    #cols = check_range(0, 100)
    cols = int(column)


    #generation_alg = check_range(1, 3)
    generation_alg = int(g)

    #print("Would you like to animate maze generation (y/n)?")
    animate_generation = yes_or_no()

    speed = 0
    if animate_generation:
        #print("Enter animation speed (delay in milliseconds)")
        speed = int(10)
        #speed = check_range(0, 10000)

    #print("Please enter a filename to save the unsolved maze to")
    #filename = get_filename("unsolved.txt")
    filename = "unsolved.txt"

    generators = ['prims', 'dfs', 'kruskals']

    generate_call = "./generator_driver"
    generate_call += " --algorithm={}".format(generators[generation_alg-1])
    generate_call += " --file={}".format(filename)
    generate_call += " --animate" if animate_generation else ""
    generate_call += " --speed={}".format(speed if speed > 0 else "0")
    generate_call += " --rows={}".format(rows) if rows > 0 else ""
    generate_call += " --cols={}".format(cols) if cols > 0 else ""

    return generate_call, filename


def get_solve_call(input_file):
    global s





    #solve_alg = check_range(1, 5)
    solve_alg = int(s)

    speed = 0
    if solve_alg != 1:
        #print("Would you like to animate maze solving (y/n)?")
        # animate_solve = True if input(">>>") == 'y' else False
        animate_solve = yes_or_no()
        if animate_solve:
            #print("Enter animation speed (delay in milliseconds)")
            #speed = check_range(0, 10000);
            speed = int(10)
    else:
        animate_solve = True

    #print("Please enter a filename to save the solved maze to")
    #output_file = get_filename("solved.txt")
    output_file = "solved.txt"

    solvers = ['play', 'bt', 'bfs', 'dfs', 'astar']

    solve_call = "./solver_driver"
    solve_call += " --algorithm={}".format(solvers[solve_alg-1])
    solve_call += " --animate" if animate_solve else ""
    solve_call += " --speed={}".format(speed if speed > 0 else "0")
    solve_call += " --infile={}".format(input_file)
    solve_call += " --outfile={}".format(output_file)

    return solve_call


def check_range(lower, upper):
    while True:
        val = input(">>>")
        if not val:
            return lower
        try:
            val = int(val)
            if (val < lower) or (val > upper):
                raise ValueError()
            return val
        except ValueError:
                error_msg = "ERROR: Please choose a number"
                error_msg += " between {} and {}".format(lower, upper)
                print(error_msg)


def yes_or_no():
    while True:
        val = 'y'
        if not val:
            return True
        if val.lower()[0] not in 'yn':
            error_msg = "ERROR: Please choose [y]es or [n]o "
            print(error_msg)
        else:
            return val[0] == 'y'


def check_for_binaries():
    generator_exists = os.path.isfile("./generator_driver")
    solver_exists = os.path.isfile("./solver_driver")
    if not (generator_exists and solver_exists):
        print("At least one of the necessary binaries does not exist")
        print("Attempt to resolve?")
        if yes_or_no():
            make_command = "make > /dev/null"
            FNULL = open(os.devnull, 'w')
            subprocess.call(make_command.split(), stdout=FNULL, stderr=FNULL)

            generator_exists = os.path.isfile("./generator_driver")
            solver_exists = os.path.isfile("./solver_driver")
            if not (generator_exists and solver_exists):
                print("Could not resolve. Try running make?")
                raise Exception("Please consult repo owner")
            else:
                print("\n=== Successfully built binaries ===\n")


def get_filename(default):
    val = input(">>>")
    if not val:
        return default
    else:
        return val

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\rGoodbye!")
    except Exception as e:
        print(e)
