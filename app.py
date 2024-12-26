import os
import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Setting up logging
logging.basicConfig(format='%(asctime)s, %(levelname)s - %(funcName)s - [%(filename)s:%(lineno)d] - %(message)s\n',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename="app.log",
                    encoding='utf-8',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.debug("This is a debug log")
logger.info("This is an info log")
logger.critical("This is critical")
logger.error("An error occurred")


def show_about():
    messagebox.showinfo("About", "WhatTheCarb - Nutrition Analysis\nVersion 1.0\nDeveloped by Sandra van Buggenum")


def analyze_nutrition():
    logging.info("Starting nutrition analysis")
    recipe_text = entry_recipe_text.get("1.0", tk.END).strip()
    logging.debug(f"Recipe text: {recipe_text}")
    if recipe_text:
        api_url = "https://api.edamam.com/api/nutrition-details?app_id=0ab8471c&app_key=37d2f7287916fe6b91cef7a82b830b1a&beta=true&force=true&kitchen=home"
        app_id = os.getenv("EDAMAM_APP_ID")
        app_key = os.getenv("EDAMAM_APP_KEY")
        logging.debug(f"App ID: {app_id}, App Key: {app_key}")

        headers = {
            "Content-Type": "application/json",
            "x-app-id": app_id,
            "x-app-key": app_key
        }

        data = {
            "title": "Recipe",
            "ingr": recipe_text.split("\n")
        }

        try:
            response = requests.post(api_url, headers=headers, json=data)
            response_data = response.json()
            logging.debug(f"Response status code: {response.status_code}")
            logging.debug(f"Response data: {response_data}")
            clear_analysis()

            if response.status_code == 200:
                display_nutrition_data(response_data, recipe_text)
            else:
                display_error(response_data.get("message", "An error occurred"))
        except Exception as e:
            logging.error(f"Exception occurred: {e}")
            display_error("An error occurred")


def display_error(message):
    messagebox.showerror("Error", message)


def clear_analysis():
    for widget in analysis_frame.winfo_children():
        widget.destroy()


def format_number(value):
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return "N/A"


def display_nutrition_data(data, ingredient):
    totalNutrients = data.get('totalNutrients', {})
    healthLabels = data.get('healthLabels', [])

    main_output = {
        "ENERC_KCAL": "Energy",
        "FAT": "Total Fat",
        "FASAT": "Saturated Fat",
        "CHOCDF": "Total Carbohydrates",
        "FIBTG": "Dietary Fiber",
        "SUGAR": "Sugars",
        "PROCNT": "Protein",
        "NA": "Sodium",
        "CA": "Calcium",
        "MG": "Magnesium",
        "K": "Potassium",
        "FE": "Iron",
        "ZN": "Zinc",
        "P": "Phosphorus",
        "VITA_RAE": "Vitamin A",
        "VITC": "Vitamin C",
        "THIA": "Thiamin (B1)",
        "RIBF": "Riboflavin (B2)",
        "NIA": "Niacin (B3)",
        "VITB6A": "Vitamin B6",
        "FOLDFE": "Folate (Equivalent)",
        "VITB12": "Vitamin B12",
        "VITD": "Vitamin D",
        "TOCPHA": "Vitamin E",
        "VITK1": "Vitamin K"
    }

    # Main frame for total nutrients
    main_frame = tk.Frame(analysis_frame, bg="#B9DFFE", bd=2, relief=tk.SOLID, highlightbackground="#035394")
    main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Title Main Frame
    tk.Label(main_frame, text="Nutritional Analysis", font=("Verdana", 14, "bold"), fg="white", bg="#5C33CC").grid(
        row=0, column=0, columnspan=4, pady=(10, 5))

    # Headers Main Frame
    tk.Label(main_frame, text="Label", font=("Verdana", 12, "bold"), fg="white", bg="#3A127A", borderwidth=2,
             relief="solid").grid(row=1, column=0, sticky="ew")
    tk.Label(main_frame, text="Quantity", font=("Verdana", 12, "bold"), fg="white", bg="#3A127A", borderwidth=2,
             relief="solid").grid(row=1, column=1, sticky="ew")
    tk.Label(main_frame, text="Unit", font=("Verdana", 12, "bold"), fg="white", bg="#3A127A", borderwidth=2,
             relief="solid").grid(row=1, column=2, sticky="ew")

    for i, (key, label) in enumerate(main_output.items(), start=2):
        if key == "CHOCDF":
            tk.Label(main_frame, text=label, font=("Verdana", 12, "bold"), fg="white", bg="#4400CC", borderwidth=2, relief="solid").grid(row=i, column=0, sticky="ew")
            quantity = format_number(data.get("totalNutrients", {}).get(key, {}).get("quantity", "N/A"))
            unit = data.get("totalNutrients", {}).get(key, {}).get("unit", "")
            daily_value = format_number(data.get("totalDaily", {}).get(key, {}).get("quantity", "N/A"))
            tk.Label(main_frame, text=f"{quantity} {unit}", font=("Verdana", 12, "bold"), bg="#D3D3D3", borderwidth=2, relief="solid").grid(row=i, column=1, sticky="ew")
            tk.Label(main_frame, text=f"{daily_value}%", font=("Verdana", 12, "bold"), bg="#D3D3D3", borderwidth=2, relief="solid").grid(row=i, column=2, sticky="ew")
        else:
            tk.Label(main_frame, text=label, font=("Verdana", 12), borderwidth=2, relief="solid").grid(row=i, column=0, sticky="ew")
            quantity = format_number(data.get("totalNutrients", {}).get(key, {}).get("quantity", "N/A"))
            unit = data.get("totalNutrients", {}).get(key, {}).get("unit", "")
            daily_value = format_number(data.get("totalDaily", {}).get(key, {}).get("quantity", "N/A"))
            tk.Label(main_frame, text=f"{quantity} {unit}", font=("Verdana", 12), borderwidth=2, relief="solid").grid(row=i, column=1, sticky="ew")
            tk.Label(main_frame, text=f"{daily_value}%", font=("Verdana", 12), borderwidth=2, relief="solid").grid(row=i, column=2, sticky="ew")

    # Right upper output table for macronutrient ratios
    right_upper_frame = tk.Frame(analysis_frame, bg="#B9DFFE", bd=2, relief=tk.SOLID, highlightbackground="#035394")
    right_upper_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # Title right upper frame
    tk.Label(right_upper_frame,
             text="Macronutrient Ratios\n(% of energy from Macronutrients):",
             font=("Verdana", 14, "bold"), fg="white", bg="#B088DE", justify=tk.LEFT).grid(row=0, column=0,
                                                                                           columnspan=3, pady=(10, 5))

    # Headers right upper frame
    tk.Label(right_upper_frame, text="Macronutrient", font=("Verdana", 12, "bold"), fg="white", bg="#3A127A",
             borderwidth=2, relief="solid").grid(row=1, column=0, sticky="ew")
    tk.Label(right_upper_frame, text="Amount", font=("Verdana", 12, "bold"), fg="white", bg="#3A127A", borderwidth=2,
             relief="solid").grid(row=1, column=1, sticky="ew")
    tk.Label(right_upper_frame, text="% of daily intake", font=("Verdana", 12, "bold"), fg="white", bg="#3A127A",
             borderwidth=2, relief="solid").grid(row=1, column=2, sticky="ew")

    # Calculate macronutrient ratios
    CHOCDF = totalNutrients.get('CHOCDF', {}).get('quantity', 0)
    PROCNT = totalNutrients.get('PROCNT', {}).get('quantity', 0)
    FAT = totalNutrients.get('FAT', {}).get('quantity', 0)

    carb_macro = CHOCDF * 4
    prot_macro = PROCNT * 4
    fat_macro = FAT * 9
    tot_cal = carb_macro + prot_macro + fat_macro

    if tot_cal != 0:
        carb_ratio = carb_macro / tot_cal
        prot_ratio = prot_macro / tot_cal
        fat_ratio = fat_macro / tot_cal
    else:
        carb_ratio = prot_ratio = fat_ratio = 0

    right_upper_frame_output = {
        "Carbs": {"quantity": carb_macro, "ratio": carb_ratio * 100},
        "Protein": {"quantity": prot_macro, "ratio": prot_ratio * 100},
        "Fat": {"quantity": fat_macro, "ratio": fat_ratio * 100}
    }

    for i, (label, details) in enumerate(right_upper_frame_output.items(), start=2):
        ratio_color = "green" if (
                (label == "Carbs" and 45 <= details["ratio"] <= 60) or
                (label == "Protein" and 10 <= details["ratio"] <= 20) or
                (label == "Fat" and 25 <= details["ratio"] <= 45)
        ) else "red"
        tk.Label(right_upper_frame, text=label, font=("Verdana", 12), borderwidth=2, relief="solid").grid(row=i,
                                                                                                          column=0,
                                                                                                          sticky="ew")
        tk.Label(right_upper_frame, text=f"{details['quantity']:.2f} g", font=("Verdana", 12), borderwidth=2,
                 relief="solid").grid(row=i, column=1, sticky="ew")
        tk.Label(right_upper_frame, text=f"{details['ratio']:.2f}%", font=("Verdana", 12), fg=ratio_color,
                 borderwidth=2, relief="solid").grid(row=i, column=2, sticky="ew")

    # Information box below the right upper frame output
    information_box = tk.Frame(right_upper_frame, bg="#B088DE", bd=2, relief=tk.SOLID, highlightbackground="#035394")
    information_box.grid(row=i + 1, column=0, columnspan=3, sticky="nsew", padx=10, pady=(10, 0))

    tk.Label(information_box,
             text="Carbs goal ratio: 45% to 65%\nProtein goal ratio: 10% to 30%\nFat goal ratio: 20% to 30%\n\nThese recommendations\nare based on the Swedish NNR\n(Nordic Nutrition Recommendations)\nfor a pretween with type 1 Diabetes",
             font=("Verdana", 14, "bold"), fg="white", bg="#8A88DE", justify=tk.LEFT).grid(row=0, column=0, pady=(10, 5))



    # Health label frame for additional information
    health_label_frame = tk.Frame(analysis_frame, bg="#B9DFFE", bd=2, relief=tk.SOLID, highlightbackground="#035394")
    health_label_frame.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=10, pady=(0, 10))

    # Title health label frame
    tk.Label(health_label_frame, text="Health labels",
             font=("Verdana", 14, "bold"), fg="white", bg="#C44DFF").grid(row=0, column=0, columnspan=3, pady=(10, 5))

    # Headers health label frame
    tk.Label(health_label_frame, text="Labels", font=("Verdana", 12, "bold"), fg="white", bg="#3A127A",
             borderwidth=2, relief="solid").grid(row=1, column=0, sticky="ew")

    # Display health labels
    for i, label in enumerate(healthLabels, start=2):
        tk.Label(health_label_frame, text=label, font=("Verdana", 12), borderwidth=2, relief="solid").grid(row=i, column=0, sticky="ew", padx=(5, 5), pady=(2, 2))

