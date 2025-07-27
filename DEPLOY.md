# Deployment instructions

## Prerequisites
- Fresh Debian VPS
- Domain DNS pointing to VPS IP

## Setup

### Install packages
```bash
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv nginx git snapd
systemctl start snapd
```

### Clone repository
```bash
cd /opt
git clone https://github.com/alexkay/hilite.me.git
cd hilite.me
```

### Setup Python environment
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Set ownership
```bash
chown -R www-data:www-data /opt/hilite.me
```

### Create systemd service
```bash
cat > /etc/systemd/system/hilite.service << 'EOF'
[Unit]
Description=Hilite.me Flask app
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/hilite.me
Environment="PATH=/opt/hilite.me/env/bin"
ExecStart=/opt/hilite.me/env/bin/gunicorn -w 4 -b 127.0.0.1:5000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```

### Configure nginx
```bash
cat > /etc/nginx/sites-available/hilite << 'EOF'
include /opt/hilite.me/nginx.conf;
EOF

ln -s /etc/nginx/sites-available/hilite /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
```

### Start services
```bash
nginx -t && systemctl reload nginx
systemctl enable hilite && systemctl start hilite
```

### Install certbot
```bash
snap install --classic certbot
ln -s /snap/bin/certbot /usr/bin/certbot
```

### Create challenge directory
```bash
mkdir -p /var/www/html/.well-known/acme-challenge
```

### Get certificate
```bash
certbot certonly --webroot -w /var/www/html -d hilite.me -d www.hilite.me
```

### Reload nginx with SSL
```bash
systemctl reload nginx
```
