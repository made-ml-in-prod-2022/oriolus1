
Kubernetes поднят с помощью minikube


Проверить статус:

kubectl cluster-info


Поднять под:

kubectl apply -f file_name.yaml


Посмотреть поды:

kubectl get pods

или 

kubectl get --watch pods


Удалить поды: 

kubectl delete --all pods 


Удалить реплику: 

kubectl delete ReplicaSet/online-inference