import read
import pandas as pd


def process_data(conn):
    # DataFrame for dim_products table
    df_dim_products = pd.read_sql("SELECT CURRENT_TIMESTAMP()+0 AS 'batch_id',curdate() AS 'batch_date', product_id ,product_name,\
                             product_price, category_id, category_name, department_id, department_name\
                             FROM products p JOIN categories c ON p.product_category_id=c.category_id\
                             JOIN departments d ON c.category_department_id=d.department_id", conn)

    # DataFrame for dim_customers table
    df_dim_customers = pd.read_sql("SELECT CURRENT_TIMESTAMP()+0 AS 'batch_id',curdate() AS 'batch_date',customer_id,\
                                 customer_fname,customer_lname,customer_email,customer_password,customer_street,\
                                 customer_city,customer_state,customer_zipcode from customers", conn)

    # DataFrame for fact_product_revenue_dly table
    df_fact_product_revenue_dly = pd.read_sql("SELECT DATE(order_date)+0 AS 'date_id',order_item_product_id as 'product_id',\
                          SUM(CASE WHEN order_status in ('CLOSED','COMPLETE') THEN order_item_subtotal END) 'product_revenue',\
                          SUM(CASE WHEN order_status in ('PROCESSING', 'PENDING','PENDING_PAYMENT') THEN order_item_subtotal END) 'outstanding_revenue'\
                          FROM orders o JOIN order_items oi ON o.order_id=oi.order_item_order_id\
                          group by order_date,order_item_product_id", conn)

    # DataFrame for revenue column in fact_revenue_dly table
    df_fact_revenue_col = pd.read_sql("SELECT DATE(order_date)+0 AS 'date_id',sum(order_item_subtotal) AS 'revenue'\
                          FROM orders o JOIN order_items oi ON o.order_id=oi.order_item_order_id\
                          where order_status IN ('CLOSED','COMPLETE') group by order_date", conn)

    # DataFrame for rest of the columns in fact_revenue_dly table
    df_fact_revenue_count_cols = pd.read_sql("SELECT DATE(order_date)+0 AS 'date_id',\
                    COUNT(order_id) 'total_order_count',\
                    SUM(order_status in ('CLOSED','COMPLETE')) 'revenue_order_cnt',\
                    SUM(order_status='CANCELED') 'canceled_order_cnt',\
                    SUM(order_status in ('PROCESSING', 'PENDING','PENDING_PAYMENT')) 'oustanding_order_cnt'\
                    FROM orders group by order_date", conn)

    # DataFrame for fact_revenue_dly table(merging both revenue and counts)
    df_fact_revenue_dly = pd.merge(df_fact_revenue_col, df_fact_revenue_count_cols, on='date_id')
    return df_dim_products, df_dim_customers, df_fact_product_revenue_dly, df_fact_revenue_dly
