from random_color_generator import get_shades_of_color

PURCHASED_COLOR = "#67BC77"
PURCHASED_COLOR_DARK = "#3d7047"
PURCHASED_COLOR_LIGHT = "#a3d6ad"

COOKED_COLOR = "#3D5467"
COOKED_COLOR_DARK = "#8a98a3"
COOKED_COLOR_LIGHT = "#24323d"

RAW_WASTE_COLOR = "#db5461"
RAW_WASTE_COLOR_LIGHT = "#83323a"
RAW_WASTE_COLOR_DARK = "#e998a0"

USED_COLOR = "#4E4F4A"

PREDICTION_FACTORS = {"Spoilage Factors": 3, "Outside Weather": 3, "World Events": 4, "Volatility Factor": 3, "T-1 Factor": 2, "Spoilage Factors": 3}
PREDICTION_FACTORS_CHEESE = {"Spoilage Factors": 4, "Outside Weather": 4, "World Events": 3, "Volatility Factor": 4, "T-1 Factor": 3, "Spoilage Factors": 4}
PREDICTION_FACTORS_TOMATO = {"Spoilage Factors": 3, "Outside Weather": 3, "World Events": 4, "Volatility Factor": 3, "T-1 Factor": 4, "Spoilage Factors": 3}
PREDICTION_FACTORS_ONION = {"Spoilage Factors": 2, "Outside Weather": 3, "World Events": 3, "Volatility Factor": 2, "T-1 Factor": 2, "Spoilage Factors": 2}

WASTAGE_FACTORS = {"Storage Temperature": 4, "Storage Pressure": 3, "Storage Humidity": 4, "Outside Weather": 2, "Storage Life": 2, "Storage Temperature": 4}
WASTAGE_FACTORS_CHEESE = {"Storage Temperature": 4, "Storage Pressure": 3, "Storage Humidity": 4, "Outside Weather": 3, "Storage Life": 4, "Storage Temperature": 4}
WASTAGE_FACTORS_TOMATO = {"Storage Temperature": 3, "Storage Pressure": 3, "Storage Humidity": 3, "Outside Weather": 2, "Storage Life": 2, "Storage Temperature": 3}
WASTAGE_FACTORS_ONION = {"Storage Temperature": 2, "Storage Pressure": 2, "Storage Humidity": 3, "Outside Weather": 4, "Storage Life": 1, "Storage Temperature": 2}

FOOD_ITEMS = ["cheese", "tomato", "onion"]

FOOD_COLOR = {FOOD_ITEMS[x]: get_shades_of_color(x) for x in range(len(FOOD_ITEMS))}

TEXT_FONT_SIZE = 15

TITLE_FONT_SIZE = 20
