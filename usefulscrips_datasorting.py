'''
#Small Updata 2019-3-1
Some general things useful in the beginning of script and in ~terminals.
#get the current directory
import os
os.getcwd()

#change directory
os.chdir

#list files
os.listdir()

#to show grafs in jupyter
% matplotlib inline

#to show grafs in ipython
import matplotlib.pyplot as plt
plt.show()

#Run script in directory in ipython
%run ./my_script.py
#clear terminal on windows ipython
!CLS
#
'''
#####DATASORTING#####
#Gives summary of counts/shape, mean, median and quartiles
df.describe()

#Get the amount of null values and type of data from df
df.info()

#check data types
df.dtypes()

#Get the length of element
len(a)

#Get the length of rows in data frame
len(df.index)

#
pd.options.mode.chained_assignment = None

#Get the shape of df
df_08.shape

#Test NA and creates a boolean that can be used to select the dataframe rows, notice that "values" function is necessary  
d=dsub['ID'].notna()
dfsub=dsub[d.values]
# =============================================================================
# Smart way of using boolean to select rows with more then 500 values. 
# Could probably be made more dense syntax wise
# =============================================================================
ind = df.iloc[:, 6:106].notna().sum()
ind2 = ind>500    
out=ind[ind2].to_frame()    
ID=out.index
HighDf=df[ID.values]

#Easy way to summarize amount of values across multiple columns. Gives good overview
NotNaList=df.notna().sum()  


#example of adding new column. OBS! df.gen = gen would not work.
df['gen'] = gen

#To get the index (rowname) from Series or dataframe. Note that this becomes
#an index object and not a series.
g=a_name.index

#check if two datasets contain matching datatypes in each column
df1.dtypes == df2.dtypes

#check if a number is even or odd, works for array and other maybe?
array  % 2 == 0

#First checks for duplicates and counts them, following removes them
sum(df_08.duplicated())
df_08.drop_duplicates(inplace=True)

#Show columns name, two options
df_18.head(1)
df_18.columns

#Convert True and False to each opposite, Inverse. A is the boolean.
b=[not i for i in a]

#open text file
var=open("textfile.txt", "r").read()
var=open("textfile.txt", "r").readlines()

#Nested loop that saves sample of data to csv, with two altering position in name
FirstNm = ["Cool", "Great", "Wow", "ZOMG"]
LastNm = ["Blue", "Titan", "Rocket", "Golden"]

for x in FirstNm:
    for y in LastNm:
        print("{0} {1}".format(x,y))
        TinyDf=df.sample(100)
        TinyDf.to_csv("{} {}.csv".format(x,y), header = 0, sep = ',') 

#Select data based on position with iloc:
#Note that .iloc returns a Pandas Series when one row is selected, and a
#Pandas DataFrame when multiple rows are selected, or a column is full selected
df1 = df.iloc[:,0:2]
data.iloc[0] #first row
data.iloc[:,-1] # last column of data frame (id)
data.iloc[[0,3,6,24], [0,5,6]] # 1st, 4th, 7th, 25th row + 1st 6th 7th columns.
data.iloc[0:5, 5:8] # first 5 rows and 5th, 6th, 7th columns of data frame (county -> phone1).

'''
Select data based on position with loc has two general purposes
Selecting rows by label/index
Selecting rows with a boolean / conditional lookup
Conditional selections with boolean arrays using data.loc[<selection>]
With boolean indexing or logical selection, you pass an array or Series of
True/False values to the .loc indexer to select the rows where your Series
 has True values.
'''
#pick columns
df["Low.2018"] 

#Save the column as dataframe
df2=df["Low.2018"]] 


data.loc(['Ola', 'Lars'])
data.loc[487]#This will return the index called 487, NOT the 487 row

#Very short for replacing a value in a specific position
df.iat[0,0] = "NewThing"
df.at['rowindex', 'columnindex'] = "NewThing"

#Takes a random subset of the dataframe.
sample_red_cof=coffee_red.sample(200)

