#include <Coordinates.h>
#include <LobotServoController.h>

#define PI 3.1415926535897932384626433832795
#define rxPin 10
#define txPin 11

SoftwareSerial mySerial(rxPin, txPin);
LobotServoController myse(mySerial);
String incomingBytes;
int x,y;
Coordinates point = Coordinates();
int servoAng;
LobotServo servos[1];

void setup() {
 // put your setup code here, to run once:
 Serial.begin(115200);
 mySerial.begin(9600);
 pinMode(13, OUTPUT);
 digitalWrite(13, LOW);

}
String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void loop() {
 // put your main code here, to run repeatedly:
while (Serial.available() > 0) {
  incomingBytes = Serial.readStringUntil('\n');
  String xval = getValue(incomingBytes, ',', 0);
  String yval = getValue(incomingBytes, ',', 1);

  Serial.println("Y:" + yval);
  Serial.print("X:" + xval);
  int xvalue = xval.toInt();
  int yvalue = yval.toInt();
  point.fromCartesian(xvalue,yvalue);
  Serial.print("r: ");
  Serial.println(point.getR());
  Serial.print("φ: ");
  Serial.print(point.getAngle());
  Serial.println(" rad");
  int angle = point.getAngle() * (180/PI);
  Serial.println(angle);
  if(angle > 90)
  {
    angle = 90;
  }
  else if (angle < 0)
  {
    angle = 0;
  }
  angle = map(angle, 0,90,500,2500);
  Serial.println(angle);

  servos[0].ID = 6;
  servos[0].Position= angle;
  myse.moveServos(servos,6,1000);
  
  }
 }
