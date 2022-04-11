#define PIN_OUT 4
#define PIN_ALIM 5 // Alimentation du circuit par une pin GPIO...
#define C_ON 'o'
#define BAUD_RATE 115200

bool state = false;

void setup() {
  pinMode(PIN_OUT,OUTPUT);
  pinMode(PIN_ALIM,OUTPUT);
  digitalWrite(PIN_ALIM,HIGH);
  digitalWrite(PIN_OUT,LOW);
  Serial.begin(BAUD_RATE);
}

void loop() {
  if (Serial.available() > 0)
  {
    char c = Serial.read();
    Serial.println(c);
    if (c == C_ON)
    {
      state = !state;
      if (state)
        digitalWrite(PIN_OUT, HIGH);
      else
        digitalWrite(PIN_OUT, LOW);
    }
  }
}
