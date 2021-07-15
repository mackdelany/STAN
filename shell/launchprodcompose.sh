export APP_CONFIG_FILE=/stan/stan/api/config/production.py
export PYTHONUNBUFFERED=1
export STAN_NGINX_IMAGE=stan_nginx
export STAN_OCTOPUS_IMAGE=stan_octopus
docker-compose up
