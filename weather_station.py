import Adafruit_DHT
import time
from datetime import datetime
import json
import os
from RPLCD.i2c import CharLCD

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  

LCD_I2C_PORT = 1  
LCD_I2C_ADDRESS = 0x27  
lcd = CharLCD(i2c_expander='PCF8574', address=LCD_I2C_ADDRESS, port=LCD_I2C_PORT, cols=16, rows=2)

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def read_sensor():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    return humidity, temperature

def update_lcd(temperature, humidity):
    try:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string(f"Temp: {temperature:.1f}C")
        lcd.cursor_pos = (1, 0)
        lcd.write_string(f"Humidity: {humidity:.1f}%")
    except Exception as e:
        print(f"LCD Error: {e}")

def save_data(humidity, temperature):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    data = {
        "timestamp": timestamp,
        "temperature": temperature,
        "humidity": humidity
    }
    
    date = datetime.now().strftime("%Y-%m-%d")
    filename = os.path.join(DATA_DIR, f"weather_data_{date}.json")
    
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                file_data = json.load(f)
                file_data.append(data)
        else:
            file_data = [data]
            
        with open(filename, 'w') as f:
            json.dump(file_data, f, indent=4)
            
    except Exception as e:
        print(f"Error saving data: {e}")

def main():
    print("Starting Weather Station...")
    print("Press CTRL+C to exit")
    
    try:
        lcd.clear()
        lcd.write_string("Weather Station")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Starting...")
        time.sleep(2)
        
        while True:
            humidity, temperature = read_sensor()
            
            if humidity is not None and temperature is not None:
                print(f"Temp={temperature:.1f}°C  Humidity={humidity:.1f}%")
                update_lcd(temperature, humidity)
                save_data(humidity, temperature)
            else:
                print("Failed to retrieve data from DHT11 sensor")
                lcd.clear()
                lcd.write_string("Sensor Error!")
            
            time.sleep(300)
            
    except KeyboardInterrupt:
        print("\nExiting Weather Station")
        lcd.clear()
        lcd.write_string("Shutting down...")
        time.sleep(2)
        lcd.clear()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            lcd.clear()
        except:
            pass

if __name__ == "__main__":
    main()
