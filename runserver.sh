# new server based on Gunicorn
/home/forge/miniconda3/envs/perseus/bin/python /home/forge/miniconda3/envs/perseus/bin/gunicorn --reload -t 120 -w 1 -b :8003 web.wsgi