'''
#####.loc######
https://www.shanelynn.ie/select-pandas-dataframe-rows-and-columns-using-iloc-loc-and-ix/
Pick out data that match the condition and shows the 3 following col
Note that when selecting columns, if one column only is selected, the .loc
operator returns a Series. For a single column DataFrame, use a one-element
list to keep the DataFrame format, for example.
'''

#Load data from webpage
import pandas as pd
movies = pd.read_csv('http://bit.ly/imdbratings') 

#Produce a series made from the descending column 
movies.title.sort_values(ascending=False)

#Sort the dataframe according to the series title.
movies.sort_values('title', inplace=True)

#Simple syntax to select rows from data
df5=df.loc[id2,:]

data.loc[data['first_name'] == 'Erasmo', ['company_name', 'email','phone']]
data.loc[data['first_name'] == 'Erasmo', 'email'] #returns Series
data.loc[data['first_name'] == 'Erasmo', ['email']]#returns df
# Select rows with name Antonio, # and all columns between 'city' and 'email'
data.loc[data['first_name'] == 'Antonio', 'city':'email']
# Select rows where the email column ends with 'hotmail.com', include all columns
data.loc[data['email'].str.endswith("hotmail.com")]
# Select rows with name equal to some values, in a column
data.loc[data['first_name'].isin(['France', 'Tyisha', 'Eric'])]
# Select rows with first name Antonio AND hotmail email addresses
data.loc[data['email'].str.endswith("gmail.com") & (data['first_name'] == 'Antonio')]
# select rows with id column between 100 and 200, and just return 'postal' and 'web' columns
data.loc[(data['id'] > 100) & (data['id'] <= 200), ['postal', 'web']]
# A lambda function that yields True/False values can also be used.
# Select rows where the company name has 4 words in it.
data.loc[data['company_name'].apply(lambda x: len(x.split(' ')) == 4)]
#Same selection can be achieved outside of the main .loc for clarity:
idx = data['company_name'].apply(lambda x: len(x.split(' ')) == 4)
data.loc[idx, ['email', 'first_name', 'company']]

#Read a folder of csv files, querys them and export them back with according to query result.
for x in ListFil:
    a=pd.read_csv(x,header=0,sep=',')
    x=x[:-4]
    south=a.query('lat < 58.27')
    north=a.query('lat > 58.27')
    north.to_csv('{}''North.csv'.format(x), header=1, sep = ',')
    south.to_csv('{}''South.csv'.format(x), header=1, sep = ',')

#Nested loop that saves sample of data to csv, with two altering position in name
FirstNm = ["Cool", "Great", "Wow", "ZOMG"]
LastNm = ["Blue", "Titan", "Rocket", "Golden"]

for x in FirstNm:
    for y in LastNm:
        print("{0} {1}".format(x,y))
        TinyDf=df.sample(100)
        TinyDf.to_csv("{} {}.csv".format(x,y), header = 0, sep = ',')


###################
#Example of how you can make "masks", in this case survied and died.
survied = df.survied == True #Note that this data cotains 0-1, where 0 is synomous to False
died = df.survied == False
df.col[survied].mean()
df.col[died].mean()
df.col[survied].hist(alpha=0.5, label=survied)
df.col[died].hist(alpha=0.5,lable=died)
plt.legend();

#Set index of the dataframe, to the column last name
data.set_index("last_name", inplace=True)

#Get columns position from columns name
id=Hymo.columns.get_loc('Paverkan')

#sort data according to match
df=df[df['col'] == "something"]

# select samples with alcohol content greater than or equal to the median
high_alcohol = df.query('alcohol > 10.299')

#Get the value from a column by the condition from a second in one line.
coffee_red[coffee_red['drinks_coffee'] == True]['height'].mean()

# get counts/mean for each rating and color. Very similiar tapply
color_counts = wine_df.groupby(['color', 'quality']).count()['pH']
color_counts = wine_df.groupby(['color', 'quality']).mean()['pH']
color_counts = wine_df.groupby(['color', 'quality']).sd()['pH']

# Get unique occurence of one column within a secondary column 
unikKommun = df.groupby('Station')['Kommun'].apply(np.unique)


#Get the count by group but only within unique values
df.groupby(['group']).nunique()
df.groupby(['group']).nunique()['id']

