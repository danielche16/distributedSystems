# reading files
f1 = open("C:\\PyghonProgramms\\warehouse_data\\warehouse_1.data", "r")
f2 = open("C:\\PyghonProgramms\\mqtt_files\\warehouse_1.data", "r")

# list to store file lines
lines = []
# read file
with open(r"C:\\PyghonProgramms\\mqtt_files\\warehouse_1.data", 'r') as fp:
    # read an store all lines into list
    lines = fp.readlines()

# Write file
with open(r"C:\\PyghonProgramms\\testfiles\\warehouse_1_new.data", 'w') as fp:
    # iterate each line
    for number, line in enumerate(lines):
        # delete line 5 and 8. or pass any Nth line you want to remove
        # note list index starts from 0
        if number not in [0, 2, 4, 6, 8, 10]:
            fp.write(line)
f3 = open("C:\\PyghonProgramms\\testfiles\\warehouse_1_new.data")


i = 0


for line1 in f1:
    i += 1
    for line2 in f3:

        # matching line1 from both files
        if line1 == line2:
            # print IDENTICAL if similar
            print("Line ", i, ": IDENTICAL")
        else:
            print("Line ", i, ":")
            # else print that line from both files
            print("\tFile 1:", line1, end='')
            print("\tFile 2:", line2, end='')
        break

# closing files
f1.close()
f2.close()
f3.close()