# Big Mouth Billy

The DHWG avatar.

## Installation

Native dependencies:

```
sudo apt-get install libsdl-mixer1.2
```

Python dependencies:

```
pip3 install -r requirements.txt
```

Install as service:

```
sudo cp billy.service /etc/systemd/system/
sudo systemctl enable billy.service
sudo systemctl start billy.service
```
