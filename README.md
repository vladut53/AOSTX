Start the container:
docker build -t amf-simulator .
docker network create amf-net
docker run -d  --name amf --network amf-net -p 83:83 amf-simulator


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
docker run --rm   --network amf-net   -v $(pwd):/etc/newman   postman/newman run /etc/newman/messages.json
newman

AMF Registration Test

→ Register Valid User 1
  POST http://amf:83/amf/register [201 CREATED, 220B, 94ms]

→ Register Valid User 2
  POST http://amf:83/amf/register [201 CREATED, 220B, 12ms]

→ Register Invalid IMSI
  POST http://amf:83/amf/register [403 FORBIDDEN, 213B, 8ms]

→ Register Duplicate User
  POST http://amf:83/amf/register [400 BAD REQUEST, 211B, 9ms]

┌─────────────────────────┬──────────────────┬──────────────────┐
│                         │         executed │           failed │
├─────────────────────────┼──────────────────┼──────────────────┤
│              iterations │                1 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│                requests │                4 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│            test-scripts │                0 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│      prerequest-scripts │                0 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│              assertions │                0 │                0 │
├─────────────────────────┴──────────────────┴──────────────────┤
│ total run duration: 186ms                                     │
├───────────────────────────────────────────────────────────────┤
│ total data received: 174B (approx)                            │
├───────────────────────────────────────────────────────────────┤
│ average response time: 30ms [min: 8ms, max: 94ms, s.d.: 36ms] │
└───────────────────────────────────────────────────────────────┘
