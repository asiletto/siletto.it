# I Quattro Pilastri dell'Architettura Event-Driven secondo Martin Fowler

L'architettura event-driven è un concetto che ha attraversato l'intera carriera di Martin Fowler, ma che per anni è rimasto sfuggente nella sua definizione precisa. Durante un workshop interno di ThoughtWorks a Denver, è emersa la necessità di fare chiarezza su questo argomento, portando all'identificazione di quattro pattern distinti che spesso vengono raggruppati sotto l'ombrello delle "architetture event-driven".

La confusione nasce dal fatto che quando si parla di sistemi event-driven, ci si può riferire a uno qualsiasi di questi quattro pattern, o addirittura a una combinazione di tutti. Comprendere le differenze è fondamentale per progettare sistemi che sfruttino al meglio le potenzialità degli eventi, evitando al contempo le insidie più comuni.

## Event Notification

Il primo e più comune pattern è quello dell'event notification, che risolve un problema fondamentale nell'architettura software: il coupling indesiderato tra sistemi. Immaginiamo un sistema di gestione clienti per una compagnia assicurativa. Quando un cliente cambia indirizzo, questo non è solo un aggiornamento anagrafico, ma richiede il ricalcolo delle quote assicurative, dato che la località influenza i premi da pagare.

In un'architettura tradizionale basata su chiamate dirette, il sistema di gestione clienti dovrebbe conoscere l'esistenza del sistema di quotazione assicurativa e chiamare le sue API specifiche. Questo crea una dipendenza problematica: un sistema generico come la gestione clienti diventa accoppiato a logiche di business specifiche del dominio assicurativo.

L'event notification ribalta questa dinamica attraverso l'emissione di eventi. Quando i dati di un cliente cambiano, il sistema di gestione clienti pubblica semplicemente un evento su una coda o un bus degli eventi. Il sistema di quotazione assicurativa, a sua volta, rimane in ascolto di questi eventi e decide autonomamente come reagire. La dipendenza viene così invertita: il sistema specializzato (quotazione) dipende da quello generico (gestione clienti), il che è molto più naturale.

Questo approccio non si limita ai sistemi enterprise, ma trova applicazione anche nelle interfacce grafiche. Una textbox non deve conoscere tutta la logica applicativa che dipende dai suoi cambiamenti; emette semplicemente eventi quando il suo contenuto viene modificato, permettendo al codice applicativo di reagire di conseguenza.

Il pattern dell'event notification porta con sé un beneficio aggiuntivo: trasforma i cambiamenti in "cittadini di prima classe" del sistema. Invece di essere operazioni transitori che scompaiono dopo l'esecuzione, i cambiamenti diventano oggetti concreti che possono essere referenziati, passati tra sistemi e analizzati. Questo è particolarmente potente quando si tratta di debug, auditing o analisi del comportamento del sistema.

La distinzione tra eventi e comandi diventa cruciale in questo contesto. Un evento comunica che qualcosa è accaduto senza prescrivere una risposta specifica ("l'indirizzo del cliente è cambiato"), mentre un comando esprime un'intenzione precisa ("ricalcola la quotazione assicurativa"). La scelta tra le due formulazioni influenza profondamente come il sistema viene percepito e compreso da chi lo sviluppa e lo mantiene.

Il grande vantaggio dell'event notification è la facilità con cui nuovi consumatori possono agganciarsi al flusso degli eventi. Aggiungere un nuovo sistema che deve reagire ai cambiamenti di indirizzo non richiede modifiche al sistema di gestione clienti né lunghe negoziazioni con il team che lo mantiene. È sufficiente collegarsi al flusso degli eventi e iniziare a processarli.

Tuttavia, questa flessibilità ha un prezzo. La natura distribuita degli eventi rende estremamente difficile comprendere il comportamento complessivo del sistema. Non esiste più un singolo punto dove è possibile leggere tutte le azioni che vengono intraprese quando un cliente cambia indirizzo. L'unico modo per capire cosa succede è osservare il flusso dei messaggi in tempo reale, rendendo il debugging e la comprensione del sistema significativamente più complessi.

## Event-Carried State Transfer

