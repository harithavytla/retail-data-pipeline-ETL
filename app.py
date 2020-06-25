import sys

from process import process_data
from read import get_connection
from config import DB_DETAILS
from write import load_data


def main():
    env = sys.argv[1]
    db_details = DB_DETAILS[env]
    source_db = db_details['SOURCE_DB']
    target_db = db_details['TARGET_DB']
    # Establishing connection to MySQL DB
    mysql_conn = get_connection(source_db)
    # Reading data from base tables through DataFrames
    df_dim_products, df_dim_customers, df_fact_product_revenue_dly, \
        df_fact_revenue_dly = process_data(mysql_conn)
    # Loading data into facts and dim tables in Postgres
    load_data(df_dim_products, df_dim_customers, df_fact_product_revenue_dly, df_fact_revenue_dly, target_db)


if __name__ == '__main__':
    main()
