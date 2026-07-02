# Deploying the gxlabs Baby Buddy fork

This fork adds `image` fields to Feeding, DiaperChange, Sleep, Pumping, and
TummyTime so photos can be attached to any event. It's designed to run in Docker
alongside (or in place of) the Home Assistant Baby Buddy add-on.

## One-time setup

1. **Copy this repo onto the host that will run the container** (your HA host,
   a Mac, a NAS — anywhere with Docker).
2. Create `data/`:
   ```bash
   mkdir -p data/media
   ```
3. **Cut over from the HA add-on** (recommended path — user picked this):
   - Stop the Baby Buddy add-on in Home Assistant.
   - Copy the add-on's SQLite database and any uploaded media into `./data/`:
     ```bash
     # From the HA host, wherever the add-on stores its data. On the standard
     # add-on this is typically under:
     #   /config/addons_config/<slug>/babybuddy.sqlite3
     # or accessible via the Samba share as \\hassio\config\...
     scp root@homeassistant:/path/to/babybuddy.sqlite3 ./data/db.sqlite3
     # If the add-on has uploaded any Notes images, grab those too:
     scp -r root@homeassistant:/path/to/babybuddy/media ./data/media
     ```
4. Generate a Django secret and put it in a `.env` next to the compose file:
   ```bash
   echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')" > .env
   ```

## Run

```bash
docker compose up -d --build
```

Migrations (including `0037_event_images`) run automatically on container start.
The fork listens on **`:8002`** so it doesn't collide with the add-on's `:8001`.

Test:
```bash
curl -H "Accept: application/json" http://<host>:8002/api/children/
```

## Point the iOS app at it

In Settings → Server, change the URL from `http://homeassistant.local:8001` to
`http://<host>:8002` and re-enter (or reuse) the API token from your Baby Buddy
user settings.

## What to expect

- The **web UI** on `:8002` is the same as the add-on's — you can still browse
  and edit events there.
- New in this fork: `POST /api/feedings/` (etc.) accepts a `multipart/form-data`
  request with an `image` file; `GET` returns the image URL in the JSON.
- The existing HA add-on can be safely deleted once the fork is working, since
  everything moved to the same DB file.
