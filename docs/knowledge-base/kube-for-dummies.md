# Kubernetes for Dummies

## Cos'è Kubernetes

Kubernetes è un framework open source per l'orchestrazione di container, originariamente sviluppato da Google. Gestisce container Docker (o di altre tecnologie) e aiuta a gestire applicazioni composte da centinaia o migliaia di container in diversi ambienti: macchine fisiche, virtuali, cloud o ambienti di deployment ibridi.

## Problemi Risolti da Kubernetes

### Il Contesto: Microservizi e Container
- L'aumento dei microservizi ha portato a un maggiore utilizzo dei container
- I container offrono l'host perfetto per piccole applicazioni indipendenti
- Le applicazioni moderne sono composte da centinaia o migliaia di container
- Gestire manualmente tali volumi di container è complesso e spesso impossibile

### Funzionalità Garantite dall'Orchestrazione

#### **Alta Disponibilità (High Availability)**
- **Caratteristiche**: L'applicazione non ha downtime
- **Vantaggi**: Sempre accessibile agli utenti
- **Requisiti**: Meccanismi di failover automatici

#### **Scalabilità**
- **Caratteristiche**: Alte performance e tempi di risposta rapidi
- **Vantaggi**: Carichi velocemente e offre alta responsività
- **Requisiti**: Distribuzione intelligente del carico

#### **Disaster Recovery**
- **Caratteristiche**: Ripristino automatico in caso di problemi infrastrutturali
- **Vantaggi**: Nessuna perdita di dati anche in caso di guasti
- **Requisiti**: Backup e restore automatizzati

## Architettura di Base

### Struttura del Cluster
Un cluster Kubernetes è composto da:
- **Almeno un Master Node**
- **Multipli Worker Node** connessi al master

### Worker Nodes
- Ogni node ha un processo **Kubelet** in esecuzione
- Kubelet permette la comunicazione tra i nodi del cluster
- Eseguono i container Docker delle applicazioni
- Qui avviene il lavoro effettivo (esecuzione delle applicazioni)

### Master Node
Il Master Node esegue diversi processi critici:

#### **API Server**
- **Funzione**: Entry point del cluster Kubernetes
- **Caratteristiche**: È un container che gestisce tutte le comunicazioni
- **Vantaggi**: Punto unico di accesso per UI, API, CLI (kubectl)

#### **Controller Manager**
- **Funzione**: Supervisiona lo stato del cluster
- **Caratteristiche**: Monitora se qualcosa necessita riparazione
- **Vantaggi**: Riavvio automatico di container morti

#### **Scheduler**
- **Funzione**: Pianifica i container sui diversi nodi
- **Caratteristiche**: Processo intelligente che considera workload e risorse
- **Vantaggi**: Distribuzione ottimale basata sulle risorse disponibili

#### **etcd**
- **Funzione**: Key-value storage per lo stato del cluster
- **Caratteristiche**: Contiene tutti i dati di configurazione e stato
- **Vantaggi**: Backup e restore del cluster tramite snapshot

#### **Virtual Network**
- **Funzione**: Connette tutti i nodi del cluster
- **Caratteristiche**: Trasforma i nodi in un'unica macchina potente
- **Vantaggi**: Somma delle risorse di tutti i nodi individuali

### Considerazioni di Produzione
- **Worker Nodes**: Solitamente più grandi, eseguono centinaia di container
- **Master Nodes**: Meno risorse necessarie ma critici per l'accesso
- **Backup Master**: In produzione si usano almeno 2 master per alta disponibilità

## Concetti Base di Kubernetes

### Pod
#### **Definizione**
- Unità più piccola configurabile dall'utente
- Wrapper di un container
- Multipli pod per worker node

#### **Caratteristiche**
- Di solito un pod per applicazione
- Può contenere multipli container (per helper containers)
- Ogni pod ha il proprio indirizzo IP
- I pod sono componenti effimeri (muoiono frequentemente)

#### **Vantaggi**
- Astrazione sui container
- Gestione automatica dei container interni
- Riavvio automatico dei container morti

#### **Svantaggi**
- IP dinamici (cambiano a ogni riavvio)
- Necessitano di servizi per la comunicazione stabile

### Service
#### **Definizione**
- Componente che fornisce un IP permanente ai pod
- Si posiziona davanti ai pod per la comunicazione

#### **Caratteristiche**
- Ciclo di vita indipendente dai pod
- IP permanente per la comunicazione tra pod
- Funziona anche come load balancer

#### **Vantaggi**
- Risolve il problema degli IP dinamici
- Distribuzione del carico automatica
- Comunicazione stabile tra componenti

## Configurazione e Deploy

### Processo di Configurazione
Tutta la configurazione passa attraverso:
- **Master Node** tramite l'**API Server**
- **Client Kubernetes**: UI (dashboard), API (script), CLI (kubectl)
- **Formato**: YAML o JSON

### Esempio di Configurazione
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-image
        ports:
        - containerPort: 8080
        env:
        - name: ENV_VAR
          value: "value"
```

### Caratteristiche della Configurazione
- **Formato Dichiarativo**: Si dichiara lo stato desiderato
- **Auto-healing**: Kubernetes mantiene automaticamente lo stato desiderato
- **Controller Manager**: Monitora e corregge discrepanze tra stato attuale e desiderato

## Conclusione

Kubernetes risolve i problemi complessi della gestione di applicazioni containerizzate su larga scala, fornendo:

1. **Orchestrazione automatica** di container
2. **Alta disponibilità** e disaster recovery
3. **Scalabilità** intelligente
4. **Gestione semplificata** tramite configurazioni dichiarative
5. **Astrazione** che semplifica la gestione dei container

La sua architettura master-worker e i concetti di pod e service forniscono una base solida per il deploy e la gestione di applicazioni moderne in ambienti di produzione.
