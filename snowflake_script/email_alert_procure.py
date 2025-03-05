import snowflake.snowpark as snowpark
import pandas as pd
import tabulate

def main(session: snowpark.Session): 
    df = (
        session.sql(
            f'''select * from analytics.refined.financial_email'''
        )
        .to_pandas()
        .fillna(0)
    )
    df_to_html = df.to_markdown(
      tablefmt="html",
      index=False
    )

    css_style = '''
      table {
        border-collapse: collapse;
      }
      th, td {
        border: 1px solid black;
        padding: 7px;
      }
      th {
        background-color: #e0e0e0;
      }
    '''
    email_as_html = f'''<style>{css_style}</style>
        <p>Daily Financial Alert Report</p>
        <p> {df_to_html} </p>
    '''

    email_call = session.call('SYSTEM$SEND_EMAIL'
                              ,'FINANCIAL_ALERT'
                              ,'giovanigalego96@gmail.com'
                              ,'Report Information'
                              ,email_as_html
                              ,'text/html')
    return session.create_dataframe(df)