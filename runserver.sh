# kill existing uwsgi processes
sudo kill -9 $(ps aux | grep -e uwsgi | awk '{ print $2 }')

# reload server
uwsgi --module=web.wsgi  --processes=3 --http=127.0.0.1:8003 --enable-threads --reload-mercy=1 --worker-reload-mercy=1