# Set up the main application window
root = tk.Tk()
root.title("WhatTheCarb - Nutrition Analysis")
root.geometry("1200x900")
root.configure(bg="#B9DFFE")

# Creating a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Adding 'About' option to the menu bar
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=show_about)

frame = tk.Frame(root, bg="#079CAA")
frame.pack(fill=tk.BOTH, expand=tk.YES, padx=20, pady=20)

label_recipe_text = tk.Label(
    frame, text="Enter Ingredients below", font=("Verdana", 16, "bold"), bg="#079CAA", fg="#FFFFFF"
)
label_recipe_text.pack(anchor=tk.CENTER)

instructions_frame = tk.Frame(frame, bg="#079CAA")
instructions_frame.pack(anchor=tk.CENTER)

instructions_text = tk.Label(
    instructions_frame,
    text="Instructions:\n1. Enter the ingredients.\n2. Click 'Analyze Ingredients'.\n3. View the nutritional analysis.\n\nExample: 14 cocktail pork meatballs or\n2 dl cooked durum wheat pasta",
    font=("Verdana", 12), bg="#079CAA", fg="#FFFFFF", justify=tk.LEFT
)
instructions_text.pack(side=tk.LEFT, padx=10, anchor=tk.W)

image_path = "C:/Users/svanb/OneDrive/Python/Automation/WhatTheCarb/nutionsapp.png"
image = Image.open(image_path)
image = image.resize((100, 100), Image.LANCZOS)
photo_image = ImageTk.PhotoImage(image)
image_label = tk.Label(instructions_frame, image=photo_image, bg="#079CAA")
image_label.image = photo_image
image_label.pack(side=tk.RIGHT, padx=20)

