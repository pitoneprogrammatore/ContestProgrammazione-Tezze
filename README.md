# Mail sender
Questo è uno script che permette di avere la stampa unione con l'email di google.
Questo script è stato riealizzato per un contest.

## Prima esecuzione
Per eseguire questo script in primo luogo bisogna creare una password per l'account di google che consente ad app esterne di accedere ai servizi ([link](https://myaccount.google.com/security?rapt=AEjHL4MbGEoWlakBM55Kv8XTcOfZgPpiF0sn6LbXOMjRPYj9pFnk5933vhH9gJGVxa0BcDmwzu1WkRwGq5kwX7oUVX-KqCwEbg)).
Cliccare la sezione sottolineata e compiere tutti i passaggi.
![Immagine](./docImages/PasswordAccount.jpg)

Una volta creata la password si copia nella variabile *password* a riga 59.
```python
# external app password is required to access to the sender account
password = 'password da genereare https://myaccount.google.com/security?rapt=AEjHL4MbGEoWlakBM55Kv8XTcOfZgPpiF0sn6LbXOMjRPYj9pFnk5933vhH9gJGVxa0BcDmwzu1WkRwGq5kwX7oUVX-KqCwEbg' 
context = ssl.create_default_context()
```
Si modifica il file contacts.json sostituendo a *recieverEmail* l'email del destinatario:
```json
[
    {"Mail": "nome@dominio", "Attached": "ciao.jpg", "nome": "Aurora",  "numero": "33333333"}
]
```
Si modifica il file format.json sostituendo a *senderEmail* l'email del mittente:
```json
{
    "From":"nome@dominio",
    "Subject":"...",
    "Message":"..."
}
```
Una volta fatti questi passaggi lo script si può eseguire:
```terminal
python3 SMTPsever.py
```
## Funzionamento dello script
Il funzionamento dello script si basa sui file *contact.json* e *format.json*. Il primo si occupa di salvare tutte le informazioni sui contatti ai quali inviare le email, il secondo si occupa di salvare il messaggio base. Ricorda che questi sono file json quindi devono rispettare la sintassi json.
### Format.json
Si possono modificare tutti i campi, nel primo va l'email del mittente, nel secondo va l'oggetto dell'email e nel terzo il testo del messaggio. Per inserire dei tag si utilizza la sintassi:
```
/*< nomeTag >*/
```
I tag servono per sostituirli con del testo che deve essere diverso per ogni destinatario (ex: nome destinatario). Il valore dei tag verrà specificato nel file *contats.json*.
### Contats.json
Il file è organizzato come un array di email, per ognuna si specifica l'email del destinatario, l'eventuale allegato che può essere omesso (L'allegato va inserito nella cartella *Attached*) e tutti i nomi dei tag che sono stati inseriti in format.json con il loro relativo valore. Per esempio:
```json
[
    {"Mail": "mario.rossi@gmail.com", "Attached": "ciao.jpg", "nome": "Mario",  "numero": "33333333"}
]
```
Questo specifica un email da inviare a mario.rossi@gmail.com, con l'allegato ciao.jpg, i tag /*<nome>*/ e /*<numero>*/ verranno sostituiti con Mario e 33333333. Ricorda che il campo *Attached* può essere omesso, se manca una definizione di un tag allora l'email non verrà inviata.