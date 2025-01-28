import React, { useState, useEffect, useRef } from 'react';

const WS_URL = "ws://localhost:9082";

const App = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [chatLog, setChatLog] = useState([]);
  const [wsStatus, setWsStatus] = useState('disconnected');

  const webSocketRef = useRef(null);
  const audioContextRef = useRef(null);
  const processorRef = useRef(null);
  const pcmDataRef = useRef([]);
  const intervalRef = useRef(null);
  const audioInputContextRef = useRef(null);
  const workletNodeRef = useRef(null);

  useEffect(() => {
    let reconnectTimeout;

    const setupWebSocket = () => {
      if (webSocketRef.current) {
        webSocketRef.current.close();
      }
      initializeWebSocket();
    };

    setupWebSocket();

    return () => {
      if (webSocketRef.current) {
        webSocketRef.current.close();
      }
      clearTimeout(reconnectTimeout);
      stopAudioRecording();
    };
  }, []);

  const initializeWebSocket = () => {
    console.log("Connecting to WebSocket:", WS_URL);
    const ws = new WebSocket(WS_URL);

    ws.onclose = (event) => {
      console.log("WebSocket closed:", event);
      setWsStatus('disconnected');
      setTimeout(() => initializeWebSocket(), 5000);
    };

    ws.onerror = (event) => {
      console.log("WebSocket error:", event);
      setWsStatus('error');
      ws.close();
    };

    ws.onopen = (event) => {
      console.log("WebSocket open:", event);
      setWsStatus('connected');
      sendSetupMessage(ws);
    };

    ws.onmessage = handleIncomingMessage;

    webSocketRef.current = ws;
  };

  const sendSetupMessage = (ws) => {
    console.log("Sending setup message");
    const setupMessage = {
      setup: { generation_config: { response_modalities: ["AUDIO"] } },
    };
    ws.send(JSON.stringify(setupMessage));
  };

  const sendAudioMessage = (b64PCM) => {
    if (!webSocketRef.current || webSocketRef.current.readyState !== WebSocket.OPEN) {
      console.log("WebSocket not ready");
      return;
    }

    const payload = {
      realtime_input: {
        media_chunks: [
          { mime_type: "audio/pcm", data: b64PCM },
        ],
      },
    };

    webSocketRef.current.send(JSON.stringify(payload));
    console.log("Sent audio data");
  };

  const handleIncomingMessage = (event) => {
    const messageData = JSON.parse(event.data);
    const response = new Response(messageData);

    if (response.text) {
      addMessageToChat("GEMINI: " + response.text);
    }
    if (response.audioData) {
      processAudioResponse(response.audioData);
    }
  };

  const initAudioContext = async () => {
    if (audioInputContextRef.current) return;

    audioInputContextRef.current = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 24000 });
    await audioInputContextRef.current.audioWorklet.addModule("audio-processor.js");
    workletNodeRef.current = new AudioWorkletNode(audioInputContextRef.current, "audio-processor");
    workletNodeRef.current.connect(audioInputContextRef.current.destination);
  };

  const processAudioResponse = async (base64AudioChunk) => {
    try {
      if (!audioInputContextRef.current) {
        await initAudioContext();
      }

      if (audioInputContextRef.current.state === "suspended") {
        await audioInputContextRef.current.resume();
      }

      const arrayBuffer = base64ToArrayBuffer(base64AudioChunk);
      const float32Data = convertPCM16LEToFloat32(arrayBuffer);
      workletNodeRef.current.port.postMessage(float32Data);
    } catch (error) {
      console.error("Error processing audio chunk:", error);
    }
  };

  const recordAudioChunk = () => {
    const buffer = new ArrayBuffer(pcmDataRef.current.length * 2);
    const view = new DataView(buffer);
    pcmDataRef.current.forEach((value, index) => {
      view.setInt16(index * 2, value, true);
    });
    const base64 = btoa(String.fromCharCode.apply(null, new Uint8Array(buffer)));
    sendAudioMessage(base64);
    pcmDataRef.current = [];
  };

  const startAudioRecording = async () => {
    try {
      audioContextRef.current = new AudioContext({ sampleRate: 16000 });

      const stream = await navigator.mediaDevices.getUserMedia({
        audio: { channelCount: 1, sampleRate: 16000 },
      });

      const source = audioContextRef.current.createMediaStreamSource(stream);
      processorRef.current = audioContextRef.current.createScriptProcessor(4096, 1, 1);

      processorRef.current.onaudioprocess = (e) => {
        const inputData = e.inputBuffer.getChannelData(0);
        const pcm16 = new Int16Array(inputData.length);
        for (let i = 0; i < inputData.length; i++) {
          pcm16[i] = inputData[i] * 0x7fff;
        }
        pcmDataRef.current.push(...pcm16);
      };

      source.connect(processorRef.current);
      processorRef.current.connect(audioContextRef.current.destination);

      intervalRef.current = setInterval(recordAudioChunk, 2000);
      setIsRecording(true);
    } catch (error) {
      console.error("Error starting audio recording:", error);
      setIsRecording(false);
    }
  };

  const stopAudioRecording = () => {
    if (processorRef.current) {
      processorRef.current.disconnect();
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
    }
    clearInterval(intervalRef.current);
    setIsRecording(false);
  };

  const addMessageToChat = (message) => {
    console.log(message);
    setChatLog(prevLog => [...prevLog, message]);
  };

  return (
    <div className="mdl-layout mdl-js-layout mdl-layout--fixed-header">
      <header className="mdl-layout__header">
        <div className="mdl-layout__header-row">
          <span className="mdl-layout-title">Gemini Live Demo</span>
        </div>
      </header>
      <main className="mdl-layout__content">
        <div className="page-content">
          <div className="demo-content">
            <div className="button-group">
              <button 
                onClick={isRecording ? stopAudioRecording : startAudioRecording} 
                className={`mdl-button mdl-js-button mdl-button--fab mdl-button--mini-fab ${isRecording ? '' : 'mdl-button--colored'}`}
                disabled={wsStatus !== 'connected'}
              >
                <i className="material-icons">{isRecording ? 'mic_off' : 'mic'}</i>
              </button>
            </div>
            <div>WebSocket Status: {wsStatus}</div>
            <div id="chatLog">
              {chatLog.map((message, index) => (
                <p key={index}>{message}</p>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

class Response {
  constructor(data) {
    this.text = data.text || null;
    this.audioData = data.audio || null;
    this.endOfTurn = data.endOfTurn || null;
  }
}

function base64ToArrayBuffer(base64) {
  const binaryString = window.atob(base64);
  const bytes = new Uint8Array(binaryString.length);
  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return bytes.buffer;
}

function convertPCM16LEToFloat32(pcmData) {
  const inputArray = new Int16Array(pcmData);
  const float32Array = new Float32Array(inputArray.length);
  for (let i = 0; i < inputArray.length; i++) {
    float32Array[i] = inputArray[i] / 32768;
  }
  return float32Array;
}

export default App;
