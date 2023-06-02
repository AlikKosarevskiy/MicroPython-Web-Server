# Here I will start network
import network

# Set up the WiFi connection
wifi_ssid = "..."
wifi_password = "..."

# Initialize the network module
sta_if = network.WLAN(network.STA_IF)

# Check if the WiFi interface is already connected
if not sta_if.isconnected():
    # Connect to the WiFi network
    sta_if.active(True)
    sta_if.connect(wifi_ssid, wifi_password)

    # Wait for the WiFi connection to complete
    while not sta_if.isconnected():
        pass

# Print the network configuration details
print("Network Configuration:", sta_if.ifconfig())
import webrepl
webrepl.start()
import main
