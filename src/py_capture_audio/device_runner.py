import sounddevice as sd

for i, dev in enumerate(sd.query_devices()):
    print(f"Device {i}: {dev['name']}")
    print(f"  Max input channels: {dev['max_input_channels']}")
    print(f"  Max output channels: {dev['max_output_channels']}")
    print(f"  Default samplerate: {dev['default_samplerate']}\n")