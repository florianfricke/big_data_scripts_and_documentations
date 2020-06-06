# HDFS

#### Daten in das HDFS speichern
Vorgehensweise zur Speicherung der Sensordaten in das HDFS:

``` bash
# Verzeichnis im HDFS anlegen
1. hdfs dfs -mkdir Iot_data

# Inhalt des HDFS Verzeichnisses auslesen
2. hdfs dfs -ls Iot_data

# Lokal gespeicherte Sensor-Daten in das HDFS Verzeichnis speichern
3. hdfs dfs -put ... Iot_data
```

#### Couch DB Daten extrahieren und in das HDFS speichern

``` bash
# Die Inhalte der Datenbank können über einen Link, der die Daten in json-Format ausgibt, abgerufen werden.
curl -X GET http://192.168.0.20:8080/sensor_data/_all_docs?include_docs=true >> ./sensor_data.json
```