#Another way of writing it:
df.groupby('Pclass').Survied.mean().plot(kind='bar')

# get total counts for each color
color_totals = wine_df.groupby('color').count()['pH']

#Divides the colors within each quality rating by the total amount of that color.
#i.e what is the % distrubution of qualities among red wine.
red_proportions = color_counts['red'] / color_totals['red']
red_proportions

#Summarize frequency within each unique valui of the column 
df.actors.value_counts()

#Counts the amount of combinations across two columns, creates a data set and get the row that match max count
df_count = df.groupby(["Start_Station"])['End_Station'].value_counts().reset_index(name="Count")

#Count combination of stations and creates a dataframe with Count as index
print(max_freq = df_count["Count"].max()) #get the maximum value from count in dataframe
df_count[df_count["Count"] == max_freq] #take out the row that matches the max value

#Useful to round down float values
print("%.2f" % varibale)


#Change name of specific column
df=df.rename(columns = {'two':'new_name'})

#If you want to replace name within a column
df = df.rename(columns=lambda x: x.replace(' ', '_'))

#Select a list of columns based on a list
List = ['Paverkad','MAVF','Alder','Bedomning']
data = Hymo[Hymo.columns.intersection(List)]


#This is similiar to grep, will grep any row that contains set character(s)
df_08[df_08['fuel'].str.contains('/')]

#Drop columns from dataframe
df_08.drop(['Stnd', 'Underhood ID', 'FE Calc Appr', 'Unadj Cmb MPG'], axis=1, inplace=True)
#drop column 1,2 4 ect
cols = [1,2,4,5,12]
df.drop(df.columns[cols],axis=1,inplace=True)

#Drop specific row
df=df.drop(df.index[6207])

#Confirm to datasets have identical column names and where they match/mismatch
df_08.columns == df_18.columns

#Save Dataset, index False means that index value wont be included as a first row. 
df_08.to_csv('data_08.csv', index=False)
#
df.to_csv("HymoDataSummary.csv", sep = ',', header=1, index = False)

#check unique within one column
df_18['cert_region'].unique()

#drop NA values from dataframe
df_18.dropna(inplace=True)

#Extract from strings
#Extract number of string
df_08.cyl.str.extract('(\d+)')

#Check if list contains pattern
for dur in movDf['Media Duration']:
    if '.' not in dur:
        print("aii!")

#Simple List manipulation

#makes a list with 4 positions very quickly
a=list("abcd")

#Gets the list index position of a specific value in the list 
GoodList = ["abc", "the", "position", "can", "be", "tricky", "to", "know", "be"]
print(GoodList.index("can"))

#If you want to insert a element in a certain position in the list
#This one inserts jolly at second position
GoodList.insert(2, "jolly")

#if you want to count frequency of a position 
print(GoodList.count("be"))

#sorts the list
GoodList.sort()

#Removes a position from the list, the last one here. 
GoodList.remove(GoodList[-1])

#How write and call position in 2D list 
Good2DList = [["abc", "the"], ["position", "can"], ["be", "tricky"], ["to", "know"], ["be"]]
Good2DList[0][1]

#Read a folder of csv files, querys them and export them back with according to query result.
for x in ListFil:
    a=pd.read_csv(x,header=0,sep=',')
    x=x[:-4]
    south=a.query('lat < 58.27')
    north=a.query('lat > 58.27')
    north.to_csv('{}''North.csv'.format(x), header=1, sep = ',')
    south.to_csv('{}''South.csv'.format(x), header=1, sep = ',')



####Convert data####
#convert list to array
sample_arr=np.asarray(new_list)

#convert column into categorical class and then from category to numeric
df3['landing_page']=pd.Categorical(df3['landing_page'])
df3['landing_page_num'] = df3.landing_page.cat.codes

#Creates a list between a range of values
list(range(1, 312))

#Creates a list the length of df rows
c=list(range(0, len(AB.index)))

#Check the position
aList = [123, 'xyz', 'zara', 'abc']
aList.index( 'xyz' )

#This converts all categorical columns to numeric
cat_columns = df.select_dtypes(['category']).columns
#cat_columns
#Index([u'col2', u'col3'], dtype='object')
df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)

