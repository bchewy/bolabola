### Creating configmap for kong.yml
kubectl create configmap kong-config --from-file=kong.yml=../../kong/kong.yml

#### Updating configmap for kong.yml from current directory...
cd ../../kong/kong.yml
kubectl create configmap kong-config --from-file=kong.yml=kong.yml --dry-run=client -o yaml | kubectl apply -f 

### Restarting pods
kubectl rollout restart deployment kong