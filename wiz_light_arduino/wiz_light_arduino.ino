int buttonPin = 9;

boolean released = true;

void setup() {
  // setup the button and start the serial
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600);
  while (! Serial);
  Serial.println("Ready");
}

void loop() {
  // if button pressed, then send 1.
  if(digitalRead(buttonPin) == LOW && released) {
    if (Serial) {
      Serial.print(1);
      released = false;
    }
  } else if(digitalRead(buttonPin) == HIGH) {
    released = true;
  }
}
