# home-assistant-config
## Installation för Docker
Se [instruktioner på home-assistant.io](https://www.home-assistant.io/docs/installation/docker/).

Checka ut konfigurationen:
```
git clone https://github.com/morberg/home-assistant-config.git home-assistant
cd home-assistant
cp ~/.homeassistant/known_devices.yaml .
```

Skapa en `secrets.yaml` med följande innehåll (eller `cp ~/.homeassistant/secrets.yaml .`):
```
api-password: xxxxx
plex-user: xxxxx
plex-password: xxxxx
unifi-user: xxxxx
unifi-password: xxxxx
apple-tv-login-id: xxxxx
```
Uppgradera docker
```
docker pull homeassistant/home-assistant
docker stop home-assistant
docker rm home-assistant
```
Starta docker:
```
docker run -d --name="home-assistant" -v /Users/niklas/docker/home-assistant:/config -e "TZ=Europe/Stockholm" -p 8123:8123 homeassistant/home-assistant
```

Kolla loggar:
```
docker logs -f --tail 20 home-assistant

Discovery fungerar inte på macOS med Docker. Har lagt till tradfri manuellt i `configuration.yaml`.
