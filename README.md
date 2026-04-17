Billy Bot

A Raspberry Pi–based voice assistant designed for continuous operation, combining speech recognition, audio playback, API integration, and offline fallback systems.

Billy Bot is not an AI model — it is a deterministic voice system built from modular components that simulate assistant-like behaviour through structured logic, audio orchestration, and external data retrieval.

Overview

Billy Bot operates as a wake-word activated voice assistant:

Listens for wake word (“billy”)
Captures user speech via microphone
Routes input through speech recognition (Google STT primary, Vosk fallback)
Processes intent using rule-based logic
Responds using either:
Pre-recorded voice clips (pygame)
Text-to-speech (pyttsx3)
External API data (requests)

The system is designed for long-running, low-intervention execution on Raspberry Pi hardware.

Core Capabilities
Functional Features
Real-time weather (Open-Meteo API)
Current time and date
Natural language timers
News lookup (GNews API)
Basic arithmetic via spoken input
System uptime tracking
Birthday countdown calculations
Interactive Systems
Number guessing game (1–100, hint-driven)
Truth or dare engine
Coin flip simulation
Magic 8-ball responses
Yes/No oracle
“Am I cooked” random evaluation system
Personality Layer
Pre-recorded voice response library
Jokes, roasts, hype messages
Affirmations and negative responses
Emotional state responses (tired, bored, etc.)
Greeting and shutdown sequences
~50 structured personality outputs
System Features
Wake word detection: “billy”
Continuous runtime loop (24/7 capable)
Bluetooth and wired audio support
Offline speech recognition fallback (Vosk)
Automatic audio routing via PulseAudio
Architecture

Billy Bot is structured around two primary output pathways:

play(filename)

Plays pre-recorded .mp3 audio files using pygame.

Handles all personality-based responses
Automatically resolves file paths using runtime directory
Blocks until playback completes
Prevents concurrent playback via RLock
say(text)

Fallback text-to-speech engine using pyttsx3.

Used for dynamic responses (weather, calculations, timers)
Activated when no audio clip exists
Runs through shared audio lock to prevent overlap
Audio Synchronisation

A re-entrant lock (threading.RLock) ensures:

No simultaneous audio playback
Safe nested calls (e.g., missing clip → fallback to TTS)
Stable multi-threaded audio behaviour
Speech Recognition Pipeline
Primary: Google Speech-to-Text
High accuracy
Low latency
Requires internet connection
Fallback: Vosk (Offline Model)
Fully local processing
No internet dependency
Used automatically on API failure
Error Handling Strategy
RequestError → fallback to Vosk
WaitTimeoutError → ignored and loop continues
Dual-layer redundancy ensures continuous operation
Timer System

Billy Bot includes a natural language duration parser capable of interpreting mixed-unit time expressions.

Supported Input Examples
“2 hours 15 minutes”
“45 minutes”
“1 hour 30 seconds”
“2 hours and 15 minutes and 30 seconds”
Algorithm Overview

The system:

Tokenises spoken input into words
Converts number words into integers using word2number
Tracks contextual pairing between numbers and time units
Accumulates total duration in seconds
Executes a non-blocking timer thread
Core Implementation Concept
Stateless word iteration
Last-number carry model
Unit-based conversion multipliers:
seconds → ×1
minutes → ×60
hours → ×3600
Execution Model
Uses threading.Timer
Non-blocking (main loop remains active)
Triggers audio notification upon completion
Dependencies
Python Packages
SpeechRecognition → microphone input handling
pygame → audio playback engine
requests → external API communication
pyttsx3 → offline speech synthesis
vosk → offline speech recognition model
word2number → speech numeric parsing
System Packages (Raspberry Pi / Linux)
espeak, espeak-ng, espeak-ng-data → TTS backend
portaudio19-dev → microphone interface
flac → speech recognition encoding support
sox → audio generation utilities
pulseaudio, bluez → Bluetooth audio stack
Setup Summary
System Installation
sudo apt install python3-pip espeak espeak-ng espeak-ng-data portaudio19-dev flac sox git -y
Python Dependencies
pip install SpeechRecognition pygame pyttsx3 requests vosk word2number --break-system-packages
Required External Components
Vosk model: vosk-model-small-en-us-0.15
GNews API key (user-specific)
Voice clip library (/Voices)
Optional Bluetooth speaker pairing via PulseAudio
File Structure
billy/
├── assistant.py
├── vosk-model-small-en-us-0.15/
├── Voices/
│   ├── startup.mp3
│   ├── greeting.mp3
│   ├── joke1.mp3
│   └── ...
├── bt-connect.sh
└── billy.log
Runtime Behaviour
Startup Sequence
Audio subsystem initialises
Speech model loads
Wake word listener begins
Startup audio clip plays
Main Loop
Microphone listens continuously
Input routed through recognition pipeline
Intent resolved via rule-based matching
Response dispatched via play() or say()
Persistence
Runs indefinitely unless manually interrupted
Designed for boot-level execution via cron
Boot Configuration
Bluetooth Setup (optional)
@reboot /home/[user]/bt-connect.sh
@reboot sleep 30 && pulseaudio --start && sleep 10 && cd /home/[user]/billy && python3 assistant.py >> /home/[user]/billy/billy.log 2>&1 &
Wired Audio
@reboot sleep 15 && cd /home/[user]/billy && python3 assistant.py >> /home/[user]/billy/billy.log 2>&1 &
Known Issues
Audio System
Bluetooth audio may disconnect due to PulseAudio instability
Incorrect default sink causes silent playback
Missing espeak-ng-data results in silent TTS failure
Speech Recognition
Missing flac causes silent Google STT failure
Microphone device conflicts may require reboot
Incorrect Vosk model path breaks offline fallback
File Handling
Incorrect audio formats (e.g. .mp4) are unsupported by pygame
Case-sensitive filenames can break startup sequences
Error Handling Summary

The system is designed around graceful degradation:

Online STT fails → offline STT activated
Missing audio clip → TTS fallback
API failure → local response or skip
Thread conflicts → locked audio queue prevents corruption

No single failure should terminate runtime execution.

What Went Wrong (Development Constraints)
PyAudio incompatibility with newer Python versions prevented standard microphone stack usage
pipwin proved unreliable and outdated for dependency resolution
playsound lacked stability and control for continuous audio systems
Bluetooth audio required manual PulseAudio configuration due to inconsistent device handling
Vosk configuration issues were sensitive to minor API and path errors
Audio format mismatches (mp4 vs mp3) caused silent failures without errors
Missing system dependencies (flac, espeak-ng-data) produced non-obvious failure states
What Was Learned
Speech systems fail silently unless explicitly instrumented
Raspberry Pi audio stacks require manual orchestration rather than default configurations
Thread-safe audio handling is essential in multi-response systems
Offline fallback systems are not optional in real-world assistant design
File format consistency is critical in media pipelines
Deterministic rule-based systems can achieve reliable assistant behaviour without ML models
Design Philosophy

Billy Bot prioritises:

Deterministic behaviour over probabilistic inference
System reliability over feature complexity
Explicit control over automated abstraction
Offline resilience over cloud dependency

The goal is functional consistency in constrained hardware environments.

Future Improvements
Enhanced natural language parsing (phrase-level intent recognition)
Structured conversation state machine
Optional local LLM integration layer
Web-based configuration dashboard
Multi-device audio distribution system
Author

Billy
https://billy-bit.com