Il secondo pattern nasce da una limitazione dell'event notification: spesso gli eventi contengono informazioni minimali, richiedendo ai sistemi consumatori di fare ulteriori chiamate per ottenere i dettagli necessari. Se un evento ci dice solo che "è cambiato qualcosa riguardo a Linda", dovremo interrogare il sistema di origine per scoprire cosa è cambiato esattamente.

Anche eventi più specifici come "l'indirizzo di Linda è cambiato" possono richiedere chiamate aggiuntive per ottenere il nuovo indirizzo, quello precedente, o altri dati del cliente necessari per processare il cambiamento. Questo genera traffico di rete aggiuntivo e crea dipendenze runtime tra i sistemi.

L'event-carried state transfer porta questa logica all'estremo: gli eventi contengono tutti i dati necessari ai sistemi consumatori, eliminando completamente la necessità di chiamate di ritorno. Il sistema di quotazione assicurativa mantiene una copia locale di tutti i dati cliente di cui ha bisogno, aggiornandola attraverso gli eventi ricevuti.

Questo approccio offre benefici significativi in termini di performance, dato che elimina le chiamate di rete sincrone, e di disponibilità, dato che il sistema di quotazione può continuare a funzionare anche se il sistema di gestione clienti non è raggiungibile. Il carico sul sistema di origine si riduce drasticamente, dato che non deve più rispondere a una miriade di query da parte dei sistemi downstream.

Il prezzo da pagare è la duplicazione dei dati e la conseguente perdita di consistenza forte. I sistemi mantengono copie dei dati che possono temporaneamente divergere dall'originale, introducendo la complessità della consistenza eventuale. Inoltre, il sistema di origine deve ora broadcast are tutti i dati che potrebbero interessare ai consumatori, non solo i cambiamenti minimi.

Questo pattern è meno comune dell'event notification, ma può essere estremamente utile in scenari dove la performance e la disponibilità sono critiche, e dove la consistenza eventuale è accettabile per il business.

## Event Sourcing

Il terzo pattern rappresenta un cambio di paradigma fondamentale nel modo in cui concepiamo la persistenza dei dati. Invece di mantenere solo lo stato corrente del sistema, l'event sourcing conserva l'intera storia dei cambiamenti sotto forma di eventi.

In un sistema tradizionale, quando un cliente cambia indirizzo, sovrascriviamo semplicemente il vecchio indirizzo con quello nuovo. Nell'event sourcing, prima creiamo un evento che rappresenta questo cambiamento e lo persiste in un log degli eventi, poi processiamo l'evento per aggiornare lo stato applicativo. La caratteristica fondamentale è che lo stato applicativo può essere completamente ricostruito riprocessando il log degli eventi dall'inizio.

Questa architettura è più familiare di quanto si possa pensare. Ogni sviluppatore software usa quotidianamente un sistema event-sourced: il version control. Git, Subversion, e tutti i sistemi di controllo versione mantengono la storia completa dei cambiamenti al codice, permettendo di ricostruire qualsiasi versione passata del repository. Lo stato corrente del working tree è derivabile dalla sequenza di commit che lo hanno generato.

Un altro esempio universalmente compreso è la contabilità. Il saldo corrente di un conto bancario è derivabile dall'insieme di tutti i crediti e debiti che lo hanno interessato. I sistemi contabili sono intrinsecamente event-sourced, e l'analogia con i ledger contabili rende il concetto accessibile anche ai non-tecnici.

I vantaggi dell'event sourcing sono molteplici. Fornisce un sistema di audit naturale e completo, permettendo di ripercorrere esattamente come si è arrivati a un particolare stato. È uno strumento di debugging potentissimo, dato che è possibile ricreare scenari problematici riprocessando gli stessi eventi in un ambiente controllato. La possibilità di viaggiare nel tempo, tornando a stati precedenti del sistema, apre scenari altrimenti impossibili.

Particolarmente interessante è la capacità di gestire correzioni retroattive. Se scopriamo che un dipendente ha lavorato 40 ore invece di 35 sei mesi fa, in un sistema tradizionale dovremmo calcolare manualmente tutti gli aggiustamenti necessari per stipendio, ferie, pensione. Con l'event sourcing, possiamo correggere l'evento originale in una copia del sistema, riprocessare tutti gli eventi successivi, e generare automaticamente gli aggiustamenti necessari confrontando i due stati finali.

