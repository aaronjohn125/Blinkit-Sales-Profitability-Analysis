import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

orders = pd.read_csv("archive/blinkit_orders.csv")
customers = pd.read_csv("archive/blinkit_customers.csv")
products = pd.read_csv("archive/blinkit_products.csv")
order_items = pd.read_csv("archive/blinkit_order_items.csv")
delivery = pd.read_csv("archive/blinkit_delivery_performance.csv")
feedback = pd.read_csv("archive/blinkit_customer_feedback.csv")
orders.info()
customers.info()
products.info()
order_items.info()
delivery.info()
feedback.info()

#let's start with revenue from different orders 
order_items["revenue"] = (order_items["quantity"] *order_items["unit_price"])

print("Total Revenue")
print(order_items["revenue"].sum())


#Which products generate the most revenue?
sales_by_product = (order_items.groupby("product_id")["revenue"].sum().reset_index())
sales_by_product = sales_by_product.merge(products[["product_id","product_name"]],how="left")

print("\n PRODUCT WISE REVENUE\n",sales_by_product.sort_values("revenue",ascending=False).head(10))


#Are deliveries meeting customer expectations?
on_time_rate = ( delivery["delivery_status"].eq("On Time").mean()* 100)

print(f"\n On Time Delivery Rate: {on_time_rate:.2f}%")
delay_reasons = ( delivery["reasons_if_delayed"].value_counts())

print(delay_reasons)



#Who are our highest-value customers?
customers_sorted = (customers.sort_values("avg_order_value",ascending=False))

print("\n highest-value customers\n",customers_sorted[["customer_name","avg_order_value"]].head(10))



total_revenue = order_items["revenue"].sum()

total_orders = orders["order_id"].nunique()

total_customers = customers["customer_id"].nunique()

avg_order_value = (total_revenue /total_orders)


print("\n****************************************")
print(f"Revenue: Rs.{total_revenue:,.2f}")
print(f"Orders: {total_orders:,}")
print(f"Customers: {total_customers:,}")
print(f"Average Order Value: Rs.{avg_order_value:,.2f}")
print("****************************************")


#are customes coming back to the app
repeat_customers = customers[customers["total_orders"] > 1]
repeat_rate = (len(repeat_customers) / len(customers)) * 100

print("\nREPEAT CUSTOMER ANALYSIS")
print(f"Repeat Customer Rate: {repeat_rate:.2f}%")
print("It has great customer retension of more than 90%")

#concentation of revenue by the top 10 most revenue generating products
sales_by_product = sales_by_product.sort_values("revenue",ascending=False)

top_10_revenue = (sales_by_product.head(10)["revenue"].sum())

revenue_share = (top_10_revenue /total_revenue) * 100

print("\nREVENUE CONCENTRATION")

print(f"Top 10 Products contribute "f"{revenue_share:.2f}% "f"of total revenue")

## PAYMENT METHOD ANALYSIS
payment_analysis = orders.groupby('payment_method').agg(Orders=('order_id','count'),Revenue=('order_total','sum'),Avg_Order_Value=('order_total','mean'))

print("\n===== PAYMENT METHOD ANALYSIS =====")
print(payment_analysis)


# Create master dataframe

df = orders.merge(customers,on='customer_id',how='left')

df = df.merge(delivery,on='order_id',how='left')

df = df.merge(feedback,on=['order_id','customer_id'],how='left')


#category wise revenue analysis
product_sales = order_items.merge(products,on='product_id')

product_sales['Revenue'] = (product_sales['quantity'] * product_sales['unit_price'])

category_revenue = (product_sales.groupby('category')['Revenue'].sum().sort_values(ascending=False))

print("\n",category_revenue)


#Category wise profit analysis
product_sales = order_items.merge(products,on='product_id')

product_sales['Revenue'] = (product_sales['quantity']* product_sales['unit_price'])

product_sales['Profit'] = (product_sales['Revenue']* product_sales['margin_percentage']/ 100)

category_profit = (product_sales.groupby('category')['Profit'].sum().sort_values(ascending=False))

total_profit = category_profit.sum()

profit_percentage = (category_profit/ total_profit) * 100

profit_summary = pd.DataFrame({'Profit': category_profit,'Profit_Percentage': profit_percentage})

profit_summary = profit_summary.round(2)

print("\nCATEGORY PROFIT CONTRIBUTION (%)")
print(profit_summary)


top_category = profit_summary.index[0]
top_profit_pct = profit_summary.iloc[0]['Profit_Percentage']

print(f"\nMost Profitable Category: {top_category}")

print(f"Contribution to Total Profit: {top_profit_pct:.2f}%")

profit_summary['Profit_Percentage'].plot(kind='bar',figsize=(10,5))

plt.title('Category Contribution to Total Profit (%)')

plt.ylabel('Profit %')
plt.xlabel('Category')

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()