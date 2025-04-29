import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.ndimage import gaussian_filter

# Colors
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
ENDC = '\033[0m'

#Const
BUSNUM = 0
BUSNAME = 5
LOADMW = 11
GENMW = 13
SUBSTATION = 4
BRANCHMVA = 10
BRANCHTYPE = 6
BRANCHFROM = 1
BRANCHTO = 3
BRANCHMAXPERCENT = 12
GENTYPE = 18
GENMW_COL = 5
GENMVAR_COL = 6

logo = r'''
____   ___   __    __    ___  ____       _____  _       ___   __    __ 
|    \ /   \ |  |__|  |  /  _]|    \     |     || |     /   \ |  |__|  |
|  o  )     ||  |  |  | /  [_ |  D  )    |   __|| |    |     ||  |  |  |
|   _/|  O  ||  |  |  ||    _]|    /     |  |_  | |___ |  O  ||  |  |  |
|  |  |     ||  `  '  ||   [_ |    \     |   _] |     ||     ||  `  '  |
|  |  |     | \      / |     ||  .  \    |  |   |     ||     | \      / 
|__|   \___/   \_/\_/  |_____||__|\_|    |__|   |_____| \___/   \_/\_/  
                                                                        
          ____  ____    ____  _      __ __  _____    ___  ____          
         /    ||    \  /    || |    |  |  ||     |  /  _]|    \         
        |  o  ||  _  ||  o  || |    |  |  ||__/  | /  [_ |  D  )        
        |     ||  |  ||     || |___ |  ~  ||   __||    _]|    /         
        |  _  ||  |  ||  _  ||     ||___, ||  /  ||   [_ |    \         
        |  |  ||  |  ||  |  ||     ||     ||     ||     ||  .  \        
        |__|__||__|__||__|__||_____||____/ |_____||_____||__|\_|        
                                                                        '''

#Vars
bus_data = []
branch_data = []
generator_data = []
bus_file_name = "N/A"
branch_file_name = "N/A"
generator_file_name = "N/A"
file_type = ""
maxLoad = float('-inf')
maxLoadNum = None
maxLoadName = None
maxGen = float('-inf')
maxGenNum = None
maxGenName = None
substationLoads = {}
maxSubName = None
maxLoadSub = float('-inf')
maxSubGenName = None
maxGenSub = float('-inf')
maxLineS = float("-inf")
maxLineSTo = None
maxLineSFrom = None
maxLinePercent = float("-inf")

#Functions
def largestBusLoadAct():
    if not bus_data:
        print(f"{RED}Error: No bus data loaded{ENDC}")
        return

    maxLoad = float('-inf')
    maxLoadNum = None
    maxLoadName = None
    
    for row in bus_data:
        try:
            load = float(row[LOADMW])
            if load > maxLoad:
                maxLoad = load
                maxLoadNum = row[BUSNUM]
                maxLoadName = row[BUSNAME]
        except (ValueError, IndexError):
            continue
    
    clear_screen()
    print(f"\n{YELLOW}MAX ACTIVE LOAD:{ENDC} {RED}{maxLoad}{ENDC} MW")
    print(f"{YELLOW}Bus Number:{ENDC} {BLUE}{maxLoadNum}{ENDC}")
    print(f"{YELLOW}Bus Name:{ENDC} {GREEN}{maxLoadName}{ENDC}")
    return
    
def largestBusGenerationAct():
    if not bus_data:
        print(f"{RED}Error: No bus data loaded{ENDC}")
        return
    
    maxGen = float('-inf')
    maxGenNum = None
    maxGenName = None
    
    for row in bus_data:
        try:
            gen = float(row[GENMW])
            if gen > maxGen:
                maxGen = gen
                maxGenNum = row[BUSNUM]
                maxGenName = row[BUSNAME]
        except (ValueError, IndexError):
            continue
    
    clear_screen()
    print(f"\n{YELLOW}MAX ACTIVE GENERATION:{ENDC} {RED}{maxGen}{ENDC} MW")
    print(f"{YELLOW}Bus Number:{ENDC} {BLUE}{maxGenNum}{ENDC}")
    print(f"{YELLOW}Bus Name:{ENDC} {GREEN}{maxGenName}{ENDC}")
    return
    
