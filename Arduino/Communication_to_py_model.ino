 // Example pin to indicate response
const int trigPin = 9;
const int echoPin = 10;
const int ledPin = 13;


int in1 = 2;
int in2 = 4;
int enA = 3;


// Variables for storing distance and duration
long duration;
int distance;

// Flag to control the while loop
boolean stopCar = false;


void setup() {
  Serial.begin(9600);  // Initialize serial communication

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPin, OUTPUT);

  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(enA, OUTPUT);
}

void loop() {

    // Trigger the ultrasonic sensor
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read the echo pulse duration in microseconds
  duration = pulseIn(echoPin, HIGH);

  // Calculate distance in centimeters
  distance = duration * 0.034 / 2;

  if (Serial.available() > 0) {
    String response = Serial.readString();  // Read response from Python
    Serial.print("Received response: ");
    Serial.println(response);

    // Example of handling response
    if (response == "Move") {
        digitalWrite(in1, HIGH);
        digitalWrite(in2, LOW);
        analogWrite(enA, 100);  // Turn on LED

        if (distance <= 15) {
          digitalWrite(ledPin, HIGH); // Turn on the LED
          
          // Stop the motors immediately
          digitalWrite(in1, LOW);
          digitalWrite(in2, LOW);
          digitalWrite(in3, LOW);
          digitalWrite(in4, LOW);
          analogWrite(enA, 0);
          analogWrite(enB, 0);
          
          // // Back up for a short duration to prevent collision
          digitalWrite(in1, HIGH);
          digitalWrite(in2, LOW); // Reverse left motor
          digitalWrite(in3, HIGH);
          digitalWrite(in4, LOW); // Reverse right motor
          analogWrite(enA, 100); // Set motor speed to maximum
          analogWrite(enB, 100); 

          delay(250);   
          // Stop the motors again
          digitalWrite(in1, LOW);
          digitalWrite(in2, LOW);
          digitalWrite(in3, LOW);
          digitalWrite(in4, LOW);
          analogWrite(enA, 0);
          analogWrite(enB, 0);
          delay(1000); // Adjust the duration as needed
          
          // Set the stopCar flag to true
          stopCar = false;




        } 
        else {
          digitalWrite(ledPin, LOW); // Turn off the LED
          
          // Move the car forward
          digitalWrite(in1, LOW);
          digitalWrite(in2, HIGH); // Forward left motor
          digitalWrite(in3, LOW);
          digitalWrite(in4, HIGH); // Forward right motor
          analogWrite(enA, 100); // Set motor speed to maximum
          analogWrite(enB, 100); // Set motor speed to maximum
          
          // Reset the stopCar flag to false
          stopCar = false;
        }

          while (stopCar) {
            // Stop the motors
            digitalWrite(in1, LOW);
            digitalWrite(in2, LOW);
            digitalWrite(in3, LOW);
            digitalWrite(in4, LOW);
            analogWrite(enA, 0);
            analogWrite(enB, 0);
          }

    } else if (response == "Stop") {
        digitalWrite(in1, LOW);
        digitalWrite(in2, LOW);
        analogWrite(enA, 0);  // Turn off LED
    }
  }
}
