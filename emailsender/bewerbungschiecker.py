import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# Gmail configuration
gmail_user = 'your-email@gmail.com'
gmail_password = 'your-app-specific-password'  # Add your App Password here

# Function to send an email with optional attachments
def send_email(to_email, subject, body, attachment_paths=None):
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Check if there are attachments
    if attachment_paths:
        for attachment_path in attachment_paths:
            if os.path.isfile(attachment_path):
                # Create the attachment
                with open(attachment_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(attachment_path)}')
                    msg.attach(part)
            else:
                print(f"Attachment {attachment_path} not found or is invalid.")

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to_email, msg.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {str(e)}")
    finally:
        server.quit()

# Load the Excel file
def load_emails_from_excel(file_path):
    try:
        df = pd.read_excel(file_path, engine='openpyxl')  # Specify engine for openpyxl
        email_addresses = df['Email'].tolist()
        return email_addresses
    except Exception as e:
        print(f"Error reading the Excel file: {str(e)}")
        return []

# Main function
if __name__ == "__main__":
    excel_file = r'E:\Vscode\pythonpj\pythonpj1\email_list.xlsx'  # Use raw string for file path
    email_list = load_emails_from_excel(excel_file)

    subject = "Test Email with Attachments"
    body = "This is a test email sent from a Python script with multiple attachments."

    # List of PDF file paths
    pdf_file_paths = [
        r'E:\Vscode\pythonpj\pythonpj1\file1.pdf',  # Update with your PDF file paths
        r'E:\Vscode\pythonpj\pythonpj1\file2.pdf',
        r'E:\Vscode\pythonpj\pythonpj1\file3.pdf',
    ]

    for email in email_list:
        send_email(email, subject, body, attachment_paths=pdf_file_paths)