def largestSubstationLoad():
    if not bus_data:
        print(f"{RED}Error: No bus data loaded{ENDC}")
        return
    
    # Dictionary to store substation loads
    substationLoads = {}
    
    for row in bus_data:
        try:
            substation = row[SUBSTATION]
            load = float(row[LOADMW])
            
            # Add load to substation's total
            if substation in substationLoads:
                substationLoads[substation] += load
            else:
                substationLoads[substation] = load
                
        except (ValueError, IndexError):
            continue
    
    # Find substation with maximum load
    maxSubName = None
    maxLoadSub = float('-inf')
    
    for substation, load in substationLoads.items():
        if load > maxLoadSub:
            maxLoadSub = load
            maxSubName = substation
    
    clear_screen()
    print(f"\n{YELLOW}MAX ACTIVE LOAD:{ENDC} {RED}{maxLoadSub}{ENDC} MW")
    print(f"{YELLOW}Substation Name:{ENDC} {GREEN}{maxSubName}{ENDC}")
    return
    
def largestSubstationGeneration():
    if not bus_data:
        print(f"{RED}Error: No bus data loaded{ENDC}")
        return
    
    # Dictionary to store substation loads
    substationGens = {}
    
    for row in bus_data:
        try:
            substation = row[SUBSTATION]
            gen = float(row[GENMW])
            
            if substation in substationGens:
                substationGens[substation] += gen
            else:
                substationGens[substation] = gen
                
        except (ValueError, IndexError):
            continue
    
    # Find substation with maximum gen
    maxSubGenName = None
    maxGenSub = float('-inf')
    
    for substation, gen in substationGens.items():
        if gen > maxGenSub:
            maxGenSub = gen
            maxSubGenName = substation
    
    clear_screen()
    print(f"\n{YELLOW}MAX ACTIVE GENERATION:{ENDC} {RED}{maxGenSub}{ENDC} MW")
    print(f"{YELLOW}Substation Name:{ENDC} {GREEN}{maxSubGenName}{ENDC}")
    return

def largestLineAppPower():
    if not branch_data:
        print(f"{RED}Error: No branch data loaded{ENDC}")
        return
    
    maxLineS = float("-inf")
    maxLineSTo = None
    maxLineSFrom = None
    maxLinePercent = float("-inf")

    for row in branch_data:
        if row[BRANCHTYPE] != "Line" :
            continue
        
        try:
            apparentPower = float(row[BRANCHMVA])
            if apparentPower > maxLineS:
                maxLineS = apparentPower
                maxLineSTo = row[BRANCHTO]
                maxLineSFrom = row[BRANCHFROM]
                maxLinePercent = row[BRANCHMAXPERCENT]
        except (ValueError, IndexError):
            continue
        
        clear_screen()
        print(f"\n{YELLOW}MAX APPARENT LOAD:{ENDC} {RED}{maxLineS}{ENDC} MVA")
        print(f"{YELLOW}From:{ENDC} {BLUE}{maxLineSFrom}{ENDC}")
        print(f"{YELLOW}To:{ENDC} {BLUE}{maxLineSTo}{ENDC}")
        print(f"{YELLOW}% of Limit:{ENDC} {MAGENTA}{maxLinePercent}%{ENDC}")
        return

