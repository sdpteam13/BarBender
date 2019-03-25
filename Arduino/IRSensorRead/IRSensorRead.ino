#include <QTRSensors.h>

//Create sensor object for 4 sensors on pins 4-7
QTRSensorsRC qtrrc((unsigned char[]) {4, 5, 6, 7}, 4, 5000, 3);
//Array of values from the sensor
unsigned int values[4];

bool docalibrate = false;

void setup() {
	Serial.begin(115200);
	if (docalibrate) {
		Serial.println("calibrating");
		for (int i = 0; i < 50; i++) {
			qtrrc.calibrate();
			delay(20);
		}
	}
	Serial.println("started");
}

void loop() {
	while (!Serial.available());
	Serial.read();
	
	if (docalibrate) {
		qtrrc.readCalibrated(values);
	} else {
		qtrrc.read(values);
	}
	
	Serial.print(values[0]);
	Serial.print(", ");
	Serial.print(values[1]);
	Serial.print(", ");
	Serial.print(values[2]);
	Serial.print(", ");
	Serial.print(values[3]);
	Serial.print("\n");
}