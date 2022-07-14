build: 
	docker-compose build 

up: 
	docker-compose up -d 

down:
	docker-compose down 	

terminal: 
	docker-compose run extractor bash  
	