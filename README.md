# onvif-client
ONVIF client tool for communicate with camera

# Install DEV environment

```
> sudo apt update
> sudo apt install python3.11
> sudo apt install python3.11-venv
> python3.11 -m venv .dev-3.11
> source .dev-3.11/bin/activate
> python -m pip install -r setup/requirements_dev.txt
```

# Running API in local

```
> uvicorn src.api:app
```

If you want to reload the server when you change the code, use `--reload` option.

# Running API in EC2 instance

```
uvicorn src.api:app --host 0.0.0.0
```
# Examples

# Use direct onvif connection to the camera and get the device information

```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/device/device_information' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "host": "1.2.3.4",
  "port": 80,
  "user": "user",
  "password": "password"
}'
```

# Use onvif connection to the camera via bosch security system and get audio outputs

```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/media/get_audio_outputs' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "bosch_security_url": "https://cbs.com/rest/vx/v1/devices/bvip2:cb80a4b7569d/connection"
}'
```

