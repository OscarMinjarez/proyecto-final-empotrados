#include <HTTPClient.h>
#include <WiFi.h>
#include <ArduinoJson.h>

const char* ssid = "IoT_LV323";
const char* password = "@dm1nLV323";

// Definir pines para el sensor ultrasónico
const int trigPin = 16;  // Pin de disparo
const int echoPin = 17; // Pin de eco
HTTPClient http;
// Definir variables
long duracion;
int distancia;

// Function prototype
void sendToServer(int distancia);

// Variables para gestionar el tiempo
unsigned long previousMillis = 0;
const long interval = 5000;  // Intervalo de tiempo en milisegundos (5 segundos)

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }
  Serial.println("Conectado a la red WiFi");
}

void loop() {
  // Obtener el tiempo actual
  unsigned long currentMillis = millis();

  // Verificar si ha pasado el intervalo de tiempo
  if (currentMillis - previousMillis >= interval) {
    // Actualizar el tiempo de la última ejecución
    previousMillis = currentMillis;

    // Realizar la medición y enviar la petición
    measureAndSend();
  }
}

void measureAndSend() {
  // Limpiar el pin de disparo
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Enviar pulso ultrasónico
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Medir la duración del eco
  duracion = pulseIn(echoPin, HIGH);

  // Calcular la distancia en centímetros
  distancia = duracion * 0.034 / 2;

  // Mostrar la distancia en el monitor serial
  Serial.print("Distancia: ");
  Serial.print(distancia);
  Serial.println(" cm");
  
  // Llamar a la función sendToServer con el parámetro de distancia
  sendToServer(distancia);
}

void sendToServer(int distance) {
  if (WiFi.status() == WL_CONNECTED) {
    String serverIp = "10.175.10.213";
    int serverPort = 3000;

    String url = "http://" + serverIp + ":" + String(serverPort) + "/cantidades";
    http.begin(url);

    DynamicJsonDocument jsonDoc(200);
    jsonDoc["cantidad"] = distance;
    jsonDoc["recipiente_id"] = 1;

    String jsonString;
    serializeJson(jsonDoc, jsonString);

    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonString);

    if (httpResponseCode > 0) {
      Serial.print("Respuesta del servidor: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.println("Error en la conexión");
    }

    http.end();
  }
}
