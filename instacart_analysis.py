# Import the libraries you'll need for this analysis
import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
# Note: These files use semicolon (;) as the separator instead of comma
orders         = pd.read_csv('/datasets/instacart_orders.csv', sep=';')
products       = pd.read_csv('/datasets/products.csv', sep=';')
departments    = pd.read_csv('/datasets/departments.csv', sep=';')
aisles         = pd.read_csv('/datasets/aisles.csv', sep=';')
order_products = pd.read_csv('/datasets/order_products.csv', sep=';')

# In this cell, type "orders" below this line and execute the cell
orders #calling the "orders" variable allows for quick inspection of the DataFrame. Displayed below is the first 5, and last 5 rows confirming data has been loaded correctly. We also get total number of rows and columns, and column header info.  

# In this cell, type "products" below this line and execute the cell
products #this shows us the catalog of items. Each product has a id name, aisle id and department id. However, there is a clear misalignment issue. The dataset columns have shifted left,leaving the department id column with no header and the indexes with a header,'product_id'.

departments #rowsxcolumns are not shown here because the dataset isn't large enough. There are only 2 columns, department name and department id. The formatting looks to be correct. 

aisles #only two column table with 134 rows. lists aisle id and aisle name. 

order_products #No clear formatting issue. Most extensive dataset.

# In this cell, type "orders.info() below this line and execute the cell
orders.info() #The column 'days_since_prior' has 28,819 missing values. There is also a discrepency with toal number of entires, indicating there may be duplicates. Lastly, all data except days_since_prior are whole numbers,this is because it contains missing values. 

# In this cell, run orders_products.info() below, but include the argument show_counts=True since this is a large file.
order_products.info(show_counts=True) #here we used show_counts=True to explicitly tell Pandas to count the null values. Missing values have been identified in the 'add_to_cart_order' column. Again, this is why the dtype is a float64.

products.info() #Missing values identified in the 'product_name' column, it is a object beacuse the data in 'product_name' are words.

departments.info() #Dataset has no missing values. 

aisles.info() #Dataset has no missing values.

# Display rows where the product_name column has missing values
print(products[products['product_name'].isna()]) #Found 1,258 rows with missing product_name values.

# Combine conditions to check for missing product names in aisles other than 100
products[(products['product_name'].isna()) & (products['aisle_id']!=100)]

#confirmed all missing values are associated with the 'aisle_id' 100. 

# Combine conditions to check for missing product names in aisles other than 21
products[(products['product_name'].isna()) & (products['department_id'] !=21)]

#Confirmed all missing values are associated with the 'department_id' 21. 
#The instruction said aisle 21, but I am using department_id 21 to correct the typo. 

# What is this aisle and department?
print(aisles[aisles['aisle_id']==100])
print()
print(departments[departments['department_id']==21])

#We can conclude that these rows were intentionally grouped into missing categories. 

# Fill missing product names with 'Unknown'
products['product_name']= products['product_name'].fillna('Unknown')

print(products['product_name'].isna().sum())

#Used .fillna() to succesesfully replace all NaN values with 'Unknown'.
#Perfromed an extra step to ensure the missing values were replaced with 'Unknown'.

# Display rows where the days_since_prior_order column has missing values
orders[orders['days_since_prior_order'].isna()]
#used isna() to display where 'days_since_prior_order' column was zero. Possibly only missing values where it was customers first order.

# Are there any missing values where it's not a customer's first order?
orders[(orders['days_since_prior_order'].isna()) & (orders['order_number'] != 1)]

#output is zero, which means only time data is missing is during customers first order. 

# Display rows where the add_to_cart_order column has missing values
order_products[order_products['add_to_cart_order'].isna()]

#No obvious pattern, mixed reordered values (1 or 0), Significant number of missing rows suggests this may not be a 'glitch'.

# Use .min() and .max() to find the minimum and maximum values for this column.
order_products['add_to_cart_order'].agg(['min','max'])

