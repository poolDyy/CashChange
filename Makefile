lint:
	ruff check .

test:
	docker exec -it backend pytest .

logs:
	docker logs -f backend

rmi-backend:
	docker stop backend && docker rm backend && docker rmi cashchange-backend

Start:
	docker compose up -d

Stop:
	docker compose stop