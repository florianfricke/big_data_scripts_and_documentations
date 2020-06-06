# Kafka Basics

### **Zookeeper starten**
```bash
1. neuen Ordner anlegen:
    data/kafka und data/zookeeper

2. config/zookeeper.properties anpassen: dataDir=C:/kafka_2.12-2.3.0/data/zookeeper

3. Zookeeper Server starten: 
zookeeper-server-start.bat C:\kafka_2.12-2.3.0\config\zookeeper.properties
```

### **Kafka starten**
```bash
1. neue Kommandozeile öffnen

2. config/server.properties anpassen: log.dirs=C:/kafka_2.12-2.3.0/data/kafka

4. Kafka Server starten
    kafka-server-start.bat C:\kafka_2.12-2.3.0\config\server.properties
```

### **Kafka Topic**
```bash
# Topic erstellen
kafka-topics.bat --zookeeper localhost:2181 --create --replication-factor 1 --partitions 3 --topic first_topic

# Auflisten aller Topics
kafka-topics --zookeeper localhost:2181 --list

# Eigenschaften eines Topics anzeigen (Leader = BrokerID)
kafka-topics --zookeeper localhost:2181 --topic first_topic --describe
```
**Retention Time:** Zeit in ms nach welcher die Nachrichten eines Topics gelöscht werden


### **Kafka CLI Producer**
```bash
# Producer erstellen
kafka-console-producer.bat --broker-list localhost:9092 --topic first_topic

# zusätliche Eigenschaften
kafka-console-producer.bat --broker-list localhost:9092 --topic first_topic --producer-propertry acks=all
```

### **Kafka CLI Consumer**
```bash
# Consumer erstellen und Nachrichten empfangen
kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic first_topic

# auch historische Messages im Topic anzeigen
--from-beginning

# Consumer Group
--group application_consumer

# Consumer Groups auflisten
kafka-consumer-groups.bat --bootstrap-server localhost:9092 --list

# Beschreibungen der Consumer Group anzeigen lassen 
# (LAG=0, die Daten wurden schon abgerufen)
kafka-consumer-groups.bat --bootstrap-server localhost:9092 --describe --group console-consumer-91118
```

