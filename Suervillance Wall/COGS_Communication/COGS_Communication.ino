//int action = 0;
//int resetPin = 7;
//Used as 5V
int highPin = 5;

int startPin = 6;
int loginPin = 7;
bool start = LOW;
bool login = LOW;

int badEndingPin = 8;
int goodEndingPin = 9;
int mazeSolvedPin = 10;
int delayTime = 500;

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
  
  Serial.begin(9600);
  //Serial.write("Process Started:");
}

void loop()
{
    while(Serial.available()){
        String message = Serial.readString();
        message.trim();
        to_cogs(message);
     }
     
    read_once(startPin,&start,"Game Started");
    read_once(loginPin,&login,"Show Login");
    
    Serial.println("N/A");
    delay(delayTime);
}

//Will Send One Msg Per if from LOW -> HIGH
//Prevents multiple msg outs from Arduino
void read_once(int pin, bool *prev, String msg){
  bool temp = digitalRead(pin);
  if(*prev != temp){
      *prev = temp;
      if(*prev){Serial.println(msg);}
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
  digitalWrite(mazeSolvedPin, LOW);
  digitalWrite(goodEndingPin, LOW);
  digitalWrite(badEndingPin, LOW); 
}
