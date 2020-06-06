# Multi Node Hadoop Cluster Installationsanleitung
## Architektur

- Master Node (master1): enthält die Informationen über das verteilte Dateisystem, plant die Ressourcenzuteilung und hat bzw. enthält 2 Domänen/Daemons:
  - Name Node: verwaltet das verteilte Dateisystem und weiß, wo sich gespeicherte Datenblöcke im Cluster befinden
  - Resource Manager: verwaltet die YARN-Jobs und übernimmt die Planung und Ausführung von Prozessen auf den Worker Nodes
- Worker Nodes (slave1, slave2): Speichern die tatsächlichen Daten und stellen die Verarbeitungsleistung für die Ausführung von Jobs bereit, enthalten 2 Domänen/Daemons:
  - Data Node/ Name Node: verwaltet die auf dem Knoten gespeicherten physischen Daten
  - Node Manager: verwaltet die Ausführung von Jobs auf dem Knoten

**Im Beispiel:**

- Hadoop Master: 192.168.0.10 (master1)
- Hadoop Slave: 192.168.0.11 (slave1)
- Hadoop Slave: 192.168.0.12 (slave2)

## Vorgehensweise
#### Hostnamen und IP Adresse ändern
```bash 
1. Bei der Installation kann der Hostname und die IP auch schon eingestellt werden. (siehe CentOS als VM in Virtualbox installieren)
2.  hostname -I #Anzeigen der IP Adresse
    hostname oder hostnamectl #Anzeigen des Hostnamens
3.  sudo hostname master1 #Ändern des Hostnamen
4.  sudo nano /etc/sysconfig/network-scripts/ifcfg-enp0s3
    BOOTPROTO=static #change to static
    IPADDR=192.168.0.10
    GATEWAY=192.168.0.1
    NETMASK=255.255.255.0
5.  sudo systemctl restart NetworkManager.service
```