input_frame = tk.Frame(frame, bg="#079CAA", bd=2, relief=tk.SOLID, highlightbackground="#08EAF3")
input_frame.pack(anchor=tk.CENTER, pady=2)

entry_recipe_text = tk.Text(input_frame, font=("Verdana", 12), height=4)
entry_recipe_text.pack(side=tk.LEFT, pady=5, ipadx=10, ipady=10)

analyze_button = tk.Button(
    frame,
    text="Analyze Ingredients",
    font=("Verdana", 12, "bold"),
    command=analyze_nutrition,
    bg="#079CAA",
    fg="white",
    activebackground="#CE0CCB",
    activeforeground="#EBE3FA",
    bd=5,
    relief=tk.RAISED
)
analyze_button.pack(pady=10)

# Create a canvas with a scrollbar
canvas = tk.Canvas(frame, bg="#B9DFFE")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview, takefocus=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)

canvas_frame = tk.Frame(canvas, bg="#C5F8FA")
canvas.create_window((0, 0), window=canvas_frame, anchor=tk.NW)
canvas_frame.bind(
    "<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
)

analysis_frame = tk.Frame(canvas, bg="#B9DFFE", bd=2, relief=tk.SOLID, highlightbackground="#035394")
canvas.create_window((0, 0), window=analysis_frame, anchor=tk.NW)
analysis_frame.bind(
    "<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
)

root.mainloop()