#checking min and max in data to see where the 'gap' begins.The data is limited to 64 items per order.

# Save all order IDs with at least one missing value in 'add_to_cart_order'
missing_cart_order_ids = order_products[order_products['add_to_cart_order'].isna()]['order_id'].unique()
missing_cart_order_ids
#used unique() to ensure each order_id is only listed once.

# Do all orders with missing values have more than 64 products?
order_counts = order_products[order_products['order_id'].isin(missing_cart_order_ids)].groupby('order_id').size()
order_counts.min()

#We group by order_id and count the number of products in each. Then found the smallest order in this missing group, concluding that all orders with missing values have more than 64 products.

# Replace missing values with 999 and convert column to integer type

order_products['add_to_cart_order'] = order_products['add_to_cart_order'].fillna(999)
#Used fillna() to fill NaN values with 999. 

order_products['add_to_cart_order'] = order_products['add_to_cart_order'].astype(int)
#converted column from float to integer, removing the decimal makes code easier to read. 

print(order_products['add_to_cart_order'].max())
#checked max value to confirm the values have been changes to 999.

# Find the number of duplicate rows in the orders dataframe

print(orders.duplicated().sum())

#There are 15 duplicated rows in the orders dataframe.

# View the duplicate rows

print(orders[orders.duplicated()])

# Remove duplicate orders

orders = orders.drop_duplicates().reset_index(drop=True)

# Double check for duplicate rows

print(orders.duplicated().sum())

#confirmed there are no more duplicate rows

# Check for fully duplicate rows

print(products.duplicated().sum())

# Check for just duplicate product IDs using subset='product_id' in duplicated()

products[products.duplicated(subset='product_id', keep=False)]

# Check for just duplicate product names (convert names to lowercase to compare better)

print(products['product_name'].str.lower().duplicated().sum())
print()
products[products['product_name'].str.lower().duplicated()]

#viewed the actual duplicated rows in addition to the number of duplicated rows. 

products[products['product_name'].str.lower() == 'high performance energy drink']

#Create a helper column with lowercased names
products['product_name_lower'] = products['product_name'].str.lower()

#Drop duplicates based on that helper column
products = products.drop_duplicates(subset='product_name_lower').reset_index(drop=True)

#Remove the helper column to keep the DataFrame clean
products = products.drop(columns=['product_name_lower'])

#Corrected confirmation: Check 'products' instead of 'order_products'
#We check the 'product_name' column specifically for duplicates
print(f"Duplicate product names remaining: {products['product_name'].str.lower().duplicated().sum()}")

#Checked for duplicates using duplicated().sum() and put my response in an f string. 

#Check for duplicate entries in the departments dataframe

departments[departments.duplicated()]

#Check for duplicate department names (ignoring capitalization)

print(departments['department'].str.lower().duplicated().sum())

#It is safe to conclude departments DataFrame has zero duplicated entires.

# Check for aisles entries in the departments dataframe
#Typo in instructions. I suppose its meant to say check for duplicate entries in the aisles dataframe

print(aisles.duplicated().sum())

#Run a case-sensitive check to ensure there are no duplicates in the aisles dataframe. 

print(aisles['aisle'].str.lower().duplicated().sum())

#Safe to conclude that there are no duplicates in the aisles dataframe. 

# Check for duplicate entries in the order_products dataframe

print(order_products.duplicated().sum())

#No need to run a case-sensitive check because all data in this dataframe are numbers and numbers dont have upper and lower case versions. 

#Check unique values for the hour of the day (Should be 0-23) Arrange in ascending order.

print("Unique hours of day:", sorted(orders['order_hour_of_day'].unique()))

#Check unique values for the day of the week (Should be 0-6) Arrange in ascending order.

print("Unique days of week:", sorted(orders['order_dow'].unique()))

#Order ranges for both columns are validated.

# Count the number of orders placed at each hour of the day
# .value_counts() calculates the frequency of each unique value in the column
hourly_counts = orders['order_hour_of_day'].value_counts()

