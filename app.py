import os
import tkinter as tk
import requests
from PIL import Image, ImageTk
import webbrowser
from dotenv import load_dotenv
import logging
from wasabi import color

# Load environment variables
load_dotenv()

# Setting up logging
logging.basicConfig(filename="app.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def analyze_recipe():
    logging.info("Starting recipe analysis")
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
                display_nutrition_data(response_data)
            else:
                display_error(response_data.get("message", "An error occurred"))
        except Exception as e:
            logging.error(f"Exception occurred: {e}")
            display_error("An error occurred")

def clear_analysis():
    for widget in analysis_frame.winfo_children():
        widget.destroy()

def format_number(value):
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return "N/A"

def display_nutrition_data(data):
    # Main output table
    main_output = {
        "ENERC_KCAL": "Energy (kcal)",
        "CHOCDF": "Carbohydrates (g)",
        "SUGAR": "Sugar carbohydrates (g)",
        "PROCNT": "Protein (g)",
        "FIBTG": "Fiber (g)",
        "FAT": "Fat (g)",
        "FAMS":	"- Monounsaturated Fat (Healthiest)",
        "FAPU":	"- Polyunsaturated Fat (Healthier)",
        "FASAT": "- Saturated Fat (Keep To A Minimum)",
        "FATRN": "- Trans Fat (sometimes) (Unhealthy)"
    }

    main_frame = tk.Frame(analysis_frame, bg="#B9DFFE", bd=2, relief=tk.SOLID, highlightbackground="#035394")
    main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Title
    tk.Label(main_frame, text="Nutritional Analysis", font=("Verdana", 14, "bold"), fg="white", bg="#5C33CC").grid(row=0, column=0, columnspan=3, pady=(10, 5))
    # Header
    tk.Label(main_frame, text="Nutrient", font=("Verdana", 12, "bold"), fg="white", bg="#3A127A", borderwidth=2, relief="solid").grid(row=1, column=0, sticky="ew")
    tk.Label(main_frame, text="Amount", font=("Verdana", 12, "bold"), fg="white", bg="#3A127A", borderwidth=2, relief="solid").grid(row=1, column=1, sticky="ew")
    tk.Label(main_frame, text="% av RDI", font=("Verdana", 12, "bold"), fg="white", bg="#3A127A", borderwidth=2, relief="solid").grid(row=1, column=2, sticky="ew")

    for i, (key, label) in enumerate(main_output.items(), start=2):
        if key == "CHOCDF":
            tk.Label(main_frame, text=label, font=("Verdana", 12, "bold"), bg="#4400CC", borderwidth=2, relief="solid").grid(row=i, column=0, sticky="ew")
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


    # Secondary right output table
    right_frame = tk.Frame(analysis_frame, bg="#B9DFFE", bd=2, relief=tk.SOLID, highlightbackground="#035394")
    right_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

    # Title
    tk.Label(right_frame, text="Nutritional Macros Ratio\n(% of energy from Carbohydrates):\n\nCarbs goal ratio: 45% to 65%\nProtein goal ratio: 10% to 30%\nFat goal ratio: 20% to 30%", font=("Verdana", 14, "bold"), fg="white", bg="#7733FF", justify=tk.LEFT).grid(row=0, column=0, columnspan=3, pady=(10, 5))
    # Header
    tk.Label(right_frame, text="Macronutrient", font=("Verdana", 12, "bold"), fg="white", bg="#3A127A", borderwidth=2, relief="solid").grid(row=1, column=0, sticky="ew")
    tk.Label(right_frame, text="Amount", font=("Verdana", 12, "bold"), fg="white", bg="#3A127A", borderwidth=2, relief="solid").grid(row=1, column=1, sticky="ew")
    tk.Label(right_frame, text="% of daily intake", font=("Verdana", 12, "bold"), fg="white", bg="#3A127A", borderwidth=2, relief="solid").grid(row=1, column=2, sticky="ew")

    secondary_right_output = {
        "Carbs": "CHOCDF",
        "Protein": "PROCNT",
        "Fat": "FAT"
    }

    for i, (label, key) in enumerate(secondary_right_output.items(), start=2):
        tk.Label(right_frame, text=label, font=("Verdana", 12), borderwidth=2, relief="solid").grid(row=i, column=0, sticky="ew")
        quantity = format_number(data.get("totalNutrients", {}).get(key, {}).get("quantity", "N/A"))
        unit = data.get("totalNutrients", {}).get(key, {}).get("unit", "")
        ratio = (float(data.get("totalNutrients", {}).get(key, {}).get("quantity", 0)) /
                 float(data.get("totalNutrients", {}).get("ENERC_KCAL", {}).get("quantity", 1))) * 100
        ratio_color = "green" if (
            (label == "Carbs" and 45 <= ratio <= 65) or
            (label == "Protein" and 10 <= ratio <= 30) or
            (label == "Fat" and 20 <= ratio <= 30)
        ) else "red"
        tk.Label(right_frame, text=f"{quantity} {unit}", font=("Verdana", 12), borderwidth=2, relief="solid").grid(row=i, column=1, sticky="ew")
        tk.Label(right_frame, text=f"{ratio:.2f}%", font=("Verdana", 12), fg=ratio_color, borderwidth=2, relief="solid").grid(row=i, column=2, sticky="ew")

    # Add diet_info
    diet_info = ""
    if data.get("totalNutrients", {}).get("FIBTG", {}).get("quantity", 0) > 5:
        diet_info += "High-Fiber\n"
    if (float(data.get("totalNutrients", {}).get("PROCNT", {}).get("quantity", 0)) /
        float(data.get("totalNutrients", {}).get("ENERC_KCAL", {}).get("quantity", 1))) * 100 > 50:
        diet_info += "High-Protein\n"
    if (float(data.get("totalNutrients", {}).get("CHOCDF", {}).get("quantity", 0)) /
        float(data.get("totalNutrients", {}).get("ENERC_KCAL", {}).get("quantity", 1))) * 100 < 20:
        diet_info += "Low-Carb\n"
    if (float(data.get("totalNutrients", {}).get("FAT", {}).get("quantity", 0)) /
        float(data.get("totalNutrients", {}).get("ENERC_KCAL", {}).get("quantity", 1))) * 100 < 15:
        diet_info += "Low-Fat\n"
    if data.get("totalNutrients", {}).get("NA", {}).get("quantity", 0) < 140:
        diet_info += "Low-Sodium\n"
    if (float(data.get("totalNutrients", {}).get("CHOCDF", {}).get("quantity", 0)) /
        float(data.get("totalNutrients", {}).get("ENERC_KCAL", {}).get("quantity", 1))) * 100 > 65:
        diet_info += "High-Carb\n"

    tk.Label(right_frame, text=diet_info, font=("Verdana", 12, "bold"), fg="#005580", bg="#CCDDFF", borderwidth=2, relief="solid").grid(row=i+1, column=2, sticky="ew")

    # Secondary left output table
    left_frame = tk.Frame(analysis_frame, bg="#B9DFFE", bd=2, relief=tk.SOLID, highlightbackground="#035394")
    left_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # Title
    tk.Label(left_frame, text="Micronutrition's", font=("Verdana", 14, "bold"), fg="white", bg="#C44DFF").grid(row=0, column=0, columnspan=3, pady=(10, 5))
    # Header
    tk.Label(left_frame, text="Nutrient", font=("Verdana", 12, "bold"), fg="white", bg="#3A127A", borderwidth=2, relief="solid").grid(row=1, column=0, sticky="ew")
    tk.Label(left_frame, text="Amount", font=("Verdana", 12, "bold"), fg="white", bg="#3A127A", borderwidth=2, relief="solid").grid(row=1, column=1, sticky="ew")
    tk.Label(left_frame, text="% av RDI", font=("Verdana", 12, "bold"), fg="white", bg="#3A127A", borderwidth=2, relief="solid").grid(row=1, column=2, sticky="ew")

    secondary_left_output = {
        "Vitamin A, RAE": "VITA_RAE",
        "Vitamin B-12": "VITB12",
        "Vitamin B-6": "VITB6A",
        "Vitamin C": "VITC",
        "Vitamin D": "VITD",
        "Vitamin E": "TOCPHA",
        "Vitamin K": "VITK1",
        "Zinc": "ZN",
        "Riboflavin": "RIBF",
        "Sodium": "NA",
        "Folate, DFE": "FOLDFE",
        "Folate, food": "FOLFD",
        "Folic acid": "FOLAC",
        "Iron": "FE",
        "Magnesium": "MG",
        "Niacin": "NIA",
        "Phosphorus": "P",
        "Potassium": "K",
        "Calcium": "CA",
        "Thiamin": "THIA"
    }

    for i, (label, key) in enumerate(secondary_left_output.items(), start=2):
        tk.Label(left_frame, text=label, font=("Verdana", 12), borderwidth=2, relief="solid").grid(row=i, column=0, sticky="ew")
        quantity = format_number(data.get("totalNutrients", {}).get(key, {}).get("quantity", "N/A"))
        unit = data.get("totalNutrients", {}).get(key, {}).get("unit", "")
        daily_value = format_number(data.get("totalDaily", {}).get(key, {}).get("quantity", "N/A"))
        tk.Label(left_frame, text=f"{quantity} {unit}", font=("Verdana", 12), borderwidth=2, relief="solid").grid(row=i, column=1, sticky="ew")
        tk.Label(left_frame, text=f"{daily_value}%", font=("Verdana", 12), borderwidth=2, relief="solid").grid(row=i, column=2, sticky="ew")

def display_error(message):
    tk.Label(analysis_frame, text=f"Error: {message}", font=("Verdana", 12), fg="red").pack(anchor=tk.W)

def show_about():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_message = tk.Label(about_window, text="About This Application\n\nWhatTheCarb - Nutrition Analysis\n\nVersion: 1.0\n\nhttps://github.com/SnowY4you/WhatTheCarb\n\nhttps://www.svanbuggenumanalytics.com/",
                             font=("Verdana", 12), padx=10, pady=10)
    about_message.pack()

root = tk.Tk()
root.title("WhatTheCarb - Nutrition Analysis")
root.geometry("1400x900")
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
    instructions_frame, text="Instructions:\n1. Enter the ingredients.\n2. Click 'Analyze Ingredients'.\n3. View the nutritional analysis.\n\nExample: 14 cocktail pork meatballs or\n2 dl cooked durum wheat pasta",
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
    command=analyze_recipe,
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
