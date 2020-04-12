import numpy.linalg
import time
import datetime
import random

saveboards = ""


def main():
    while True:
        preset = input("Preset? (e)asy - (m)edium - e(x)pert - (n)one\n")
        preset = preset.lower()
        if preset == "n":
            width = int(input("Width?\n"))
            height = int(input("Height?\n"))
            mines = int(input("Mines?\n"))
        elif preset == "e":
            width = 9
            height = 9
            mines = 10
        elif preset == "m":
            width = 16
            height = 16
            mines = 40
        elif preset == "x":
            width = 30
            height = 16
            mines = 99
        else:
            print("Bad input\n\n")
            continue
        repeats = int(input("Repeats?\n"))
        break
    global saveboards
    saveboards = input("Save boards? y/n\n")

    print("Starting...")
    t0 = time.perf_counter()
    wins = 0
    losses = 0
    for i in range(repeats):
        if i % 1000 == 0:
            print(i)
        result = game(width, height, mines)
        if result == True:
            wins += 1
        else:
            losses += 1
    print("Wins:", wins)
    print("Losses:", losses)
    print("Time taken:", time.perf_counter() - t0)
    time.sleep(5)


def game(width, height, mines):
    global saveboards
    width = width
    height = height
    mines = mines
    ### 0-8 --- Number
    ### 9 --- Mine
    board = [[0 for i in range(height)] for j in range(width)]
    ### "F" --- Flagged
    ### "O" --- Opened
    ### "N" --- Nothing
    ### "C" --- Completed
    actions = [["N" for i in range(height)] for j in range(width)]

    # Action list for saving board
    # Format:
    # 	O = Opened
    # 	F = Flagged
    # 	N = Nuked
    # 	C = Completed
    # 	Symbol <space> X <space> Y <\n>
    AL = []

    # Generate mines
    locs = []
    for i in range(width):
        for j in range(height):
            locs.append((i, j))
    for i in range(mines):
        a = random.randint(0, len(locs) - 1)
        pos = locs.pop(a)
        board[pos[0]][pos[1]] = 9

    # Calculate the numbers
    for i in range(width):
        for j in range(height):
            k = 0

            if board[i][j] == 9:
                continue

            # top row
            if j > 0:
                if board[i][j - 1] == 9:
                    k += 1
                if i > 0:
                    if board[i - 1][j - 1] == 9:
                        k += 1
                if i < width - 1:
                    if board[i + 1][j - 1] == 9:
                        k += 1

            # bottom row
            if j < height - 1:
                if board[i][j + 1] == 9:
                    k += 1
                if i > 0:
                    if board[i - 1][j + 1] == 9:
                        k += 1
                if i < width - 1:
                    if board[i + 1][j + 1] == 9:
                        k += 1

            # left and right
            if i > 0:
                if board[i - 1][j] == 9:
                    k += 1
            if i < width - 1:
                if board[i + 1][j] == 9:
                    k += 1

            board[i][j] = k

    # Pick and open one random non-mine square

    # Loop
    # 1) Loop through all Opened squares, if any
    # 	 2) if there is a zero:
    # 		Turn that square to Completed
    # 		Open all adjacent squares
    # 	 3) if number of Nothings around that square equals to the number on the square:
    # 		Flag those squares
    # 		Turn that square to Completed
    # 	 4) if the number of flagged squares around that square equals to the number on the square:
    # 		Open all Nothing squares
    # 		Turn that square to Completed
    # 	 5) if number of Opened squares is 0:
    # 		Board completed
    # 	 6) if number of flags and opened squares stays the same throughout the whole loop, break out from 1)
    #
    # 7) Create the two matrixes, first one is size N*M, second 1*M(add elements dynamically, possibly convert from list to matrix), and a set for Nothing coordinates
    # 8) Loop through the Opened:
    # 	 Create columns for each looped entry
    # 	 Add all coordinate pairs of Nothing that are adjacent to that square to a list
    # Expand the columns with rows for each coordinate pair, with value 0
    # 9) Loop through the Opened:
    # 	 Loop through adjacent Nothings:
    # 		Change value to 1 at  loop number, indexof(coord)
    # 	 Add the (number - no. flags around) to the Vector
    # 10) linealg.solve
    # 11)

    while True:
        rx = random.randint(0, width - 1)
        ry = random.randint(0, height - 1)
        if board[rx][ry] != 9:
            actions[rx][ry] = "O"
            AL.append("O {0} {1}".format(rx, ry))
            break

    Done = False
    Solved = False
    OldOcount = 0
    OldFcount = 0
    OldNcount = 0
    while Done == False:
        gonethrough = 0
        while True:
            for i in range(width):
                for j in range(height):

                    if actions[i][j] != "O":
                        continue

                    if board[i][j] == 9:
                        AL.append("N {0} {1}".format(i, j))
                        Done = True

                    # 2)
                    if board[i][j] == 0:  # Open adjacent
                        if j > 0:
                            if actions[i][j - 1] == "N":
                                actions[i][j - 1] = "O"
                                AL.append("O {0} {1}".format(i, j - 1))
                            if i > 0:
                                if actions[i - 1][j - 1] == "N":
                                    actions[i - 1][j - 1] = "O"
                                    AL.append("O {0} {1}".format(i - 1, j - 1))
                            if i < width - 1:
                                if actions[i + 1][j - 1] == "N":
                                    actions[i + 1][j - 1] = "O"
                                    AL.append("O {0} {1}".format(i + 1, j - 1))
                        if j < height - 1:
                            if actions[i][j + 1] == "N":
                                actions[i][j + 1] = "O"
                                AL.append("O {0} {1}".format(i, j + 1))
                            if i > 0:
                                if actions[i - 1][j + 1] == "N":
                                    actions[i - 1][j + 1] = "O"
                                    AL.append("O {0} {1}".format(i - 1, j + 1))
                            if i < width - 1:
                                if actions[i + 1][j + 1] == "N":
                                    actions[i + 1][j + 1] = "O"
                                    AL.append("O {0} {1}".format(i + 1, j + 1))
                        if i > 0:
                            if actions[i - 1][j] == "N":
                                actions[i - 1][j] = "O"
                                AL.append("O {0} {1}".format(i - 1, j))
                        if i < width - 1:
                            if actions[i + 1][j] == "N":
                                actions[i + 1][j] = "O"
                                AL.append("O {0} {1}".format(i + 1, j))
                        actions[i][j] = "C"
                        # AL.append("C {0} {1}".format(i, j))
                        continue

                    # 3)
                    list_of_Ns = []
                    if j > 0:
                        if actions[i][j - 1] == "N":
                            list_of_Ns.append((0, -1))
                        if i > 0:
                            if actions[i - 1][j - 1] == "N":
                                list_of_Ns.append((-1, -1))
                        if i < width - 1:
                            if actions[i + 1][j - 1] == "N":
                                list_of_Ns.append((1, -1))
                    if j < height - 1:
                        if actions[i][j + 1] == "N":
                            list_of_Ns.append((0, 1))
                        if i > 0:
                            if actions[i - 1][j + 1] == "N":
                                list_of_Ns.append((-1, 1))
                        if i < width - 1:
                            if actions[i + 1][j + 1] == "N":
                                list_of_Ns.append((1, 1))
                    if i > 0:
                        if actions[i - 1][j] == "N":
                            list_of_Ns.append((-1, 0))
                    if i < width - 1:
                        if actions[i + 1][j] == "N":
                            list_of_Ns.append((1, 0))

                    # 4)
                    fc = 0
                    if j > 0:
                        if actions[i][j - 1] == "F":
                            fc += 1
                        if i > 0:
                            if actions[i - 1][j - 1] == "F":
                                fc += 1
                        if i < width - 1:
                            if actions[i + 1][j - 1] == "F":
                                fc += 1
                    if j < height - 1:
                        if actions[i][j + 1] == "F":
                            fc += 1
                        if i > 0:
                            if actions[i - 1][j + 1] == "F":
                                fc += 1
                        if i < width - 1:
                            if actions[i + 1][j + 1] == "F":
                                fc += 1
                    if i > 0:
                        if actions[i - 1][j] == "F":
                            fc += 1
                    if i < width - 1:
                        if actions[i + 1][j] == "F":
                            fc += 1

                    if fc == board[i][j]:
                        for c in list_of_Ns:
                            actions[i + c[0]][j + c[1]] = "O"
                            AL.append("O {0} {1}".format(i + c[0], j + c[1]))
                        actions[i][j] = "C"
                        # AL.append("C {0} {1}".format(i, j))
                        continue

                    if len(list_of_Ns) == board[i][j] - fc:
                        for c in list_of_Ns:
                            actions[i + c[0]][j + c[1]] = "F"
                            AL.append("F {0} {1}".format(i + c[0], j + c[1]))
                        actions[i][j] = "C"
                        # AL.append("C {0} {1}".format(i, j))
                        continue

            gonethrough += 1
            Fcount = 0
            Ocount = 0
            Ncount = 0
            for i in range(width):
                for j in range(height):
                    if actions[i][j] == "F":
                        Fcount += 1
                        continue
                    if actions[i][j] == "O" or actions[i][j] == "C":
                        Ocount += 1
                    if actions[i][j] == "N":
                        Ncount += 1

            if Ncount == 0 and Fcount == mines:
                Done = True
                Solved = True
                break

            if (
                OldOcount == Ocount and OldFcount == Fcount and OldNcount == Ncount
            ):  # Move to more sophisticated methods
                if gonethrough >= 2:
                    break
            else:
                OldOcount = Ocount
                OldFcount = Fcount
                OldNcount = Ncount
                gonethrough = 0

            if Done == True:
                break  # nuked

        if Done == True:  # No need to filter later
            break

        # Matrix evaluation
        rows = []  # main data
        total = []  # square values

        coords = []

        Ms = mines
        for i in range(width):
            for j in range(height):
                if actions[i][j] == "N":
                    coords.append((i, j))
                    continue
                if actions[i][j] == "F":
                    Ms -= 1

        for i in range(width):
            for j in range(height):

                if actions[i][j] != "O":
                    continue
                temp = [0 for a in range(len(coords))]
                Fs = 0

                if j > 0:
                    if actions[i][j - 1] == "N":
                        temp[coords.index((i, j - 1))] = 1
                    elif actions[i][j - 1] == "F":
                        Fs += 1
                    if i > 0:
                        if actions[i - 1][j - 1] == "N":
                            temp[coords.index((i - 1, j - 1))] = 1
                        elif actions[i - 1][j - 1] == "F":
                            Fs += 1
                    if i < width - 1:
                        if actions[i + 1][j - 1] == "N":
                            temp[coords.index((i + 1, j - 1))] = 1
                        elif actions[i + 1][j - 1] == "F":
                            Fs += 1
                if j < height - 1:
                    if actions[i][j + 1] == "N":
                        temp[coords.index((i, j + 1))] = 1
                    elif actions[i][j + 1] == "F":
                        Fs += 1
                    if i > 0:
                        if actions[i - 1][j + 1] == "N":
                            temp[coords.index((i - 1, j + 1))] = 1
                        elif actions[i - 1][j + 1] == "F":
                            Fs += 1
                    if i < width - 1:
                        if actions[i + 1][j + 1] == "N":
                            temp[coords.index((i + 1, j + 1))] = 1
                        elif actions[i + 1][j + 1] == "F":
                            Fs += 1
                if i > 0:
                    if actions[i - 1][j] == "N":
                        temp[coords.index((i - 1, j))] = 1
                    elif actions[i - 1][j] == "F":
                        Fs += 1
                if i < width - 1:
                    if actions[i + 1][j] == "N":
                        temp[coords.index((i + 1, j))] = 1
                    elif actions[i + 1][j] == "F":
                        Fs += 1

                rows.append(temp)
                total.append((board[i][j] - Fs))

        rows.append([1 for i in range(len(coords))])

        total.append(Ms)

        solution = numpy.linalg.lstsq(rows, total)[0]

        # Analyze the solution
        small = 1
        smallindex = 0
        OorF = False
        smallest = []
        for val in range(len(solution)):
            if abs(solution[val] - 1) < 0.000005:
                A = coords[val]
                actions[A[0]][A[1]] = "F"
                AL.append("F {0} {1}".format(A[0], A[1]))
                OorF = True
            elif abs(solution[val]) < 0.000005:
                A = coords[val]
                actions[A[0]][A[1]] = "O"
                AL.append("O {0} {1}".format(A[0], A[1]))
                OorF = True
            else:
                if abs(solution[val]) < small:
                    small = abs(solution[val])
                    smallindex = val
                    smallest = []
                    smallest.append(val)
                elif abs(abs(solution[val]) - small) < 0.000005:
                    smallest.append(val)

        if OorF == False:
            if len(smallest) == 1:
                A = coords[smallindex]
                actions[A[0]][A[1]] = "O"
                AL.append("O {0} {1}".format(A[0], A[1]))
            elif len(smallest) > 1:
                A = coords[random.choice(smallest)]
                actions[A[0]][A[1]] = "O"
                AL.append("O {0} {1}".format(A[0], A[1]))

    if saveboards == "y":
        writeboard(board, AL, height, width, mines)

    return Solved


def writeboard(board, AL, height, width, mines):
    fname = str(datetime.datetime.now())
    fname = fname.replace(".", "-")
    fname = fname.replace(":", "-")
    f = open(
        str(width) + "-" + str(height) + "x" + str(mines) + "---" + fname + ".txt", "w"
    )

    for i in range(height):
        for j in range(width):
            f.write(str(board[j][i]))
        f.write("\n")

    for a in AL:
        f.write(a)
        f.write("\n")

    f.close()


if __name__ == "__main__":
    main()