def generateHeatMap():
    if not bus_data:
        print("{RED}Error: No bus data loaded{ENDC}")
        return
    
    # Extract coordinates and generation values
    x_coords = []
    y_coords = []
    gen_values = []
    
    for row in bus_data:
        try:
            x = float(row[2])  # X coordinate (2nd column)
            y = float(row[1])  # Y coordinate (3rd column)
            gen = float(row[GENMW])  # Generation (13th column)
            
            x_coords.append(x)
            y_coords.append(y)
            gen_values.append(gen)
        except (ValueError, IndexError):
            continue
    
    if not x_coords or not y_coords or not gen_values:
        print("Error: No valid data points found")
        return
        
    # Create grid
    grid_size = 200
    x_grid = np.linspace(min(x_coords), max(x_coords), grid_size)
    y_grid = np.linspace(min(y_coords), max(y_coords), grid_size)
    X, Y = np.meshgrid(x_grid, y_grid)
    Z = np.zeros_like(X)
    
    # Calculate standard deviation for Gaussian based on grid size
    # Use smaller sigma for better cluster detection
    sigma = max_distance = np.sqrt((max(x_coords) - min(x_coords))**2 + (max(y_coords) - min(y_coords))**2) / 30
    
    # Normalize generation values to prevent domination by large values
    max_gen = max(gen_values)
    normalized_gens = [((gen/max_gen)**0.5) * max_gen for gen in gen_values]
    
    # Add Gaussian contribution from each generation point
    for x, y, gen in zip(x_coords, y_coords, normalized_gens):
        if gen > 0:  # Only consider positive generation
            # Calculate distances from this point to all grid points
            distances = np.sqrt((X - x)**2 + (Y - y)**2)
            # Add Gaussian weighted by normalized generation
            Z += gen * np.exp(-(distances**2) / (2 * sigma**2))
    
    # Enhance clusters by applying local density scaling
    density = gaussian_filter(Z > 0, sigma=sigma*2)
    Z = Z * (1 + density)
    
    # Apply final scaling to enhance visibility of lower values
    Z = np.power(Z, 0.4)  # More aggressive power scaling
    
    # Create the heat map
    clear_screen()
    plt.figure(figsize=(10, 8))
    xbuffer = (max(x_coords) - min(x_coords))*0.1
    ybuffer = (max(y_coords) - min(y_coords))*0.1
    
    # Use imshow without interpolation
    plt.imshow(Z, extent=[min(x_coords) - xbuffer, max(x_coords) + xbuffer, 
                         min(y_coords) - ybuffer, max(y_coords) + ybuffer],
               origin='lower', cmap='YlOrRd', aspect='auto')
    
    plt.colorbar(label='Generation (MW)')
    plt.title('Generation Heat Map')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    
    # Add scatter points for actual bus locations
    plt.scatter(x_coords, y_coords, c='black', s=2, alpha=0.5)
    
    plt.show()
    return

def generateLoadHeatMap():
    if not bus_data:
        print("{RED}Error: No bus data loaded{ENDC}")
        return
    
    # Extract coordinates and load values
    x_coords = []
    y_coords = []
    load_values = []
    
    for row in bus_data:
        try:
            x = float(row[2])  # X coordinate (2nd column)
            y = float(row[1])  # Y coordinate (3rd column)
            load = float(row[LOADMW])  # Load value
            
            x_coords.append(x)
            y_coords.append(y)
            load_values.append(load)
        except (ValueError, IndexError):
            continue
    
    if not x_coords or not y_coords or not load_values:
        print("Error: No valid data points found")
        return
        
    # Create grid
    grid_size = 200
    x_grid = np.linspace(min(x_coords), max(x_coords), grid_size)
    y_grid = np.linspace(min(y_coords), max(y_coords), grid_size)
    X, Y = np.meshgrid(x_grid, y_grid)
    Z = np.zeros_like(X)
    
    # Calculate standard deviation for Gaussian based on grid size
    # Use smaller sigma for better cluster detection
    sigma = max_distance = np.sqrt((max(x_coords) - min(x_coords))**2 + (max(y_coords) - min(y_coords))**2) / 30
    
    # Normalize load values to prevent domination by large values
    max_load = max(load_values)
    normalized_loads = [((load/max_load)**0.5) * max_load for load in load_values]
    
    # Add Gaussian contribution from each load point
    for x, y, load in zip(x_coords, y_coords, normalized_loads):
        if load > 0:  # Only consider positive loads
            # Calculate distances from this point to all grid points
            distances = np.sqrt((X - x)**2 + (Y - y)**2)
            # Add Gaussian weighted by normalized load
            Z += load * np.exp(-(distances**2) / (2 * sigma**2))
    
    # Enhance clusters by applying local density scaling
    density = gaussian_filter(Z > 0, sigma=sigma*2)
    Z = Z * (1 + density)
    
    # Apply final scaling to enhance visibility of lower values
    Z = np.power(Z, 0.4)  # More aggressive power scaling
    
    # Create the heat map
    clear_screen()
    plt.figure(figsize=(10, 8))
    xbuffer = (max(x_coords) - min(x_coords))*0.1
    ybuffer = (max(y_coords) - min(y_coords))*0.1
    
    # Use imshow without interpolation
    plt.imshow(Z, extent=[min(x_coords) - xbuffer, max(x_coords) + xbuffer, 
                         min(y_coords) - ybuffer, max(y_coords) + ybuffer],
               origin='lower', cmap='YlOrRd', aspect='auto')
    
    plt.colorbar(label='Load (MW)')
    plt.title('Load Heat Map')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    
    # Add scatter points for actual bus locations
    plt.scatter(x_coords, y_coords, c='black', s=2, alpha=0.5)
    
    plt.show()
    return

