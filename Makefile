lint:
	ruff check .

test:
	docker exec -it backend pytest .

b-logs:
	docker logs -f backend

t-logs:
	docker logs -f telegram

rmi-backend:
	docker stop backend && docker rm backend && docker rmi cashchange-backend

rmi-telegram:
	docker stop telegram && docker rm telegram && docker rmi cashchange-telegram

Start:
	docker compose up -d

Stop:
	docker compose stop