Un vantaggio inaspettato è la possibilità di utilizzare completamente la memoria RAM per lo stato applicativo. Se la verità risiede nel log degli eventi, lo stato corrente diventa semplicemente una cache derivata che può risiedere interamente in memoria. Questo approccio è stato utilizzato con successo in sistemi ad alta performance come LMAX, un sistema di trading che raggiunge 6 milioni di transazioni al secondo su un singolo thread Java, proprio grazie all'eliminazione dell'accesso al database durante l'elaborazione.

Tuttavia, l'event sourcing introduce complessità significative. La gestione dello schema degli eventi nel tempo diventa cruciale, dato che gli eventi devono rimanere interpretabili anche dopo anni. La performance delle query può degradare se non si implementano strategie di snapshot appropriate. La ricostruzione dello stato da zero può diventare lenta con l'accumularsi degli eventi. Inoltre, la natura append-only del log rende difficile gestire requisiti di compliance come il "diritto all'oblio" del GDPR.

## CQRS

Il quarto e ultimo pattern è CQRS (Command Query Responsibility Segregation), che estende il principio di separazione tra comandi e query anche a livello architetturale. L'idea di base è semplice: utilizziamo modelli di dati diversi per le operazioni di scrittura (comandi) e quelle di lettura (query).

In un sistema tradizionale, lo stesso modello di dati serve sia per aggiornare le informazioni che per leggerle. CQRS propone di utilizzare strutture dati ottimizzate per ciascun caso d'uso. Il write model è progettato per garantire consistenza e validazione durante gli aggiornamenti, mentre i read model sono ottimizzati per le specifiche esigenze di query delle diverse interfacce utente.

Questo approccio si rivela particolarmente potente quando combinato con l'event sourcing. Gli eventi generati dal write model vengono utilizzati per popolare e mantenere aggiornati molteplici read model, ognuno specializzato per un particolare tipo di query o interfaccia utente. Un sistema di e-commerce potrebbe avere read model separati per la ricerca prodotti, l'analisi delle vendite, e la gestione dell'inventario, tutti alimentati dagli stessi eventi di business.

CQRS offre vantaggi significativi in termini di scalabilità, dato che i read model possono essere replicati e ottimizzati indipendentemente dal write model. Permette inoltre di utilizzare tecnologie diverse per lettura e scrittura, scegliendo i database più appropriati per ciascun caso d'uso. La flessibilità nell'evoluzione dell'interfaccia utente aumenta notevolmente, dato che è possibile aggiungere nuove viste dei dati senza impattare il modello di scrittura.

Tuttavia, CQRS introduce complessità architetturale significativa. La sincronizzazione tra write e read model può essere problematica, specialmente in caso di errori o inconsistenze. La consistenza eventuale diventa inevitabile, richiedendo che l'interfaccia utente gestisca appropriatamente i ritardi tra scrittura e lettura. La duplicazione del codice e la necessità di mantenere molteplici rappresentazioni degli stessi dati aumentano il carico di manutenzione.

## Quando Utilizzare Questi Pattern

La scelta del pattern appropriato dipende fortemente dal contesto e dai requisiti del sistema. L'event notification è il punto di partenza naturale per la maggior parte dei sistemi, dato che fornisce benefici immediati in termini di disaccoppiamento con complessità limitata. È particolarmente utile quando si vuole permettere a sistemi multipli di reagire agli stessi eventi senza creare dipendenze dirette.

L'event-carried state transfer diventa attraente quando la performance e la disponibilità sono critiche, e quando la consistenza eventuale è accettabile per il business. È particolarmente indicato per sistemi geograficamente distribuiti o quando i sistemi upstream hanno limitazioni di throughput.

L'event sourcing richiede una giustificazione più forte, dato che introduce complessità architetturale significativa. È indicato quando l'audit trail è un requisito business forte, quando si ha bisogno di analizzare l'evoluzione storica dei dati, o quando la possibilità di riprocessare eventi è cruciale per il business. I sistemi finanziari, i sistemi di compliance, e i sistemi dove la ricostruibilità dello stato è critica sono candidati naturali.

CQRS dovrebbe essere considerato quando le esigenze di lettura e scrittura sono significativamente diverse, quando si ha bisogno di ottimizzazioni specifiche per le query, o quando si sta già utilizzando event sourcing e si vuole sfruttare appieno i suoi benefici.

