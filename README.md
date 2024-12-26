# WhatTheCarb ![Icon](https://github.com/SnowY4you/WhatTheCarb/blob/main/nutionsapp.png?raw=true)

A little app to make life easier

## Overview

WhatTheCarb is a nutrition analysis application designed to help users quickly and easily get detailed nutrition information for their recipes. This app leverages the Edamam API to provide comprehensive nutritional data, making it especially useful for individuals with specific dietary needs, such as those with diabetes.

## Installation

To get started with WhatTheCarb, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SnowY4you/WhatTheCarb.git
   cd WhatTheCarb

 2. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create an API at Edamam:**
   - Visit [Edamam](https://www.edamam.com/) and create an account to get your API credentials.

4. **Create a `.env` file:**
   ```bash
   touch .env
   ```

   Add the following lines to the `.env` file:
   ```plaintext
   EDAMAM_APP_ID="your_app_id"
   EDAMAM_APP_KEY="your_app_key"
   ```

## Usage

To run the application, simply execute the following command:
```bash
python app.py
```

## Features

### Full Recipe Nutrition Analysis

Submit the full text of any recipe or ingredient list. Edamam will extract the full nutrition and ingredient data from the text. No more need to spend hours entering your recipes line by line. The nutrition analysis takes less than a second!

### Text Analysis

Our Natural Language Processing engine allows for the extraction of food named entities from text. We also allow combined entity extraction with food database search. Once a text is submitted and entities are extracted, our database is searched for additional food matches to the extracted entities.

### Structured Data and Nutrition Data Output

Edamam returns detailed information for each ingredient line for the Recipe Analysis and for each text string for the Text Analysis. You can get information for the entire recipe as a whole or broken down automatically for each ingredient.

For each food (flour, eggs, etc.), Edamam returns data for calories, fats, carbohydrates, protein, cholesterol, sodium, etc. for a total of 28 macro and micronutrients.

All food nutrient data is enriched with diet, allergy, and health labeling, as calculated by Edamam based on the food's ingredients. Vegan, Paleo, Gluten-Free, Low-Sodium, and Dairy-Free are some of the 90+ claims generated automatically.

## Why This Project?

I came up with the idea for WhatTheCarb because my 12-year-old son has had type 1 diabetes since he was 4 years old. This app aims to make life easier for people like my son by providing quick and accurate nutritional information for their meals.

## Screenshots

Here are some screenshots of the WhatTheCarb application:

![Description of screenshot 1](https://github.com/SnowY4you/WhatTheCarb/blob/main/WhatTheCarb02.png?raw=true)
*Description of screenshot 1*

![Description of screenshot 2](https://github.com/SnowY4you/WhatTheCarb/blob/main/WhatTheCarb01.png?raw=true)
*Description of screenshot 2*

## Additional Resources

- Info about Tkinter commands: [Tkinter Documentation](https://tcl.tk/man/tcl8.6/TclCmd/contents.htm)
- Info about the Nutrition Analysis API: [Edamam Nutrition Analysis API](https://developer.edamam.com/edamam-docs-nutrition-api)

---

Thank you for using WhatTheCarb! If you have any questions or feedback, please feel free to reach out.
<p align="center">
  <img src="https://github.com/SnowY4you/WhatTheCarb/blob/main/Edamam_Badge_White.svg?raw=true" alt="Edamam Badge" width="150" height="150">
</p>