#How to combine factor/category column to text and then merge them.
mapDf['Stkoor_E']=mapDf['Stkoor_E'].astype('str')
mapDf['Stkoor_N']=mapDf['Stkoor_N'].astype('str')
mapDf['Koor']=mapDf['Stkoor_E']+" "+mapDf['Stkoor_N']


#Converts string numbers to float/int
pd.to_numeric
#Convert series or list from int to float e.gself.
df_18.cyl.astype('int')

#.join function example. join list to str
a=seperator.join(katg)
seperator = ', '


#Converts a series to string to allow for replace functinon. "b" is the series.
g=b.to_string()
g.replace('e', 'abc')

#replace values in the entire df, similiar to gsub 
t=dfsub.replace("<", "", regex=True) 

#Does the same as above for the entire dataframe if the data is not split in columns 
for x in range(0,len(df.index)):
    a = df.iloc[x]
    c=a.to_string()
    df.iloc[x]=c.replace('e', 'abc')


#Store dataframe under new variable
df2=pd.DataFrame(df)

#A
pd.to_numeric(s, errors='coerce')

#check if a element is a digit
char.isdigit()

#Way to split each element in a series of columns if they have a specific pattern, kinda
# columns to split by "/"
split_columns = ['fuel', 'air_pollution_score', 'city_mpg', 'hwy_mpg', 'cmb_mpg', 'greenhouse_gas_score']

# apply split function to each column of each dataframe copy, and ~store first and second occurence that match pattern
for c in split_columns:
    df1[c] = df1[c].apply(lambda x: x.split("/")[0])
    df2[c] = df2[c].apply(lambda x: x.split("/")[1])

# combine dataframes to add to the original dataframe.
# Interesting that append can be used in this way too.
new_rows = df1.append(df2)

# =============================================================================
# Quick loop to select col that contains more than x rows with values
# =============================================================================
for x in df.iloc[:, 3:102].notna().sum():
    count +=1
    if x > 450:
        coList.append(df.columns[count])
newdf = df[coList]

####ALL THINGS TIME/DATE RELATED####
#Convert column to time, you might need to add %Y-%m etc format. 
#Very convient solution most of the time though!
mapDf['Tid'] =  pd.to_datetime(mapDf['Tid']) 

from datetime import datetime

#To convert the following format using strptime: 2016-09-24 17:42:27.839496
dt = datetime.strptime(df.timestamp[0], '%Y-%m-%d %H:%M:%S.%f')

#to convert 20180912, note that %y is used for %
dt=datetime.strptime(df.timestamp[0]), '%Y%m%d)

#to add convert from df:
for i in df.timestamp:
    time_list.append(datetime.strptime(i, '%Y-%m-%d %H:%M:%S.%f'))

#Get curent time in unix time 
tid=time.time()
#Converts unix time to date in different ways 
dateconv=np.vectorize(dt.datetime.fromtimestamp) 
tid2= dateconv(tid) 
tid3=dt.datetime.fromtimestamp(tid)
# =============================================================================
# Get specific month/day anything from date column (strptime works with str and strf with date obj(?))
# =============================================================================
monthList = []
for x in movDf['Media Create Date']:
    a=datetime.strptime(x, "%Y:%m:%d %H:%M:%S")
    monthList.append(int(datetime.strftime(a, "%m")))

#Get current time in dates
datetime.datetime.now()

df['new_col'] = time_list


#If two datetime objects are subracted, python returns a timedelta value.
#e.g. datetime.timedelta(14, 19387, 13517)
#where first value is days, second seconds and third millisecond.



#Really interesting line, uses the index of subset dataset as an indicator
#for which part of the data frame that should be removed.
df_18.drop(hb_18.index, inplace=True)

#merge in pandas
#simple example
df3=df2.merge(df_cnty, how="inner", on='user_id')

pd.merge(left, right, how='inner', on=None, left_on=None, right_on=None,
         left_index=False, right_index=False, sort=True,
         suffixes=('_x', '_y'), copy=True, indicator=False,
         validate=None)

#get the count of rows within unique combinations and select row with max
    comb_count=df.groupby(['Start_Station','End_Station']).size().reset_index().rename(columns={0:'Count'})
    max_comb=comb_count.loc[comb_count['Count'].idxmax()]

