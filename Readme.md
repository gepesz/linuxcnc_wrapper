

# Bejövő és kimenő WebSocket/REST API üzenetek formátuma és tartalma

Az egységes JSON üzenetformátum biztosítja, hogy a REST API és a WebSocket egyaránt könnyen kezelhető és bővíthető legyen.

## Bejövő üzenetek formátuma (WebSocket és REST API)
### REST API bejövő üzenetek (HTTP GET vagy POST kérések)
- Parancsok küldése, állapotlekérdezés a wrapper felé
- A HTTP POST kérések JSON formátumú paramétereket is tartalmazhatnak.

*Mozgatás REST API-n keresztül:*

`
POST /motion/move{
	 "x": 100.0,
	 "y": 50.0,
	 "z": -10.0
	}
`

*Gép engedélyezése REST API-n keresztül*

`
POST /motion/enable
`

### WebSocket bejövő üzenetek

A WebSocket kliens parancsokat küldhet

*Mozgatás WebSocket-en keresztül*

```
{
  "type": "command",
  "command": "move",
  "parameters": {
    "x": 100.0,
    "y": 50.0,
    "z": -10.0
  }
}
```
*Gép engedélyezése WebSocket-en keresztül*

```
{
  "type": "command",
  "command": "enable_machine"
}
```

*Ismeretlen parancs esetén*

```
{
  "type": "command",
  "command": "unknown_command"
}
```

A wrapper hibát küld vissza, ha ismeretlen parancsot kap.

## Kimenő üzenetek formátuma (WebSocket és REST API válaszok)

A wrapper minden válaszában az alábbi egységes szerkezetet használjuk:

- **type**: (response, error, event) – az üzenet típusa.
- **command** vagy **query**: milyen parancsra vagy lekérdezésre érkezik a válasz.
- **status**: (success, in_progress, failed) – a végrehajtás állapota.
- **payload**: a visszaküldött adatok.
- **error**: ha hiba történt, itt lesz a részletes üzenet.

### REST API kimenő válaszok

*Mozgatás válasz*

```
{
  "type": "response",
  "command": "move_machine",
  "status": "in_progress",
  "payload": {
    "x": 100.0,
    "y": 50.0,
    "z": -10.0
  }
}
```

*Sikeres művelet válasz*

```
{
  "type": "response",
  "command": "enable_machine",
  "status": "success"
}
```

*Hibás parancs válasz*

```
{
  "type": "error",
  "command": "move_machine",
  "status": "failed",
  "error": "Invalid axis position"
}
```

### WebSocket kimenő válaszok

*Gép állapot esemény (folyamatos frissítés)*

```
{
  "type": "event",
  "command": "machine_status",
  "status": "success",
  "payload": {
    "machine_status": "running",
    "motion_mode": "G1",
    "position": {"X": 100.0, "Y": 50.0, "Z": -10.0}
  }
}
```

*Gép engedélyezés válasz*

```
{
  "type": "response",
  "command": "enable_machine",
  "status": "success"
}
```
 
*Ismeretlen parancs válasz*

```
{
  "type": "error",
  "command": "unknown_command",
  "status": "failed",
  "error": "Unknown command"
}
```

## Bejövő és kimenő üzenetek táblázatos formában



| Üzenet típus           | REST API Bejövő                                  | WebSocket bejövő                                                                  | RestAPI kimenő                                                                                                 | Websocket kimenő                                                                                                                |
|------------------------|--------------------------------------------------|-----------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| Mozgatás               | POST /motion/move {"x":100.0,"y":50.0,"x":-10.0} | {"type":"command", "command":"move", "parameters":{"x":100.0,"y":50.0,"x":-10.0}} | {"type":"response","command":"move_machine", "status":"in_progress", "payload":{"x":100.0,"y":50.0,"z":-10.0}} | Ugyan az mint a REST válasz                                                                                                     |
| Gép engedélyezés       | POST /motion/enable                              | {"type":"command", "command":"enable_machine"}                                    | {"type":"response","command":"enable_machine", "status":"success"}                                             | Ugyan az mint a REST válasz                                                                                                     |
| Gép állapot lekérdezés | GET /status                                      | (nincs külön kérés, mert folyamatos)                                              | {"type":"response","command":"get_machine", "status":"success", "payload":{"status":"running"}}                | { "type":"event", "command":"machine_status", "status":"success", "payload": {"machine_status":"running", "motion_mode":"G1"} } |
| Hibás parancs          | POST /motion/move {"x":"wrong_value"}            | {"type":"command", "command":"invalid_command"}                                   | {"type":"error","command":"move_machine", "status":"failed", "error":"Invalid axis position"}                  | {"type":"error", "command":"invalid_command", "status":"failed", "error":"Unknown command"}                                     |



