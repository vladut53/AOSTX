Start the container:
docker build -t amf-simulator .
docker run -d -p 83:83 --name amf amf-simulator


Healthcheck:
curl http://localhost:83/healthcheck


Test Registration – Valid IMSI 
curl -X POST http://localhost:83/amf/register \
-H "Content-Type: application/json" \
-d '{"user_id": "ue123", "name": "Alice", "site_code": "NY01", "imsi": "123456789012345"}'


Test Registration – Invalid IMSI
curl -X POST http://localhost:83/amf/register \
-H "Content-Type: application/json" \
-d '{"user_id": "ue124", "name": "Bob", "site_code": "LA01", "imsi": "888888888888888"}'


Register Duplicate User
curl -X POST http://localhost:83/amf/register \
-H "Content-Type: application/json" \
-d '{"user_id": "ue123", "name": "Alice Again", "site_code": "NY01", "imsi": "123456789012345"}'


All registered users:
curl http://localhost:83/amf/users


View SQLite DB Content
docker exec -it amf sqlite3 amf_users.db
SELECT * FROM users;


Newmann Test:
docker run --rm -v $(pwd):/etc/newman postman/newman \
  run /etc/newman/amf_test_collection.json

