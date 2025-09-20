// Demonstration of MQTT with Raspberry Pi
// Interfacing LED to NodeMCU & controlling from NodeRED over MQTT Protocol from Raspberry pi
// Date : 06 / 07 / 2025
// Libraries Required as following : 
// Arduino JSON (Benoit Blanchon) - v7.3.1 (Install from library manager)
// PubSubClient (Nick O'Leary) - v2.8 (https://github.com/knolleary/pubsubclient)


#ifdef ESP8266
#include <ESP8266WiFi.h>
#elif defined(ESP32)
#include <WiFi.h>
#else
#error "Board not found"
#endif

#include <PubSubClient.h>

#define Relay1            16      // D0 pin of NodeMCU


const char* ssid = "Your Wifi Name";
const char* password = "Your WiFi Password";
const char* mqtt_server = "IP address of Raspberry pi"; // Local IP address of Raspberry Pi

const char* username = "";    // leave this blank if there is no credential
const char* pass = "";        // leave this blank if there is no credential

#define sub1 "device1/lamp1"

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE	(50)

char msg[MSG_BUFFER_SIZE];
int value = 0;

void setup_wifi()
{
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);   //station mode
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length)
{
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");

  //strstr is used to trace the substring in main string
  //Here it is used to trace the message i.e. payload in subscribed topic
  if (strstr(topic, sub1))  
  {
    for (int i = 0; i < length; i++)
    {
      Serial.print((char)payload[i]);
    }
    Serial.println();
    // Switch on the LED if an 1 was received as first character
    if ((char)payload[0] == '1')
    {
      digitalWrite(Relay1, HIGH);
    } 
    else 
    {
      digitalWrite(Relay1, LOW); 
    }
  }
  else
  {
    Serial.println("unsubscribed topic");
  }

}

void reconnect()
{

  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);    
    if (client.connect(clientId.c_str() , username, pass)) 
    {
      Serial.println("connected");
      //client.publish("outTopic", "hello world");
      client.subscribe(sub1);
    } 
    else 
    {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}



void setup()
{

  pinMode(Relay1, OUTPUT);

  Serial.begin(115200);

  setup_wifi();

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop()
{

  if (!client.connected()) 
  {
    reconnect();
  }
  client.loop();

}
