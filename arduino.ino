const int solenoidPins[12] = {2,3,4,5,6,7,8,9,10,11,12,13};
const int NUM_SOLENOIDS = 12;
const int PULSE_DURATION = 200;

void setup() {
  Serial.begin(115200);
  while (!Serial) {}

  Serial.println("Arduino ready.");

  for(int i = 0; i < NUM_SOLENOIDS; i++){
    pinMode(solenoidPins[i], OUTPUT);
    digitalWrite(solenoidPins[i], LOW);
  }
}

void loop() {

  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    Serial.print("Received: ");
    Serial.println(input);
    if (input.length() == NUM_SOLENOIDS) {
      Serial.println("Length OK, firing solenoids...");

      for (int i = 0; i < NUM_SOLENOIDS; i++) {
        if (input.charAt(i) == '1') {
          digitalWrite(solenoidPins[i], HIGH);
          Serial.print("Solenoid ");
          Serial.print(i);
          Serial.println(" -> ON");
        } else {
          digitalWrite(solenoidPins[i], LOW);
          Serial.print("Solenoid ");
          Serial.print(i);
          Serial.println(" -> OFF");
        }
      }

      delay(PULSE_DURATION);

      for (int i = 0; i < NUM_SOLENOIDS; i++) {
        digitalWrite(solenoidPins[i], LOW);
      }

      Serial.println("Pulse complete. All OFF.");
    } 
    else {
      Serial.print("ERROR: Expected 12 chars, got ");
      Serial.println(input.length());
    }

    Serial.println("---");
  }
}
