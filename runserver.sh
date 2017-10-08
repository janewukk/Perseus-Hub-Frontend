# kill existing uwsgi processes
sudo kill -9 $(ps aux | grep -e uwsgi | awk '{ print $2 }')

# reload server
uwsgi --module web.wsgi --master --socket --enable-threads /var/www/perseus/perseus.sock --chmod-socket=666 