# Sort the counts by the index (the hour)
# This ensures the chart displays hours chronologically from 0 to 23
hourly_counts_sorted = hourly_counts.sort_index()

# Create the bar plot
# We use a bar plot to clearly see the differences between individual hours
# figsize sets the width and height of the chart for better readability
hourly_counts_sorted.plot(kind='bar', figsize=(12, 6), color='skyblue', edgecolor='black')

# Add a descriptive title
# This helps the reader immediately understand the purpose of the graph
plt.title('Total Number of Orders by Hour of Day', fontsize=16)

# Label the X-axis
# We specify that '0' represents midnight to make the chart user-friendly
plt.xlabel('Hour of Day (0 = Midnight, 23 = 11:00 PM)', fontsize=12)

# Label the Y-axis
# This clarifies exactly what the bar height represents
plt.ylabel('Number of Orders', fontsize=12)

# Add a grid on the Y-axis
# The 'alpha' makes the lines faint so they don't distract from the data
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Use tight_layout to ensure labels aren't cut off
# This is a best practice for clean, professional-looking visualizations
plt.tight_layout()

# Display the plot
plt.show()

# 1. Count the number of orders for each day of the week
# .value_counts() identifies how many orders were placed on Day 0, Day 1, etc.
dow_counts = orders['order_dow'].value_counts()

# 2. Sort the results by the index (0-6)
# This ensures the chart follows the natural order of a week
dow_counts_sorted = dow_counts.sort_index()

# 3. Create a bar plot to visualize the frequency of orders
# Using 'lightgreen' helps differentiate this chart from the hourly analysis
dow_counts_sorted.plot(kind='bar', figsize=(10, 6), color='orange', edgecolor='black')

# 4. Add a title to clearly define the data being shown
plt.title('Total Number of Orders by Day of Week', fontsize=16)

# 5. Label the X-axis
# Note: In this dataset, 0 and 1 usually represent the weekend (Sunday and Monday)
plt.xlabel('Day of Week (0 = Sunday, 1 = Monday, ..., 6 = Saturday)', fontsize=12)

# 6. Label the Y-axis
plt.ylabel('Number of Orders', fontsize=12)

# 7. Add a faint grid on the Y-axis for better readability of the values
plt.grid(axis='y', linestyle='--', alpha=0.6)

# 8. Use tight_layout to prevent labels from being cut off
plt.tight_layout()

# 9. Display the plot
plt.show()

#Based on the trends, Sunday and Monday show the highest volume of orders. It levels out Tuesday through Saturday. 

# Count the frequency of each interval of days since the last order
wait_counts = orders['days_since_prior_order'].value_counts()

# Sort the results by the index (the number of days)
# This will ensure ascending order for easier readability
wait_counts_sorted = wait_counts.sort_index()

# Create a bar plot to visualize the distribution
# We use a wider figure (12, 6) to accommodate the 30 day labels
wait_counts_sorted.plot(kind='bar', figsize=(12, 6), color='turquoise', edgecolor='black')

# Add a title to describe the visualization
plt.title('Distribution of Days Since Prior Order', fontsize=16)

# Label the X-axis to represent the time interval
plt.xlabel('Days Since Prior Order', fontsize=12)

# Label the Y-axis to show the volume of orders
plt.ylabel('Number of Orders', fontsize=12)

# Add a faint grid for easier measurement of the bar heights
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Clean up to ensure all X-axis labels are visible
plt.tight_layout()

# Display the plot
plt.show()

#Distribution shows outliers at day 7 and 30. Marketing tactics or sales would be most effective just before those days. 

"""
Is there a difference in 'order_hour_of_day' distributions on Wednesdays and Saturdays?"""

# Create a mask for orders placed on Wednesdays (Day 3)
wednesday_mask = orders['order_dow'] == 3

# Create a mask for orders placed on Saturdays (Day 6)
saturday_mask = orders['order_dow'] == 6

