//int action = 0;
bool startReady;
bool loginReady;

//int resetPin = 7;/
int highPin = 5;
int startPin = 6;
int loginPin = 7;
int badEndingPin = 8;
int goodEndingPin = 9;
int mazeSolvedPin = 10;
int delayTime = 10000;

void setup()
{
  pinMode(highPin, OUTPUT);
  pinMode(startPin, INPUT);
  pinMode(loginPin, INPUT);
  pinMode(mazeSolvedPin, OUTPUT);
  pinMode(goodEndingPin, OUTPUT);
  pinMode(badEndingPin, OUTPUT);
  //pinMode(resetPin, INPUT);

  digitalWrite(highPin, HIGH);
  startReady = true;
  loginReady = true;
  
  Serial.begin(9600);
  //Serial.write("Process Started:");
}

void loop()
{
    while(Serial.available()){
        String message = Serial.readString();
        message.trim();
        //Serial.println("Arduino:" + message);
        to_cogs(message);
        //action(Serial.parseInt());
     }
    if(digitalRead(startPin) == HIGH) {
        Serial.println("Game Started");
        //action(1);
        //startReady = false;
        delay(delayTime);
    }
    if(digitalRead(loginPin) == HIGH) {
        Serial.println("Show Login");
        //action(2);
        //loginReady = false;
        delay(delayTime);
    }
    else{
        Serial.println("N/A");
        delay(delayTime);
    }
}

void to_cogs(String a)
{
    if(a == "Maze Solved"){
      digitalWrite(mazeSolvedPin, HIGH);
    }
    else if(a == "Good Ending"){
      digitalWrite(goodEndingPin, HIGH);
    }
    else if(a == "Bad Ending"){
      digitalWrite(badEndingPin, HIGH);
    }
    //Serial.println("Arduino: " + a);
}

void toggle(int pin)
{
  bool pinState = digitalRead(pin);
  digitalWrite(pin, !pinState);
}

void reset()
{
  startReady = true;
  loginReady = true;
  digitalWrite(mazeSolvedPin, LOW);
  digitalWrite(goodEndingPin, LOW);
  digitalWrite(badEndingPin, LOW); 
}
