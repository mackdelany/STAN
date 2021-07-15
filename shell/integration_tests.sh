## Note this must be run from dir root

echo "Starting containers..."
export APP_CONFIG_FILE=/stan/stan/api/config/production.py
export PYTHONUNBUFFERED=1
export STAN_NGINX_IMAGE=stan_nginx
export STAN_OCTOPUS_IMAGE=stan_octopus
docker-compose up -d

echo "Sleeping for 10s to let the containers get groovy..."
sleep 10s

echo "Running tests...."
./shell/api_test.sh -f ./tests/integration_tests/integration_test.json test all

echo "Stopping containers..."
docker-compose stop