def displayLoadedFiles():
    clear_screen()
    print(f"\n{YELLOW}Loaded Files:{ENDC}")
    print(f"{CYAN}Bus File:{ENDC} {GREEN}{bus_file_name}{ENDC}")
    print(f"{CYAN}Number of Bus Rows:{ENDC} {GREEN}{len(bus_data) if bus_data else 'N/A'}{ENDC}")
    print(f"{CYAN}Branch File:{ENDC} {GREEN}{branch_file_name}{ENDC}")
    print(f"{CYAN}Number of Branch Rows:{ENDC} {GREEN}{len(branch_data) if branch_data else 'N/A'}{ENDC}")
    print(f"{CYAN}Generator File:{ENDC} {GREEN}{generator_file_name}{ENDC}")
    print(f"{CYAN}Number of Generator Rows:{ENDC} {GREEN}{len(generator_data) if generator_data else 'N/A'}{ENDC}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def readFile(file):
    global bus_data, branch_data, generator_data, file_type, bus_file_name, branch_file_name, generator_file_name
    
    file_type = file.readline().strip()
    
    if file_type not in ['Bus', 'Branch', 'Gen']:
        raise ValueError(f"{RED}Invalid file type: {file_type}. Expected 'Bus', 'Branch', or 'Gen'{ENDC}")
    
    file.readline()
    
    # Read the data
    data = []
    for line in file:
        values = line.strip().split(',')
        if file_type == 'Bus' and len(values) != 20:
            raise ValueError(f"Bus data should have 20 columns, found {len(values)}")
        elif file_type == 'Branch' and len(values) != 15:
            raise ValueError(f"Branch data should have 15 columns, found {len(values)}")
        elif file_type == 'Gen' and len(values) != 25:
            raise ValueError(f"Generator data should have 25 columns, found {len(values)}")
        
        # Convert values to appropriate types
        row = []
        for value in values:
            try:
                # Try to convert to float first
                row.append(float(value))
            except ValueError:
                # If not a number, keep as string
                row.append(value)
        
        data.append(row)
    
    # Store data in appropriate structure
    if file_type == 'Bus':
        bus_data = data
        bus_file_name = csv_name
    elif file_type == 'Branch':
        branch_data = data
        branch_file_name = csv_name
    elif file_type == 'Gen':
        generator_data = data
        generator_file_name = csv_name

def rankGenerationTypes():
    if not generator_data:
        print(f"{RED}Error: No generator data loaded{ENDC}")
        return
    
    # Dictionary to store generation type statistics
    gen_stats = {}
    
    for row in generator_data:
        try:
            gen_type = row[GENTYPE]
            mw = float(row[GENMW_COL])
            mvar = float(row[GENMVAR_COL])
            mva = (mw**2 + mvar**2)**0.5  # Calculate MVA
            
            if gen_type not in gen_stats:
                gen_stats[gen_type] = {
                    'total_mva': 0.0,
                    'total_mw': 0.0,
                    'total_mvar': 0.0,
                    'count': 0
                }
            
            # Update statistics for this generation type
            gen_stats[gen_type]['total_mva'] += mva
            gen_stats[gen_type]['total_mw'] += mw
            gen_stats[gen_type]['total_mvar'] += mvar
            gen_stats[gen_type]['count'] += 1
            
        except (ValueError, IndexError):
            continue
    
    if not gen_stats:
        print(f"{RED}No valid generation data found{ENDC}")
        return
    
    # Sort generation types by total MVA
    sorted_types = sorted(gen_stats.items(), 
                         key=lambda x: x[1]['total_mva'], 
                         reverse=True)
    
    # Find the maximum length of generation type names
    max_type_length = max(len(gen_type) for gen_type, _ in sorted_types)
    type_width = max(30, max_type_length + 2)  # Minimum width of 30, or longer if needed
    
    # Display results
    clear_screen()
    print(f"\n{YELLOW}Generation Type Rankings by MVA:{ENDC}")
    print(f"{CYAN}{'Type':<{type_width}} {'MVA':>12} {'MW':>12} {'Mvar':>12} {'Count':>8}{ENDC}")
    print("-" * (type_width + 12 + 12 + 12 + 8 + 3))  # +3 for spaces between columns
    
    for gen_type, stats in sorted_types:
        # Truncate long names and add ellipsis if needed
        display_type = gen_type[:type_width-3] + "..." if len(gen_type) > type_width-3 else gen_type
        print(f"{GREEN}{display_type:<{type_width}} {stats['total_mva']:>12.2f} {stats['total_mw']:>12.2f} {stats['total_mvar']:>12.2f} {stats['count']:>8}{ENDC}")
    
    # Add a summary line
    print("-" * (type_width + 12 + 12 + 12 + 8 + 3))
    total_mva = sum(stats['total_mva'] for _, stats in sorted_types)
    total_mw = sum(stats['total_mw'] for _, stats in sorted_types)
    total_mvar = sum(stats['total_mvar'] for _, stats in sorted_types)
    total_count = sum(stats['count'] for _, stats in sorted_types)
    print(f"{YELLOW}{'TOTAL':<{type_width}} {total_mva:>12.2f} {total_mw:>12.2f} {total_mvar:>12.2f} {total_count:>8}{ENDC}")

#MAIN LOOP
while True:
    #Get input from user 
    print(f"{CYAN}{logo}{ENDC}")
    print(f"\n{CYAN}Enter CSV Name (or 'exit' to quit){ENDC}")
    csv_name = input().strip()

    if csv_name.lower() == 'exit':
        print(f"{GREEN}DONE{ENDC}")
        break

    try:
        with open(csv_name, 'r') as file:
            clear_screen()
            print(f"{GREEN}Successfully opened {BLUE}{csv_name}{ENDC}")
            readFile(file)
            displayLoadedFiles()
            
            while True:
                print(f"\n{CYAN}What would you like to do?{ENDC}")
                print(f"\n{YELLOW}BUS OPERATIONS:{ENDC}")
                print("1. Find Max Active Bus Load")
                print("2. Find Max Active Bus Generation")
                print(f"\n{YELLOW}SUBSTATION OPERATIONS:{ENDC}")
                print("3. Find Max Active Substation Load")
                print("4. Find Max Active Substation Generation")
                print(f"\n{YELLOW}BRANCH OPERATIONS:{ENDC}")
                print("5. Find Largest Line Apparent Power")
                print(f"\n{YELLOW}GENERATOR OPERATIONS:{ENDC}")
                print("6. Rank Generation Types by MVA")
                print(f"\n{YELLOW}VISUALIZATION:{ENDC}")
                print("7. Generate Generation Heat Map")
                print("8. Generate Load Heat Map")
                print(f"\n{YELLOW}OTHER:{ENDC}")
                print("9. Select another file")
                print("10. Display loaded files")
                print("11. Exit")
                
                choice = input(f"{CYAN}Enter your choice (1-11):{ENDC} ").strip()
                
                if choice == '1':
                    clear_screen()
                    largestBusLoadAct()
                elif choice == '2':
                    clear_screen()
                    largestBusGenerationAct()
                elif choice == '3':
                    clear_screen()
                    largestSubstationLoad()
                elif choice == '4':
                    clear_screen()
                    largestSubstationGeneration()
                elif choice == '5':
                    clear_screen()
                    largestLineAppPower()
                elif choice == '6':
                    clear_screen()
                    rankGenerationTypes()
                elif choice == '7':
                    clear_screen()
                    generateHeatMap()
                elif choice == '8':
                    clear_screen()
                    generateLoadHeatMap()
                elif choice == '9':
                    clear_screen()
                    break
                elif choice == '10':
                    clear_screen()
                    displayLoadedFiles()
                elif choice == '11':
                    clear_screen()
                    print(f"{GREEN}DONE{ENDC}")
                    exit()
                else:
                    clear_screen()
                    print(f"{RED}Invalid choice. Please try again.{ENDC}")
                    
    except FileNotFoundError:
        clear_screen()
        print(f"{RED}Error: File '{csv_name}' not found. Please try again.{ENDC}")
    except Exception as e:
        clear_screen()
        print(f"{RED}An error occurred: {e}. Please try again.{ENDC}")

    """
    -Time varying analysis
    -Learn about optimal power flow (615, 460)
    -Economic dispatch
    """