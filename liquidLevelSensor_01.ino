int resval = 0;  // holds the value
int respin = A0; // sensor pin used
 
void setup() {
 
  // start the serial console
  Serial.begin(9600);
}
 
void loop() {
 
  resval = analogRead(respin); //Read data from analog pin and store it to resval variable
 
  if (resval <= 100) {
    Serial.print("Water Level: Empty    resval: ");
    Serial.println(resval);
  }
  else if (resval > 100 && resval <= 300) {
    Serial.print("Water Level: Low    resval: ");
    Serial.println(resval);
  }
  else if (resval > 300 && resval <= 330) {
    Serial.print("Water Level: Medium   resval: ");
    Serial.println(resval);
  }
  else if (resval > 330) {
    Serial.print("Water Level: High   resval: ");
    Serial.println(resval);
  }
  delay(1000);
}
