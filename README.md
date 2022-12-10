## Small data engineering task related to open data given by the city of Helsinki related to real estates  

### What the code does

1. Reads the .csv-file containing the data and  drops some unnecessary columns and NaN values  
2. Reads the dataframe to a SQL table using SQLite  
3. Calculates how the fraction of residential buildings in all buildings regarding to floor are has developed over the last three years 2020, 2021 and 2022  
4. Does some ***very*** basic data visualization by scatterplotting build date, floor are and floor count attributes  

### How to run the code  
You can clone this repository and do the following commands in the directory:  
1.	python3 -m venv venv  
2.	source venv/bin/activate 
3.	pip install -r requirements.txt  
4.	python3 ./app.py  

### TODO:
The code has some comments, where it could be improved and refactored. This program might get some updates over time as it was made in a very short time. Still here is a list, where it could be improved:  

- **CHECKING THE SCHEMA:** When the data is transferred from the .csv-file to a Pandas dataframe and again to a SQL table, the schema gets altered. For example, some of the data contains a number presented as a string, which then get transformed in a funny way along the way. For example postal codes are handled as FLOATS in the SQLite, like postal code "00100" is presented as 100.0 in the SQL table. These should be fixed in the long run.  
- **REFACTORING:** There is a lot of room for improvement regarding refactoring code. For example, the visualizing and database handling could be separated to separate modules. Also the queries are a bit of copy-paste, as the year and building codes only changes. Doing a single function for the computing, which then gets the year and building codes as a parameter would be a solid fix in the first place.  
- **DATA VISUALIZATION:** The data visualization is very basic, as mentioned before.  
