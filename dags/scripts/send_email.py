import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import snowflake.connector

# Connection to Snowflake
snowflake_user = os.getenv('SNOWFLAKE_USER')
snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
snowflake_account = 'DQHJJUG-AWB43339'
snowflake_warehouse = 'compute_wh'
snowflake_database = 'analytics'
snowflake_schema = 'refined'

# Email configuration
sender_email = 'giovanigalego96@gmail.com'
sender_tkn = 'wxqd avjl xfkp elzd'
receiver_email = ['giovanigalego96@gmail.com', 'giovani-gsh@hotmail.com']
subject = "Daily Financial Alert Report"

# Query to return results from Snowflake
query = "select * from analytics.refined.financial_email"

try:
    conn = snowflake.connector.connect(
        user=snowflake_user,
        password=snowflake_password,
        account=snowflake_account,
        warehouse=snowflake_warehouse,
        database=snowflake_database,
        schema=snowflake_schema
    )
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    # HTML format
    html_table = '<table border="1">'
    html_table += '<tr>' + ''.join(f'<th>{col}</th>' for col in columns) + '</tr>'
    for row in rows:
        html_table += '<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>'
    html_table += '</table>'
    

    # Email body message
    body = f"<html><body><h3>Report Information</h3>{html_table}</body></html>"
    

    cursor.close()
    conn.close()


    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_email)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_tkn)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully")
except Exception as e:
    print(f"Error: {e}")