#Create column with random ID kinda.
data['id'] = [random.randint(0,1000) for x in range(data.shape[0])]

#Useful to get an overview of what the null.values are (is there something that
#that connects them, e.g. beloning to same factor). Will show hist of all split_columns
#with rows which have age = null.
df[df.col.isnull()].hist(figsize=(10,8));

#One way of filling in null. This will take the mean from the given column and
#use that value to fill in the nulls of that col
df.fillna(df.mean(),inplace=True)

df2.budget[df2.cast.str.contains("Emma Watson")].mean()

#Store the console output to a txtfile 
import sys
sys.stdout = open('file.txt', 'w')

#finds the loading directories for module
sys.path 
#Find path to module, here pandas 
pd.__file__

#in numpy and prbly other axis 0 is vertical, and axis 1 is horizontal

#Great for finding no numeric values in column     
print(pd.to_numeric(df['Subscribers'], errors='coerce').isnull())

#Dictionaries, basic syntax
thisdict =	{
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
print(thisdict)

x = thisdict["model"]

# Adding a new key value pair to addictonary. Can be good to combine with zip function
wordFreqDic.update( {'before' : 23} )


#A way to remove duplicates within a list. This script use the fact that dict only allows dict.
#Then list is converted back from dict to list!
mylist = ["a", "b", "a", "c", "c"]
mylist = list(dict.fromkeys(mylist))
print(mylist)


#Merge multiple csv into single file 
import os
import pandas as pd
os.chdir("D:\GRoot\HymoUpdate\Merge")


fout=open("HymoCleanData.csv","a")
# first file:
for line in open("Hymo1.csv"):
    fout.write(line)
# now the rest:
for num in range(2,3):
    f = open("Hymo"+str(num)+".csv")
    f.__next__() # skip the header
    for line in f:
         fout.write(line)
    f.close() # not really needed
fout.close()

#Changes the display option for pd output. Change column amount displayed
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 15)
pd.set_option('display.width', 1000)

#Ultra important line for slicing data!!! No loc, alternative to loc!
df[(df['NOC'] == "SWE") & (df['Sport'] == 'Football')]

# =============================================================================
# Away to rearrange/change columns order in df 
# =============================================================================
chk=movDf.columns.tolist()
NewCol=['Media Create Date',
 'Media Duration',
 'MovieLink',
 'GPS Latitude',
 'GPS Longitude',
 'GPS Altitude',
 'Season',
 'Camera Angle',
 'NumAngle',
 'Drone',
 'Flight Pitch Degree',
 'Flight Roll Degree',
 'Flight Yaw Degree',
 'Gimbal Pitch Degree',
 'Gimbal Roll Degree',
 'Gimbal Yaw Degree']
movDf = movDf[newCol]

# =============================================================================
# #List Comp ex
# =============================================================================
squares = []

for x in range(0,101):
    squares.append(x**2)
print(squares)

squares2=[x**2 for x in range(0,101)]
print(squares2)

#List comprehnesion start with variable that per defintion becomes a list that is appended.
#this is followed by the expression that is performed on the iterable of the for loop.

movies = [("Star wars", 1974), ("Gandhi", 1988), ("Close Encounters", 1999),("Gone with the wind",1990), ("Gattaca",1997),("2001 A space odessy",1968),
          ("Raiders of the lost arc",1971),("Groundhog day", 1986),("Rear Window", 1977),("Ghostbusters", 1987),("To kill a mockingbird", 1958)]

type(movies[0])

#Funny thing that order is almost opposite of "logic", x append and possibly do something with x, x iterate, x condition. 
#This would in for loop be iterate x, check condition and append.
movies2 = [x for x in movies if x.startswith("G")]
#append title (or rather the first element prior to "," in list position). It iterates over both position both only evaluate the first to check secibd
movies3 = [title for (title, year) in movies if year > 1995]

#Example of list comprenhension that uses two if statements as condition for apply
a = [x for x in df.Age if x >= 30 and x <= 35]

