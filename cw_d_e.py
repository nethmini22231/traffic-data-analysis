#Author: W.R.U.Yasasmie
#Date: 2024.12.24
#Student ID: 20240878 / w2121113
# Reference:
# - W3Schools Pathfinder: https://pathfinder.w3schools.com/



# Task A: Input Validation

# importing necessary modules
import tkinter as tk
from tkinter import Canvas
import csv
import os
from collections import defaultdict


# Function to validate the input date
def validate_date_input():
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """

    while True:
        try:
            # Input and validate the day
            day = int(input("Enter the day as DD: "))
            if not (1 <= day <= 31):
                print(f"Day out of range! You entered {day}. Please enter a value between 1 and 31!")
                continue


            # Input and validate the month
            month = int(input("Enter the month as MM: "))
            if not (1 <= month <= 12):
                print(f"Month out of range! You entered {month}. Please enter a value between 1 and 12!")
                continue


            # Input and validate the year
            year = int(input("Enter the year as YYYY: ")) 
            if not (2000 <= year <= 2024):
                print(f"Year out of range! You entered {year}. Please enter a value between 2000 and 2024!")
                continue
            
        
            # Return the validated date in a string format
            return f"{day:02}{month:02}{year}" 


        except ValueError:
           # Handle invalid input
           print("Integer required, Please enter a valid date as DD MM YYYY using numeric value.")


# Task B: Processed Results

# function to process data from the csv file
def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric hybrids
    - Two-wheeled vehicles, and other requested metrics
    """

    try:
        #open the csv file for reading
        with open(file_path, mode = "r") as csv_file:
            reader = csv.DictReader(csv_file)
           

            # initialize variables to store statistics
            total_vehicles = 0
            total_trucks = 0
            total_electric = 0
            total_two_wheeled = 0
            total_bicycles = 0
            buses_north = 0
            straight_moving = 0
            over_speed_limit = 0
            elm_vehicles = 0
            hanley_vehicles = 0
            elm_scooters = 0
            rain_hours=set()
            hourly_counts = {}
        
            # iterate through each row in the csv file
            for row in reader: 
                total_vehicles += 1
              
                # Count trucks
                if row["VehicleType"] == "Truck":
                    total_trucks += 1

                # Count electric vehicles
                if row["elctricHybrid"] == "TRUE":
                    total_electric += 1


                # Count two-wheeled vehicles
                if row["VehicleType"] in ["Bike", "Motorbike", "Scooter"]:
                    total_two_wheeled += 1


                # Count bicycles seperately
                if row["VehicleType"] == "Bike":
                    total_bicycles += 1


                # Count buses heading north
                if (
                    row["VehicleType"].strip().lower() == "Bus" and
                    row["JunctionName"].strip().lower() == "Elm Avenue/Rabbit Road" and
                    row["travel_Direction_out"].strip().upper() == "N"
                ):
                    buses_north += 1


                # Count vehicles traveling straight
                if row["travel_Direction_in"] == row["travel_Direction_out"]:
                    straight_moving += 1

               
                # Count vehicles over the speed limit
                if int(row["VehicleSpeed"]) > int(row["JunctionSpeedLimit"]):
                    over_speed_limit += 1


                # Count Elm Avenue vehicles and scooters
                if row["JunctionName"] == "Elm Avenue/Rabbit Road":
                    elm_vehicles += 1
                    if row["VehicleType"] == "Scooter":
                        elm_scooters += 1

                # Count Hanley Highway vehicles
                if row["JunctionName"] == "Hanley Highway/Westway":
                    hanley_vehicles += 1


                # Count rain hours
                if row["Weather_Conditions"] == "Rain":
                    rain_hours.add(row["timeOfDay"].split(":")[0])

                # Collect hourly counts
                hour = row['timeOfDay'].strip().split(':')[0]
                if hour not in hourly_counts:
                    hourly_counts[hour] = 0
                hourly_counts[hour] += 1

                    

        #calculate percentage
        elm_scooter_percentage=(elm_scooters / elm_vehicles)*100 if elm_vehicles> 0 else 0

        # Calculate percentages and averages
        percentage_trucks = round((total_trucks / total_vehicles) * 100, 2) if total_vehicles > 0 else 0
        average_bikes_per_hour = round(total_two_wheeled / 24, 2)

        # Identify peak traffic hour(s)
        peak_hour = max(hourly_counts, key=hourly_counts.get, default=None)
        peak_hour_volume = hourly_counts[peak_hour] if peak_hour else 0
        peak_hours = [
            hour for hour in hourly_counts if hourly_counts[hour] == peak_hour_volume
        ]
        
        # Prepare outcomes
        results = {
                "Total Vehicles": total_vehicles,
                "Total Trucks": total_trucks,
                "Total Electric Vehicles": total_electric,
                "Total Two-Wheeled Vehicles": total_two_wheeled,
                "Total Bicycles": total_bicycles,
                "Total Buses (North)": buses_north,
                "Straight Moving Vehicles": straight_moving,
                "Over Speed Limit Vehicles": over_speed_limit,
                "Elm Avenue Vehicles": elm_vehicles,
                "Hanley Highway Vehicles": hanley_vehicles,
                "Elm Scooter Percentage": round(elm_scooter_percentage, 2),
                "Total Rain Hours": len(rain_hours),
                "Peak Hour": peak_hour,
                "Peak Hour Volume": peak_hour_volume,
                "Peak Hour": peak_hours,
                "Average Bikes Per Hour": average_bikes_per_hour,
                "Truck Percentage": round(percentage_trucks, 2),
         }

        return results
        

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except KeyError as e:
        print(f"Error: Missing column in CSV - {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def display_results(results):
    """
    Displays the calculated results in a clear and formatted way.
    """

    if results is None:
        print("No results to display. Please check the input file or processing logic.")
        return

    print("\n******************************************************************************")
    print(f"Data file selected is {file_name}\n\n")
    
    print(f"The total number of vehicles recorded for this date is {results['Total Vehicles']}")
    print(f"The total number of trucks recorded for this date is {results['Total Trucks']}")
    print(f"The total number of electric vehicles for this date is {results['Total Electric Vehicles']}")
    print(f"The total number of two-wheeled vehicles for this date is {results['Total Two-Wheeled Vehicles']}")
    print(f"The total number of bicycles for this date is {results['Total Bicycles']}")
    print(f"The total number of buses leaving Elm Avenue/Rabbit Road heading North is {results['Total Buses (North)']}")
    print(f"The total number of vehicles through both junctions not turning left or right is {results['Straight Moving Vehicles']}")
    print(f"The percentage of total vehicles recorded that are trucks for this date is {results['Truck Percentage']}%")
    print(f"The average number of bikes per hour for this date is {results['Average Bikes Per Hour']}")
    print(f"The total number of vehicles recorded as over the speed limit for this date is {results['Over Speed Limit Vehicles']}")
    print(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {results['Elm Avenue Vehicles']}")
    print(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {results['Hanley Highway Vehicles']}")
    print(f"{results['Elm Scooter Percentage']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.")
    print(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {results['Peak Hour Volume']}")
    print(f"The number of hours of rain for this date is {results['Total Rain Hours']}")


    # To display peak hours correctly
    if results["Peak Hour"]:
        peak_hours_display = [
            f"Between {hour}:00 and {int(hour) + 1}:00" for hour in results["Peak Hour"]
        ]
        peak_hours_display_str = ", ".join(peak_hours_display)
        print(f"The peak hour(s) on Hanley Highway/Westway is/are: {peak_hours_display_str}")
    else:
        print("No peak hour detected.")
        
    print("\n******************************************************************************")


# Task C: Save Results to Text File
def save_results_to_file(results, file_name):
    """
    Saves the processed results to a text file and appends if the program loops.
    """
    try:
        with open("results.txt", "a") as file:
            file.write("\n************************************************************************************\n")
            file.write(f"Data file selected is {file_name}\n\n")
            file.write(f"The total number of vehicles recorded for this date is {results['Total Vehicles']}\n")
            file.write(f"The total number of trucks recorded for this date is {results['Total Trucks']}\n")
            file.write(f"The total number of electric vehicles for this date is {results['Total Electric Vehicles']}\n")
            file.write(f"The total number of total two-wheeled vehicles for this date is {results['Total Two-Wheeled Vehicles']}\n")
            file.write(f"The total number of bicycles for this date is {results['Total Bicycles']}\n")
            file.write(f"The total number of buses leaving Elm Avenue/Rabbit Road heading North is {results['Total Buses (North)']}\n")
            file.write(f"The total number of vehicles through both junctions not turning left or right is {results['Straight Moving Vehicles']}\n")
            file.write(f"The percentage of total vehicles recorded that are trucks for this date is {results['Truck Percentage']}%\n")
            file.write(f"The average number of bikes per hour for this date is {results['Average Bikes Per Hour']}\n")
            file.write(f"The total number of vehicles recorded as over the speed limit for this date is {results['Over Speed Limit Vehicles']}\n")
            file.write(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {results['Elm Avenue Vehicles']}\n")
            file.write(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {results['Hanley Highway Vehicles']}\n")
            file.write(f"{results['Elm Scooter Percentage']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.\n")
            file.write(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {results['Peak Hour Volume']}\n")
            file.write(f"The number of hours of rain for this date is {results['Total Rain Hours']}\n")

            if results["Peak Hour"]:
                file.write("The peak hour(s) on Hanley Highway/Westway is/are:\n")
                for hour in results["Peak Hour"]:
                    file.write(f"  - Between {hour}:00 and {int(hour)+1}:00\n")
            else:
                file.write("No peak hour detected.\n")
                
            file.write("***************************************************************************************\n")
            print("Results saved to results.txt")
            
    except Exception as e:
        print(f"Error saving results: {e}")


# Process and display outcomes if the file exists
if __name__ == "__main__":
    while True:
        # Ask for the day, month, year)
        date = validate_date_input()

        # Create the file name using the extracted components
        file_name = f"traffic_data{date}.csv"
        file_path = os.path.join(r"C:\Users\ASUS\Desktop\CW SD\cw",file_name)
        print(f"Processing file: {file_path}")
        
        # Display results for each processed file
        results = process_csv_data(file_path)
        display_results(results)

        #Save results to a text file
        if results:
           save_results_to_file(results, file_name)

        # Ask if the user wants to process another file
        choice = input("Do you want to load another dataset? (Y/N): ").strip().lower()
        if choice not in ['y', 'yes']:
            print("Exiting program.")
            break
        


class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.window = tk.Tk()
        self.window.title(f"Traffic Histogram for {self.date}")
        self.window.geometry("1400x900")

        # Canvas for drawing the histogram
        self.canvas = tk.Canvas(self.window, width=1400, height=900, bg="white")
        self.canvas.pack()

        # Draw the histogram
        self.draw_histogram()

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        left_margin = 100
        right_margin = 1000
        bar_width = 20
        bar_spacing = 1
        group_spacing = 2 # Additional spacing between groups of two bars
        label_spacing = 10
        max_height = 500
        max_count = max(
            max(counts) for counts in self.traffic_data.values()
        )  # Get max count for scaling

        if max_count == 0:
            self.canvas.create_text(
                500, 350, text="No traffic data available.", font=("Times New Roman", 16), fill="light blue"
            )
            return

        # Add title
        self.canvas.create_text(
            500, 30, text=f"Histogram of Vehicles per Hour ({self.date})", font=("Times New Roman", 16), fill="black"
        )

        # Add legend below the title
        self.add_legend()

        for hour, counts in self.traffic_data.items():
            x_axis_y = left_margin + int(hour) * (bar_width + bar_spacing + group_spacing) * 2
            y1_elm = 650 - (counts[0] / max_count * max_height)
            y1_hanley = 650 - (counts[1] / max_count * max_height)

            # Draw Elm Avenue bar
            self.canvas.create_rectangle(x_axis_y, y1_elm, x_axis_y + bar_width, 650, fill="light blue", outline="black")
            self.canvas.create_text(
                x_axis_y + bar_width // 2, y1_elm - 10, text=str(counts[0]), fill="black"
            )

            # Draw Hanley Highway bar
            self.canvas.create_rectangle(
                x_axis_y + bar_width + bar_spacing, y1_hanley, x_axis_y + 2 * bar_width + bar_spacing, 650, fill="blue", outline="black"
            )
            self.canvas.create_text(
                x_axis_y + 3 * bar_width // 2, y1_hanley - 10, text=str(counts[1]), fill="black"
            )

        # Add x-axis title
        self.canvas.create_text(
            550, 670 + 40, text="Hours 00:00 to 24:00", font=("Times New Roman", 16), fill="black"
        )
        
        # Add x-axis labels
        for hour in range(24):
            x = left_margin + hour * (bar_width + group_spacing + bar_spacing) * 2 + bar_width
            self.canvas.create_text(x, 670, text=str(hour), anchor="n")

        # Add x-axis
        self.canvas.create_line(
            left_margin - 10,
            650,
            left_margin + 25 * (2 * bar_width + group_spacing + bar_spacing)+ 70,
            650,
            fill="black",
        )

        # Add y-axis
        y_axis_x = left_margin - 10
        self.canvas.create_line(
            y_axis_x, 650, y_axis_x, 650 - max_height - 10, fill="black"
        )

        # Add y-axis labels
        interval = max(1, max_count // 10)
        for i in range(0, max_count + 1, interval):
            y = 650 - (i / max_count * max_height)
            self.canvas.create_text(
                y_axis_x - 20, y, text=str(i), font=("Times New Roman", 10), anchor="e"
            )
            self.canvas.create_line(
                y_axis_x - 5, y, y_axis_x, y, fill="black"
            )
            

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        self.canvas.create_rectangle(50, 50, 70, 70, fill="light blue", outline="black")
        self.canvas.create_text(80, 60, text="Elm Avenue/Rabbit Road", anchor="w", font=("Times New Roman", 12))

        self.canvas.create_rectangle(50, 80, 70, 100, fill="blue", outline="black")
        self.canvas.create_text(80, 90, text="Hanley Highway/Westway", anchor="w", font=("Times New Roman", 12))


    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.window.mainloop()


class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.base_directory = r"C:\\Users\\ASUS\\Desktop\\CW SD\\cw\\cw de"
        self.traffic_data = {}

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        self.traffic_data = defaultdict(lambda: [0, 0])
        try:
            with open(file_path, mode="r") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    hour = row["timeOfDay"].split(":")[0]
                    if row["JunctionName"] == "Elm Avenue/Rabbit Road":
                        self.traffic_data[hour][0] += 1
                    elif row["JunctionName"] == "Hanley Highway/Westway":
                        self.traffic_data[hour][1] += 1
            print(f"Successfully loaded data from {file_path}.")

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except KeyError as e:
            print(f"Error: Missing column in CSV - {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.traffic_data = {}
        print("Cleared previous data.")

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        while True:
            # Prompt for input until a valid date is provided
            while True:
               date = input("Enter the date (DDMMYYYY) of the file you want to process: ").strip()

               # check if the input is in the correct format (exactly 8 digits and numeric)
               if len(date) == 8 and date.isdigit():
                   break
               else:
                   print("Invalid format! Please enter the date in DDMMYYYY format.")
                    
            file_name = f"traffic_data{date}.csv"
            file_path = os.path.join(self.base_directory, file_name)

            # Clear previous data and load the file
            self.clear_previous_data()
            self.load_csv_file(file_path)

            # Display histogram if data exists
            if self.traffic_data:
                histogram = HistogramApp(self.traffic_data, date)
                histogram.run()
            else:
                print("Warning: No traffic data found in the file.")

            # Ask if the user wants to process another file
            while True:
               choice = input("Do you want to load another dataset? (Y/N): ").strip().lower()
               if choice in ['y', 'yes']:
                   break # Exit the inner loop and process another dataset
               elif choice in ['n','no']:
                   print("Exiting program.")
                   return # Exit the program
               else:
                   print("Invalid input. Please enter 'Y' to continue or 'N' to quit.")
                
    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        print("Welcome to the Multi CSV Processor.")
        self.handle_user_interaction()


if __name__ == "__main__":
    processor = MultiCSVProcessor()
    processor.process_files()
