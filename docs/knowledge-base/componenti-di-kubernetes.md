# I Componenti Fondamentali di Kubernetes

Kubernetes è una piattaforma complessa con numerosi componenti, ma nella pratica quotidiana come DevOps engineer o sviluppatore software, ci si trova a lavorare principalmente con una manciata di elementi essenziali. Comprendere questi componenti di base permette di iniziare immediatamente a utilizzare Kubernetes per distribuire applicazioni in modo efficace e scalabile.

## Pod

Il pod rappresenta l'unità più piccola e fondamentale di Kubernetes. Non si tratta semplicemente di un container, ma piuttosto di un'astrazione che crea un livello di running environment sopra il container stesso. Questa architettura permette a Kubernetes di astrarre dalla specifica tecnologia di containerizzazione utilizzata, che sia Docker o altri runtime, offrendo così la flessibilità di cambiare tecnologia senza dover modificare l'approccio di lavoro.

Un pod normalmente ospita un singolo container applicativo, anche se tecnicamente può contenerne di più quando sono presenti helper container o servizi ausiliari che devono funzionare strettamente accoppiati all'applicazione principale. Questa unità logica semplifica la gestione delle applicazioni mantenendo al contempo la separazione delle responsabilità.

La caratteristica più importante dei pod è la loro natura effimera. Possono morire facilmente a causa di crash dell'applicazione, esaurimento delle risorse del nodo, o altre problematiche infrastrutturali. Quando un pod muore, ne viene automaticamente creato uno nuovo al suo posto, ma questo comporta anche l'assegnazione di un nuovo indirizzo IP, creando potenziali problemi di comunicazione.

## Service

Per risolvere il problema dell'instabilità degli indirizzi IP dei pod, Kubernetes introduce il concetto di service. Un service fornisce un indirizzo IP statico e permanente che può essere associato ai pod, garantendo che la comunicazione tra i diversi componenti dell'applicazione rimanga stabile nel tempo.

La bellezza dei service risiede nel fatto che il loro ciclo di vita è completamente indipendente da quello dei pod. Anche quando un pod viene ricreato con un nuovo indirizzo IP, il service mantiene la sua identità e continua a funzionare come punto di accesso stabile. Questo elimina la necessità di aggiornare costantemente gli endpoint di comunicazione quando i pod vengono ricreati.

I service si dividono principalmente in due tipologie. I service esterni permettono l'accesso all'applicazione dall'esterno del cluster, rendendola disponibile attraverso browser o client esterni. I service interni, invece, sono progettati per la comunicazione interna tra i componenti del cluster, come ad esempio tra un'applicazione e il suo database, mantenendo questi servizi protetti da accessi esterni non autorizzati.

Tuttavia, l'URL di un service esterno tipicamente include l'indirizzo IP del nodo e il numero di porta, risultando poco pratico per un uso in produzione. Per questo motivo entra in gioco un altro componente essenziale.

## Ingress

L'ingress rappresenta il punto di ingresso intelligente per il traffico esterno verso il cluster Kubernetes. Invece di esporre direttamente i service con URL complessi, l'ingress permette di configurare nomi di dominio leggibili e protocolli sicuri per accedere alle applicazioni.

Quando una richiesta arriva dall'esterno, passa prima attraverso l'ingress che si occupa di instradare il traffico verso il service appropriato. Questo meccanismo consente di avere URL puliti e professionali, utilizzando protocolli HTTPS e nomi di dominio personalizzati, rendendo l'applicazione accessibile con modalità standard e sicure.

L'ingress agisce essenzialmente come un reverse proxy intelligente, gestendo le regole di routing, la terminazione SSL, e altre funzionalità avanzate di gestione del traffico che sarebbero complesse da implementare direttamente nei service.

## ConfigMap e Secret

La gestione della configurazione rappresenta un aspetto critico in qualsiasi applicazione distribuita. Tradizionalmente, informazioni come URL di database o altri endpoint vengono embedded nel codice dell'applicazione o nei file di proprietà inclusi nell'immagine del container. Questo approccio richiede la ricostruzione dell'immagine ogni volta che si modifica una configurazione, rendendo il processo di deployment laborioso per cambiamenti anche minori.

