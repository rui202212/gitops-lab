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

Appliquer les manifests Kubernetes

```bash
kubectl apply -f concrete-deployment.yaml
kubectl apply -f concrete-service.yaml
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

Hard reset minikube

```bash
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