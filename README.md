# onvif-client
ONVIF client tool for communicate with camera

# Install DEV environment

```
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