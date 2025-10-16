# gitops-lab
a GitOps pipeline

## Définition de GitOps selon ma comprihension
Tout l'état de mon infrastructure est décrit en code sous format de fichier (comme YAML, JSON, etc.) stocké dans Git, c'est le principe de IaC = Infrastructure as Code; les changements sont faits via des Pull Request, les agents (comme Jenkins, ArgoCD, etc.) observe le dépôt  et automatise la synchronisation entre Git et l'infrastructure: si un changement est détecté (comme Commit, Pull Request, etc.), il applique la nouvelle configuration automatiquement; on a ainsi la traçabilité complète des versions.


## Schéma textuel 
Développeur
--> (Commit / Push / etc.) --> Git (code de configuration)
--> Terraform
--> Docker (container, build image)
--> ArgoCD (observe le dépôt Git)
--> Kubernetes 
--> Prometheus / Grafana (surveillance)
--> application
