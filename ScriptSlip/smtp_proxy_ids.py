import smtpd
import asyncore
import re
import smtplib

class IDSProxySMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print(f"[+] Received message from: {mailfrom}")
        print(f"[+] Intended recipients: {rcpttos}")

        try:
            decoded_data = data.decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"[!] Failed to decode data: {e}")
            return '550 IDS : Cannot decode email body.'

        if mailfrom.lower() != "it.support@mindbreak.local":
            return '550 IDS : Only requests from it.support@mindbreak.local are accepted.'

        if "sys.admin@mindbreak.local" not in [r.lower() for r in rcpttos]:
            return '550 IDS : Service restricted to sys.admin@mindbreak.local.'

        if not re.search(r'Content-Type: application/octet-stream', decoded_data, re.IGNORECASE):
            return '550 IDS : Please attach the script file as attachment.'

        if "Bonjour, voici le script bash demande." not in decoded_data:
            return '550 IDS : Message incomplete. Please respect the internal communication model. Use : Bonjour, voici le script bash demande.'

        if "Subject: Automatisation des taches" not in decoded_data:
            return '550 IDS : Message incomplete. Please respect the internal communication model. Use : Subject: Automatisation des taches'
                    
        print("[+] Mail validated, forwarding to Postfix local")
        try:
            smtp = smtplib.SMTP('localhost', 25)
            smtp.sendmail(mailfrom, rcpttos, data)
            smtp.quit()
            return None
        except Exception as e:
            print(f"[!] Error forwarding to local Postfix : {e}")
            return '451 IDS : Internal temporary error.'

if __name__ == "__main__":
    print("[*] Proxy SMTP IDS started on port 2525")
    server = IDSProxySMTPServer(('0.0.0.0', 2525), None)
    asyncore.loop()
