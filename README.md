# Bürgerbot

The automated F5 for desperate Berliners. Looks for available days to schedule a visit to a Bürgeramt in Berlin.

## Running with Docker:
Assuming docker and docker-composed are installed and running:
```
make run
```

## Alternative option:
### Installing
```
pip install -r requeriments.txt
```

### Running

```
./app.py
```

It will refresh the page every 10 seconds looking for any available day in the next 2 months.
