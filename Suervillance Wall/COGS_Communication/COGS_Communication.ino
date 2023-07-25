//int action = 0;
bool startReady;
bool loginReady;

//int resetPin = 7;/
int startPin = 6;
int loginPin = 7;
int mazeSolvedPin = 10;
int goodEndingPin = 9;
int badEndingPin = 8;
int delayTime = 1000;
int highPin = 5;


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
        action(Serial.parseInt());
     }
   /*if(digitalRead(resetPin) == HIGH)
    {
        Serial.println("Reset");
        reset();
        delay(delayTime);
    }*/
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
    /*else
    {
      if(Serial.available()){
        action(Serial.parseInt());
      }
    }*/
}
void action(int a)
{
      switch (a) {
        case 1:
          //startReady = false;
          Serial.println("Game Started");
          break;
        case 2: 
          //loginReady = false;
          Serial.println("Show Login");
          break;
        case 21845:
        case -10923:
        case 3:
          digitalWrite(mazeSolvedPin, HIGH);
          Serial.println("Maze Solved");
          //delay(5000);
          break;
        case -14564:
        case 4:
          digitalWrite(goodEndingPin, HIGH);
          Serial.println("Good Ending");
          //delay(5000);
          break;
        case -18205:
        case 5:
          digitalWrite(badEndingPin, HIGH);
          Serial.println("Bad Ending");
          //delay(5000);
          break;
        case 6:
          reset();
          Serial.println("Game Reset");
          break;
        default:
          Serial.println(a);
          break;
    }
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