I ConfigMap risolvono questo problema fornendo un meccanismo per esternalizzare la configurazione dell'applicazione. Un ConfigMap contiene dati di configurazione come URL di database, stringhe di connessione, o altre impostazioni che l'applicazione deve conoscere. Connettendo un ConfigMap al pod, l'applicazione può accedere a questi dati senza che siano hardcoded nell'immagine, permettendo modifiche rapide della configurazione senza rebuild.

Per informazioni sensibili come password, certificati, o chiavi di accesso, Kubernetes offre i Secret. Funzionalmente simili ai ConfigMap, i Secret sono specificamente progettati per gestire dati confidenziali. Le informazioni vengono stored in formato base64, offrendo un livello base di offuscamento, e possono essere gestite con politiche di accesso più restrittive.

Sia i ConfigMap che i Secret possono essere utilizzati all'interno dei pod come variabili d'ambiente o montati come file, offrendo flessibilità nella modalità di consumo da parte dell'applicazione.

## Volume

La natura effimera dei pod crea una sfida significativa per la persistenza dei dati. Quando un pod con un database viene ricreato, tutti i dati contenuti al suo interno andrebbero persi, causando problemi evidenti per qualsiasi applicazione che necessita di mantenere lo stato.

I volume di Kubernetes risolvono questo problema fornendo un meccanismo per attach storage persistente ai pod. Lo storage può essere locale, residente sullo stesso nodo fisico dove gira il pod, oppure remoto, localizzato su sistemi esterni al cluster come cloud storage o storage on-premise.

È fondamentale comprendere che Kubernetes non gestisce direttamente la persistenza dei dati. Il cluster fornisce l'interfaccia per connettere storage esterno, ma la responsabilità del backup, della replicazione, e della gestione della durabilità dei dati rimane all'amministratore del sistema. Questo approccio mantiene Kubernetes focalizzato sull'orchestrazione dei container piuttosto che sulla gestione dei dati.

## Deployment

Affidarsi a un singolo pod per servire un'applicazione crea un single point of failure inaccettabile per ambienti di produzione. Se il pod muore, gli utenti non possono più accedere all'applicazione, causando downtime.

I Deployment rappresentano la soluzione a questo problema, fornendo un blueprint per creare e gestire multiple repliche di un pod. Invece di creare pod individuali, si definisce un Deployment specificando quante repliche dell'applicazione si desidera eseguire simultaneamente.

Il Deployment si occupa automaticamente di mantenere il numero desiderato di repliche attive. Se una replica muore, il Deployment ne crea immediatamente una nuova. Il service associato funziona anche come load balancer, distribuendo il traffico tra le repliche disponibili e reindirizzando automaticamente le richieste se una replica diventa non disponibile.

Questa architettura permette di ottenere alta disponibilità e di scalare facilmente l'applicazione aumentando o diminuendo il numero di repliche secondo necessità. Nella pratica, si lavora quasi sempre con Deployment piuttosto che con pod individuali, poiché offrono maggiore controllo e resilienza.

## StatefulSet

Mentre i Deployment funzionano perfettamente per applicazioni stateless, le applicazioni che mantengono stato, come i database, richiedono un approccio diverso. Il problema principale risiede nella gestione dell'accesso concorrente ai dati persistenti.

Se si utilizzassero semplici Deployment per replicare un database, ogni replica dovrebbe accedere allo stesso storage condiviso, creando potenziali problemi di consistenza dei dati. È necessario un meccanismo che coordini quali repliche possono scrivere e quali possono leggere in un determinato momento.

Gli StatefulSet sono specificamente progettati per questo scenario. Oltre a fornire capacità di replicazione simili ai Deployment, gestiscono la sincronizzazione degli accessi ai dati, garantendo che le operazioni di lettura e scrittura avvengano in modo ordinato e consistente.

Tuttavia, la gestione di database attraverso StatefulSet può risultare complessa e laboriosa. Per questo motivo, molte organizzazioni preferiscono mantenere i database fuori dal cluster Kubernetes, utilizzando servizi di database gestiti o infrastrutture dedicate, mentre eseguono nel cluster solo le applicazioni stateless che si connettono ai database esterni.

