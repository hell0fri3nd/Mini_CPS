const int led1 = 7;
const int led2 = 8;
const int led_0 = 4;
const int del = 1000;

const int ldrPin = A0;
const int tempPin = 1;

int val;
float avgTemp;
float avgLight;
String data_out="";

int i;
int e;
boolean processing = 0;
boolean incoming_state = 0;
String data_in="";

void setup() {
Serial.begin(9600);
pinMode(led1, OUTPUT);
pinMode(led2, OUTPUT);
pinMode(led_0, OUTPUT);
pinMode(ldrPin, INPUT);
}

void loop() {
  
  Serial.print("idle\n");
  
  while(processing == 0){
    // Resests to avoid blocking by wrong input
    data_in = "";
    
    digitalWrite(led_0, HIGH);
    delay(del);
    digitalWrite(led_0, LOW);
    
    // Checks raspberry start order
    while (Serial.available() > 0){
          
      incoming_state = (Serial.read() - '0');
      data_in += incoming_state;
   
      if(Serial.available() == 0) {
        if(data_in == "0"){
          processing = 0;
        } else if (data_in == "1") {
          processing = 1;
        }
      }      
    }
    
    delay(del);
  }
  
  while(processing == 1){
    // --- [Starting] Process 1 ---
    for(i=0; i<=9; i++){      
      digitalWrite(led1, HIGH);
      delay(del);
      digitalWrite(led1, LOW);
      
      val = analogRead(tempPin);
      float mv = ( val/1024.0)*5000;
      float cel = mv/10;
      
      avgTemp = (avgTemp + cel) / 2;
      
      delay(del);
    }    
    
    // --- Process 1 done ---
    // --- [Starting] Process 2 ---
      
    for(e=0; e<=9; e++){      
      digitalWrite(led2, HIGH);
      delay(del);
      digitalWrite(led2, LOW);
      
      int ldrStatus = analogRead(ldrPin);
      avgLight = (avgLight + ldrStatus) / 2;
      
      delay(del);
    }
      
      // --- Process 2 done ---
      
      // Resets
      data_in = "";
      processing = false;
      
      digitalWrite(led1, HIGH);
      digitalWrite(led2, HIGH);
      digitalWrite(led_0, HIGH);
      
      // Notifying Raspberry 
      data_out = String(avgTemp) + ", " + String(avgLight) + "\n";
      Serial.print(data_out);
      
      delay(del*4);
      
      digitalWrite(led1, LOW);
      digitalWrite(led2, LOW);
      digitalWrite(led_0, LOW);
  }
}
