# amazon-chronos-forecasting-test
amazon-chronos-forecasting-test

## build
docker build -t chronos-forecast-api .

## run docker
docker run -p 8000:8000 chronos-forecast-api

## invoke to forecast
curl -X POST "http://localhost:8000/forecast" \
     -H "Content-Type: application/json" \
     -d '{"data": [379.28, 410.44, 411.05, 394.36, 394.94, 394.74, 403.31, 396.36, 428.22, 413.82, 426.50, 424.07, 415.11], "prediction_length": 3}'
