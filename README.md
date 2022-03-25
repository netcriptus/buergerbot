# Bürgerbot

The automated F5 for desperate Berliners. Looks for available days to schedule a visit to a Bürgeramt in Berlin.

## Running with Docker:
Assuming docker and docker-composed are installed and running:
```
make run
```

Then open a browser on http://0.0.0.0:5000

## Alternative option:
### Installing

MacOS:
```
CFLAGS="-I/usr/local/opt/openssl/include" LDFLAGS="-L/usr/local/opt/openssl/lib" UWSGI_PROFILE_OVERRIDE=ssl=true pip install uwsgi --no-binary :all:
pip install -r requeriments.txt
```

Linux (Debian based):
```
apt-get install -y libssl-dev
pip install -r requeriments.txt
```

### Running

```
uwsgi --ini uwsgi.ini
```

It will refresh the page every 10 seconds looking for any available day in the next 2 months.
