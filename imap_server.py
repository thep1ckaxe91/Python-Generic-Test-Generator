import imaplib
import smtplib
import email
import time
from email.mime.text import MIMEText

# ==== CONFIG ====
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
EMAIL_ACCOUNT = "thep1ckaxe.receiver@gmail.com"
EMAIL_PASSWORD = "rexb jevv lese ihso"
SUBJECT_PREFIX = "pythonmastery"
REPLY_MESSAGE = """Hello,

The token is: 380r9u-jokf2039rj-sdf23f-of-k23490jfimkdg3049jre0g92j4-o-fmdoigjn309jfmdoig34nm09ogngisdsfi1378r9gkpfdlmnbjajssxzx.;c,vm;b

Paste the token to a "token.txt" file and submit, it should be accepted.
"""

def check_and_reply():
    # Connect to IMAP and search emails
    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    imap.select("INBOX")

    status, messages = imap.search(None, '(UNSEEN SUBJECT "{}")'.format(SUBJECT_PREFIX))
    if status != "OK":
        print("No messages found.")
        imap.logout()
        return

    for num in messages[0].split():
        status, data = imap.fetch(num, "(RFC822)")
        if status != "OK":
            continue

        msg = email.message_from_bytes(data[0][1])

        # Ensure it's text-only
        if msg.is_multipart():
            continue  # skip multipart emails
        body = msg.get_payload(decode=True).decode()

        from_addr = email.utils.parseaddr(msg["From"])[1]
        print(f"Replying to: {from_addr}")

        # Send reply
        smtp = smtplib.SMTP_SSL(SMTP_SERVER, 465)
        smtp.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)

        reply = MIMEText(REPLY_MESSAGE)
        reply["Subject"] = "Re: " + msg["Subject"]
        reply["From"] = EMAIL_ACCOUNT
        reply["To"] = from_addr

        smtp.sendmail(EMAIL_ACCOUNT, from_addr, reply.as_string())
        smtp.quit()

    imap.logout()

if __name__ == "__main__":
    while True:
        time.sleep(1)
        check_and_reply()
