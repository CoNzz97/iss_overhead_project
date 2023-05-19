import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 53.408371  # Your latitude
MY_LONG = -2.991573  # Your longitude
MY_EMAIL = "pythontesting1111@gmail.com"
PASSWORD = "yvduawqkmfyzzplr"
GMAIL_SMTP = "smtp.gmail.com"


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.

    if round(iss_latitude) in range(48, 59) and round(iss_longitude) in range(-7, 4):
        return True
    else:
        print("Not Overhead")


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}


def is_night():
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    current_hour = time_now.hour
    if current_hour >= sunset or current_hour <= sunrise:
        return True
    else:
        print("Not Dark Enough")


# If the ISS is close to my current position
# and it is currently dark
def main():
    if is_iss_overhead() and is_night():
        # Then send me an email to tell me to look up.
        with smtplib.SMTP(GMAIL_SMTP) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="pythontesting100@myyahoo.com",
                msg="Subject:Look Up!\n\n"
                    "The ISS is currently overhead!"
            )
    else:
        print("Sleeping for 60 seconds")
        time.sleep(60)
        print("Checking again")
        main()
# BONUS: run the code every 60 seconds.
main()