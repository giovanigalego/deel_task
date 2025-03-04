import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import snowflake.connector

# Snowflake connection parameters
snowflake_user = os.getenv('SNOWFLAKE_USER')
snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
snowflake_account = 'opb84404.us-east-1'
snowflake_warehouse = 'compute_wh'
snowflake_database = 'deel'
snowflake_schema = 'raw'

# Email configuration
sender_email = 'giovanigalego96@gmail.com'
sender_password = os.getenv('EMAIL_SENDER_PASSWORD')
# 'wxqd avjl xfkp elzd'
receiver_email = ['giovanigalego96@gmail.com', 'giovani-gsh@hotmail.com']
subject = "Snowflake Query Results"

# Query Snowflake table
query = "select * from analytics.refined.fact_financials where invoice_created_at >= '2024-04-24' and send_alert = 1"  # Adjust query as needed

try:
    # Connect to Snowflake
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

    # Format rows as an HTML table
    html_table = '<table border="1">'
    html_table += '<tr>' + ''.join(f'<th>{col}</th>' for col in columns) + '</tr>'
    for row in rows:
        html_table += '<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>'
    html_table += '</table>'
    
    # Email body
    body = f"<html><body><h3>Snowflake Query Results</h3>{html_table}</body></html>"
    
    # Close connection
    cursor.close()
    conn.close()

    # Create email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_email)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))  # Attach HTML content

    # Send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully")
except Exception as e:
    print(f"Error: {e}")





# import smtplib
# import os
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# sender_email = 'giovanigalego96@gmail.com'
# sender_password = 'wxqd avjl xfkp elzd'
# receiver_email = ['giovanigalego96@gmail.com','giovani-gsh@hotmail.com']

# subject = "Test Email"
# body = "This is a test email"
# msg = MIMEMultipart()
# msg['From'] = sender_email
# msg['To'] = ', '.join(receiver_email)
# msg['Subject'] = subject

# msg.attach(MIMEText(body, 'plain'))
# try:
#     with smtplib.SMTP('smtp.gmail.com', 587) as server:
#         server.starttls()
#         server.login(sender_email, sender_password)
#         text = msg.as_string()
        
#         server.sendmail(sender_email, receiver_email, text)
#         print("Email sent successfully")
# except:
#     print("Error: unable to send email")