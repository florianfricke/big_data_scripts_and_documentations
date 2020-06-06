# Multi Node Hadoop Cluster - SPARK Installationsanleitung

## Erste Schritte
Die Anleitung verfolgt die im Verzeichnis Hadoop vorgestellte Multi Node Hadoop Architektur. 

### Vorraussetzungen um Spark einzurichten:
1. Hadoop und alle zugehörige Konfiguration, die in der Markdown Multi Node Hadoop Installation erläutert werden, sind installiert.
2. Führe auf der Kommandozeile des Master Nodes den Befehl `jps` aus, um zu kontrollieren ob HDFS und Yarn aktiv sind. 
\
Erwartete Ausgabe: \
12161 SecondaryNameNode \
11912 NameNode \
12392 ResourceManager

1. Falls HDFS und Yarn inaktiv sind, diese mit den folgenden Befehlen starten:
start-dfs.sh \
start-yarn.sh

## Spark installieren
Die folgenden Befehle sind auf dem Master Node auszuführen.
```bash
1. # # Spark downloaden
    wget http://mirror.checkdomain.de/apache/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz

2. tar -xvf spark-2.4.4-bin-hadoop2.7.tgz #

3.  # Spark Verzeichnis umbennen
    mv spark-2.4.4-bin-hadoop2.7 spark #

4.  # Pfad von Spark, Hadoop und Python zu den Umgebungsvariablen hinzufügen
    nano /home/hadoop/.bashrc
        export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
        export SPARK_HOME=/home/hadoop/spark
        export PATH=$PATH:$SPARK_HOME/bin
        export LD_LIBRARY_PATH=$HADOOP_HOME/lib/native:$LD_LIBRARY_PATH
        export PYSPARK_PYTHON=/usr/bin/python3

5.  # Kommandozeile mitteilen, das .bashrc verändert wurde
    source /home/hadoop/.bashrc #

6.  # Spark Default Template Config Datei umbennen
    mv $SPARK_HOME/conf/spark-defaults.conf.template $SPARK_HOME/conf/spark-defaults.conf

Zu Schritt 7: die Konfigurationsparameter können fest in der Datei hinterlegt werden oder bei jedem Ausführen eines Spark-Skripts mit Spark Submit an den Befehl angehängt werden. (siehe folgender Abschnitt)

7.  # optional
    nano $SPARK_HOME/conf/spark-defaults.conf
        spark.master yarn
        spark.driver.memory 512m
        spark.yarn.am.memory 512m
        spark.executor.memory 512m

Spark History Server konfigurieren
Spark bietet die Möglichkeit mit dem Spark History Server, Logs der Skript- bzw. Jobausführungen in HDFS zu speichern und in einer Weboberfläche anzuzeigen.

8. # Diese Zeilen der Datei hinzufügen.
    nano $SPARK_HOME/conf/spark-defaults.conf
        spark.eventLog.enabled  true
        spark.eventLog.dir hdfs://192.168.0.10:9000/spark-logs
        spark.history.provider            org.apache.spark.deploy.history.FsHistoryProvider
        spark.history.fs.logDirectory     hdfs://192.168.0.10:9000/spark-logs
        spark.history.fs.update.interval  5s
        spark.history.ui.port  18080


9.  # Anlegen eines Verzeichnisses für die Log-Dateien im HDFS.
    hdfs dfs -mkdir /spark-logs

10. # Port für die Web-UI des History Servers bei der Firewall freischalten.
    su
    firewall-cmd --zone=public --add-port=18080/tcp --permanent
    firewall-cmd –reload
    su hadoop


11. # Starten des History Servers.
    $SPARK_HOME/sbin/start-history-server.sh 
    Erreichbar unter: http://192.168.0.10:18080
```

## Spark Submit: Spark Scripts ausführen
Alternativ kann ein Jupyter Notebook verwendet werden um Spark Code auszuführen.
```bash
# Ein Python Skript wird mit Spark-Submit ausgeführt.
$SPARK_HOME/bin/spark-submit load_df.py

# Das Skript wird im Client Modus über Yarn ausgeführt.
$SPARK_HOME/bin/spark-submit --master yarn --deploy-mode client load_df_example.py

# Das Skript wird im Cluster Modus über Yarn ausgeführt.
$SPARK_HOME/bin/spark-submit --master yarn --deploy-mode cluster load_df_example.py

# Konfiguration der Memory Allocation beim Ausführen eines Skriptes.
$SPARK_HOME/bin/spark-submit --master yarn --deploy-mode cluster --driver-memory 512m --executor-memory 512m load_df_example.py

# Ausführen eines Python Files unter Verwendung eines zusätzlichen Packages. (im Beispiel: Apache Bahir)
$SPARK_HOME/bin/spark-submit --packages org.apache.bahir:spark-streaming-mqtt_2.11:2.3.2 ~/spark_scripts/spark_streaming_mqtt_data_to_hdfs.py

# Starten der Spark-Shell über Yarn.
$SPARK_HOME/bin/spark-shell --master yarn
```