# Redis for Dummies

Redis, acronimo di Remote Dictionary Server, rappresenta molto più di un semplice sistema di cache. Si tratta di un database in-memory completamente funzionale che può servire come database primario per applicazioni complesse, capace di gestire e persistere multiple tipologie di dati. Questa versatilità lo rende particolarmente adatto alle moderne architetture di microservizi che richiedono flessibilità e prestazioni elevate.

## Perché Redis Risolve la Complessità dei Sistemi Multi-Database

Immaginiamo un'applicazione di social media complessa con milioni di utenti. Tradizionalmente, potreste trovarvi a gestire un database relazionale come MySQL per i dati strutturati, Elasticsearch per ricerche veloci e filtri avanzati, un database a grafo per rappresentare le connessioni tra utenti, un database documentale per i contenuti multimediali condivisi, e infine un servizio di cache per migliorare le prestazioni generali dell'applicazione.

Questa configurazione comporta sfide significative. Ogni servizio dati richiede competenze specifiche per il deployment, l'esecuzione e la manutenzione. Ciascuno scala diversamente e ha requisiti infrastrutturali unici, complicando la gestione complessiva. Dal punto di vista economico, utilizzare servizi gestiti dai cloud provider può risultare costoso poiché ogni servizio viene fatturato separatamente.

Sul fronte dello sviluppo, il codice dell'applicazione diventa complesso dovendo interfacciarsi con molteplici servizi dati, ognuno con il proprio connettore e logica specifica. Questo rende anche il testing particolarmente impegnativo. Inoltre, ogni connessione tra servizi introduce latenza aggiuntiva, anche se ogni singolo servizio fosse veloce di per sé.

Redis come database multi-modale risolve elegantemente queste problematiche. Mantenendo un singolo servizio dati, l'applicazione necessita di una sola interfaccia programmatica, riducendo drasticamente la latenza eliminando i vari hop di rete interni e semplificando l'architettura complessiva.

## L'Architettura Modulare di Redis

Il funzionamento di Redis si basa su un core centrale che è un key-value store già capace di gestire multiple tipologie di dati. Questo core può essere esteso attraverso moduli specializzati per diverse necessità applicative. Redis Search offre funzionalità di ricerca simili a Elasticsearch, mentre Redis Graph fornisce capacità di storage per dati a grafo, e così via.

L'aspetto brillante di questa architettura è la sua natura modulare. Le diverse funzionalità database non sono integrate rigidamente in un unico sistema monolitico, ma possono essere selezionate e aggiunte secondo le specifiche esigenze dell'applicazione. Quando Redis viene utilizzato come database primario, la funzionalità di cache è disponibile automaticamente, eliminando la necessità di implementare logiche separate per gestire, popolare e invalidare la cache.

Come database in-memory, Redis offre prestazioni eccezionali che si riflettono non solo sulla velocità dell'applicazione, ma anche sull'esecuzione dei test. Non richiedendo schema predefiniti come altri database, Redis non necessita di tempo per inizializzare e costruire strutture complesse prima dell'esecuzione dei test. È possibile iniziare con un database Redis vuoto e generare i dati necessari al volo, accelerando significativamente i cicli di sviluppo.

## Persistenza e Durabilità dei Dati

La natura in-memory di Redis solleva naturalmente domande sulla persistenza dei dati. Se il processo Redis o il server su cui opera dovesse fallire, tutti i dati in memoria andrebbero persi. Redis affronta questa sfida attraverso molteplici meccanismi di persistenza e strategie di backup.

La replicazione rappresenta il metodo più semplice per garantire backup dei dati. Se l'istanza master di Redis dovesse cadere, le repliche continuerebbero a funzionare mantenendo tutti i dati. Tuttavia, se tutte le istanze Redis dovessero spegnersi simultaneamente, i dati andrebbero comunque persi.

Per una vera persistenza, Redis implementa diversi meccanismi. Gli snapshot possono essere configurati in base a tempo o numero di richieste, salvando periodicamente lo stato dei dati su disco. Questo metodo comporta la potenziale perdita degli ultimi minuti di dati, tipicamente configurati per snapshot ogni cinque minuti o un'ora secondo le necessità.

Come alternativa, Redis utilizza l'AOF (Append Only File), dove ogni modifica viene salvata continuamente su disco. Al riavvio di Redis o dopo un'interruzione, il sistema rilegge i log AOF per ricostruire lo stato completo. L'AOF offre maggiore durabilità ma può risultare più lento rispetto agli snapshot.

È possibile combinare entrambi gli approcci, utilizzando l'AOF per la persistenza continua e snapshot regolari per salvare stati intermedi facilitando il recovery. Anche se l'intera infrastruttura sottostante dovesse fallire, tutti i dati rimangono al sicuro e un nuovo database Redis può essere ricreato con tutti i dati intatti.

## Ottimizzazione dei Costi con Redis on Flash

L'archiviazione in memoria può risultare costosa, richiedendo potenzialmente più server rispetto a database che memorizzano dati su disco, dato che la memoria ha limitazioni di dimensione. Esiste quindi un trade-off tra costi e prestazioni.

Redis Enterprise offre una soluzione chiamata Redis on Flash che ottimizza questo aspetto. Il concetto è elegante nella sua semplicità: estende la RAM al flash drive o SSD, dove i valori utilizzati frequentemente rimangono in RAM mentre quelli utilizzati raramente vengono spostati su SSD. Per Redis, questo appare semplicemente come RAM aggiuntiva sul server.

