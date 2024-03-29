build-client-image:
	docker build -f client/Dockerfile -t nimble-hackathon-client --no-cache .
build-server-image:
	docker build -f server/Dockerfile -t nimble-hackathon-server --no-cache .
docker-run-client:
	docker run -dp 127.0.0.1:8080:8080 nimble-hackathon-client
docker-run-server:
	docker run -dp 127.0.0.1:8080:8080 nimble-hackathon-server
k8s-deploy-client:
	kubectl apply -f client/deployment.yaml
k8s-deploy-server:
	kubectl apply -f server/deployment.yaml