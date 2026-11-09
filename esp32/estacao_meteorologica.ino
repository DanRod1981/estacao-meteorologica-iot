#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "Teste_unifi";
const char* password = "teste123";

const char* servidor = "192.168.10.250";

void setup() {

  Serial.begin(115200);

  dht.begin();

  Serial.println("Conectando ao WiFi...");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi conectado!");
}

void loop() {

  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {

    Serial.println("Erro ao ler DHT22");

    delay(2000);
    return;
  }

  if (WiFi.status() == WL_CONNECTED) {

    HTTPClient http;

    String url =
      String("http://") + servidor + ":5000/dados?temp=" + String(t, 1) + "&umi=" + String(h, 1);

    Serial.println(url);

    http.begin(url);

    int codigo = http.GET();

    Serial.print("HTTP: ");
    Serial.println(codigo);

    http.end();
  }

  delay(5000);
}