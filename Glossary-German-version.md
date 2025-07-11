# FOSS-Glossar

Dieses Glossar wurde im Rahmen eines OSADL-Mitgliederprojekts von einer
Arbeitsgruppe aus Rechtsanwälten und Software-Entwicklern erstell
und wird unter der CC0-1.0 lizenziert. In keinem Fall handelt es sich
um eine individuelle Rechtsberatung.

Version: 1.0, Juli 2025

## Abgeleitetes Werk

Wenn ein bestehendes Werk mit Erlaubnis verändert oder erweitert wird,
entsteht ein abgeleitetes Werk und es wird ein sogenanntes
Bearbeiter-Urheberrecht erworben. Das ursprüngliche Urheberrecht bleibt
dabei erhalten, sodass sowohl der ursprüngliche Urheber als auch der
Bearbeiter ein Mitspracherecht bei der Lizenzierung des abgeleiteten
Werks haben. Das Mitspracherecht des Bearbeiters kann durch eine
[Copyleft-Klausel](#copyleft) in der ursprünglichen Lizenz des Werks
eingeschränkt werden.

Wenn bestimmte von einer Software-Komponente unverzichtbare Funktionen
in einer externen [Bibliothek](#bibliothek) und nicht in der jeweiligen
Software selbst enthalten sind, ist die einzelne Komponente nicht
selbständig ablauffähig. Erst durch dynamische oder statische
[Verlinkung](#verlinkung) mit den anderen Komponenten wird die Software
ausführbar. Dadurch entsteht im urheberrechtlichen Sinne ein
abgeleitetes Werk. Andere Verbindungen als durch einen solchen
Funktionsaufruf wie zum Beispiel über eine Netzwerk-Schnittstelle, über
UNIX-Sockets, über Pipes, über gemeinsam genutzten Speicher, durch
Interpretation oder Kompilierung führen dagegen nicht zu einem
abgeleiteten Werk. Diese Unterscheidung ist besonders im Zusammenhang
mit [Copyleft](#copyleft) relevant. In speziellen Fällen kann eine
individuelle Betrachtung notwendig sein.

## Abhängigkeit

Es gibt unterschiedliche Arten von Abhängigkeiten von
Software-Komponenten untereinander, die z.B. danach unterschieden
werden, ob sie bei der Auslieferung, beim Bau oder beim Ablaufen der
Software relevant sind. Diese werden folgendermaßen unterschieden und an
den jeweiligen Stellen beschrieben:

-   [Paketabhängigkeit](#paketabhängigkeit)
-   [Build-Abhängigkeit](#build-abhängigkeit)
-   [Linkabhängigkeit](#linkabhängigkeit)

## Betriebssystem

Das Betriebssystem stellt alle Funktionen bereit, die benötigt werden,
um Programme auf einem Computer auszuführen. In einem Linux-basierten
System gehören dazu in der Regel der [Linux-Kernel](#linux-kernel) und
die Treiber-Module, sofern diese Module konfiguriert sind, sowie ein
erstes Programm wie z.B. die Shell mit den dafür erforderlichen
[Bibliotheken](#bibliothek), um weitere Programme starten zu können.
Dies entspricht der traditionellen Definition eines Betriebssystems. Ob
und, wenn ja, welche weiteren Komponenten man noch als zum
Betriebssystem gehörig bezeichnen will, bleibt der individuellen
Definition in einem bestimmten Kontext überlassen. Kandidaten dafür sind

-   Allgemeine Verwaltungsprogramme (bei Linux *coreutils* und
    *util-linux*)
-   Hintergrund-Programme aller Art zum Beispiel für Graphik, Uhrzeit,
    Login
-   Weitere Sprachbibliotheken zum Beispiel für C++

In diesem Zusammenhang wird zwischen „Kernel Space" und „User Space"
unterschieden. Im Kernel Space läuft der Betriebssystem-Kernel sowie die
Treiber-Module, die mit der Computer-Hardware kommunizieren. Im User
Space laufen die Anwendungsprogramme und die von diesen benötigten
Bibliotheken. Die Kommunikation zwischen Kernel Space und User Space
läuft über eine Betriebssystem-unabhängige Schnittstelle, die sogenannte
Syscall-Schnittstelle, die eine urheberrechtliche Trennung darstellt.
Aufrufe von Anwendungsprogrammen oder Bibliotheken aus dem User Space in
den Kernel Space werden als „Systemaufrufe" („system calls") bezeichnet.
Die Lizenz des Linux-Kernels enthält einen expliziten Hinweis, dass
solche Systemaufrufe kein [abgeleitetes Werk](#abgeleitetes-werk) vom
Linux-Kernel erzeugen.

## Bibliothek

Viele Funktionen eines Computer-Programms werden von zahlreichen anderen
Software-Komponenten in gleicher Weise benötigt. Dabei handelt es sich
zum Beispiel um Standard-Funktionen, etwa zur Speicherverwaltung oder
zum Zugriff auf Speichermedien. Häufig sind es aber auch vollständige
Subsysteme, mit denen zum Beispiel mathematische Berechnungen
durchgeführt oder grafische Benutzeroberflächen in eine Software
integriert werden können.Würde jedes einzelne Programm alle benötigten
Funktionen vollständig selbst enthalten, könnten
[Linux-Distributionen](#linux-distribution) nicht mehr auf wenigen CDs
oder DVDs ausgeliefert werden; vielmehr wären hierfür Hunderte oder
sogar Tausende Datenträger erforderlich. Aus diesem Grund werden
gemeinsam benötigte Funktionen in sogenannten Bibliotheken
zusammengefasst. Diese können dann von verschiedenen Programmen
gemeinsam genutzt werden. Die Verbindung erfolgt über die
[Verlinkung](#verlinkung), welche die Zusammenarbeit der Komponenten
technisch ermöglicht.

## Binäres Distributionspaket

Ein binäres Distributions-Paket beinhaltet alle individuellen Dateien,
die von bestimmten Applikationen oder Bibliotheken benötigt werden.
Normalerweise sind die jeweiligen Applikationen bzw. Bibliotheken, nach
denen das Paket benannt ist, im Paket enthalten; Im Einzelfall können
aber auch weitere spezielle Bibliotheken, Konfigurations-Dateien sowie
Logos, Bilder, Audio-/Video-Dateien und Schriften enthalten sein. Diese
Dateien haben nicht notwendigerweise irgendeine urheberrechtliche
Beziehung untereinander im Sinne eines [gemeinsamen
Werks](#gemeinsames-werk). Weitere Applikationen bzw. Bibliotheken, die
nicht nur von den speziellen im Paket enthaltenen, sondern auch von
anderen Applikationen oder Bibliotheken benötigt werden und im
jeweiligen System vorausgesetzt werden können, sind nicht im Paket
enthalten. Stattdessen beinhaltet das Paket eine Liste dieser Pakete,
die als [externe Paketabhängigkeiten](#externe-paketabhängigkeit)
bezeichnet wird. Eine der wichtigsten Funktionen des
Installations-Programms, mit dem ein binäres Distributionspaket auf
einem Computer installiert wird, besteht darin, zu überprüfen, ob alle
benötigten externen Pakete installiert sind und, wenn dies nicht der
Fall ist, die fehlenden Pakete automatisch vom
[Linux-Distributions-Server](#linux) herunterzuladen und zu
installieren. Schließlich beinhaltet ein binäres Distributionspaket auch
noch Angaben zu den Lizenzen der enthaltenen Software-Komponenten. Da
diese von den jeweiligen Paket-Maintainern freiwillig und mehr oder
weniger sorgfältig bereitgestellt wurden, müssen diese Angaben nicht
notwendigerweise korrekt sein. Außerdem beziehen sich diese Angaben auf
die Gesamtheit der enthaltenen Software und nicht auf jede individuelle
Komponente. In jedem Fall kann das Vorhandensein von
[Copyleft-Lizenzen](#copyleft) nicht dahingehend interpretiert werden,
dass ein [gemeinsames Werk](#gemeinsames-werk) von Software-Komponenten
vorliegt. Hierfür ist vielmehr die individuelle Erfassung der
[Quellcode-Provenienz](#quellcode-provenienz) der einzelnen binären
Komponenten erforderlich.

## Build-Abhängigkeit

Build-Abhängigkeiten sind Programme und Komponenten, die benötigt
werden, um Quellcode in Binärprogramme oder -Bibliotheken zu übersetzen,
die aber selbst nicht Teil der resultierenden Binärkomponente sind. Dazu
gehören z.B. Tools wie ein Compiler. Wird die Übersetzung von einem
[Paketmanagementsystem](#paketmanagementsystem) durchgeführt, dann kann
dieses auch die notwendigen Build-Abhängigkeiten auflösen.
Build-Abhängigkeiten bilden normalerweise kein [abgeleitetes
Werk](#abgeleitetes-werk) von den resultierenden Binärkomponenten.

## Callgraph

Mit dem Namen „Callgraph" (kann auch „Dependency graph" genannt werden)
wird ein Programm bezeichnet, mit dem sich die rekursiven
[Linkabhängigkeiten](#linkabhängigkeit) zwischen Programmen oder
Bibliotheken auf der einen Seite und Bibliotheken auf der anderen Seite
sichtbar machen lassen. „Rekursiv" bedeutet dabei, dass
Linkabhängigkeiten vollständig aufgelöst werden, also auch
Abhängigkeiten von Abhängigkeiten berücksichtigt werden. Anstelle von
„rekursiv" kann der Begriff „transitiv" verwendet werden, der in diesem
Zusammenhang die gleiche Bedeutung hat. Der vom Programm „Callgraph"
herstellbare Beziehungsgraph wird ebenfalls „Callgraph" genannt. Da
Linkabhängigkeiten nur bei Binärprogrammen sichtbar gemacht werden
können, bezieht sich ein Callgraph immer auf Binärkomponenten. Im
Callgraph des Server-Programms *bluetoothd* in Abbildung 1 lässt sich
die bis zu fünfstufiger Abhängigkeit -- zunächst des Programms von
Bibliotheken und dann von den Bibliotheken zu anderen Bibliotheken --
erkennen. Zum Schluss benötigen praktisch alle Bibliotheken noch die
Bibliothek der Sprache C (*libc.so.6*). Normalerweise werden immer alle
rekursiv in einer [Linkabhängigkeit](#linkabhängigkeit) verbundenen und
somit zu einem [abgeleiteten Werk](#abgeleitetes-werk) führenden
Komponenten erfasst. Im Gegensatz zur
[Paketabhängigkeit](#paketabhängigkeit) lassen sich die in einem
Callgraph als verbunden dargestellten Komponenten im Hinblick auf
möglicherweise enthaltene [Copyleft-Lizenzen](#copyleft) auswerten. Über
die Darstellung des reinen Callgraphen hinaus erlaubt das Programm
Callgraph auch die Analyse der Funktionsnamen, die in einer Bibliothek
verwendet werden, sowie die Ausgabe der Namen der Quellcode-Dateien, die
für die Herstellung einer binären Komponente verwendet wurden. Letzteres
wird [Quellcode-Provenienz](#quellcode-provenienz) genannt und ist für
die exakte Ermittlung der anzuwendenden Lizenzen von Bedeutung.

![](bluetoothd.svg)Abbildung 1: Beispiel eines Callgraph des
Server-Programms \"bluetoothd\"

## Copyleft

Bei Schöpfung eines [abgeleiteten Werks](#abgeleitetes-werk) bestehen
grundsätzlich keine Einschränkungen bei der Wahl der Lizenzbedingungen
für die Bearbeitung. Allerdings kann es passieren, dass sich die
Lizenzbedingungen des ursprünglichen Werks und der Bearbeitung
widersprechen und infolgedessen das abgeleitete Werk nicht mehr
rechtskonform lizenzierbar ist. Die Lizenzbedingungen des ursprünglichen
Werks können aber eine Klausel beinhalten, nach der das abgeleitete Werk
nur dann kopiert und weitergegeben werden darf, wenn für die Bearbeitung
die Ursprungslizenz verwendet wird. Eine solche Lizenzklausel wird
„Copyleft", eine solche Lizenz „Copyleft-Lizenz" und eine auf diese
Weise lizenzierte Software „Copyleft-Software" genannt.

## Copyright-Vermerk

Die üblicherweise verwendete Form des Hinweises auf Rechteinhaber und
Urheber für in einem Unternehmen hergestellte Software lautet

Copyright © JAHR RECHTEINHABER, author URHEBER

Dabei ist die Nennung des Autors nach dessen Wahl optional. Der erste
Teil müsste auf Deutsch korrekterweise als Rechteinhabervermerk und der
zweite Teil als Urhebervermerk bezeichnet werden. Für den Vermerk in
seiner Gesamtheit wird üblicherweise der Begriff Urhebervermerk
verwendet, obwohl es dabei fast immer um die Benennung des
Rechteinhabers geht. Auf Englisch wird der erste Teil als „Copyright
notice", der zweite Teil als „Author attribution" bezeichnet. Für den
Vermerk in seiner Gesamtheit wird im Gegensatz zum Deutschen nicht der
zweite Teil, sondern der erste Teil des Vermerks verwendet und dieser
entsprechend „Copyright notice" genannt. Um Missverständnisse zu
vermeiden, und weil es in der Regel um die Rechte an einer Software
geht, wird empfohlen, auf Deutsch grundsätzlich das Mischwort
„Copyright-Vermerk" zu verwenden. Der Begriff „Urhebervermerk" bleibt
dann auf Situationen beschränkt, in denen es tatsächlich um die durch
das Persönlichkeitsrecht gewährten Urheberrechte geht.

## Download-Server

[FOSS](#foss) von [Linux-Distributionen](#linux-distribution)
wird üblicherweise auf Download-Servern angeboten, die von den
entsprechenden Organisationen (zum Beispiel „Canonical", „Debian" oder
„Fedora") betrieben werden. Diese Download-Server von Distributionen
haben eine wichtige Funktion bei der Auflösung von [externen
Paketabhängigkeiten](#externe-paketabhängigkeit), wenn bei der
Installation von Distributions-Paketen weitere vom
[Paketmanagementsystem](#paketmanagementsystem) ermittelte abhängige
Pakete automatisch heruntergeladen und installiert werden. Um die
Lastanforderungen an diese Download-Server und damit auch die Kosten so
gering wie möglich zu halten, bieten Universitäten und große
Internet-Provider lokale sogenannte Mirror-Server an, deren Inhalte
engmaschig mit den Primär-Servern der Distributionen synchronisiert
werden. Download-Server gibt es aber nicht nur für komplette
[Linux-Distributionen](#linux-distribution), sondern auch für einzelne
Software-Komponenten in
Quellcode- oder Binärform, die als [Repository](#repository) bezeichnet
werden. Häufig enthalten Repositories nicht nur einzelne Komponenten,
sondern bieten auch ein Versionskontrollsystem und eine
Entwicklungs-Plattform (z.B. GitHub). Diese Repositories gelten als
primäre Hosts für Open Source-Softwareprojekte, und die dort
archivierten Namen und Versionsnummern sind maßgeblich für die
Referenzierung eines bestimmten Software-Releases zum Beispiel in einer
SBOM.

## Dynamische Verlinkung

[Verlinkung](#verlinkung)

## ELF-Header

Die Abkürzung ELF steht für „Executable and Linkable Format". Bei
Applikationen stehen in diesem Header die Namen der benötigten
Bibliotheken („NEEDED") und die Namen der benötigten Funktionen („UND",
steht für „undefined"). Bibliotheken enthalten im ELF-Header die Namen
der bereitgestellten Funktionen („FUNC"), mit denen sich Applikationen
zur Laufzeit verbinden und diese dann nutzen können. Außerdem kann der
ELF-Header die Informationen darüber speichern, welche Quellcode-Datei
für die Herstellung einer jeden binären Software verwendet wurde, was
für die Ermittlung der [Quellcode-Provenienz](#quellcode-provenienz)
genutzt wird. Mit den Programmen „readelf" und „pyreadelf" lässt sich
die gesamte ELF-Datenstruktur eines Programms oder einer Bibliothek
auslesen und darstellen. Die ELF-Header werden auch vom Programm
[Callgraph](#callgraph) verwendet, um einen Beziehungsgraphen der
untereinander in einer [Linkabhängigkeit](#linkabhängigkeit) verbundenen
Software-Komponenten herzustellen und die Voraussetzungen für die
genannte Quellcode-Provenienz zu schaffen.

## Erschöpfungsgrundsatz

Grundsätzlich betrifft der Erschöpfungsgrundsatz die Bedingungen, unter
denen ein Werk weiterverbreitet werden darf, nachdem es erstmalig in den
Verkehr gebracht wurde. Das Urheberrecht gewährt dem Schöpfer eines
Werkes insbesondere zwei wichtige Rechte: Erstens verbietet das
Urheberrecht allen anderen Personen, das Werk zu kopieren, solange sie
dafür keine Erlaubnis vom Schöpfer erworben haben, der Schöpfer besitzt
also das ausschließliche Vervielfältigungsrecht. Zweitens gewährt das
Urheberrecht dem Schöpfer das Recht zu entscheiden, ob und, wenn ja, an
wen er das Werk verbreitet, er besitzt also auch das ausschließliche
Verbreitungsrecht. Dies ändert sich, nachdem das Werk erstmals veräußert
wurde. Denn während das Kopierverbot als Folge des ausschließlichen
Vervielfältigungsrechts auch nach Veräußerung weiterhin gilt und
unproblematisch ist, würde es eine sehr weitgehende Einschränkung des
freien Verkehrs von Gütern bedeuten, wenn der Schöpfer eines Werks die
Verbreitung eines Originals oder Vervielfältigungsstücks dieses Werks
auch nach dessen Veräußerung kontrollieren könnte. Daher erlischt nach
der ersten Veräußerung das Recht eines Schöpfers bezogen auf das
Original oder eines Vervielfältigungsstücks, die Verbreitung von
ebendiesem zu kontrollieren. Ähnliches gilt auch für Patent- und
Markenrechte. Dieses Erlöschen von Rechten wird als Erschöpfung
bezeichnet, und speziell für Software ist die Erschöpfung des
ausschließlichen Verbreitungsrechts bei Veräußerung innerhalb der EU und
des EWR in § 69c Nr. 3 S. 2 UrhG geregelt. Wichtige Voraussetzung für
eine Weiterveräußerung unter den Grundsätzen der Erschöpfung ist, dass
die ursprüngliche Veräußerung der Software durch den Schöpfer oder mit
dessen Zustimmung, unter Beachtung etwaiger Lizenzvorgaben, erfolgt,
dass die Software nach der Erstveräußerung nicht verändert wurde und
dass die Software nicht auf einem eigenen Datenträger zurückbehalten
wird. Wenn diese Bedingungen zutreffen, darf die Software also ohne
weitere Erlaubnis des Schöpfers weitergegeben werden. Dies gilt auch für
Software, die bereits beim Ersterwerb in einem Gerät installiert war und
dann unverändert und nicht anderswo installiert weiterveräußert wird wie
zum Beispiel das Car-Entertainment-System in einem Gebrauchtwagen oder
das Betriebssystem eines weiterverkauften gebrauchten Internet-Routers.
In beiden Fällen muss nicht der Verkäufer der gebrauchten Ware die
Lizenzpflichten erfüllen, sondern derjenige, der die Software nach der
letztmaligen Veränderung ursprünglich in den Verkehr gebracht hat, also
im Beispiel der Autobauer bzw. der Router-Hersteller.

## Externe Paketabhängigkeit

[Paketabhängigkeit](#paketabhängigkeit)

## FOSS

Die Abkürzung FOSS steht für „Free and Open Source Software" und wird
für Software verwendet, deren Lizenz die dafür definierten Anforderungen
erfüllt. Im wesentlichen muss eine solche Lizenz die uneingeschränkte
Nutzung, Veränderung und Analyse der Software sowie deren Weitergabe
unter freiheitlichen und nicht-diskriminierenden Bedingen gestatten.
Die beiden mitunter auch verwendeten Begriffe „Freie Software" und
"Open Source-Software" sind juristisch identisch, entstammen allerdings
unterschiedlichen Ideologien. Die Zusammenfassung als FOSS erfolgt,
um beide Ideologien zu würdigen, ohne eine bestimmte davon besonders
hervorzuheben.

## Freie Software

[FOSS](#foss)

## Gemeinsames Werk

[Abgeleitetes Werk](#abgeleitetes-werk)

## Interne Paketabhängigkeit

[Paketabhängigkeit](#paketabhängigkeit)

## Linkabhängigkeit

Mit Linkabhängigkeit wird die Tatsache bezeichnet, dass
Software-Komponenten spätestens zur Laufzeit bestimmte
[Bibliotheken](#bibliothek) benötigen, um ablaufen zu können. Im
Gegensatz zur [Paketabhängigkeit](#paketabhängigkeit) kommt es dabei zu
einer ganz bestimmten Art von Verbindung, die [Verlinkung](#verlinkung)
genannt wird und grundsätzlich ein [abgeleitetes
Werk](#abgeleitetes-werk) erzeugt, was bei
[Copyleft-Lizenzen](#copyleft) zu berücksichtigen ist.

## Linux

Wenn es nicht aus dem Zusammenhang erkennbar ist, sollte der
alleinstehende Begriff „Linux" vermieden werden. Denn im Einzelfall
können damit ganz verschieden Dinge wie zum Beispiel der
[Linux-Kernel](#linux-kernel), das [Betriebssystem](#betriebssystem),
oder eine komplette [Linux-Distribution](#linux-distribution) gemeint
sein.

## Linux-Distribution

Mit einer Linux-Distribution (Abkürzung: „Distro") ist die gebündelte
Zusammenstellung funktional aufeinander abgestimmter Softwarepakete
gemeint, mit der sich ein vollständiges Linux-System, etwa eine
Workstation oder ein Server, installieren lässt. Wesentliche
Bestandteile einer Distribution sind der [Paketmanager](#paketmanager)
zur Installation und Verwaltung von Software, ein
[Download-Server](#download-server) (inkl. Spiegel-Servern), [binäre
Distributionspakete](#binäres-distributionspaket) und
[Quellcode-Distributionspakete](#quellcode-distributionspaket) sowie ein
Update-Mechanismus zur Behebung von Sicherheitslücken und funktionalen
Fehlern. Nicht zuletzt wird in vielen Fällen auch ein öffentlicher
Entwicklungsserver bereitgestellt (z.B.
[https://koji.fedoraproject.org/koji/](https://koji.fedoraproject.org/koji/)
für „Fedora"), auf dem die
Entwicklung und die Tests der Softwarepakete stattfinden. Die am meisten
verwendeten Distributionen basieren auf der „Debian"- oder der
„Fedora"-Distribution. Beide stellen Softwarepakete sowohl in binärer
als auch in Quellcode-Form zur Verfügung. Da die übliche
Installationsmethode bei diesen Distributionen ausschließlich auf
binären Distributionspaketen beruht, stellt die Verfügbarkeit der
Quellcode-Distributionspakete ein wesentliches Element für die Erfüllung
der Offenlegungspflichten der Copyleft-Lizenzen dar. Diese werden
ausschließlich zum Download, üblicherweise über den Paketmanager zur
Verfügung gestellt. Dabei sollte beachtet werden, dass die
Distributionen nicht alle Versionen von Quellcode-Paketen dauerhaft
bereitstellen, sodass sich ein nachträgliches Herunterladen älterer
Versionen als schwierig bis unmöglich darstellen kann. In diesem
Zusammenhang ist die Distribution „Gentoo" zu erwähnen, bei der es sich
immer um eine komplette Quellcode-Distribution handelt.

## Linux-Kernel

Der Linux-Kernel ist eine alleinstehende Software, welche es einem
Programm ermöglicht, auf die individuelle Hardware eines Computers
zuzugreifen. Jede [Linux-Distribution](#linux-distribution) enthält den
Linux-Kernel in einer bestimmten Version und stellt passende
Hilfsprogramme dafür zur Verfügung.

## Open Source-Software

[FOSS](#foss)

## OSSelot-Projekt

Das OSSelot-Projekt hat das Ziel, eine möglichst große Anzahl häufig
verwendeter [FOSS](#foss) basierend auf dem jeweiligen
[Repository](#repository) zu kuratieren und die dabei hergestellten
Dokumente in üblichen Formaten der Allgemeinheit unter einer permissiven
[FOSS](#foss)-Lizenz verfügbar zu machen, so dass unnötige Parallelarbeit
vermieden wird. Im Rahmen des Projekts wird sämtliche kuratierte
Software, bei der dies möglich ist, in einer Standard-Konfiguration
übersetzt und die [Quellcode-Provenienz](#quellcode-provenienz)
ermittelt.

## Paketabhängigkeit

Der Begriff Paketabhängigkeit ist, wenn er alleinsteht, mehrdeutig. Mit
„interner Paketabhängigkeit" werden die Komponenten bezeichnet, die sich
in einem binären Distributionspaket befinden. Dabei kann es sich z.B. um
Programme und Bibliotheken handeln, aber zusätzlich auch um Fonts,
Grafiken und Dokumentation.

Dagegen wird die Bezeichnung „externe Paketabhängigkeit" für andere
binäre Distributionspakete verwendet, welche die Komponenten eines
Pakets zur Ausführung benötigen und die der
[Paketmanager](#paketmanager) daher bei der Installation automatisch
mitinstalliert. Weder die interne noch die externe Paketabhängigkeit
führt notwendigerweise zu einer urheberrechtlichen Verbindung im Sinne
eines [abgeleiteten Werks](#abgeleitetes-werk).

## Paketmanagementsystem

Das Paketmanagementsystem stellt die wesentliche Software-Komponente
einer [Linux-Distribution](#linux-distribution) dar und wurde speziell
dafür entwickelt. Mit dieser Software, die in der Regel aus einer
Vielzahl individueller Applikationen und Bibliotheken besteht, werden
[Quellcode-Distributionspakete](#quellcode-distributionspaket) und
[binäre Distributionspakete](#binäres-distributionspaket) hergestellt,
verwaltet und auf [Download-Servern](#download-server) bereitgestellt.
Anwender können
[Quellcode-Distributionspakete](#quellcode-distributionspaket)
herunterladen und mit dem gleichen Verfahren lokal herstellen, wie dies
auf den öffentlichen Entwicklungsservern geschieht, um beispielsweise
Programmfehler zu beheben oder um die Funktionalität zu erweitern. Die
beiden vermutlich am häufigsten verwendeten Paket-Formate sind „deb"
(zum Beispiel für die Distributionen „Debian" und „Ubuntu") und „rpm"
(zum Beispiel für die Distribution „Fedora"). Weitere Paket-Formate für
bestimmte Programmiersprachen sind z.B. Java (Maven, Gradle), Python
(Pip) sowie C++ (Conan).

## Paketmanager

Der Paketmanager ist ein wichtiger Bestandteil von
[Paketmanagementsystemen](#paketmanagementsystem) und sorgt dafür, dass
die gesamte auf einem Computer installierte Software konsistent ist,
d.h. dass alle Komponenten verfügbar sind, die zur Ausführung der
installierten Programme benötigt werden. Daher darf auf einem von einem
Paketmanager verwalteten System Software niemals direkt installiert oder
entfernt werden, da dann die intern vom Paketmanager verwaltete Liste
über installierte Software-Komponenten nicht mehr mit der Realität
übereinstimmen würde und jede weitere Verwendung des Paketmanagers
zwangsläufig fehlerhaft wäre. Während Interpretersprachen wie Python
oder Javascript häufig Quellcode zur Laufzeit ausführen und direkt
verwaltet werden können, erfordern Compiler-Sprachen wie C++ zunächst
eine Übersetzung des Codes in Maschinenbefehle; dies spiegelt sich auch
in der Struktur und Nutzung der jeweiligen
[Paketmanagementsysteme](#paketmanagementsystem) wider. 

## Quellcode-Distributionspaket

Als Grundlage für die Herstellung eines [binären
Distributionspakets](#binäres-distributionspaket) dient das
[Quellcode-Distributionspaket](#quellcode-distributionspaket). Dieses
enthält die eindeutige URL zum Bezug des originalen Quellcodes vom
jeweiligen [Repository](#repository), eventuell erforderliche Patche und
Anweisungen zur Konfiguration und zum Kompilieren. In der Regel gibt es
ein spezielles Programm des [Paketmanagers](#paketmanager), mit dem sich
das Quellcode-Distributionspaket aus den Spezifikationen eines Pakets
herstellen lässt. Entweder im gleichen oder in einem weiteren Schritt
können dann auch binäre Distributionspakete hergestellt werden.
Üblicherweise entstehen aus einem einzigen Quellcode-Distributionspaket
mehrere binäre Distributionspakete. Während das
Quellcode-Distributionspaket in der Regel unabhängig von einer
bestimmten Computer-Architektur ist, kann das binäre Distributionspaket
nur auf den jeweiligen Computern verwendet werden, für die es
hergestellt wurde.

## Quellcode-Provenienz

Da nicht jede Datei, die in einem [Repository](#repository) oder in
einem [Quellcode-Distributionspaket](#quellcode-distributionspaket)
enthalten ist, für den Bau einer bestimmten Binärdatei verwendet wird,
kann aus den dort angegebenen Lizenzinformationen nicht auf die
Lizenzierung einer aus diesen Quellcodes hergestellten Software
geschlossen werden. Dies gilt auch für Lizenzangaben in einem kompletten
[binären Distributionspaket](#binäres-distributionspaket), das in der
Regel mehrere binäre Software-Komponenten enthält; denn es wird nicht
vermerkt, für welche Komponente die jeweilige Lizenzinformation gilt.
Die einzige Möglichkeit, eine korrekte Information zur Lizenzierung
einer binären Software zu erhalten, besteht darin, bei der Herstellung
die verwendeten Quellcode-Dateien zu protokollieren und der binären
Software im [ELF-Header](#elf-header) mitzugeben. Dies wird
Quellcode-Provenienz genannt und wird vom Programm
[Callgraph](#callgraph) unterstützt.

## Rechteinhabervermerk

[Copyright-Vermerk](#copyright-vermerk)

## Repository

[FOSS](#foss) wird von den Entwicklern üblicherweise auf
Internet-Servern in einem sogenannten Repository verfügbar machen. Dort
können die einzelnen Dateien und der Verlauf ihrer Herstellung
eingesehen und nachverfolgt werden. Darüber hinaus werden in bestimmten
Abständen stabile und besonders gut getestete Versionen als Release
bezeichnet und mit einem Versions-Tag versehen. Dieser Versions-Tag
dient dann zur Identifikation eines bestimmten Entwicklungsstands und
wird in der Regel auch von [Linux-Distributionen](#linux-distribution)
übernommen. Die Quellcode-Dateien im Repository bzw. der im Repository
verwendete Release-Tag stellen die einzige allgemein verbindliche
Referenz einer Software-Version dar. Aus einem einzigen Release eines
Repository können unzählige
[Quellcode-Distributionspakete](#quellcode-distributionspaket) der
verschiedenen Distributionen entstehen und aus diesen wiederum ein
Vielfaches an [binären
Distributionspaketen.](#binäres-distributionspaket) Daher bezieht sich
das [OSSelot-Projekt](#osselot-projekt) ausschließlich auf das jeweilige
Repository einer Software und auf die dort verwendeten Release-Tags.

## Statische Verlinkung

[Verlinkung](#verlinkung)

## Urhebervermerk

[Copyright-Vermerk](#copyright-vermerk)

## Verbundenes Werk

[Abgeleitetes Werk](#abgeleitetes-werk)

## Verlinkung

Verlinkung bedeutet, dass zwei Software-Komponenten auf eine spezielle
Weise untereinander verbunden werden, so dass Programmcode der beiden
Komponenten gemeinsam genutzt werden kann. Eine solche Verlinkung kann
beim letzten Schritt der Software-Herstellung erfolgen, so dass die
Software-Komponenten in einer einzigen Datei zusammengefasst werden.
Dies wird als statische Verlinkung bezeichnet. Es ist aber auch möglich,
die betroffenen Software-Komponenten mit einer standardisierten
Software-Schnittstelle auszurüsten, so dass diese unabhängig voneinander
hergestellt und ausgeliefert werden können. Erst zur Laufzeit der
jeweiligen Software kommt es dann zur Verlinkung. Dies wird als
dynamische Verlinkung bezeichnet. Im urheberrechtlichen Sinne, d.h. im
Hinblick auf die Erzeugung eines [abgeleiteten
Werks,](#abgeleitetes-werk) besteht kein Unterschied zwischen statischer
und dynamischer Verlinkung. Denn in jedem Fall kommt es zur
[Linkabhängigkeit](#linkabhängigkeit). Daher ist zu ermitteln, ob es
sich mindestens in einem der Fälle um eine [Copyleft-Lizenz](#copyleft)
handelt, so dass die entsprechenden besonderen Lizenzpflichten für die
anderen Software-Komponenten beachtet werden müssen. Damit die
dynamische Verlinkung zur Laufzeit festgestellt und eingerichtet werden
kann, sind die beiden Software-Komponenten am Anfang des Codes mit einem
sogenannten [ELF-Header](#elf-header) ausgerüstet. Die vielfältigen
hierarchischen Link-Beziehungen zwischen Applikationen und Bibliotheken
lassen sich mit dem Programm [Callgraph](#callgraph) als
Beziehungsgraphen oder auch in Textform darstellen. Andere Arten der
Verbindung von bzw. Kommunikation zwischen Software-Komponenten werden
nicht als Verlinkung bezeichnet und erzeugen im Normalfall auch kein
[abgeleitetes Werk](#abgeleitetes-werk).
