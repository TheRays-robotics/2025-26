void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}
float weight = 0;
void loop() {
  // put your main code here, to run repeatedly:

  if (Serial.available() > 0) {
    //weight = random(-1000,1000);
    String line = Serial.readStringUntil(10, 1000);

    //Serial.println(line);
    if (line != "") {
      float depth = line.toFloat();
      if (depth < 2.5) {

        weight += 20;
      }
      if (depth > 2.5) {
        weight -= 20;
      }
      weight = max(min(180, weight), 0);
      Serial.println(weight);
    }
  }
}