Questa strategia permette a Redis di utilizzare meglio le risorse dell'infrastruttura sottostante, sfruttando sia RAM che SSD per l'archiviazione dati, aumentando la capacità di storage per ogni server e riducendo conseguentemente i costi infrastrutturali.

## Scaling e Clustering di Redis

Quando un'istanza Redis raggiunge i limiti di memoria o diventa un bottleneck per le richieste, diventa necessario aumentare la capacità e le dimensioni della memoria del database. Redis supporta il clustering, permettendo di avere un'istanza primaria o master per letture e scritture, con multiple repliche per le sole letture.

Questo approccio scala Redis per gestire più richieste e aumenta l'alta disponibilità del database. Se il master fallisce, una delle repliche può assumere il controllo permettendo al database di continuare a funzionare senza interruzioni.

Le repliche mantengono copie dei dati dell'istanza primaria, quindi più repliche significano maggiore spazio memoria necessario. Distribuire queste repliche tra molteplici nodi o server previene il rischio di perdita completa dei dati se un singolo server dovesse fallire.

Quando il dataset cresce troppo per essere contenuto nella memoria di un singolo server, o quando il master deve gestire troppe scritture, entra in gioco il concetto di sharding. Lo sharding divide il dataset completo in chunk più piccoli o subset di dati, dove ogni shard è responsabile del proprio subset.

Invece di avere un'istanza master che gestisce tutte le scritture dell'intero dataset, è possibile suddividerlo in quattro shard, ognuno responsabile per letture e scritture di un subset dei dati. Ogni shard richiede meno capacità di memoria contenendo solo una frazione dei dati totali, permettendo di distribuire ed eseguire gli shard su nodi più piccoli e scalare il cluster orizzontalmente.

Con la crescita del dataset e l'aumento delle necessità di risorse, è possibile effettuare resharding del database Redis, suddividendo ulteriormente i dati in chunk ancora più piccoli e creando più shard.

## Geo-Replicazione e Active-Active Deployment

Per applicazioni che necessitano di alta disponibilità e prestazioni elevate attraverso multiple localizzazioni geografiche, Redis Enterprise offre funzionalità avanzate. Consideriamo uno scenario dove abbiamo un cluster Redis replicato e shardato in una regione, ad esempio nel data center di Londra, ma con utenti geograficamente distribuiti in tutto il mondo.

L'obiettivo è distribuire globalmente applicazione e servizi dati vicino agli utenti per migliorare le prestazioni, e garantire uno switch-over immediato ad un altro data center se quello principale dovesse cadere. Questo richiede repliche dell'intero cluster Redis in data center di multiple regioni geografiche.

Ogni cluster agirebbe come istanza Redis locale nella propria regione, con dati sincronizzati tra questi cluster geograficamente distribuiti. Questa configurazione, chiamata Active-Active deployment in Redis Enterprise, fornisce bassa latenza per gli utenti e resilienza completa anche se un'intera regione dovesse andare offline.

Se la connessione o sincronizzazione tra regioni si interrompesse temporaneamente per problemi di rete, i cluster Redis nelle diverse regioni possono aggiornare i dati indipendentemente. Una volta ristabilita la connessione, possono sincronizzare nuovamente le modifiche.

## Risoluzione dei Conflitti con CRDT

La sincronizzazione tra multiple regioni solleva la questione di come Redis risolva le modifiche agli stessi dataset da regioni diverse, garantendo che nessun cambiamento vada perso e mantenendo la consistenza dei dati.

Redis Enterprise utilizza i CRDT (Conflict-free Replicated Data Types) per risolvere automaticamente qualsiasi conflitto a livello database senza perdita di dati. Redis possiede meccanismi integrati per unire modifiche effettuate allo stesso dataset da fonti multiple, in modo che nessuna modifica vada persa e tutti i conflitti vengano risolti appropriatamente.

Dato che Redis supporta multiple tipologie di dati, ogni tipo utilizza le proprie regole di risoluzione conflitti ottimizzate per quella specifica tipologia. Invece di sovrascrivere semplicemente le modifiche di una fonte scartando tutte le altre, tutte le modifiche parallele vengono mantenute e risolte intelligentemente, il tutto automaticamente gestito dalla funzionalità di geo-replicazione active-active.

## Redis in Kubernetes

Redis si adatta perfettamente ai microservizi complessi che necessitano di supportare multiple tipologie di dati e facile scaling del database senza preoccuparsi della consistenza dati. Con Kubernetes diventato lo standard per l'esecuzione di microservizi, l'integrazione di Redis in questo ambiente rappresenta un caso d'uso molto interessante e comune.

Con Redis open source, è possibile distribuire Redis replicato come Helm chart o file manifest Kubernetes, utilizzando le regole di replicazione e scaling già discusse per impostare ed eseguire un database Redis altamente disponibile. L'unica differenza è che gli host dove Redis viene eseguito saranno pod Kubernetes invece di istanze EC2 o altri server fisici o virtuali.

Redis Enterprise offre un cluster Redis gestito distribuibile come operatore Kubernetes. Un operatore Kubernetes è un concetto che permette di raggruppare tutte le risorse necessarie per operare una specifica applicazione o servizio, eliminando la necessità di gestione manuale.

L'operatore Redis Enterprise su Kubernetes automatizza deployment e configurazione dell'intero database Redis nel cluster Kubernetes, gestisce scaling, backup e recovery del cluster Redis se necessario, assumendo la completa operazione del cluster Redis all'interno del cluster Kubernetes.