#A script for adding values from two lists (That should have been easy to figure out x)))
a = []
count = 0
for x in range(len(V)):
    a.append((v[x]+V[x]))

#List comprehension to get list of 2 dimension according to amount of unique values     
TheList = [[] for i in range(len(df.NOC.unique()))]


#map, and 
#A list of tuples. 
temp = [("Berlin", 29), ("Cairo",36), ("Buenos Aires", 19), ("Los Angeles", 26),
    ("Tokyo",28), ("New York",28), ("London", 22), ("Beijing", 32)]

type(temp)

# =============================================================================
# #usage of map and lambda to convert temp to farenheit
# =============================================================================
#c_to_f store the labmda function so it is callable

c_to_f =lambda data: (data[0], (9/5)*data[1] +32)

#
((9/5)*temp[0][1]+32) #

#Example of how to iterate over list of tuples. 
for x in temp:
    print(x[0])
    print(x[1])

#Kinda neat 
a=list(map(c_to_f, temp))

# =============================================================================
# Useful for mapping new values on categories, by maping a dict on a column
# =============================================================================
season = {1:"Winter", 2:"Winter", 3:"Spring",4:"Spring",5:"Spring",6:"Summer",7:"Summer",8:"Summer", 9:"Autumn", 10:"Autumn", 11:"Autumn", 12:"Winter"}
movDf['Month']  = movDf['Month'].map(season) 

# =============================================================================
# #Filter,  removes data that does not comply with condition 
# =============================================================================
import statistics 
data = [1.3, 2.7, 0.8, 4.1, 4.3,-0.1]
avg = statistics.mean(data)
#Returns values greater then avg
list(filter(lambda x: x > avg, data))

countries = ["","Aregentina", "","Brazil", "Chile", "","Colombia","","Ecuador", "Venzuela"]

a = 1

#Returns everything that is true according to statement
#I think that None is just "filling" the necessary argument spot for the filter.
#The default bool of python, "" will return false while anyother value returns true 
#Also would remove 0.0 & 0 since those also is regarded as false 
list(filter(None, countries))  


# =============================================================================
# #WEBSCRAPING
# =============================================================================



#Very short pandas syntax to read table section of html and return as a list
import pandas as pd

dfs = pd.read_html('https://pythonprogramming.net/parsememcparseface/',header=0)
for df in dfs:
    print(df)
dfs[0]



# =============================================================================
# A fairly compact efficient way to build up a new aggregation data frame,  
# containing multiple numeric and factor columns. 
# =============================================================================
factDf = pd.DataFrame()
factHold = df.iloc[:,0:4]

for x in factHold['Koordinat'].unique():
    store=factHold[(factHold['Koordinat'] == x)]
    store=store.iloc[0].to_frame()
    factDf=pd.concat([factDf, store], axis=1)
    
factDf=factDf.transpose()

ind = df.iloc[:, 6:106].notna().sum()
ind2 = ind>500    
out=ind[ind2].to_frame()    
ID=out.index
HighDf=df[ID.values]

HighDf.set_index(df['Koordinat'], inplace=True)  
testDf = pd.DataFrame()

for x in HighDf.columns:
    testDf[x]=HighDf.groupby(HighDf.index).mean()[x]

HighDf.insert(0, "Koordinat", value=HighDf.index)
mrgDf=factDf.merge(testDf,on='Koordinat', how='inner')    

# =============================================================================
# How to create a loop with two simultanious variables
# =============================================================================
degList=list(picDf["Gimbal Yaw Degree"])
lonList=list(range(0, picDf['Gimbal Yaw Degree'].shape[0]))

for x,y in zip(degList,lonList):
    if x < 0:
        picDf['Gimbal Yaw Degree'][y] = abs(x)*2
        
        
        
# =============================================================================
# How to change display output in pandas. Such as Maxrow or column_width        
# =============================================================================
#https://pandas.pydata.org/pandas-docs/stable/user_guide/options.html
#https://www.youtube.com/watch?v=yiO43TQ4xvc
        
pd.get_option('display.max_rows') #60
pd.set_option('display.max_rows', 200)

pd.get_option('display.max_colwidth') #50, I.e. printed string length 
pd.set_option('display.max_colwidth', 200)
