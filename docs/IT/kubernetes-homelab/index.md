---
tags:
  - architettura-software
---

# Kubernetes homelab

Questo progetto documenta la creazione di un ambiente Kubernetes completo per uso domestico, ideale per sperimentare e apprendere tecnologie cloud-native. Un homelab Kubernetes offre l'opportunità di acquisire competenze pratiche su orchestrazione di container, alta disponibilità e automazione dell'infrastruttura in un ambiente controllato.

## Kube for dummies

Dove si esplora l'architettura e il funzionamento di kubernetes.

[Kubernetes for Dummies](knowledge-base/kube-for-dummies.md)

## Setup dei nodi e del bastion
Dove si crea la configurazione iniziale dell'infrastruttura e si predispone il sistema di accesso sicuro.

[Host a Docker Registry](/knowledge-base/host-a-docker-registry.md)
[Talos linux](knowledge-base/talos-for-dummies.md)
[Setup a k8s bastion](/knowledge-base/kubernetes-bastion.md)
## Air-gapped Talos linux 
Dove si installa un sistema operativo specializzato in ambiente isolato dalla rete esterna.

[Air-gapped Talos Linux](/knowledge-base/air-gapped-talos-linux.md)
## Monitoraggio con Prometheus e Grafana
Dove si configurano strumenti per la visualizzazione e l'analisi delle metriche di sistema in tempo reale.

## Distributed block storage con Longhorn
Dove si installa un sistema di storage persistente e ridondante per le applicazioni stateful.

## Log Management
Dove si implementa un sistema centralizzato per la raccolta, l'analisi e la visualizzazione dei log distribuiti, garantendo tracciabilità e diagnosi rapida dei problemi in ambienti complessi.

## LiteLLM Proxy
Dove si costruisce un layer di astrazione per i modelli di linguaggio, ottimizzando costi, gestendo fallback automatici e garantendo alta disponibilità dei servizi AI nell'infrastruttura Kubernetes.

## Vault
Dove si implementa una gestione sicura dei segreti con rotazione automatica delle credenziali, protezione crittografica e integrazione profonda con l'identity management nativo di Kubernetes.

## Cert Manager con Let's Encrypt
Dove si automatizza completamente il ciclo di vita dei certificati SSL/TLS, eliminando la gestione manuale e garantendo comunicazioni sicure senza interruzioni di servizio.

## Osservabilità
Dove si costruisce un sistema integrato di monitoraggio che correla metriche, log e tracce distribuite per fornire visibilità completa dalla performance infrastrutturale fino all'esperienza utente finale.