# Apply the masks to filter the data, then count the hours and sort by index
wednesday_hours = orders[wednesday_mask]['order_hour_of_day'].value_counts().sort_index()
saturday_hours = orders[saturday_mask]['order_hour_of_day'].value_counts().sort_index()

# Combine the Wednesday and Saturday series into a single DataFrame
# axis=1: aligns the data side-by-side as columns
# keys: provides the column headers for each day
combined_hours = pd.concat([wednesday_hours, saturday_hours], axis=1, keys=['Wednesday', 'Saturday'])

# Fill any missing values with 0 
combined_hours = combined_hours.fillna(0)

# Display the first few rows to verify the alignment
print(combined_hours.head())

#Isolate the hours for each day
wednesday_hours = orders[orders['order_dow'] == 3]['order_hour_of_day']
saturday_hours = orders[orders['order_dow'] == 6]['order_hour_of_day']

#Plot them together
plt.figure(figsize=(10, 6))

#Plot Wednesday in blue
plt.hist(wednesday_hours, bins=24, alpha=0.5, label='Wednesday', color='blue')

#Plot Saturday in orange
plt.hist(saturday_hours, bins=24, alpha=0.5, label='Saturday', color='red')

#Add labels (Y-axis is now back to "Number of Orders")
plt.title('Comparison of Order Hours: Wednesday vs. Saturday')
plt.xlabel('Hour of Day')
plt.ylabel('Number of Orders')
plt.xticks(range(0, 24))
plt.legend()

plt.show()
#Both Wednesday and Saturday show the highest activity during midday, though Saturday shoppers tend to start their day later than those on Wednesday.
#Overall, the patterns are very similar, proving that peak shopping hours remain consistent regardless of the day of the week.

"""
What's the distribution for the number of orders per customer?
"""

#Count how many orders each user has made
# We group by user_id and count the number of order_ids for each
user_order_counts = orders.groupby('user_id')['order_id'].count()

# Sort the results from the grouping to see the order counts in order
user_order_counts_sorted = user_order_counts.sort_values()

#user_order_counts contains the total orders for each user_id
plt.figure(figsize=(12, 6))
plt.hist(user_order_counts, bins=30, color='green', edgecolor='black')

#Add a clear title and label the axes
plt.title('Distribution of Orders per Customer', fontsize=16)
plt.xlabel('Number of Orders', fontsize=12)
plt.ylabel('Number of Customers', fontsize=12)

#Add a faint grid to help gauge the customer count
plt.grid(axis='y', linestyle='--', alpha=0.7)

#Display the plot
plt.show()

"""
What are the top 20 popular products
"""

# Merge the order_products and products DataFrames using the 'product_id' column
# We use an 'inner' merge to ensure we only keep items that exist in both tables
order_info = order_products.merge(products, on='product_id')

# Group by both ID and Name, then use .size() to count the occurrences
# .size() returns the total number of rows for each unique product
product_counts = order_info.groupby(['product_id', 'product_name']).size()

# Sort the counts in descending order so the most frequently ordered items are at the top
product_counts_sorted = product_counts.sort_values(ascending=False)

# Display the top results to verify the ranking
print(product_counts_sorted.head(20))

#Convert the Series to a DataFrame and reset the index
#This turns the MultiIndex (id, name) into regular columns
top_20_df = product_counts_sorted.head(20).reset_index()

#Rename the count column (which usually defaults to 0 or 'size') 
top_20_df.columns = ['product_id', 'product_name', 'count']

#Print the table (showing both ID and Name as requested)
print(top_20_df)

#Create the bar chart using ONLY product_name for the labels
plt.figure(figsize=(12, 10))
plt.bar(top_20_df['product_name'], top_20_df['count'], color='tan', edgecolor='black')

#Formatting
plt.title('Top 20 Most Popular Products', fontsize=16)
plt.xlabel('Product Name', fontsize=12)
plt.ylabel('Number of Times Ordered', fontsize=12)
plt.xticks(rotation=45, ha='right') # Rotate names so they don't overlap
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()

