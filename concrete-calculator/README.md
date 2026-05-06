# Calculateur BA

Cette application Flask sert à calculer des armatures et ses espacements à partir d'une section d'acier requis.

## Tester localement

Créer et activer un environnement virtuel

```powershell
python -m venv venv 
C:\Users\lurui\AppData\Local\Programs\Python\Python311\python.exe -m venv venv
#ici je dois forcer l'utilisation d'une version de python localement
.\venv\Scripts\Activate
```  

Installer les dépendances:
```bash  
pip install flask psycopg2-binary
```  

Générer automatiquement requirements.txt

```bash
pip freeze > requirements.txt
```

Lancer l'application

```bash
python app.py
```

Ecouter sur le port 5000 en ouvrant [http://localhost:5000](http://localhost:5000)


* Pour supprimer venv de force dans Powershell
```powershell  
Remove-Item -Recurse -Force venv
```  


## Docker

Construire l'image localement

```bash
docker build -t concrete-calculator:1.0 .
```

Lancer localement sur le port 5001 et supprimer automatiquement le container après l'arrêt (--rm) avec terminal interactif (-it)

```bash
docker run -it --rm -p 5001:5000 --name concrete-calculator concrete-calculator:1.0
```

Ecouter sur le port 5001 en ouvrant [http://localhost:5001](http://localhost:5001)

## Pousser l'image sur Docker Hub

```bash
docker tag concrete-calculator:1.0 matougong/concrete-calculator:1.0
docker push matougong/concrete-calculator:1.0
```

## Déployer sur Minikube

Démarrer minikube

```bash
minikube start
```  
Vérifier avec `kubectl get nodes` on doit avoir  
```shell
NAME       STATUS   ROLES           AGE    VERSION
minikube   Ready    control-plane   125m   v1.32.0
```  
Contexte kubectl `kubectl config current-context` on doit avoir  
```shell  
minikube
```  
si ce n'est pas le cas utliser `kubectl config use-context minikube` pour corriger.


En cas de ConfigMap: 
```bash  
kubectl create configmap db-init --from-file=db/init.sql
```  
Pour vérifier DB init (voir exécution SQL):
```bash  
kubectl logs <pod-postgres>
```  

Appliquer les manifests Kubernetes

```bash
kubectl apply -f concrete-deployment.yaml
kubectl apply -f concrete-service.yaml
# or
kubectl apply -f k8s/
```  

Pour vérifier

```bash
kubectl get all
kubectl get pods
kubectl get deploy
kubectl get svc
```

Pour ouvrir l'application automatiquement dans le navigateur par défaut

```bash
minikube service concrete-service
minikube service concrete-service --url   # pour afficher url à utiliser dans le navigateur
```

Pour avoir le IP du noeud

```bash
minikube ip
```

Quand on supprime un pod, Kubernetes relance un pod

```bash
kubectl delete pod <pod>
```

```bash
PS D:\formations\LearnIT\2025-26\20251120GitOps\concrete-calculator> kubectl get pods
NAME                                   READY   STATUS    RESTARTS   AGE
concrete-calculator-687b4fb598-6rzn9   1/1     Running   0          11m
concrete-calculator-687b4fb598-h824m   1/1     Running   0          11m
PS D:\formations\LearnIT\2025-26\20251120GitOps\concrete-calculator> kubectl delete pod concrete-calculator-687b4fb598-h824m
pod "concrete-calculator-687b4fb598-h824m" deleted
PS D:\formations\LearnIT\2025-26\20251120GitOps\concrete-calculator>
PS D:\formations\LearnIT\2025-26\20251120GitOps\concrete-calculator> kubectl get pods
NAME                                   READY   STATUS    RESTARTS   AGE
concrete-calculator-687b4fb598-6rzn9   1/1     Running   0          16m
concrete-calculator-687b4fb598-cxhdw   1/1     Running   0          59s
PS D:\formations\LearnIT\2025-26\20251120GitOps\concrete-calculator>
```

Ouvrir un shell dans un pod

```bash
kubectl exec -it <pod-name> -- /bin/sh
```

Pour supprimer les ressources k8s:
```bash
kubectl delete -f k8s/
```  
Pour forcer la supression de pod:
```bash  
kubectl delete pod <nom> --force --grace-period=0
```  

Pour tout nettoyer dans le namespace:
```bash  
kubectl delete all --all
```  

Hard reset minikube

```bash
minikube stop
minikube delete
```

# Ajouter une base de données

## ajout localement `db` avec docker  
Créer une base de données PostgreSQL pour stocker des les données liées aux calculs et/ou statistiques.

```bash
docker run -d \
  --name db \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=concrete \
  -p 5442:5432 \
  -v postgres_data:/var/lib/postgresql \
  postgres

docker run -d --name db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=concrete -p 5442:5432 -v postgres_data:/var/lib/postgresql postgres
```

Accéder au container:

```bash
docker exec -it db psql -U user -d concrete
```

Créer une table, par exemple table `diameters` pour stocker des diamètres d'acier d'armatures:

```SQL
CREATE TABLE diameters (
    name VARCHAR(10),
    diameter_mm INTEGER
);
INSERT INTO diameters VALUES
('HA6', 6),
('HA8', 8),
('HA10', 10),
('HA12', 12),
('HA14', 14),
('HA16', 16),
('HA20', 20);

-- tester avec suppresion d'une ligne puis rafraichir la page dans le navigateur
DELETE FROM diameters WHERE name = 'HA6';
```

## ajout docker-compose et lancer app + db  
```bash  
docker-compose up --build

docker-compose down # pour arrêter
docker-compose up --build

docker-compose down -v # pour forcer la suppression de volume
docker-compose up --build
```  

## construire l'image de Flask app et pousser sur docker hub
```bash
docker build -t concrete-calculator:2.0 .

docker tag concrete-calculator:2.0 matougong/concrete-calculator:2.0
docker push matougong/concrete-calculator:2.0
```

# Helm  

installer Helm sur Windows suivant la doc https://helm.sh/docs/intro/install/

| Variable        | Provient de  |
| --------------- | ------------ |
| `.Release.Name` | helm install |
| `.Values.xxx`   | values.yaml  |
| `.Chart.Name`   | Chart.yaml   |  

créer un premier chart: `helm create <chartname>`

personnaliser le chart: ouvrir le fichier concrete-chart/values.yaml et modifier par exemple :

```yaml
replicaCount: 2

image:
  repository: matougong/concrete-calculator
  tag: "2.0"
```
  
tester le rendu: `helm lint <chartname>` ou `helm template <chartname>`  
Cela affiche les manifestes Kubernetes (Deployment, Service, etc.)

## tester helm  
afficher les manifests générés:
```bash  
helm template concrete ./helm/concrete-chart
# debug
helm template concrete ./helm/concrete-chart --debug
```  
par exemple, affichage dans le terminal:
```shell    
> helm template concrete ./helm/concrete-chart --debug
level=DEBUG msg="Original chart version" version=""
level=DEBUG msg="Chart path" path=D:\formations\LearnIT\2025-26\20251120GitOps\gitops-lab\concrete-calculator\helm\concrete-chart
level=DEBUG msg="number of dependencies in the chart" chart=concrete-chart dependencies=0
---
# Source: concrete-chart/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: concrete
spec:
  type: NodePort
  selector:
    app: concrete
  ports:
    - port: 80
      targetPort: 5000
      nodePort: 30080
---
# Source: concrete-chart/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: concrete
spec:
  replicas: 2
  selector:
    matchLabels:
      app: concrete
  template:
    metadata:
      labels:
        app: concrete
    spec:
      containers:
      - name: concrete-calculator
        image: matougong/concrete-calculator:2.0
        ports:
        - containerPort: 5000
        env:
        - name: DB_HOST
          value: postgres
```  

## installer helm  
```bash  
helm install concrete ./helm/concrete-chart
```  

## modifier  
```bash  
helm upgrade concrete ./helm/concrete-chart
```  

## voir l'historique  
```bash  
helm history concrete
```  
on attend une sorte d'historique:
```shell  
> helm history concrete
REVISION        UPDATED                         STATUS          CHART                   APP VERSION    DESCRIPTION     
1               Tue May  5 18:32:40 2026        superseded      concrete-chart-0.1.0    1.0            Install complete
2               Tue May  5 18:54:00 2026        superseded      concrete-chart-0.1.1    1.0            Upgrade complete
3               Wed May  6 02:44:15 2026        deployed        concrete-chart-0.2.0    2.0            Upgrade complete
```  

## supprimer helm deployment
équivalent de `kubectl delete`  
```bash  
helm uninstall concrete
```  

# ArgoCD  
outil qui déploie Kubernetes automatiquement depuis Git.  

## Créer un namespace pour ArgoCD  
```bash
kubectl create namespace argocd
```

## Installer ArgoCD 
```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# installer une version fixe plus stable
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v2.9.3/manifests/install.yaml
```

## Vérifier les pods
```bash
kubectl get pods -n argocd
```

résultat:  
```sh
> kubectl get pods -n argocd
NAME                                                READY   STATUS    RESTARTS   AGE
argocd-application-controller-0                     1/1     Running   0          80s
argocd-applicationset-controller-5ff6f55574-hxft8   1/1     Running   0          81s
argocd-dex-server-c65b55f58-strp9                   1/1     Running   0          81s
argocd-notifications-controller-54948869bc-jjkfp    1/1     Running   0          80s
argocd-redis-5d849fc6db-sx6kh                       1/1     Running   0          80s
argocd-repo-server-7998764c69-zhrdr                 1/1     Running   0          80s
argocd-server-65ff77776b-sgdjv                      1/1     Running   0          80s
```

## accéder à l'interface web ArgoCD  
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```  
Exposer l'interface web ArgoCD avec port-forward et ouvrir [http://localhost:8080](http://localhost:8080)


## Récupérer le mot de passe admin
```bash
kubectl get secret argocd-initial-admin-secret -n argocd -o yaml
```
résultat:
```sh  
apiVersion: v1
data:
  password: eE03cnJvV3hVZTlkam9oRA==
kind: Secret
metadata:
  creationTimestamp: "2026-05-06T01:48:24Z"
  name: argocd-initial-admin-secret
  namespace: argocd
  resourceVersion: "11683"
  uid: 2089acfe-97e8-42de-ada8-b5a959448502
type: Opaque
```  
le password dessus est encodée en Base64. Pour avoir le mot de passe en clair, utiliser plutôt dans Git Bash / WSL
```bash
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 --decode
``` 


## Identifiant

```
username: admin
password: xM7rroWxUe9djohD
```

## Créer une application ArgoCD et la déployer

Repository URL : https://github.com/rui202212/gitops-lab.git
targetRevision : dev
Path           : concrete-calculator/helm/concrete-chart
Cluster        : https://kubernetes.default.svc
Namespace      : argocd


Déployer ArgoCD app.yaml
```bash  
kubectl apply -f argocd/app.yaml
```  

Vérifier avec `kubectl get pods` ou `kubectl get all`
ArgoCD gère:
- deployment  
- service  
- pods  
  
```sh  
> kubectl get all
NAME                            READY   STATUS    RESTARTS   AGE
pod/concrete-69488f9899-cjwx6   1/1     Running   0          11h
pod/concrete-69488f9899-j2b85   1/1     Running   0          10h
pod/postgres-6db5c8c8bd-c98zf   1/1     Running   0          170m

NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/concrete     NodePort    10.98.128.111   <none>        80:30080/TCP   11h
service/kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP        12h
service/postgres     ClusterIP   10.97.54.241    <none>        5432/TCP       170m

NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/concrete   2/2     2            2           11h
deployment.apps/postgres   1/1     1            1           170m

NAME                                  DESIRED   CURRENT   READY   AGE
replicaset.apps/concrete-69488f9899   2         2         2       11h
replicaset.apps/postgres-6db5c8c8bd   1         1         1       170m
```  

## Debug et logs  
```bash  
kubectl describe application concrete -n argocd

kubectl logs -n argocd deployment/argocd-application-controller

```  