#### Installation eines Multi Node Hadoop Cluster
``` bash
1. Wenn nicht bereits konfiguriert: Hostnamen und IP Adresse ändern (siehe oben)
2. Wenn nicht bereits konfiguriert: Mapping der Nodes: spezifizieren der IPs gefolgt von dem Hostnamen jedes Nodes (ausführen auf jedem Node) [IP Hostname]
Hinweis: den vorherigen Inhalt löschen (localhost…)
    sudo vi /etc/hosts
    192.168.0.10 master1
    192.168.0.11 slave1
    192.168.0.12 slave2
Test ob Nodes im lokalen Netzwerk erreichbar sind: 
    ping 192.168.0.11

3. Auf der Kommandozeile Testen ob Java installiert ist (auf allen Nodes muss Java installiert sein):  
    java -version

beispielhafte Ausgabe:
    openjdk version "1.8.0.232"
    OpenJDK Runtime Enviroment (build 1.8.0_232-b09)
    OpenJDK 64-Bit Server VM (build 25.232-b09, mixed mode)

3.1. Ausgabe des Java Paths:
    update-alternatives --display java

3.2 Java installieren, falls noch nicht vorhanden:
    sudo yum install -y java-1.8.0-openjdk

4. Hadoop User erstellen (auf allen Nodes): Zu Beginn wird empfohlen, einen separaten Benutzer für Hadoop zu erstellen, um das Hadoop-Dateisystem vom Unix-Dateisystem zu isolieren.
    su  # Befehle als root ausführen 
        password: 
    useradd hadoop  # Erstellen eines Benutzers aus dem Root-Konto 
    passwd hadoop 
        New passwd: 
        Retype new passwd 


5. Alle Einstellungen auf dem hadoop User ausführen, dafür den Benutzer wechseln:
    su hadoop

6. SSH konfigurieren (nur auf dem Master), damit die Nodes untereinander kommunizieren können (muss kein Passwort mehr auf den Nodes eingeben, dauerhafte Authentifizierung)
(SSH ist notwendig für verschiedene Clusteroperationen wie bspw. Starten eines Service):
    ssh-keygen -b 4096 #shh-Schlüssel erstellen 
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys 
    chmod 0600 ~/.ssh/authorized_keys 
    ssh-copy-id -i ~/.ssh/id_rsa.pub hadoop@slave1 #user@host
    ssh-copy-id -i ~/.ssh/id_rsa.pub hadoop@slave2  #die Schlüssel werden auf die Nodes kopiert und so konfiguriert, dass der Zugriff gewährt wird 
    ssh slave1 #Testen ob ssh Verbindung möglich ist 
    exit

7. Hadoop downloaden (Binary Version) und entpacken:
    cd /home/hadoop
    wget http://artfiles.org/apache.org/hadoop/common/hadoop-3.1.3/hadoop-3.1.3.tar.gz
    tar -xvf hadoop-3.1.3.tar.gz
    mv hadoop-3.1.3 hadoop

8. Hadoop zum Path hinzufügen:
    nano /home/hadoop/.profile
    PATH=/home/hadoop/hadoop/bin:/home/hadoop/hadoop/sbin:$PATH

9. Pfad von Hadoop zu den Umgebungsvariablen hinzufügen:
    nano /home/hadoop/.bashrc
    export HADOOP_HOME=/home/hadoop/hadoop
    export PATH=${PATH}:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin

10. Kommandozeile mitteilen, das .bashrc verändert wurde
    source /home/hadoop/.bashrc

11. Test auf der Kommandozeile ob $HADOOP_HOME richtig gesetzt wurde:
echo $HADOOP_HOME

12. cd $HADOOP_HOME/etc/hadoop
    1. Java Home in den Hadoop Einstellungen spezifizieren:
        nano hadoop-env.sh
        die Zeile: export JAVA_HOME= anpassen auf
        export JAVA_HOME=/usr/lib/jvm/jre-1.8.0-openjdk
    2. Testen ob Hadoop Path richtig gesetzt wurde:
        hadoop version
    3. Portnummer für den Name Node der Hadoop-Instanz spezifizieren: (hostname:port)
        nano core-site.xml
        <configuration>
            <property>
                <name>fs.default.name</name>
                <value>hdfs://master1:9000</value>
            </property>
        </configuration>
    4. HDFS Konfigurationen setzen: enthält Informationen über
    Replikationsfaktor und Speicherort der Daten auf den Data Nodes.
    Wichtig: Replikationsfaktor =< Anzahl Data Nodes/Slaves
        nano hdfs-site.xml
        <configuration>
            <property>
                    <name>dfs.namenode.name.dir</name>
                    <value>/home/hadoop/data/nameNode</value>
            </property>
            <property>
                    <name>dfs.datanode.data.dir</name>
                    <value>/home/hadoop/data/dataNode</value>
            </property>
            <property>
                    <name>dfs.replication</name>
                    <value>2</value>
            </property>
        </configuration>


    5. Yarn konfigurieren (YARN als Default-Framework für Map-Reduce Operationen festlegen)
        nano mapred-site.xml
        <configuration>
            <property>
                    <name>mapreduce.framework.name</name>
                    <value>yarn</value>
            </property>
            <property>
                    <name>yarn.app.mapreduce.am.env</name>
                    <value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value>
            </property>
            <property>
                    <name>mapreduce.map.env</name>
                    <value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value>
            </property>
            <property>
                    <name>mapreduce.reduce.env</name>
                    <value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value>
            </property>
        </configuration>

    6. Yarn konfigurieren (für yarn.resourcemanager.hostname die IP des Masters setzen)
        nano yarn-site.xml
        <configuration>
            <property>
                    <name>yarn.acl.enable</name>
                    <value>0</value>
            </property>
            <property>
                    <name>yarn.resourcemanager.hostname</name>
                    <value>192.168.0.10</value>
            </property>
            <property>
                    <name>yarn.nodemanager.aux-services</name>
                    <value>mapreduce_shuffle</value>
            </property>
        </configuration>


  7. Workers konfigurieren: (Wird von Startskripten verwendet, um erforderliche 
  Daemons auf allen Knoten zu starten), 
  den gesamten Dateiinhalt durch die Data Nodes Hostnamen ersetzten:
    nano workers
    slave1
    slave2

    Hinweis: Default-Datei Inhalt wie bspw. localhost muss gelöscht werden. 
    Die Datei und dessen Inhalt, wird in Schritt 13 auf 
    alle Data Nodes repliziert und ist somit auf alle Nodes konsistent.

    8. Memory Allocation konfigurieren
        1. Ausführliche Information siehe Abschnitt unten (im Bsp. Worker/Slave Nodes mit 2GB Ram)
        2. Die folgenden Zeilen hinzufügen:
            nano yarn-site.xml
            <property>
                    <name>yarn.nodemanager.resource.memory-mb</name>
                    <value>1536</value>
            </property>
            <property>
                    <name>yarn.scheduler.maximum-allocation-mb</name>
                    <value>1536</value>
            </property>
            <property>
                    <name>yarn.scheduler.minimum-allocation-mb</name>
                    <value>128</value>
            </property>
            <property>
                    <name>yarn.nodemanager.vmem-check-enabled</name>
                    <value>false</value>
            </property>
    3. Die folgenden Zeilen hinzufügen:
        nano mapred-site.xml
        <property>
                <name>yarn.app.mapreduce.am.resource.mb</name>
                <value>512</value>
        </property>
        <property>
                <name>mapreduce.map.memory.mb</name>
                <value>256</value>
        </property>
        <property>
                <name>mapreduce.reduce.memory.mb</name>
                <value>256</value>
        </property>


13. Konfigurationsdateien auf alle Data Nodes replizieren
    1. Hadoop Binary kopieren
        cd /home/hadoop/
        scp hadoop-*.tar.gz slave1:/home/hadoop
    2. Auf die Data Nodes mit ssh verbinden
        ssh slave1
    3. Das Binary entpacken
        tar -xzf hadoop-3.1.2.tar.gz
        mv hadoop-3.1.2 hadoop
        exit
    4. Für alle Data/Slave Nodes Schritt 1-3 wiederholen
    5. Die Konfigurationsdateien vom Master auf alle Data/Slave Nodes kopieren
        for node in slave1 slave2; do
            scp ~/hadoop/etc/hadoop/* $node:/home/hadoop/hadoop/etc/hadoop/;
        done

14. Firewall und Firewallzonen konfigurieren
    Für alle Nodes:
        su root 
        systemctl start firewalld.service #falls Firewall nicht gestartet ist 
        firewall-cmd --permanent --new-zone=Hadoop #erstellen einer neuen Firewall-Zone mit dem Namen Hadoop

    Für die Namenodes & Datanodes:
        firewall-cmd --zone=hadoop --add-port=8030/tcp --permanent
        ...

    Einstellungen neu laden:
        firewall-cmd --reload

15. Formatieren/Einrichten des Name Nodes
    hdfs namenode -format

16. Starten der DFS Daemon (HDFS), d.h. starten des Name Node, Secondary Name Node und der Data Nodes
    start-dfs.sh
Hinweis: Bei Ausführen des Befehls können Fehler auftreten, mögliche Fehlerquellen sind unten in einem Abschnitt aufegführt.

17. Starten des YARN Daemon
    start-yarn.sh

18. Information über das laufende HDFS Cluster ausgeben:
    hdfs dfsadmin -report

19. Status der Hadoop-Prozesse anzeigen lassen:
    jps
Hinweis: falls der jps Befehl nich gefunden wird yum install ant ausführen

20. Zugriff im Browser: [http://master1:9870/](http://master1:9870/)

Falls die Nodes nicht als aktiv angezeigt werden (unter Live Nodes), dass diese aktiv sind, muss die Firewall deaktiviert, bzw. richtig konfiguriert werden:

    sudo systemctl stop firewalld
    sudo systemctl disable firewalld
```
## Fehlerquellen und deren Lösung
```bash
Fehlerfall: 
Die Data Nodes werden nach start-dfs.sh Befehl nicht gestartet und sind unter Lives Nodes in der Weboberfläche sind aufzufinden.

Lösungsvariante: 
Durch erneutes Einrichten oder Vornehmen von Änderungen am Cluster im Master Node ist die aktuelle ClusterID mit den auf den Data Nodes konfigurierten ClusterID nicht identisch.
Auf den Datennodes unter /home/hadoop/hadoop/logs/hadoop-hadoop-datanode-slave1.log ist der Fehler mit der ClusterID sichtbar.

Auszuführende Befehle (auf dem Master):
  1. stop-dfs.sh && stop-yarn.sh
  2. hdfs namenode -format -clusterId CID-8bf63244-0510-4db6-a949-8f74b50f2be9

Hinweis: Die Aktuelle Cluster-ID ist in der Weboberfläche unter dem Reiter Overview zu finden.
  1. start-dfs.sh && start-yarn.sh
```