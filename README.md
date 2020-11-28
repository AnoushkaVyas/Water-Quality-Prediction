# Water Quality Prediction Tool
![Python](https://img.shields.io/badge/LICENSE-MIT-blue?logo=appveyor&style=for-the-badge)
![Python](https://img.shields.io/badge/built--with-Python-green?logo=appveyor&style=for-the-badge)

## To run the Tool:

Run the following commands:
```python
cd Water-Quality-Prediction
python3 main.py
```

## For Method 1:

1. Input: Latitude, Longitude
2. Output: values for `station_number`, `station_name`, `water_type`, `q_ph`, `q_temp`, `q_turb`, `q_nitrates`, `q_phosphate`, `q_coli`, `WQI`, `WQC` as per the latest reading in GEMS dataset.

### Buttons for Method 1:

1. `Get WQI`: To display station details, water quality parameter values, and to calculate water quality.

## For Method 2:

1. Input: A .csv file with River Name, Station Codes and their latitude and longitude information, and the water quality parameters for all the stations.
2. Output: OIP values and water quality classification value. 

### Buttons for Method 2:

1. `Open`: Add the input .csv file.
2. `Read File`: Reads the .csv file.
3. `Compute OIP`: Displays a table with OIP and WQC and saves this as filename.csv, where filename.csv is input in the Ouput File textbox.
4. `River Stretch`: Plots the river and stations with their OIP and WQC.

## For Method 3:

In this method, we are required to apply Machine Learning Algorithms to the GEMS dataset for Water Quality Estimation.
1. The extract parameters like Turbidity, Nitrates, Phosphates etc from this data for different dates and locations within India.
2. We then compute the WQI values using the weights in Question - 1, these will serve as the target values.
3. We have used GradientBoostingRegressor for training on the dataset.

### Buttons for Method 3:

1. Use the `Open` button to select the `.csv` file containing user input. `test.csv` has been provided as a sample.
2. Use `graph` button to plot the line plot of the predicted WQI values.
3. Use `Show Predictions` button to show the predicted WQI and WQC in a tabular format.
4. Use `Export CSV` to download the result as a .csv file.
5. Use the `CLEAR` button to clear the canvas.

