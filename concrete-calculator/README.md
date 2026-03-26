# Calculateur BA

Cette application Flask sert à calculer des armatures et ses espacements à partir d'une section d'acier requis.

## Tester localement

Créer et activer un environnement virtuel

```powershell
python -m venv venv
.\venv\Scripts\Activate
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

## ArgoCD

Créer un namespace pour ArgoCD

```bash
kubectl create namespace argocd
```

Installer ArgoCD

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Vérifier les pods

```bash
kubectl get pods -n argocd
```

résultat:

```sh
PS D:\formations\LearnIT\2025-26\20251120GitOps\gitops-lab> kubectl get pods -n argocd
NAME                                               READY   STATUS    RESTARTS       AGE
argocd-application-controller-0                    1/1     Running   0              4m2s
argocd-applicationset-controller-fc5545556-cknsw   1/1     Running   0              4m3s
argocd-dex-server-f59c65cff-rffj2                  1/1     Running   1 (3m1s ago)   4m3s
argocd-notifications-controller-59f6949d7-rz6mp    1/1     Running   0              4m3s
argocd-redis-75c946f559-ccbrb                      1/1     Running   0              4m3s
argocd-repo-server-6959c47c44-hwv4x                1/1     Running   0              4m2s
argocd-server-65544f4864-zhzc4                     1/1     Running   0              4m2s
```

Exposer l'interface web ArgoCD avec port-forward et ouvrir [http://localhost:8080](http://localhost:8080)

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Récupérer le mot de passe admin

```bash
kubectl get secret argocd-initial-admin-secret -n argocd -o yaml
```

Identifiant

```
username: admin
password brut: R1BTalRTZHhpckM0SlFyQQ==
password décodé de base64: GPSjTSdxirC4JQrA
```

Créer une application ArgoCD dans son interface

```
Repository URL : https://github.com/rui202212/gitops-lab.git
Revision       : main
Path           : concrete-calculator/k8s
Cluster        : https://kubernetes.default.svc
Namespace      : concrete
```
