import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("txtdata.csv", names=['sec','subsec','data'])
seclist = ['Ancient India', 'Medieval India', 'Colonial India',
 'Independence and Modern India']

def main_menu():
    global df
    print("\nWelcome to the History of India Program!")
    print('Select mode of operation')
    print("1.Edit Mode")
    print("2.View Mode")
    print("3.Exit")
    
    a = input("Enter your choice (1-3): ")
    
    if a == "1":
        editor()
    elif a == "2":
        viewer()
    elif a == "3":
        print("Exiting the program...")
        df.to_csv("txtdata.csv", index=False, columns=None, header=False)
        exit()
def editor():
    global df, seclist, subseclist
    print("-- Existing Sections--")
    for i in range(len(seclist)):
        print(str(i+1)+".", seclist[i])
    print(str(i+2)+".", "Previous Menu")
    sec = input("Enter the section number to edit(1-{}): ".format(i+2))
    if sec == str(i+2):
        main_menu()
        return
    try:
        sec = seclist[int(sec)-1]
    except IndexError:
        raise(IndexError("Enter a Valid Input"))
    print("\n--- Edit Mode ---")
    print("1. Add/Edit a new topic")
    print("2. Delete an existing topic")
    print("3. Back to Main Menu")
    choice = input("Enter your choice (1-4): ")
    if choice == '1':
        subseclist = df[df['sec']==sec]['subsec'].unique()
        print("\n")
        print("--Pre existing Topics in {}--".format(sec))
        for i in subseclist:
            print(i)
        print("\n--- Add a new topic or Enter name of prexisting to edit it---")
        subsec = input("Enter the name of the topic: ")
        if subsec in subseclist:
            ovr = input("Do you want to overwrite the existing topic Data for {} [O] or want to append to it[A]? [O/A]: ".format(subsec))
            if ovr.upper() == 'O':
                df.drop(list(df[df['subsec'] == subsec].index), inplace=True)
                print("Enter the new data to overwrite the topic \"{}\"", subsec)
                print("Enter the data Line by line by using enter to seperate lines, once you are done press ENTER twice or Ctrl+Z to save")
                lines = []
                while True:
                    try:
                        line = input()
                    except EOFError:
                        break
                    if line == "":
                        break
                    lines.append(line.strip())
                xdict = {'sec': [sec]*len(lines), 'subsec': [subsec]*len(lines), 'data': lines}
                xdf = pd.DataFrame(xdict)
                df = pd.concat([df, xdf],ignore_index=True,axis=0)
                print("Done!")
                print(df)            
            elif ovr.upper() == 'A':
                print("Enter the data Line by line by using enter to seperate lines, once you are done press ENTER twice or Ctrl+Z to save")
                lines = []
                while True:
                    try:
                        line = input()
                    except EOFError:
                        break
                    if line == "":
                        break
                    lines.append(line.strip())
                xdict = {'sec': [sec]*len(lines), 'subsec': [subsec]*len(lines), 'data': lines}
                xdf = pd.DataFrame(xdict)
                df = pd.concat([df, xdf],ignore_index=True,axis=0)
                print("Done!")
                print(df)
        else:
            print("Enter the data Line by line by using enter to seperate lines, once you are done press ENTER twice or Ctrl+Z to save")
            lines = []
            while True:
                try:
                    line = input()
                except EOFError:
                    break
                if line == "":
                    break
                lines.append(line.strip())
            xdict = {'sec': [sec]*len(lines), 'subsec': [subsec]*len(lines), 'data': lines}
            xdf = pd.DataFrame(xdict)
            df = pd.concat([df, xdf],ignore_index=True,axis=0)
            print("Done!")
            print(df)
    elif choice == '2':
        print("\n--- Delete an existing topic ---")
        subseclist = df[df['sec']==sec]['subsec'].unique()
        print("--Pre existing Topics in {}--".format(sec))
        for i in subseclist:
            print(i)
        subsec = input("Enter the name of the topic to delete: ")
        try:
            df.drop(df[df['subsec'] == subsec].index, inplace=True)
            print("Topic \"{}\" deleted successfully!".format(subsec))
        except KeyError:
            print("Topic \"{}\" not found!".format(subsec))
    elif choice == '3':
        print("\n--- Back to Main Menu ---")
        main_menu()
def viewer():
    global a, sec, subsec
    print("1. View a topic")
    print("2. View Graphical Data")
    print("3. Back to Main Menu")

    choice = input("Enter your choice (1-3): ")
    
    if choice == "1":
        for i in range(len(seclist)):
            print(str(i+1)+".", seclist[i])
        sec = input("Enter the section number to edit(1-{}): ".format(i+1))

        try:
            sec = seclist[int(sec)-1]
        except IndexError: 
            print("Invalid section number!")
            viewer()

        subseclist = df[df['sec']==sec]['subsec'].unique().tolist()

        print("--Topics in {}--".format(sec))
        for i in range(len(subseclist)):
            print(str(i+1)+".", subseclist[i])
        sec = input("Enter the topic number to edit(1-{}): ".format(i+1))

        try:
            subsec = subseclist[int(sec)-1]
        except IndexError:
            print("Invalid topic number!")
            viewer()
            
        print("You are Reading")
        print(sec)
        print(subsec)
        print("------------")
        for i in df[df['subsec'] == subsec]['data']:
            print('\n')
            print(i)
            
    elif choice == "2":
        print("Graphical Data About Indian Subcontinent")
        grapher()
    
    elif choice == "3":
        main_menu()
def grapher():
    print("1. Population")
    print("2. GDP")
    print("3. Literacy Rate")
    print("4. Life Expectancy")
    print("5. Back to Previous Menu")
    choice = input("Enter your choice (1-5): ")
    if choice == "1":
        years = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
        population_crores = [37.6, 44.8, 55.5, 69.8, 83.8, 105.3, 123.4,136.6]
        plt.plot(years, population_crores, marker='o')
        plt.title('Population of India')
        plt.xlabel('Year')
        plt.ylabel('Population (Crores)')
        plt.show()
    elif choice == "2":
        years = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
        gdp_lakh_crores = [2.7, 4.1, 6.5, 10.2, 17.0, 27.8, 44.2, 58.3]
        plt.plot(years, gdp_lakh_crores, marker='o', linestyle='-', color='b')
        plt.title('GDP of India Over the Years (in Lakh Crores)')
        plt.xlabel('Year')
        plt.ylabel('GDP (in Lakh Crores)')
        plt.grid(True)
        plt.show()
    elif choice == "3":
        years = [1951, 1961, 1971, 1981, 1991, 2001, 2011, 2021]
        literacy_rate = [18.3, 28.3, 34.5, 43.6, 52.2, 64.8, 74.0, 77.7]
        plt.figure(figsize=(10, 6))
        plt.plot(years, literacy_rate, marker='o', linestyle='-', color='b')
        plt.title('Literacy Rate of India Over the Years')
        plt.xlabel('Year')
        plt.ylabel('Literacy Rate (%)')
        plt.grid(True)
        plt.show()
    elif choice == "4":
        years = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
        life_expectancy = [35.0, 41.2, 48.4, 55.4, 58.6, 62.5, 66.8, 69.7]
        plt.figure(figsize=(10, 6))
        plt.plot(years, life_expectancy, marker='o', linestyle='-', color='b')
        plt.title('Life Expectancy of India Over the Years')
        plt.xlabel('Year')
        plt.ylabel('Life Expectancy (in years)')
        plt.grid(True)
        plt.show()

    elif choice == "5":
        viewer()
    else:
        print("Invalid choice!")
while True:
    main_menu()