plt.show()

"""
How many items do people typically buy in one order? What does the distribution look like?
"""

# Group by order_id and count the number of products in each order
items_per_order = order_products.groupby('order_id')['product_id'].count()

# Count how many times each order size (e.g., a 5-item order) occurs
order_size_dist = items_per_order.value_counts().sort_index()

#Create a bar plot to show how many items are typically in an order
order_size_dist.plot(kind='bar', figsize=(15, 7), color='red', edgecolor='black')

#Add descriptive titles and axis labels
plt.title('Distribution of Order Sizes', fontsize=16)
plt.xlabel('Number of Items per Order', fontsize=12)
plt.ylabel('Total Number of Orders', fontsize=12)

#Modify the x-axis to show every 2nd number
plt.xticks(ticks=range(0, len(order_size_dist), 2), 
           labels=order_size_dist.index[::2], 
           rotation=0)

#Add a faint grid for easier comparison of order volumes
plt.grid(axis='y', linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()

#Most orders are small, typically containing between 1 and 10 items, with the frequency of orders decreasing significantly as the basket size increases. This shows a negative correlation between basket size and total number of orders. 

#Filter the distribution to include only orders with fewer than 35 items
order_size_dist_filtered = order_size_dist[order_size_dist.index < 35]

#Create the bar plot for the filtered data
order_size_dist_filtered.plot(kind='bar', figsize=(15, 7), color='red', edgecolor='black')

#Format the x-axis to show every 2nd item count for clarity
plt.xticks(ticks=range(0, len(order_size_dist_filtered), 2), 
           labels=order_size_dist_filtered.index[::2], 
           rotation=0)

#Add titles and labels
plt.title('Distribution of Order Sizes (Filtered: < 35 Items)', fontsize=16)
plt.xlabel('Number of Items per Order', fontsize=12)
plt.ylabel('Total Number of Orders', fontsize=12)

#Add a faint grid and clean layout
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()

plt.show()
"""The typical order contains 5 or 6 items, with most orders having between 1 and 20 items."""

"""What are the top 20 items that are reordered most frequently?"""

# Create a DataFrame containing only items that have been reordered
reordered_products = order_products[order_products['reordered'] == 1]

# Merge the filtered reordered items with the products table
reordered_info = reordered_products.merge(products, on='product_id')

# Group by product_id and product_name to count reorders for each item
reorder_counts = reordered_info.groupby(['product_id', 'product_name']).size()

#Sort the counts
reorder_counts_sorted = reorder_counts.sort_values(ascending=False)

#Get the top 20 and convert to a clean DataFrame
# reset_index() pulls 'product_id' and 'product_name' out of the index and into columns
top_20_reorders_table = reorder_counts_sorted.head(20).reset_index()

#Rename the count column for clarity
top_20_reorders_table.columns = ['product_id', 'product_name', 'reorder_count']

#Display the results as a table
print(top_20_reorders_table)

#Prepare the data (Resetting the index to separate IDs from Names)
top_20_reorders_df = reorder_counts_sorted.head(20).reset_index()
top_20_reorders_df.columns = ['product_id', 'product_name', 'reorder_count']

#Create a horizontal bar chart
plt.figure(figsize=(12, 10))

#We specifically use the 'product_name' column for the Y-axis and 'reorder_count' for the bar width
plt.barh(top_20_reorders_df['product_name'], top_20_reorders_df['reorder_count'], 
         color='pink', edgecolor='black')

#This flips the axis so the largest bar is at the top since the barh plot plots items from the bottom up by default. 
plt.gca().invert_yaxis()

#Add title and labels
plt.title('Top 20 Most Frequently Reordered Products', fontsize=16)
plt.xlabel('Number of Reorders', fontsize=12)
plt.ylabel('Product Name', fontsize=12)

#Add a faint grid for better readability
plt.grid(axis='x', linestyle='--', alpha=0.5)

#Ensure the layout is clean
plt.tight_layout()

plt.show()

#we can conclude that the most frequently reordered products are mainly fresh produce and organic items, suggesting that customers rely on the service primarily for regular restocking of perishables.

"""It looks like produce and dairy comprise the most reordered products as well. It makes sense that perishables would be the most reordered items."""

"""
For each product, what proportion of its orders are reorders?
"""

#Merge the datasets
#Combining order_products with products to get names and IDs
order_info_combined = order_products.merge(products, on='product_id')

#Group the data. Calculate the mean of 'reordered'
#Grouping by ID and Name, then calculating the average reorder rate
reorder_rate_series = order_info_combined.groupby(['product_id', 'product_name'])['reordered'].mean()

#Sort the results
# Sorting by the calculated rate in descending order (highest rates first)
reorder_rate_sorted = reorder_rate_series.sort_values(ascending=False)

#Convert to a DataFrame
# Use reset_index to move 'product_id' and 'product_name' out of the index and into columns
reorder_rate_df = reorder_rate_sorted.reset_index()

#Rename the calculated column for better clarity
reorder_rate_df.columns = ['product_id', 'product_name', 'reorder_rate']

#Optional Sorting (As per reviewer's request for "informative slice")
#We will keep the data sorted by 'reorder_rate' to show the top/bottom as requested.

# --- Reviewer Feedback Implementation ---

#Display the table's shape so the reviewer knows the full result was produced
print(f"Table Shape: {reorder_rate_df.shape}")
print(f"Total unique products analyzed: {reorder_rate_df.shape[0]}")
print("-" * 50)

# Show an informative slice: The Top 5 and Bottom 5 reorder rates
print("Informative Slice: Top 5 and Bottom 5 Products by Reorder Rate")
informative_slice = pd.concat([reorder_rate_df.head(5), reorder_rate_df.tail(5)])
display(informative_slice)

"""
For each customer, what proportion of their products ordered are reorders?
"""
# Merge order_products with orders to bring in customer_id and order_timing
order_customer_info = order_products.merge(orders, on='order_id')

# Group the data by user_id
user_groups = order_customer_info.groupby('user_id')

# Calculate the average reorder rate for each user
user_reorder_rate = user_groups['reordered'].mean()

# Sort the customers by their reorder rate in descending order
user_reorder_sorted = user_reorder_rate.sort_values(ascending=False)

# Convert the Series into a clean DataFrame
user_reorder_df = user_reorder_sorted.reset_index()

# Rename columns for clarity: 'reordered' becomes 'user_reorder_rate'
user_reorder_df.columns = ['user_id', 'user_reorder_rate']

# Display the first few rows of the new DataFrame
user_reorder_df

"""
What are the top 20 items that people put in their carts first?
"""
# Combine the two datasets on the common 'product_id' column
order_products_named = order_products.merge(products, on='product_id')

# Create a DataFrame containing only the first item added to each cart
first_items = order_products_named[order_products_named['add_to_cart_order'] == 1]

# Group by product and count how many times each was the first item added
first_item_counts = first_items.groupby(['product_id', 'product_name']).size()

# Calculate the total occurrences for each product being the first added
first_item_counts = first_items.groupby(['product_id', 'product_name']).size()

# Sort the products by first-in-cart frequency from highest to lowest
first_item_counts_sorted = first_item_counts.sort_values(ascending=False)

# Extract the top 20 products most likely to be added to the cart first
top_20_first_items = first_item_counts_sorted.head(20)

# Display the top 20 results
print(top_20_first_items)

"""
The products that are most often placed into the cart first are produce, dairy, and beverages
such as soda or water. I couldn't really say why that is without experience using Instacart
because this could have more to do with app design than properties of the products. I do notice
that there is considerable overlap between this result and the previous result for most popular
and most reordered item types. It could simply be that the app prioritizes popular items as the
first suggested purchases, so it happens to be more convenient for customers to place these
items in their cart first.
"""
