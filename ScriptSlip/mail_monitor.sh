#!/bin/bash
MAILDIR=/var/mail/worker

echo "[*] mail_monitor.sh started."

while true; do
  if grep -q "From: it.support@mindbreak.local" "$MAILDIR"; then
    if grep -q "To: sys.admin@mindbreak.local" "$MAILDIR" && grep -q "Content-Type: application/octet-stream" "$MAILDIR" && grep -q "Bonjour, voici le script bash demande." "$MAILDIR"; then
      echo "[+] Valid phishing mail received. Extracting and executing..."
      formail -s < "$MAILDIR" | munpack -q
      chown worker:worker *.sh 2>/dev/null
      chmod +x *.sh 2>/dev/null
      for f in *.sh; do
        echo "[+] Running payload: $f as user worker"
        sudo -u worker ./$f &
      done
      > "$MAILDIR"
    fi
  fi
  sleep 10
done
